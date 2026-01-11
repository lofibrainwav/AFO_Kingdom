# Trinity Score 엣지 케이스 및 회귀 테스트
"""
Trinity Score 계산의 엣지 케이스와 회귀 테스트
SSOT 가중치(眞35%, 善35%, 美20%, 孝8%, 永2%) 검증
"""

import pytest
from AFO.domain.metrics.trinity import (TrinityInputs, TrinityMetrics,
                                        calculate_trinity)


class TestTrinityScoreEdgeCases:
    """Trinity Score 엣지 케이스 테스트"""

    def test_perfect_health_score(self):
        """완벽 건강 상태에서의 Trinity Score 검증"""
        # Given: 모든 기관 정상 (현재 시스템 상태)
        inputs = TrinityInputs(
            truth=1.0,  # Redis/PostgreSQL 정상
            goodness=1.0,  # 모든 기관 정상
            beauty=1.0,  # API 정상
            filial_serenity=1.0,  # Ollama 정상
        )

        # When: Trinity Score 계산
        metrics = TrinityMetrics.from_inputs(inputs, eternity=1.0)

        # Then: 완벽 점수 확인
        assert metrics.trinity_score == 1.0
        assert metrics.balance_status == "balanced"
        assert metrics.balance_delta == 0.0

    def test_partial_failure_score(self):
        """부분 실패 상태에서의 Trinity Score 검증"""
        # Given: 일부 기관 실패
        inputs = TrinityInputs(
            truth=0.5,  # Redis 실패
            goodness=0.75,  # 3/4 기관 정상
            beauty=1.0,  # API 정상
            filial_serenity=0.0,  # Ollama 실패
        )

        # When: Trinity Score 계산
        metrics = TrinityMetrics.from_inputs(inputs, eternity=0.75)

        # Then: 부분 점수 확인
        expected_score = (
            0.35 * 0.5 + 0.35 * 0.75 + 0.20 * 1.0 + 0.08 * 0.0 + 0.02 * 0.75
        )
        assert abs(metrics.trinity_score - expected_score) < 0.001
        assert metrics.balance_status in ["warning", "imbalanced"]

    def test_critical_failure_score(self):
        """심각한 실패 상태에서의 Trinity Score 검증"""
        # Given: 대부분 기관 실패
        inputs = TrinityInputs(
            truth=0.0,  # 데이터베이스 실패
            goodness=0.25,  # 1/4 기관만 정상
            beauty=0.0,  # API 실패
            filial_serenity=0.0,  # LLM 실패
        )

        # When: Trinity Score 계산
        metrics = TrinityMetrics.from_inputs(inputs, eternity=0.25)

        # Then: 낮은 점수 확인
        assert metrics.trinity_score < 0.3
        assert metrics.balance_status == "imbalanced"

    def test_zero_division_protection(self):
        """0으로 나누기 방지 테스트"""
        # Given: 모든 값이 0
        inputs = TrinityInputs(truth=0.0, goodness=0.0, beauty=0.0, filial_serenity=0.0)

        # When: Trinity Score 계산
        metrics = TrinityMetrics.from_inputs(inputs, eternity=0.0)

        # Then: 안전하게 처리
        assert metrics.serenity_core == 0.0  # 기하평균 0 처리
        assert metrics.trinity_score >= 0.0
        assert metrics.balance_status == "balanced"  # delta = 0

    def test_weight_validation(self):
        """SSOT 가중치 검증"""
        # Given: TrinityMetrics 클래스
        metrics = TrinityMetrics.from_inputs(TrinityInputs(1, 1, 1, 1), eternity=1)

        # Then: 가중치 합계가 1.0인지 확인
        total_weight = (
            metrics.WEIGHT_TRUTH
            + metrics.WEIGHT_GOODNESS
            + metrics.WEIGHT_BEAUTY
            + metrics.WEIGHT_SERENITY
            + metrics.WEIGHT_ETERNITY
        )
        assert abs(total_weight - 1.0) < 1e-6

    def test_balance_delta_calculation(self):
        """균형 차이 계산 검증"""
        # Given: 불균형한 점수들
        inputs = TrinityInputs(
            truth=1.0,  # 최고
            goodness=0.5,  # 중간
            beauty=0.2,  # 최저
            filial_serenity=0.7,
        )

        # When: 계산
        metrics = TrinityMetrics.from_inputs(inputs, eternity=0.8)

        # Then: delta = max - min
        values = [1.0, 0.5, 0.2, 0.7, 0.8]
        expected_delta = max(values) - min(values)
        assert abs(metrics.balance_delta - expected_delta) < 0.001

    @pytest.mark.parametrize(
        "inputs,expected_status",
        [
            (TrinityInputs(1, 1, 1, 1), "balanced"),  # 완벽 균형
            (TrinityInputs(0.8, 0.5, 0.8, 0.5), "warning"),  # 중간 불균형
            (TrinityInputs(1, 0, 1, 0), "imbalanced"),  # 심한 불균형
        ],
    )
    def test_balance_status_parametrized(self, inputs, expected_status):
        """균형 상태 파라미터화 테스트"""
        metrics = TrinityMetrics.from_inputs(inputs, eternity=0.8)
        assert metrics.balance_status == expected_status


class TestTrinityScoreRegression:
    """Trinity Score 회귀 테스트"""

    def test_calculate_trinity_helper_function(self):
        """calculate_trinity 헬퍼 함수 회귀 테스트"""
        # Given: 0-1 스케일 입력
        result = calculate_trinity(
            truth=1.0, goodness=1.0, beauty=1.0, filial_serenity=1.0, eternity=1.0
        )

        # Then: 완벽 점수
        assert result.trinity_score == 1.0
        assert result.balance_status == "balanced"

    def test_100_scale_conversion(self):
        """100점 스케일 변환 테스트"""
        # Given: 100점 스케일 입력
        result = calculate_trinity(
            truth=100,
            goodness=100,
            beauty=100,
            filial_serenity=100,
            eternity=100,
            from_100_scale=True,
        )

        # Then: 1.0으로 변환되어 계산
        assert result.trinity_score == 1.0

    def test_to_dict_serialization(self):
        """직렬화 테스트"""
        # Given: TrinityMetrics
        metrics = TrinityMetrics.from_inputs(TrinityInputs(1, 1, 1, 1), eternity=1)

        # When: 딕셔너리 변환
        data = metrics.to_dict()

        # Then: 필수 키들 존재
        required_keys = [
            "truth",
            "goodness",
            "beauty",
            "filial_serenity",
            "eternity",
            "trinity_score",
            "balance_status",
            "weights",
        ]
        for key in required_keys:
            assert key in data

    def test_error_handling(self):
        """예외 처리 테스트"""
        # Given: 잘못된 입력
        # When: 계산 시도
        result = calculate_trinity(float("nan"), 1, 1, 1, 1)

        # Then: 안전하게 처리 (fallback)
        assert isinstance(result, TrinityMetrics)
        assert result.trinity_score == 0  # fallback 값
