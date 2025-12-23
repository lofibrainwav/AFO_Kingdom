"""
Trinity Score Calculator (SSOT)
동적 Trinity Score 계산기 - SSOT 가중치 기반 정밀 산출
PDF 페이지 1: Trinity Score 계산기, 페이지 3: 5대 가치 동적 평가

Phase 5: Trinity Type Validator 적용 - 런타임 Trinity Score 검증
"""

import logging
from collections.abc import Callable
from typing import Any, TypeVar

import numpy as np

F = TypeVar("F", bound=Callable[..., Any])

try:
    from AFO.utils.trinity_type_validator import validate_with_trinity
except ImportError:
    # Fallback for import issues - 시그니처를 실제 함수와 일치시킴
    def validate_with_trinity(func: F) -> F:
        """Fallback decorator when trinity_type_validator is not available."""
        return func


try:
    from config.friction_calibrator import \
        friction_calibrator as _friction_calibrator

    friction_calibrator: Any = _friction_calibrator
except ImportError:
    # Mock friction calibrator
    class MockFrictionCalibrator:
        def calculate_serenity(self) -> Any:
            """Mock serenity calculation for fallback."""
            return type("MockMetrics", (), {"score": 85.0})()

    friction_calibrator = MockFrictionCalibrator()

logger = logging.getLogger(__name__)

# SSOT 가중치 (agents.md Ⅱ. SSOT)
# Truth(35%), Goodness(35%), Beauty(20%), Serenity(8%), Eternity(2%)
SSOT_WEIGHTS = np.array([0.35, 0.35, 0.20, 0.08, 0.02])


class TrinityCalculator:
    """
    Trinity Score Calculator (SSOT Implementation)
    """

    def __init__(self) -> None:
        pass

    @validate_with_trinity
    def calculate_raw_scores(self, query_data: dict[str, Any]) -> list[float]:
        """
        Calculates Raw Scores [0.0, 1.0] for each Pillar.
        Ideally this delegates to specific evaluators (TruthVerifier, RiskGate, etc.)
        For this service method, we implement the logic aggregation.

        Phase 5: Trinity 검증 적용 - 런타임 품질 모니터링
        """
        # 1. 眞 (Truth): Validation & Architecture
        # Simplified logic based on input quality
        truth = 1.0
        if "invalid" in query_data or query_data.get("valid_structure") is False:
            truth = 0.0

        # 2. 善 (Goodness): Risk & Ethics
        goodness = 1.0
        risk = query_data.get("risk_level", 0.0)
        if risk > 0.1:
            goodness = 0.0  # Block logic

        # 3. 美 (Beauty): Narrative & UX
        beauty = 1.0
        if query_data.get("narrative") == "partial":
            beauty = 0.85

        # 4. 孝 (Serenity): Automation Friction
        # Integrated with FrictionCalibrator (Phase 13)
        serenity_metrics = friction_calibrator.calculate_serenity()
        serenity = serenity_metrics.score / 100.0  # Normalize 0-100 to 0.0-1.0

        # 5. 永 (Eternity): Logging
        eternity = 1.0
        # Placeholder

        return [truth, goodness, beauty, serenity, eternity]

    def calculate_trinity_score(
        self, raw_scores: list[float], static_score: float | None = None
    ) -> float:
        """
        Calculates final Trinity Score using SSOT Weights.

        [Option A: 7:3 Golden Ratio]
        If static_score is provided:
            Final = (Static Score * 0.7) + (Dynamic Score * 0.3)
        Else:
            Final = Dynamic Score (calculated from raw_scores)

        Range: 0.0 to 100.0
        """
        if len(raw_scores) != 5:
            raise ValueError(f"Must have 5 raw scores, got {len(raw_scores)}")

        if not all(0.0 <= s <= 1.0 for s in raw_scores):
            raise AssertionError("Raw scores must be between 0.0 and 1.0")

        # 1. Calculate Dynamic Score (Execution Based) - 30% Weight
        weighted_sum = np.dot(raw_scores, SSOT_WEIGHTS)
        dynamic_score = weighted_sum * 100

        if static_score is not None:
            # 2. Apply Golden Ratio (70% Static + 30% Dynamic)
            # Static score is inherent value (0-100)
            final_score = (static_score * 0.7) + (dynamic_score * 0.3)
            logger.info(
                f"[Trinity 7:3] Static({static_score})*0.7 + Dynamic({dynamic_score:.1f})*0.3 = {final_score:.1f}"
            )
        else:
            # Fallback to pure dynamic if no static provided (Legacy compatibility)
            final_score = dynamic_score
            logger.info(
                f"[TrinityCalculator] Raw: {raw_scores} -> Score: {final_score:.1f}"
            )

        return float(round(final_score, 1))

    async def calculate_persona_scores(
        self, persona_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> dict[str, float]:
        """
        페르소나 기반 Trinity Score 계산 (Phase 2 확장)

        Args:
            persona_data: 페르소나 데이터 (id, name, type, role 등)
            context: 추가 맥락 정보

        Returns:
            5기둥 점수 딕셔너리 (truth, goodness, beauty, serenity, eternity)
        """
        # 페르소나 타입에 따른 기본 점수 설정
        persona_type = persona_data.get("type", persona_data.get("id", "unknown"))
        role = persona_data.get("role", "")

        # 페르소나별 기본 점수 (眞善美孝永)
        base_scores = {
            "commander": [90.0, 85.0, 80.0, 95.0, 90.0],
            "family_head": [75.0, 95.0, 85.0, 90.0, 85.0],
            "creator": [80.0, 75.0, 95.0, 80.0, 75.0],
            "zhuge_liang": [95.0, 80.0, 75.0, 85.0, 90.0],  # 眞 (Truth)
            "sima_yi": [80.0, 95.0, 75.0, 90.0, 85.0],  # 善 (Goodness)
            "zhou_yu": [75.0, 80.0, 95.0, 85.0, 80.0],  # 美 (Beauty)
        }

        # 페르소나 타입에 맞는 기본 점수 선택
        if persona_type in base_scores:
            scores = base_scores[persona_type]
        elif "truth" in role.lower() or "strategist" in role.lower():
            scores = [95.0, 80.0, 75.0, 85.0, 90.0]  # 제갈량 스타일
        elif "goodness" in role.lower() or "guardian" in role.lower():
            scores = [80.0, 95.0, 75.0, 90.0, 85.0]  # 사마의 스타일
        elif "beauty" in role.lower() or "architect" in role.lower():
            scores = [75.0, 80.0, 95.0, 85.0, 80.0]  # 주유 스타일
        else:
            scores = [80.0, 80.0, 80.0, 85.0, 80.0]  # 기본값

        # 맥락 정보에 따른 점수 조정 (선택적)
        if context:
            # 맥락에 따라 점수 미세 조정 가능
            context_boost = context.get("boost", 0.0)
            if context_boost:
                scores = [min(100.0, s + context_boost) for s in scores]

        return {
            "truth": scores[0],
            "goodness": scores[1],
            "beauty": scores[2],
            "serenity": scores[3],
            "eternity": scores[4],
        }


# Singleton Instance
trinity_calculator = TrinityCalculator()
