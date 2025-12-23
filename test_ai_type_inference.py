#!/usr/bin/env python3
"""
AI 타입 추론 테스트용 임시 파일
Phase 4: 타입 커버리지 향상 적용 예시.
"""

from typing import Any


def process_data(data: Any) -> list[str] | dict[str, str] | str:
    """데이터 처리 함수 - 타입 힌트 추가됨."""
    if isinstance(data, list):
        return [item.upper() for item in data if isinstance(item, str)]
    if isinstance(data, dict):
        return {k: v.upper() for k, v in data.items() if isinstance(v, str)}
    return str(data).upper()


def calculate_score(values: list[int | float]) -> float:
    """점수 계산 함수 - 타입 힌트 추가됨."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def validate_input(value: float, min_val: float, max_val: float) -> bool:
    """입력 검증 함수 - 타입 힌트 추가됨."""
    if not isinstance(value, (int, float)):
        return False
    return min_val <= value <= max_val


if __name__ == "__main__":
    # 테스트 실행

    # process_data 테스트
    result1 = process_data(["hello", "world"])

    result2 = process_data({"name": "alice", "city": "seoul"})

    # calculate_score 테스트
    result3 = calculate_score([10, 20, 30])

    # validate_input 테스트
    result4 = validate_input(25, 0, 100)
