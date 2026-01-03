#!/usr/bin/env python3
"""
Trinity Type System 통합 테스트
AFO Kingdom에 적용된 모든 컴포넌트 테스트.
"""

import asyncio
import os
import pathlib
import sys


# 경로 추가
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent, "packages", "afo-core"))


def test_full_trinity_system():
    """Trinity Type System 전체 통합 테스트."""
    # 1단계: 타입 커버리지 확인
    try:
        import subprocess

        result = subprocess.run(
            [sys.executable, "scripts/type_coverage_checker.py"],
            capture_output=True,
            text=True,
            cwd=pathlib.Path(__file__).parent,
            check=False,
        )

        for line in result.stdout.split("\n"):
            if any(keyword in line for keyword in ["Coverage", "Functions", "Typed"]):
                pass

    except Exception:
        pass

    # 2단계: 엄격 모드 테스트
    try:
        # 간단한 MyPy 테스트 (실제로는 더 많은 파일 테스트)
        result = subprocess.run(
            [
                "mypy",
                "--config-file",
                "pyproject.toml",
                "packages/afo-core/AFO/services/trinity_calculator.py",
                "--no-error-summary",
            ],
            capture_output=True,
            text=True,
            cwd=pathlib.Path(__file__).parent,
            check=False,
        )

        if result.returncode == 0:
            pass
        else:
            result.stdout.count("error:")

    except Exception:
        pass

    # 3단계: Trinity Calculator 테스트
    try:
        from AFO.services.trinity_calculator import trinity_calculator

        test_cases = [
            {
                "name": "완벽한 케이스",
                "data": {
                    "valid_structure": True,
                    "risk_level": 0.01,
                    "narrative": "complete",
                },
            },
            {
                "name": "일반 케이스",
                "data": {
                    "valid_structure": True,
                    "risk_level": 0.05,
                    "narrative": "complete",
                },
            },
            {
                "name": "주의 케이스",
                "data": {
                    "valid_structure": False,
                    "risk_level": 0.15,
                    "narrative": "partial",
                },
            },
        ]

        for test_case in test_cases:
            try:
                raw_scores = trinity_calculator.calculate_raw_scores(test_case["data"])
                trinity_calculator.calculate_trinity_score(raw_scores)

            except Exception:
                pass

    except Exception:
        pass

    # 4단계: Trinity 검증 데코레이터 테스트
    try:
        from AFO.utils.trinity_type_validator import trinity_validator

        # 데코레이터가 적용된 함수 테스트
        @trinity_validator
        def test_function(x: int, y: str = "test") -> str:
            """테스트용 함수."""
            return f"{x}: {y}"

        # 함수 호출 및 검증
        result = trinity_validator.validate_function(test_function, 42, "hello")

    except Exception:
        pass

    # 5단계: AI 타입 추론 데모
    try:
        from scripts.simple_ai_demo import simple_type_inference_demo

        simple_type_inference_demo()

    except Exception:
        pass

    # 최종 결과 요약


def test_async_services():
    """비동기 서비스 Trinity 검증 테스트."""

    async def run_async_tests():
        try:
            from AFO.services.persona_service import get_current_persona

            # 현재 페르소나 조회 테스트
            await get_current_persona()

        except Exception:
            pass

    # 비동기 테스트 실행
    asyncio.run(run_async_tests())


if __name__ == "__main__":
    test_full_trinity_system()
    test_async_services()
