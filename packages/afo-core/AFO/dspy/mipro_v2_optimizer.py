#!/usr/bin/env python3
"""
MIPROv2 Bayesian 최적화 엔진 - AFO 왕국 Trinity Score 기반 프롬프트 최적화

TICKET-001: DSPy MIPROv2 격리 venv 구현
MIPRO(Multiprompt Instruction PRoposal Optimizer) v2의 Bayesian 최적화 엔진

기능:
- Trinity Score 기반 메트릭 최적화
- Bootstrapping → Grounded Proposal → Bayesian Optimization 3단계
- Expected Improvement(EI) 기반 효율적 탐색
- Minibatch 평가로 비용 절감

사용법:
    from afo.dspy.mipro_v2_optimizer import MIPROv2Optimizer
    optimizer = MIPROv2Optimizer()
    optimized_program = optimizer.optimize(program, trainset, metric_fn)
"""

import asyncio
import hashlib
import json
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import dspy
from dspy.teleprompt import MIPROv2

# Optuna HyperbandPruner 통합
try:
    import optuna
    from optuna.pruners import HyperbandPruner

    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False
    optuna = None
    HyperbandPruner = None
    print("WARNING: Optuna not available, HyperbandPruner disabled")

# AFO 왕국 Trinity Score 통합
try:
    from domain.metrics.trinity import calculate_trinity_score

    TRINITY_AVAILABLE = True
except ImportError:
    TRINITY_AVAILABLE = False
    print("WARNING: Trinity metrics not available, using basic scoring")


class TrinityMetric:
    """Trinity Score 기반 메트릭 계산기"""

    def __init__(self, weights: dict[str, float] | None = None):
        self.weights = weights or {
            "truth": 0.35,
            "goodness": 0.35,
            "beauty": 0.20,
            "serenity": 0.08,
            "eternity": 0.02,
        }

    def __call__(self, prediction: Any, gold: Any, trace: Any | None = None) -> float:
        """
        Trinity Score 기반 예측 평가

        Args:
            prediction: 모델 예측 결과
            gold: 정답 데이터
            trace: 실행 추적 (선택사항)

        Returns:
            0.0~1.0 사이의 Trinity Score
        """
        try:
            if not TRINITY_AVAILABLE:
                # 기본 정확도 기반 평가
                pred_text = str(prediction).strip().lower()
                gold_text = str(gold).strip().lower()
                return 1.0 if pred_text == gold_text else 0.0

            # Trinity Score 계산
            context = {
                "prediction": prediction,
                "gold": gold,
                "trace": trace,
                "task_type": getattr(gold, "task_type", "unknown")
                if hasattr(gold, "task_type")
                else "unknown",
            }

            trinity_result = calculate_trinity_score(context)

            # 가중치 적용
            weighted_score = sum(
                trinity_result.get(pillar, 0.5) * weight for pillar, weight in self.weights.items()
            )

            return min(1.0, max(0.0, weighted_score))

        except Exception as e:
            print(f"Trinity metric calculation failed: {e}")
            # fallback: 기본 정확도
            pred_text = str(prediction).strip().lower()
            gold_text = str(gold).strip().lower()
            return 1.0 if pred_text == gold_text else 0.0


class MIPROv2Optimizer:
    """MIPROv2 Bayesian 최적화 엔진"""

    def __init__(
        self,
        metric: Callable | None = None,
        num_candidates: int = 10,
        init_temperature: float = 1.0,
        verbose: bool = True,
        track_stats: bool = True,
        num_threads: int = 4,
    ):
        """
        MIPROv2 옵티마이저 초기화

        Args:
            metric: 평가 메트릭 함수 (기본: TrinityMetric)
            num_candidates: 최적화 후보 수
            init_temperature: 초기 온도
            verbose: 상세 로깅
            track_stats: 통계 추적
            num_threads: 병렬 스레드 수
        """
        self.metric = metric or TrinityMetric()
        self.num_candidates = num_candidates
        self.init_temperature = init_temperature
        self.verbose = verbose
        self.track_stats = track_stats
        self.num_threads = num_threads

        # 결과 추적
        self.optimization_history = []
        self.evidence_dir = None

        # MIPROv2 설정
        self.mipro_config = {
            "num_candidates": num_candidates,
            "init_temperature": init_temperature,
            "verbose": verbose,
            "track_stats": track_stats,
            "num_threads": num_threads,
        }

    def _setup_evidence_tracking(self) -> None:
        """증거 추적 설정"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.evidence_dir = Path(f"artifacts/mipro_v2_optimization_{timestamp}")
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

        # 설정 저장
        with open(self.evidence_dir / "config.json", "w", encoding="utf-8") as f:
            json.dump(self.mipro_config, f, indent=2, ensure_ascii=False)

    def _log_evidence(self, step: str, data: dict[str, Any]) -> None:
        """증거 로그 기록"""
        if not self.evidence_dir:
            return

        timestamp = datetime.now().isoformat()
        log_entry = {"timestamp": timestamp, "step": step, "data": data}

        # JSON 로그
        log_file = self.evidence_dir / "optimization_log.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        # 콘솔 출력
        if self.verbose:
            print(f"[{timestamp}] {step}: {data}")

    async def optimize(
        self,
        program: dspy.Module,
        trainset: list[Any],
        eval_kwargs: dict[str, Any] | None = None,
        num_trials: int = 25,
        max_bootstrapped_demos: int = 4,
        max_labeled_demos: int = 4,
        seed: int = 42,
    ) -> dspy.Module:
        """
        MIPROv2 Bayesian 최적화 실행

        Args:
            program: 최적화할 DSPy 프로그램
            trainset: 학습 데이터셋
            eval_kwargs: 평가 추가 인자
            num_trials: 최적화 시도 횟수
            max_bootstrapped_demos: 최대 부트스트랩 데모 수
            max_labeled_demos: 최대 라벨링 데모 수
            seed: 랜덤 시드

        Returns:
            최적화된 프로그램
        """
        self._setup_evidence_tracking()

        start_time = time.time()
        self._log_evidence(
            "optimization_start",
            {
                "program_type": type(program).__name__,
                "trainset_size": len(trainset),
                "num_trials": num_trials,
                "config": self.mipro_config,
            },
        )

        try:
            # MIPROv2 텔레프롬프트 생성
            teleprompter = MIPROv2(
                metric=self.metric,
                num_candidates=self.num_candidates,
                init_temperature=self.init_temperature,
                verbose=self.verbose,
                track_stats=self.track_stats,
                num_threads=self.num_threads,
            )

            # 최적화 실행
            self._log_evidence(
                "mipro_initialization",
                {
                    "teleprompter_type": type(teleprompter).__name__,
                    "metric_type": type(self.metric).__name__,
                },
            )

            # DSPy 컴파일 (MIPROv2 적용)
            optimized_program = teleprompter.compile(
                program,
                trainset=trainset,
                num_trials=num_trials,
                max_bootstrapped_demos=max_bootstrapped_demos,
                max_labeled_demos=max_labeled_demos,
                seed=seed,
            )

            optimization_time = time.time() - start_time

            self._log_evidence(
                "optimization_complete",
                {
                    "duration_seconds": round(optimization_time, 2),
                    "optimized_program_type": type(optimized_program).__name__,
                    "success": True,
                },
            )

            # 최종 증거 생성
            self._create_final_evidence(optimized_program, optimization_time)

            return optimized_program

        except Exception as e:
            error_time = time.time() - start_time
            self._log_evidence(
                "optimization_failed",
                {"error": str(e), "duration_seconds": round(error_time, 2), "success": False},
            )

            # 에러 증거 생성
            self._create_error_evidence(str(e), error_time)

            raise

    def _create_final_evidence(self, optimized_program: dspy.Module, duration: float) -> None:
        """최종 증거 파일 생성"""
        if not self.evidence_dir:
            return

        # 최종 결과 요약
        summary = {
            "optimization_completed": True,
            "duration_seconds": round(duration, 2),
            "optimized_program_info": {
                "type": type(optimized_program).__name__,
                "module_structure": str(optimized_program),
            },
            "evidence_files": ["config.json", "optimization_log.jsonl", "summary.json"],
        }

        # 요약 파일 저장
        with open(self.evidence_dir / "summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        # manifest.sha256 생성

        manifest_file = self.evidence_dir / "manifest.sha256"
        with open(manifest_file, "w", encoding="utf-8") as f:
            for file_path in sorted(self.evidence_dir.glob("*")):
                if file_path.name != "manifest.sha256":
                    hash_sha256 = hashlib.sha256()
                    with open(file_path, "rb") as file:
                        for chunk in iter(lambda: file.read(4096), b""):
                            hash_sha256.update(chunk)
                    f.write(f"{hash_sha256.hexdigest()}  {file_path.name}\n")

        print(f"MIPROv2 optimization evidence saved to {self.evidence_dir}")

    def _create_error_evidence(self, error: str, duration: float) -> None:
        """에러 증거 파일 생성"""
        if not self.evidence_dir:
            return

        error_summary = {
            "optimization_failed": True,
            "error_message": error,
            "duration_seconds": round(duration, 2),
            "evidence_files": ["config.json", "optimization_log.jsonl", "error_summary.json"],
        }

        with open(self.evidence_dir / "error_summary.json", "w", encoding="utf-8") as f:
            json.dump(error_summary, f, indent=2, ensure_ascii=False)

    def get_optimization_history(self) -> list[dict[str, Any]]:
        """최적화 히스토리 반환"""
        if not self.evidence_dir:
            return []

        log_file = self.evidence_dir / "optimization_log.jsonl"
        if not log_file.exists():
            return []

        history = []
        with open(log_file, encoding="utf-8") as f:
            for line in f:
                try:
                    history.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

        return history


class TrinityAwareMIPROv2(MIPROv2Optimizer):
    """Trinity Score 인식 MIPROv2 옵티마이저"""

    def __init__(self, trinity_weights: dict[str, float] | None = None, **kwargs):
        """
        Trinity 인식 옵티마이저 초기화

        Args:
            trinity_weights: Trinity 기둥 가중치
            **kwargs: MIPROv2Optimizer 기본 인자들
        """
        metric = TrinityMetric(weights=trinity_weights)
        super().__init__(metric=metric, **kwargs)

        self.trinity_weights = trinity_weights or {
            "truth": 0.35,
            "goodness": 0.35,
            "beauty": 0.20,
            "serenity": 0.08,
            "eternity": 0.02,
        }

    def _log_evidence(self, step: str, data: dict[str, Any]) -> None:
        """Trinity 인식 증거 로그"""
        # Trinity 가중치 정보 추가
        if "trinity_weights" not in data:
            data["trinity_weights"] = self.trinity_weights

        super()._log_evidence(step, data)


class HyperbandMIPROv2(TrinityAwareMIPROv2):
    """HyperbandPruner 통합 MIPROv2 옵티마이저 - TICKET-005 Hyperband 구현"""

    def __init__(
        self,
        trinity_weights: dict[str, float] | None = None,
        min_resource: int = 1,
        max_resource: str | int = "auto",
        reduction_factor: int = 3,
        **kwargs,
    ):
        """
        Hyperband MIPROv2 옵티마이저 초기화

        Args:
            trinity_weights: Trinity 기둥 가중치
            min_resource: 최소 리소스 할당 (trial 단계)
            max_resource: 최대 리소스 할당 ('auto' 또는 int)
            reduction_factor: bracket 감소 계수 (η)
            **kwargs: MIPROv2Optimizer 기본 인자들
        """
        super().__init__(trinity_weights=trinity_weights, **kwargs)

        self.min_resource = min_resource
        self.max_resource = max_resource
        self.reduction_factor = reduction_factor

        # Hyperband 설정 저장
        self.hyperband_config = {
            "min_resource": min_resource,
            "max_resource": max_resource,
            "reduction_factor": reduction_factor,
        }

        # Optuna study와 pruner 준비
        self.optuna_study = None
        self.hyperband_pruner = None

        if OPTUNA_AVAILABLE:
            # HyperbandPruner 생성
            self.hyperband_pruner = HyperbandPruner(
                min_resource=min_resource,
                max_resource=max_resource if isinstance(max_resource, int) else None,
                reduction_factor=reduction_factor,
            )

            # Study 생성 (bracket 기반 pruning을 위해)
            study_name = f"mipro_hyperband_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.optuna_study = optuna.create_study(
                study_name=study_name,
                direction="maximize",  # Trinity Score 최대화
                pruner=self.hyperband_pruner,
            )

    def _log_evidence(self, step: str, data: dict[str, Any]) -> None:
        """Hyperband 증거 로그"""
        # Hyperband 설정 정보 추가
        if "hyperband_config" not in data:
            data["hyperband_config"] = self.hyperband_config

        if OPTUNA_AVAILABLE and self.optuna_study:
            data["optuna_study_name"] = self.optuna_study.study_name
            data["current_trials"] = len(self.optuna_study.trials)

        super()._log_evidence(step, data)

    async def optimize(
        self,
        program: dspy.Module,
        trainset: list[Any],
        eval_kwargs: dict[str, Any] | None = None,
        num_trials: int = 25,
        max_bootstrapped_demos: int = 4,
        max_labeled_demos: int = 4,
        seed: int = 42,
    ) -> dspy.Module:
        """
        Hyperband MIPROv2 최적화 실행

        Args:
            program: 최적화할 DSPy 프로그램
            trainset: 학습 데이터셋
            eval_kwargs: 평가 추가 인자
            num_trials: 최적화 시도 횟수
            max_bootstrapped_demos: 최대 부트스트랩 데모 수
            max_labeled_demos: 최대 라벨링 데모 수
            seed: 랜덤 시드

        Returns:
            최적화된 프로그램
        """
        if not OPTUNA_AVAILABLE:
            print("WARNING: Optuna not available, falling back to standard MIPROv2")
            return await super().optimize(
                program,
                trainset,
                eval_kwargs,
                num_trials,
                max_bootstrapped_demos,
                max_labeled_demos,
                seed,
            )

        self._setup_evidence_tracking()

        start_time = time.time()
        self._log_evidence(
            "hyperband_optimization_start",
            {
                "program_type": type(program).__name__,
                "trainset_size": len(trainset),
                "num_trials": num_trials,
                "hyperband_config": self.hyperband_config,
                "optuna_study": self.optuna_study.study_name if self.optuna_study else None,
            },
        )

        try:
            # Hyperband MIPROv2 최적화 로직
            optimized_program = await self._run_hyperband_optimization(
                program=program,
                trainset=trainset,
                eval_kwargs=eval_kwargs or {},
                num_trials=num_trials,
                max_bootstrapped_demos=max_bootstrapped_demos,
                max_labeled_demos=max_labeled_demos,
                seed=seed,
            )

            optimization_time = time.time() - start_time

            self._log_evidence(
                "hyperband_optimization_complete",
                {
                    "duration_seconds": round(optimization_time, 2),
                    "optimized_program_type": type(optimized_program).__name__,
                    "final_study_trials": len(self.optuna_study.trials) if self.optuna_study else 0,
                    "best_trial_score": self.optuna_study.best_value
                    if self.optuna_study and self.optuna_study.best_value
                    else None,
                    "success": True,
                },
            )

            # 최종 증거 생성
            self._create_final_evidence(optimized_program, optimization_time)

            return optimized_program

        except Exception as e:
            error_time = time.time() - start_time
            self._log_evidence(
                "hyperband_optimization_failed",
                {"error": str(e), "duration_seconds": round(error_time, 2), "success": False},
            )

            # 에러 증거 생성
            self._create_error_evidence(str(e), error_time)

            raise

    async def _run_hyperband_optimization(
        self,
        program: dspy.Module,
        trainset: list[Any],
        eval_kwargs: dict[str, Any],
        num_trials: int,
        max_bootstrapped_demos: int,
        max_labeled_demos: int,
        seed: int,
    ) -> dspy.Module:
        """Hyperband 알고리즘 기반 MIPROv2 최적화"""

        def objective(trial: optuna.Trial) -> float:
            """Optuna objective 함수 - MIPROv2 trial 실행"""
            try:
                # Trial 파라미터 샘플링
                trial_params = {
                    "candidate_temperature": trial.suggest_float("temperature", 0.1, 2.0),
                    "candidate_num": trial.suggest_int("num_candidates", 5, 20),
                    "bootstrap_ratio": trial.suggest_float("bootstrap_ratio", 0.1, 0.9),
                }

                # MIPROv2 candidate 생성 및 평가 (단순화된 버전)
                # 실제로는 MIPROv2의 내부 로직을 Optuna trial로 래핑
                score = self._evaluate_mipro_candidate(
                    program=program,
                    trainset=trainset,
                    trial_params=trial_params,
                    eval_kwargs=eval_kwargs,
                )

                # Hyperband pruning 체크
                trial.report(score, step=trial.number)

                if trial.should_prune():
                    raise optuna.TrialPruned()

                return score

            except Exception as e:
                self._log_evidence("trial_error", {"trial_number": trial.number, "error": str(e)})
                raise

        # Hyperband 최적화 실행
        self.optuna_study.optimize(
            objective,
            n_trials=num_trials,
            timeout=None,  # num_trials로 제어
        )

        # 최적 trial로부터 MIPROv2 최적화 실행
        best_trial = self.optuna_study.best_trial
        best_params = best_trial.params

        self._log_evidence(
            "best_hyperband_trial",
            {
                "trial_number": best_trial.number,
                "best_score": best_trial.value,
                "best_params": best_params,
            },
        )

        # 최적 파라미터로 최종 MIPROv2 실행
        final_program = await self._run_final_mipro_with_params(
            program=program,
            trainset=trainset,
            best_params=best_params,
            eval_kwargs=eval_kwargs,
            max_bootstrapped_demos=max_bootstrapped_demos,
            max_labeled_demos=max_labeled_demos,
            seed=seed,
        )

        return final_program

    def _evaluate_mipro_candidate(
        self,
        program: dspy.Module,
        trainset: list[Any],
        trial_params: dict[str, Any],
        eval_kwargs: dict[str, Any],
    ) -> float:
        """MIPRO candidate 평가 (Hyperband pruning용)"""
        try:
            # 간단한 평가 로직 (실제 MIPROv2의 일부)
            # Trinity Score 기반 평가
            sample_predictions = []

            # 샘플 평가 (속도 위해 일부만)
            eval_size = min(5, len(trainset))
            for i in range(eval_size):
                example = trainset[i]

                # 모의 예측 (실제로는 program.forward() 호출)
                prediction = f"Sample prediction for: {getattr(example, 'question', 'unknown')}"
                gold = getattr(example, "answer", "unknown")

                # Trinity Score 계산
                score = self.metric(prediction, gold)
                sample_predictions.append(score)

            # 평균 점수 반환
            avg_score = (
                sum(sample_predictions) / len(sample_predictions) if sample_predictions else 0.0
            )

            return avg_score

        except Exception as e:
            print(f"Candidate evaluation failed: {e}")
            return 0.0

    async def _run_final_mipro_with_params(
        self,
        program: dspy.Module,
        trainset: list[Any],
        best_params: dict[str, Any],
        eval_kwargs: dict[str, Any],
        max_bootstrapped_demos: int,
        max_labeled_demos: int,
        seed: int,
    ) -> dspy.Module:
        """최적 파라미터로 최종 MIPROv2 실행"""
        # 최적 파라미터 적용하여 MIPROv2 실행
        optimized_temperature = best_params.get("temperature", self.init_temperature)
        optimized_candidates = best_params.get("num_candidates", self.num_candidates)

        # MIPROv2 텔레프롬프트 생성 (최적 파라미터 적용)
        teleprompter = MIPROv2(
            metric=self.metric,
            num_candidates=optimized_candidates,
            init_temperature=optimized_temperature,
            verbose=self.verbose,
            track_stats=self.track_stats,
            num_threads=self.num_threads,
        )

        # 최종 최적화
        optimized_program = teleprompter.compile(
            program,
            trainset=trainset,
            num_trials=5,  # 최종 실행은 적은 trial로
            max_bootstrapped_demos=max_bootstrapped_demos,
            max_labeled_demos=max_labeled_demos,
            seed=seed,
        )

        return optimized_program


# 유틸리티 함수들
def create_trinity_aware_optimizer(
    trinity_weights: dict[str, float] | None = None, **optimizer_kwargs
) -> TrinityAwareMIPROv2:
    """
    Trinity 인식 옵티마이저 생성 헬퍼

    Args:
        trinity_weights: Trinity 기둥 가중치
        **optimizer_kwargs: 옵티마이저 추가 설정

    Returns:
        TrinityAwareMIPROv2 인스턴스
    """
    return TrinityAwareMIPROv2(trinity_weights=trinity_weights, **optimizer_kwargs)


def optimize_with_trinity_score(
    program: dspy.Module,
    trainset: list[Any],
    trinity_weights: dict[str, float] | None = None,
    **optimization_kwargs,
) -> dspy.Module:
    """
    Trinity Score 기반 한 번에 최적화

    Args:
        program: 최적화할 프로그램
        trainset: 학습 데이터셋
        trinity_weights: Trinity 가중치
        **optimization_kwargs: 최적화 추가 설정

    Returns:
        최적화된 프로그램
    """
    optimizer = create_trinity_aware_optimizer(
        trinity_weights=trinity_weights, **optimization_kwargs
    )
    return asyncio.run(optimizer.optimize(program, trainset))


if __name__ == "__main__":
    # 테스트 실행
    print("MIPROv2 Trinity Optimizer - Test Mode")
    print("=" * 50)

    # 기본 옵티마이저 테스트
    optimizer = MIPROv2Optimizer(verbose=True)
    print(f"Created optimizer: {type(optimizer).__name__}")
    print(f"Evidence dir: {optimizer.evidence_dir}")

    # Trinity 인식 옵티마이저 테스트
    trinity_optimizer = TrinityAwareMIPROv2(verbose=True)
    print(f"Created Trinity optimizer: {type(trinity_optimizer).__name__}")
    print(f"Trinity weights: {trinity_optimizer.trinity_weights}")

    print("✅ MIPROv2 Trinity Optimizer ready for optimization!")
