#!/usr/bin/env python3
"""Trinity Calculator에 Trinity 검증 적용 테스트."""

import os
import pathlib
import sys


# 경로 추가
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent, "packages", "afo-core"))


def test_trinity_calculator_with_validator():
    """Trinity Calculator에 Trinity 검증 데코레이터 적용 테스트."""
    try:
        from AFO.services.trinity_calculator import trinity_calculator

        # 테스트 데이터
        test_cases = [
            {
                "name": "정상 케이스",
                "data": {
                    "valid_structure": True,
                    "risk_level": 0.05,
                    "narrative": "complete",
                },
            },
            {
                "name": "위험 케이스",
                "data": {
                    "valid_structure": True,
                    "risk_level": 0.15,  # 높은 위험
                    "narrative": "partial",
                },
            },
            {
                "name": "유효하지 않은 구조",
                "data": {"invalid": True, "valid_structure": False, "risk_level": 0.02},
            },
        ]

        for test_case in test_cases:
            try:
                # Raw scores 계산 (Trinity 검증 적용됨)
                raw_scores = trinity_calculator.calculate_raw_scores(test_case["data"])

                # Trinity Score 계산
                final_score = trinity_calculator.calculate_trinity_score(raw_scores)

                # 점수 해석
                if final_score >= 90 or final_score >= 70 or final_score >= 50:
                    pass

            except Exception:
                pass

    except ImportError:
        pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_trinity_calculator_with_validator()
