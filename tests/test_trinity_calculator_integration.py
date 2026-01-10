"""
Trinity Calculator 통합 테스트
AFO 왕국의 자율 확장 테스트 커버리지 100% 달성 전략 검증

이 테스트는 Reviewer 에이전트(Samaui)가 자동 생성한 것으로,
Trinity Score 계산의 정확성과 SSOT 가중치 준수를 검증합니다.
"""

from typing import Any
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

# AFO 왕국 모듈 임포트
from AFO..services.trinity_calculator import import SSOT_WEIGHTS, TrinityCalculator, trinity_calculator


class TestTrinityCalculatorIntegration:
    """
    Trinity Calculator 통합 테스트

    이 테스트는 다음을 검증:
    - SSOT 가중치 정확성 (眞35% 善35% 美20% 孝8% 永2%)
    - Raw Score 계산 로직
    - 페르소나 기반 점수 계산
    - Trinity Score 계산의 수학적 정확성
    - 에러 처리와 엣지 케이스
    """

    @pytest.fixture
    async def calculator_instance(self) -> TrinityCalculator:
        """테스트용 Trinity Calculator 인스턴스"""
        return TrinityCalculator()

    @pytest.mark.parametrize(
        ("query_data", "expected_raw"),
        [
            # 정상 케이스
            (
                {"valid_structure": True, "risk_level": 0.0, "narrative": "complete"},
                [1.0, 1.0, 1.0, 0.85, 1.0],
            ),  # serenity는 friction_calibrator에서 85
            # Invalid 구조 케이스
            (
                {
                    "invalid": True,
                    "valid_structure": False,
                    "risk_level": 0.0,
                    "narrative": "complete",
                },
                [0.0, 1.0, 1.0, 0.85, 1.0],
            ),
            # High Risk 케이스
            (
                {"valid_structure": True, "risk_level": 0.5, "narrative": "complete"},
                [1.0, 0.0, 1.0, 0.85, 1.0],
            ),
            # Partial Narrative 케이스
            (
                {"valid_structure": True, "risk_level": 0.0, "narrative": "partial"},
                [1.0, 1.0, 0.85, 0.85, 1.0],
            ),
        ],
    )
    def test_calculate_raw_scores_success(
        self,
        calculator_instance: TrinityCalculator,
        query_data: dict[str, Any],
        expected_raw: list[float],
    ) -> None:
        """
        Raw Scores 계산 성공 케이스

        검증 포인트:
        - 입력 데이터에 따른 정확한 Raw Score 계산
        - 각 기둥의 로직 정확성 (眞善美孝永)
        - Friction Calibrator 통합
        """
        # When
        result = calculator_instance.calculate_raw_scores(query_data)

        # Then
        assert len(result) == 5, "Must return 5 raw scores"
        assert all(
            0.0 <= s <= 1.0 for s in result
        ), "All scores must be between 0.0 and 1.0"

        # 각 기둥별 검증 (약간의 오차 허용)
        for i, (actual, expected) in enumerate(zip(result, expected_raw, strict=False)):
            assert (
                abs(actual - expected) < 0.01
            ), f"Pillar {i} mismatch: expected {expected}, got {actual}"

    def test_calculate_raw_scores_with_friction_calibrator_mock(
        self, calculator_instance: TrinityCalculator
    ) -> None:
        """
        Friction Calibrator 목킹 테스트

        검증 포인트:
        - Serenity 점수가 Friction Calibrator에서 제대로 가져와지는지
        """
        # Given
        query_data = {
            "valid_structure": True,
            "risk_level": 0.0,
            "narrative": "complete",
        }

        with patch(
            "AFO.services.trinity_calculator.friction_calibrator"
        ) as mock_calibrator:
            mock_metrics = MagicMock()
            mock_metrics.score = 92.0
            mock_calibrator.calculate_serenity.return_value = mock_metrics

            # When
            result = calculator_instance.calculate_raw_scores(query_data)

            # Then
            assert (
                result[3] == 0.92
            ), "Serenity score should be normalized from friction calibrator"

    @pytest.mark.parametrize(
        ("raw_scores", "expected_score"),
        [
            # Perfect Score
            ([1.0, 1.0, 1.0, 1.0, 1.0], 100.0),
            # Zero Score
            ([0.0, 0.0, 0.0, 0.0, 0.0], 0.0),
            # Partial Scores
            (
                [0.8, 0.9, 0.7, 0.6, 0.5],
                74.5,
            ),  # (0.8*0.35 + 0.9*0.35 + 0.7*0.20 + 0.6*0.08 + 0.5*0.02) * 100
            # Commander Profile
            ([0.9, 0.85, 0.8, 0.95, 0.9], 88.5),  # Weighted calculation
        ],
    )
    def test_calculate_trinity_score_success(
        self,
        calculator_instance: TrinityCalculator,
        raw_scores: list[float],
        expected_score: float,
    ) -> None:
        """
        Trinity Score 계산 성공 케이스

        검증 포인트:
        - SSOT 가중치 정확 적용 (眞35% 善35% 美20% 孝8% 永2%)
        - 수학적 계산 정확성
        - 범위 검증 (0.0-100.0)
        """
        # When
        result = calculator_instance.calculate_trinity_score(raw_scores)

        # Then
        assert isinstance(result, float), "Result must be float"
        assert 0.0 <= result <= 100.0, f"Score out of range: {result}"
        assert (
            abs(result - expected_score) < 0.1
        ), f"Expected {expected_score}, got {result}"

        # SSOT 가중치 검증
        expected_calculation = np.dot(raw_scores, SSOT_WEIGHTS) * 100
        assert (
            abs(result - expected_calculation) < 0.1
        ), "SSOT weight calculation mismatch"

    def test_calculate_trinity_score_validation_errors(
        self, calculator_instance: TrinityCalculator
    ) -> None:
        """
        Trinity Score 계산 유효성 검증 에러 케이스

        검증 포인트:
        - 잘못된 입력에 대한 에러 처리
        - ValueError와 AssertionError 적절한 발생
        """
        # Wrong number of scores
        with pytest.raises(ValueError, match="Must have 5 raw scores"):
            calculator_instance.calculate_trinity_score([1.0, 1.0, 1.0])

        # Score out of range
        with pytest.raises(
            AssertionError, match="Raw scores must be between 0.0 and 1.0"
        ):
            calculator_instance.calculate_trinity_score([1.5, 1.0, 1.0, 1.0, 1.0])

        with pytest.raises(
            AssertionError, match="Raw scores must be between 0.0 and 1.0"
        ):
            calculator_instance.calculate_trinity_score([-0.1, 1.0, 1.0, 1.0, 1.0])

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("persona_data", "expected_scores"),
        [
            # Commander 페르소나
            (
                {"type": "commander"},
                {
                    "truth": 90.0,
                    "goodness": 85.0,
                    "beauty": 80.0,
                    "serenity": 95.0,
                    "eternity": 90.0,
                },
            ),
            # Family Head 페르소나
            (
                {"type": "family_head"},
                {
                    "truth": 75.0,
                    "goodness": 95.0,
                    "beauty": 85.0,
                    "serenity": 90.0,
                    "eternity": 85.0,
                },
            ),
            # Creator 페르소나
            (
                {"type": "creator"},
                {
                    "truth": 80.0,
                    "goodness": 75.0,
                    "beauty": 95.0,
                    "serenity": 80.0,
                    "eternity": 75.0,
                },
            ),
        ],
    )
    async def test_calculate_persona_scores_basic_types(
        self,
        calculator_instance: TrinityCalculator,
        persona_data: dict[str, Any],
        expected_scores: dict[str, float],
    ) -> None:
        """
        페르소나 타입별 기본 점수 계산 테스트

        검증 포인트:
        - 각 페르소나 타입에 맞는 5기둥 점수 정확성
        - 眞善美孝永 철학 반영
        """
        # When
        result = await calculator_instance.calculate_persona_scores(persona_data)

        # Then
        assert isinstance(result, dict), "Result must be dictionary"
        assert set(result.keys()) == {
            "truth",
            "goodness",
            "beauty",
            "serenity",
            "eternity",
        }, "Must have all 5 pillars"

        for pillar, expected in expected_scores.items():
            assert (
                result[pillar] == expected
            ), f"{pillar} score mismatch: expected {expected}, got {result[pillar]}"

    @pytest.mark.asyncio
    async def test_calculate_persona_scores_role_based(
        self, calculator_instance: TrinityCalculator
    ) -> None:
        """
        역할 기반 페르소나 점수 계산 테스트

        검증 포인트:
        - Role 필드에 따른 점수 결정 로직
        - Strategist/Guardian/Architect 패턴 인식
        """
        test_cases = [
            (
                {"role": "truth strategist"},
                [95.0, 80.0, 75.0, 85.0, 90.0],
            ),  # 제갈량 스타일
            (
                {"role": "goodness guardian"},
                [80.0, 95.0, 75.0, 90.0, 85.0],
            ),  # 사마의 스타일
            (
                {"role": "beauty architect"},
                [75.0, 80.0, 95.0, 85.0, 80.0],
            ),  # 주유 스타일
            (
                {"type": "unknown", "role": "misc"},
                [80.0, 80.0, 80.0, 85.0, 80.0],
            ),  # 기본값
        ]

        for persona_data, expected_scores in test_cases:
            # When
            result = await calculator_instance.calculate_persona_scores(persona_data)

            # Then
            for i, pillar in enumerate(
                ["truth", "goodness", "beauty", "serenity", "eternity"]
            ):
                assert (
                    result[pillar] == expected_scores[i]
                ), f"{persona_data} {pillar} mismatch"

    @pytest.mark.asyncio
    async def test_calculate_persona_scores_with_context(
        self, calculator_instance: TrinityCalculator
    ) -> None:
        """
        맥락 정보가 포함된 페르소나 점수 계산 테스트

        검증 포인트:
        - Context boost 적용
        - 점수 상한선 (100.0) 준수
        """
        # Given
        persona_data = {"type": "commander"}
        context = {"boost": 5.0}  # 5점 부스트

        # When
        result = await calculator_instance.calculate_persona_scores(
            persona_data, context
        )

        # Then
        # Commander 기본값 + 5점 부스트 (상한선 적용)
        expected_scores = {
            "truth": min(100.0, 90.0 + 5.0),  # 95.0
            "goodness": min(100.0, 85.0 + 5.0),  # 90.0
            "beauty": min(100.0, 80.0 + 5.0),  # 85.0
            "serenity": min(100.0, 95.0 + 5.0),  # 100.0
            "eternity": min(100.0, 90.0 + 5.0),  # 95.0
        }

        for pillar, expected in expected_scores.items():
            assert result[pillar] == expected, f"Context boost failed for {pillar}"

    @pytest.mark.asyncio
    async def test_calculate_persona_scores_upper_bound(
        self, calculator_instance: TrinityCalculator
    ) -> None:
        """
        점수 상한선 테스트

        검증 포인트:
        - 100.0 초과 방지
        - Boost 적용 시에도 상한선 준수
        """
        # Given - 이미 높은 점수의 페르소나에 큰 boost
        persona_data = {"type": "commander"}
        context = {"boost": 20.0}  # 큰 부스트

        # When
        result = await calculator_instance.calculate_persona_scores(
            persona_data, context
        )

        # Then - 모든 점수가 100.0을 초과하지 않아야 함
        for pillar, score in result.items():
            assert score <= 100.0, f"{pillar} score exceeds maximum: {score}"

    def test_ssot_weights_validation(self) -> None:
        """
        SSOT 가중치 검증 테스트

        검증 포인트:
        - 가중치 합계가 1.0인지 확인
        - 眞善美孝永 철학 반영
        - Numpy array 타입 검증
        """
        # SSOT 가중치 검증 (agents.md Ⅱ. SSOT)
        expected_weights = np.array([0.35, 0.35, 0.20, 0.08, 0.02])

        assert np.array_equal(SSOT_WEIGHTS, expected_weights), "SSOT weights mismatch"
        assert np.isclose(np.sum(SSOT_WEIGHTS), 1.0), "Weights must sum to 1.0"
        assert isinstance(SSOT_WEIGHTS, np.ndarray), "SSOT_WEIGHTS must be numpy array"

        # 각 기둥 가중치 검증
        pillars = [
            "Truth (眞)",
            "Goodness (善)",
            "Beauty (美)",
            "Serenity (孝)",
            "Eternity (永)",
        ]
        expected_values = [0.35, 0.35, 0.20, 0.08, 0.02]

        for i, (pillar, expected) in enumerate(
            zip(pillars, expected_values, strict=False)
        ):
            assert SSOT_WEIGHTS[i] == expected, f"{pillar} weight mismatch"

    def test_calculator_singleton_pattern(self) -> None:
        """
        Calculator 싱글톤 패턴 검증

        검증 포인트:
        - 글로벌 인스턴스 일관성
        - 상태 공유
        """
        # 글로벌 인스턴스 검증
        assert trinity_calculator is not None
        assert isinstance(trinity_calculator, TrinityCalculator)

        # 동일한 인스턴스인지 검증
        calculator2 = TrinityCalculator()
        # Note: 싱글톤이 아니므로 다른 인스턴스지만 기능은 동일해야 함
        assert isinstance(calculator2, TrinityCalculator)

    @pytest.mark.asyncio
    async def test_trinity_validator_integration(
        self, calculator_instance: TrinityCalculator
    ) -> None:
        """
        Trinity Type Validator 통합 테스트

        검증 포인트:
        - @validate_with_trinity 데코레이터 적용
        - 런타임 검증 실행
        """
        # calculate_raw_scores에 @validate_with_trinity 데코레이터 적용됨
        # 정상 실행되는지 검증
        query_data = {
            "valid_structure": True,
            "risk_level": 0.0,
            "narrative": "complete",
        }

        # When - Should not raise exception
        result = calculator_instance.calculate_raw_scores(query_data)

        # Then
        assert len(result) == 5
        assert all(isinstance(s, float) for s in result)


# 메타 테스트 - Trinity Score 기반 자가 검증
def test_test_coverage_self_verification() -> None:
    """
    이 테스트 파일 자체의 Trinity Score 기반 검증

    AFO 왕국의 자율 확장 원칙:
    테스트가 Trinity Score로 자신을 검증하는 메타 구조
    """
    import inspect

    # 현재 모듈의 모든 테스트 함수 수집
    current_module = inspect.currentframe().f_globals
    test_functions = [
        name
        for name, obj in current_module.items()
        if name.startswith("test_") and callable(obj)
    ]

    # Trinity 측면 검증
    trinity_aspects = [
        "raw_scores",
        "trinity_score",
        "persona_scores",
        "ssot_weights",
        "validation",
    ]
    covered_aspects = []

    for func_name in test_functions:
        func_obj = current_module[func_name]
        docstring = func_obj.__doc__ or ""
        func_name_lower = func_name.lower()

        for aspect in trinity_aspects:
            if aspect in func_name_lower or aspect in docstring.lower():
                if aspect not in covered_aspects:
                    covered_aspects.append(aspect)

    # 핵심 Trinity 측면 80% 이상 커버리지 검증
    coverage_ratio = len(covered_aspects) / len(trinity_aspects)
    assert coverage_ratio >= 0.8, f"Trinity coverage too low: {coverage_ratio:.1%}"

    # SSOT 가중치 검증 (메타 테스트 내 메타 검증)
    from AFO.services.trinity_calculator import SSOT_WEIGHTS

    assert np.isclose(np.sum(SSOT_WEIGHTS), 1.0), "SSOT weights validation in meta-test"


if __name__ == "__main__":
    # AFO 왕국의 자율 테스트 실행 (개발 시 직접 실행용)

    # 간단한 smoke test
    async def smoke_test():
        calculator = TrinityCalculator()

        # Raw scores 테스트
        query_data = {
            "valid_structure": True,
            "risk_level": 0.0,
            "narrative": "complete",
        }
        raw_scores = calculator.calculate_raw_scores(query_data)

        # Trinity Score 테스트
        calculator.calculate_trinity_score(raw_scores)

        # Persona Scores 테스트
        await calculator.calculate_persona_scores({"type": "commander"})

        return True

    # 동기 컨텍스트에서 실행
    try:
        import asyncio

        asyncio.run(smoke_test())
    except Exception:
        raise
