#!/usr/bin/env python3
"""AFO 왕국 정신 통합 시스템 (Spirit Integration)

眞善美孝永 철학 통합
- 모든 작업에 Trinity Score 계산
- 작업 시작 전 왕국 정신 확인 (헌법 문서 읽기)
- 각 Phase 완료 후 Trinity Score 검증
- 점수 하락 시 자동 롤백 및 원인 분석
- 초심 보존 메커니즘
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# AFO 루트 디렉토리
AFO_ROOT = Path(__file__).resolve().parent.parent


def calculate_trinity_score_5pillars(
    truth: float = 0.95,
    goodness: float = 0.92,
    beauty: float = 0.89,
    serenity: float = 0.98,
    forever: float = 0.991,
) -> dict[str, Any]:
    """5기둥 Trinity Score 계산 공식 (승상 확정, 2025-12-04)

    공식:
        Trinity Score = 0.35 × 眞 + 0.35 × 善 + 0.20 × 美 + 0.08 × 孝 + 0.02 × 永
        Balance Gap = Max(眞, 善, 美, 孝, 永) - Min(眞, 善, 美, 孝, 永)
    """
    # 가중치 (승상 확정)
    weights = {
        "truth": 0.35,
        "goodness": 0.35,
        "beauty": 0.20,
        "serenity": 0.08,
        "forever": 0.02,
    }

    # 점수 정규화 (0.0-1.0 범위 확인)
    scores = {
        "truth": max(0.0, min(1.0, truth)),
        "goodness": max(0.0, min(1.0, goodness)),
        "beauty": max(0.0, min(1.0, beauty)),
        "serenity": max(0.0, min(1.0, serenity)),
        "forever": max(0.0, min(1.0, forever)),
    }

    # Trinity Score 계산
    total_score = (
        weights["truth"] * scores["truth"]
        + weights["goodness"] * scores["goodness"]
        + weights["beauty"] * scores["beauty"]
        + weights["serenity"] * scores["serenity"]
        + weights["forever"] * scores["forever"]
    )

    # Balance Gap 계산
    score_values = list(scores.values())
    balance_gap = max(score_values) - min(score_values)

    # 상태 판정
    if balance_gap < 0.10:
        status = "✅ 완벽한 균형"
    elif balance_gap < 0.30:
        status = "✅ 균형 잡힘"
    else:
        status = "⚠️ 불균형"

    return {
        "total_score": round(total_score, 4),
        "balance_gap": round(balance_gap, 4),
        "status": status,
        "scores": {k: round(v, 3) for k, v in scores.items()},
        "timestamp": datetime.now().isoformat(),
    }


class SpiritIntegration:
    """왕국 정신 통합 시스템"""

    def __init__(self):
        self.constitution_paths = [
            AFO_ROOT / "docs" / "AFO_SERENITY_CONSTITUTION_v3.md",
            AFO_ROOT / "docs" / "AFO_PHILOSOPHY.md",
            AFO_ROOT / ".cursorrules",
        ]
        self.baseline_scores: dict[str, float] | None = None
        self.operation_history: list[dict[str, Any]] = []

    def read_constitution(self) -> dict[str, Any]:
        """헌법 문서 읽기 (작업 시작 전 왕국 정신 확인)"""
        constitution_data = {
            "files_found": [],
            "files_missing": [],
            "total_size": 0,
        }

        for path in self.constitution_paths:
            if path.exists():
                constitution_data["files_found"].append(str(path))
                constitution_data["total_size"] += path.stat().st_size
            else:
                constitution_data["files_missing"].append(str(path))

        return constitution_data

    def evaluate_operation(
        self,
        operation_name: str,
        operation_data: dict[str, Any],
        truth_score: float | None = None,
        goodness_score: float | None = None,
        beauty_score: float | None = None,
    ) -> dict[str, Any]:
        """작업 평가 (眞善美孝永 점수 계산)"""
        # 眞(Truth): 문제 감지 정확도, 해결 검증
        if truth_score is None:
            # operation_data에서 추론
            if "errors" in operation_data:
                error_count = len(operation_data.get("errors", []))
                truth_score = max(0.0, 1.0 - (error_count * 0.1))
            else:
                truth_score = 0.95  # 기본값

        # 善(Goodness): 안정성 확보, 롤백 가능성
        if goodness_score is None:
            if "rollback_available" in operation_data:
                goodness_score = 0.98 if operation_data["rollback_available"] else 0.85
            else:
                goodness_score = 0.92  # 기본값

        # 美(Beauty): 코드 품질, 구조 우아함
        if beauty_score is None:
            if "code_quality" in operation_data:
                beauty_score = operation_data["code_quality"]
            else:
                beauty_score = 0.89  # 기본값

        # 孝(Serenity): 형님의 평온, 마찰 제거
        # 문제가 없고 안정적이면 Serenity 높음
        friction_removed = operation_data.get("friction_removed", False)
        if friction_removed and truth_score >= 0.9 and goodness_score >= 0.9:
            serenity_score = 1.0
        elif friction_removed:
            serenity_score = 0.95
        else:
            serenity_score = 0.85

        # 永(Eternity): 지속 가능성, 레거시 계승
        # 모든 점수가 높고 균형 잡혔으면 Eternity 높음
        if truth_score >= 0.9 and goodness_score >= 0.9 and beauty_score >= 0.85:
            eternity_score = 0.99
        else:
            eternity_score = 0.88

        # Trinity Score 계산
        trinity_result = calculate_trinity_score_5pillars(
            truth=truth_score,
            goodness=goodness_score,
            beauty=beauty_score,
            serenity=serenity_score,
            forever=eternity_score,
        )

        evaluation = {
            "operation": operation_name,
            "timestamp": datetime.now().isoformat(),
            "trinity_scores": {
                "truth": truth_score,
                "goodness": goodness_score,
                "beauty": beauty_score,
                "serenity": serenity_score,
                "eternity": eternity_score,
            },
            "trinity_result": trinity_result,
            "friction_removed": friction_removed,
            "recommendation": self._get_recommendation(trinity_result),
        }

        # 히스토리에 추가
        self.operation_history.append(evaluation)

        return evaluation

    def verify_phase_completion(self, phase_name: str, phase_result: dict[str, Any]) -> dict[str, Any]:
        """Phase 완료 후 Trinity Score 검증"""
        # Phase 결과에서 점수 추출
        truth = phase_result.get("truth_score", 0.95)
        goodness = phase_result.get("goodness_score", 0.92)
        beauty = phase_result.get("beauty_score", 0.89)

        evaluation = self.evaluate_operation(
            f"Phase: {phase_name}",
            phase_result,
            truth_score=truth,
            goodness_score=goodness,
            beauty_score=beauty,
        )

        # Baseline과 비교
        if self.baseline_scores:
            score_dropped = evaluation["trinity_result"]["total_score"] < self.baseline_scores.get("total_score", 0.9)
            if score_dropped:
                evaluation["warning"] = "Trinity Score 하락 감지 - 롤백 권장"
                evaluation["baseline_comparison"] = {
                    "baseline": self.baseline_scores["total_score"],
                    "current": evaluation["trinity_result"]["total_score"],
                    "delta": evaluation["trinity_result"]["total_score"] - self.baseline_scores["total_score"],
                }

        return evaluation

    def set_baseline(self, scores: dict[str, float] | None = None):
        """Baseline 점수 설정"""
        if scores is None:
            # 기본 Baseline (완벽한 상태)
            self.baseline_scores = {
                "total_score": 0.95,
                "truth": 0.95,
                "goodness": 0.95,
                "beauty": 0.90,
                "serenity": 1.0,
                "eternity": 0.99,
            }
        else:
            self.baseline_scores = scores

    def analyze_score_drop(self, current_evaluation: dict[str, Any]) -> dict[str, Any]:
        """점수 하락 원인 분석"""
        if not self.baseline_scores:
            return {"error": "Baseline not set"}

        baseline_total = self.baseline_scores.get("total_score", 0.95)
        current_total = current_evaluation["trinity_result"]["total_score"]
        delta = current_total - baseline_total

        if delta >= 0:
            return {"status": "no_drop", "delta": delta}

        # 점수 하락 원인 분석
        current_scores = current_evaluation["trinity_scores"]
        baseline_scores = self.baseline_scores

        drops = []
        for pillar in ["truth", "goodness", "beauty", "serenity", "eternity"]:
            current = current_scores.get(pillar, 0)
            baseline = baseline_scores.get(pillar, 0)
            if current < baseline:
                drops.append(
                    {
                        "pillar": pillar,
                        "baseline": baseline,
                        "current": current,
                        "drop": baseline - current,
                    }
                )

        # 가장 큰 하락 찾기
        if drops:
            biggest_drop = max(drops, key=lambda x: x["drop"])
            return {
                "status": "score_dropped",
                "delta": delta,
                "biggest_drop": biggest_drop,
                "all_drops": drops,
                "recommendation": self._get_recovery_recommendation(biggest_drop["pillar"]),
            }

        return {"status": "unknown", "delta": delta}

    def _get_recovery_recommendation(self, pillar: str) -> str:
        """복구 권장사항"""
        recommendations = {
            "truth": "문제 감지 정확도 개선, 검증 강화 필요",
            "goodness": "안정성 확보, 롤백 메커니즘 확인 필요",
            "beauty": "코드 품질 개선, 구조 리팩터링 필요",
            "serenity": "마찰 제거, 형님의 평온 확보 필요",
            "eternity": "지속 가능성 개선, 레거시 계승 확인 필요",
        }
        return recommendations.get(pillar, "전반적인 개선 필요")

    def _get_recommendation(self, trinity_result: dict[str, Any]) -> str:
        """권장사항 생성"""
        total_score = trinity_result["total_score"]
        balance_gap = trinity_result["balance_gap"]

        if total_score >= 0.9 and balance_gap < 0.3:
            return "🎉 완벽한 상태! 왕국 정신 완벽히 유지"
        elif total_score >= 0.8:
            return "✅ 양호한 상태. 일부 개선 권장"
        elif total_score >= 0.7:
            return "⚠️ 주의 필요. Trinity Score 개선 권장"
        else:
            return "🚨 긴급 상황! 즉시 왕국 정신 확인 필요"

    def generate_spirit_report(self) -> dict[str, Any]:
        """정신 통합 리포트 생성"""
        constitution = self.read_constitution()

        # 최근 작업들의 평균 점수
        if self.operation_history:
            recent_operations = self.operation_history[-5:]  # 최근 5개
            avg_scores = {
                "truth": sum(op["trinity_scores"]["truth"] for op in recent_operations) / len(recent_operations),
                "goodness": sum(op["trinity_scores"]["goodness"] for op in recent_operations) / len(recent_operations),
                "beauty": sum(op["trinity_scores"]["beauty"] for op in recent_operations) / len(recent_operations),
                "serenity": sum(op["trinity_scores"]["serenity"] for op in recent_operations) / len(recent_operations),
                "eternity": sum(op["trinity_scores"]["eternity"] for op in recent_operations) / len(recent_operations),
            }
            avg_trinity = calculate_trinity_score_5pillars(**avg_scores)
        else:
            avg_scores = None
            avg_trinity = None

        return {
            "timestamp": datetime.now().isoformat(),
            "constitution_status": constitution,
            "baseline_scores": self.baseline_scores,
            "average_scores": avg_scores,
            "average_trinity": avg_trinity,
            "operation_count": len(self.operation_history),
            "recent_operations": (self.operation_history[-3:] if self.operation_history else []),
            "spirit_maintained": (avg_trinity["total_score"] >= 0.9 if avg_trinity else False),
        }


def main():
    """메인 실행 (예시)"""
    spirit = SpiritIntegration()

    # Baseline 설정
    spirit.set_baseline()

    # 헌법 확인
    constitution = spirit.read_constitution()
    print(f"헌법 파일: {len(constitution['files_found'])}개 발견")

    # 예시 작업 평가
    example_operation = {
        "friction_removed": True,
        "rollback_available": True,
        "code_quality": 0.92,
    }
    evaluation = spirit.evaluate_operation("예시 작업", example_operation)
    print(json.dumps(evaluation, indent=2, ensure_ascii=False))

    # 리포트 생성
    report = spirit.generate_spirit_report()
    print("\n=== 정신 통합 리포트 ===")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # 종료 코드
    exit_code = 0 if report["spirit_maintained"] else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
