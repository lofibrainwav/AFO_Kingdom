"""
SSOT 드리프트 방지 테스트 (CI 즉사 시스템)

이 테스트가 실패하면 즉시 CI가 중단되어 SSOT 위반을 방지합니다.
SSOT 가중치 합계가 1.0인지 검증하여 재발을 원천 차단합니다.
"""

import pytest

from AFO.observability.rule_constants import WEIGHTS, WEIGHTS_HASH, validate_weights


class TestSSOTWeights:
    """SSOT 가중치 무결성 테스트"""

    def test_weights_sum_is_one(self):
        """SSOT 가중치 합계 검증: 합계가 정확히 1.0이어야 함"""
        total = round(sum(float(v) for v in WEIGHTS.values()), 5)
        assert total == 1.0, f"SSOT VIOLATION: WEIGHTS sum is {total}, must be 1.0"

    def test_weights_structure(self):
        """SSOT 가중치 구조 검증: 필수 키들이 존재해야 함"""
        required_keys = {"truth", "goodness", "beauty", "serenity", "eternity"}
        assert set(WEIGHTS.keys()) == required_keys, (
            f"Missing keys in WEIGHTS: {required_keys - set(WEIGHTS.keys())}"
        )

    def test_weights_values_range(self):
        """SSOT 가중치 값 범위 검증: 0.0 <= value <= 1.0"""
        for pillar, weight in WEIGHTS.items():
            assert 0.0 <= weight <= 1.0, f"Invalid weight for {pillar}: {weight}"

    def test_weights_hash_exists(self):
        """SSOT 해시 스탬프 존재 검증"""
        assert WEIGHTS_HASH is not None, "WEIGHTS_HASH must be defined"
        assert len(WEIGHTS_HASH) == 12, f"WEIGHTS_HASH must be 12 chars, got {len(WEIGHTS_HASH)}"

    def test_validate_weights_function(self):
        """validate_weights 함수 정상 작동 검증"""
        # 정상 가중치로 테스트
        validate_weights(WEIGHTS)  # 예외 발생하지 않아야 함

        # 잘못된 합계로 테스트
        invalid_weights = WEIGHTS.copy()
        invalid_weights["truth"] = 0.5  # 합계가 1.0이 아니게 됨

        with pytest.raises(ValueError, match="SSOT VIOLATION"):
            validate_weights(invalid_weights)

    def test_weights_immutable(self):
        """SSOT 가중치 불변성 검증: 직접 수정 불가"""
        original_hash = WEIGHTS_HASH

        # WEIGHTS를 수정하려고 하면 해시가 바뀌어야 함
        # (실제로는 WEIGHTS가 수정되면 안 되지만, 테스트를 위해)
        # 이 테스트는 WEIGHTS가 변경되면 해시도 변경되는지 확인
        import hashlib

        current_hash = hashlib.sha256(str(sorted(WEIGHTS.items())).encode()).hexdigest()[:12]
        assert current_hash == original_hash, "WEIGHTS has been modified - SSOT violation detected"
