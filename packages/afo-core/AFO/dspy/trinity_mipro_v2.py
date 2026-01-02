"""
TrinityAwareMIPROv2 - 왕국 철학 기반 MIPROv2 최적화

Trinity Score 가중치:
- 眞 (Truth): 35% - 기술적 정확성
- 善 (Goodness): 35% - 윤리·안정성
- 美 (Beauty): 20% - 구조적 우아함
- 孝 (Serenity): 8% - 평온·마찰 최소
- 永 (Eternity): 2% - 지속 가능성
"""

import optuna
from dspy.teleprompt import MIPROv2
from optuna.pruners import HyperbandPruner


class TrinityAwareMIPROv2(MIPROv2):
    """왕국 Trinity 철학 기반 MIPROv2 최적화 클래스"""

    def __init__(self, metric, num_trials: int = 20, **kwargs):
        """
        TrinityAwareMIPROv2 초기화

        Args:
            metric: 평가 메트릭 함수
            num_trials: 최적화 시도 횟수
            **kwargs: MIPROv2 추가 파라미터
        """
        # MIPROv2 (dspy 3.0.4) does not take num_trials in __init__
        super().__init__(metric=metric, **kwargs)
        self.num_trials = num_trials

        # Trinity Score 가중치 (왕국 철학)
        self.trinity_weights = {
            "truth": 0.35,  # 眞 - 기술적 정확성
            "goodness": 0.35,  # 善 - 윤리·안정성
            "beauty": 0.20,  # 美 - 구조적 우아함
            "serenity": 0.08,  # 孝 - 평온·마찰 최소
            "eternity": 0.02,  # 永 - 지속 가능성
        }

        print("🏰 TrinityAwareMIPROv2 초기화 완료")
        print(f"   Trinity 가중치: {self.trinity_weights}")
        print(f"   최적화 시도 횟수: {num_trials}")

    def evaluate_trinity_score(self, example, pred, trace=None) -> float:
        """
        Trinity Score 기반 평가

        Args:
            example: 정답 예시
            pred: 모델 예측
            trace: 실행 추적 (선택사항)

        Returns:
            Trinity Score (0.0 ~ 1.0)
        """
        # 眞 (Truth) - 정확성 평가
        if hasattr(example, "answer") and hasattr(pred, "answer"):
            truth_score = float(pred.answer.lower().strip() == example.answer.lower().strip())
        else:
            truth_score = 0.5  # 기본값

        # 善 (Goodness) - 길이 적절성
        if hasattr(pred, "answer"):
            answer_len = len(pred.answer)
            goodness_score = (
                1.0 if 50 <= answer_len <= 200 else max(0.1, 1.0 - abs(125 - answer_len) / 125)
            )
        else:
            goodness_score = 0.5

        # 美 (Beauty) - 구조적 우아함 (간단한 휴리스틱)
        if hasattr(pred, "answer"):
            beauty_score = (
                1.0
                if any(keyword in pred.answer.lower() for keyword in ["분석", "설명", "결과"])
                else 0.7
            )
        else:
            beauty_score = 0.5

        # 孝 (Serenity) - 마찰 최소화 (응답 일관성)
        serenity_score = 0.8  # 기본적으로 높은 점수

        # 永 (Eternity) - 지속 가능성 (안정성)
        eternity_score = 0.9  # 기본적으로 높은 점수

        # Trinity Score 계산
        trinity_score = (
            self.trinity_weights["truth"] * truth_score
            + self.trinity_weights["goodness"] * goodness_score
            + self.trinity_weights["beauty"] * beauty_score
            + self.trinity_weights["serenity"] * serenity_score
            + self.trinity_weights["eternity"] * eternity_score
        )

        return trinity_score

    def compile(self, student, trainset, **kwargs):
        """
        Trinity Score 기반 MIPROv2 컴파일

        Args:
            student: 최적화할 프로그램
            trainset: 학습 데이터셋
            **kwargs: 추가 파라미터

        Returns:
            최적화된 프로그램
        """
        print("🏰 TrinityAwareMIPROv2 컴파일 시작")
        print(f"   학습 데이터셋 크기: {len(trainset)}")
        print(f"   최적화 시도 횟수: {self.num_trials}")

        # Trinity Score 기반 메트릭 래퍼
        def trinity_metric(example, pred, trace=None):
            return self.evaluate_trinity_score(example, pred, trace)

        # 부모 클래스 메트릭 설정
        self.metric = trinity_metric

        # Optuna study 생성 (HyperbandPruner 사용)
        study = optuna.create_study(
            direction="maximize", pruner=HyperbandPruner(), study_name="trinity_mipro_v2"
        )

        # MIPROv2에 study 전달
        kwargs["study"] = study

        print("🏰 MIPROv2 최적화 실행 중...")

        # 부모 클래스 compile 호출
        optimized_program = super().compile(student, trainset, **kwargs)

        print("🏰 TrinityAwareMIPROv2 컴파일 완료")
        print(".2f")
        return optimized_program


# Trinity Score 계산 유틸리티
def calculate_trinity_score(
    truth: float, goodness: float, beauty: float, serenity: float = 0.8, eternity: float = 0.9
) -> float:
    """
    Trinity Score 계산 유틸리티

    Args:
        truth: 정확성 점수 (0.0 ~ 1.0)
        goodness: 안정성 점수 (0.0 ~ 1.0)
        beauty: 우아함 점수 (0.0 ~ 1.0)
        serenity: 평온 점수 (0.0 ~ 1.0)
        eternity: 지속성 점수 (0.0 ~ 1.0)

    Returns:
        Trinity Score (0.0 ~ 1.0)
    """
    weights = {
        "truth": 0.35,
        "goodness": 0.35,
        "beauty": 0.20,
        "serenity": 0.08,
        "eternity": 0.02,
    }

    return (
        weights["truth"] * truth
        + weights["goodness"] * goodness
        + weights["beauty"] * beauty
        + weights["serenity"] * serenity
        + weights["eternity"] * eternity
    )


if __name__ == "__main__":
    # 테스트
    print("🏰 TrinityAwareMIPROv2 테스트")

    # 간단한 테스트 메트릭
    def test_metric(example, pred, trace=None):
        return 0.8  # 테스트용 고정 점수

    # 클래스 초기화 테스트
    optimizer = TrinityAwareMIPROv2(metric=test_metric, num_trials=5)
    print(f"✅ TrinityAwareMIPROv2 초기화 성공: {optimizer.trinity_weights}")

    # Trinity Score 계산 테스트
    score = calculate_trinity_score(0.9, 0.8, 0.7, 0.8, 0.9)
    print(".3f")
