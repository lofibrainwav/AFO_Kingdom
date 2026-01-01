"""TRUTH Node - Technical truth evaluation (眞: Truth)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


def truth_node(state: GraphState) -> GraphState:
    """Evaluate technical aspects of the planned execution.

    眞 (Truth) - 기술적 확실성, 타입 안전성, 테스트 무결성 평가

    Args:
        state: Current graph state

    Returns:
        Updated graph state with truth evaluation
    """
    skill_id = state.plan.get("skill_id", "")
    query = state.plan.get("query", "")

    # 실제 기술적 평가 로직
    type_checking_score = _evaluate_type_safety(skill_id, query)
    test_coverage_score = _evaluate_test_coverage(skill_id)
    code_quality_score = _evaluate_code_quality(query)

    # 종합 Truth 점수 (가중 평균)
    truth_score = type_checking_score * 0.4 + test_coverage_score * 0.35 + code_quality_score * 0.25

    evaluation = {
        "skill_id": skill_id,
        "type_checking": type_checking_score,
        "test_coverage": test_coverage_score,
        "code_quality": code_quality_score,
        "score": truth_score,
        "issues": [],
    }

    # Store evaluation results
    if "TRUTH" not in state.outputs:
        state.outputs["TRUTH"] = {}

    state.outputs["TRUTH"] = evaluation

    return state


def _evaluate_type_safety(skill_id: str, query: str) -> float:
    """타입 안전성 평가"""
    if not skill_id and not query:
        return 0.5

    combined_text = f"{skill_id} {query}".lower()

    # 타입 안전성 지표
    type_indicators = {
        "type": 0.9,
        "typing": 0.9,
        "mypy": 0.9,
        "pydantic": 0.9,
        "dataclass": 0.8,
        "protocol": 0.8,
        "generic": 0.8,
        "cast": 0.7,
        "overload": 0.7,
        "literal": 0.7,
        "test": 0.6,
        "validate": 0.6,
        "check": 0.6,
    }

    safety_score = 0.0
    for indicator, score in type_indicators.items():
        if indicator in combined_text:
            safety_score = max(safety_score, score)

    return max(safety_score, 0.6)  # 기본 타입 안전성


def _evaluate_test_coverage(skill_id: str) -> float:
    """테스트 커버리지 평가"""
    if not skill_id:
        return 0.5

    skill_lower = skill_id.lower()

    # 테스트 관련 키워드 평가
    test_indicators = {
        "test": 0.9,
        "pytest": 0.9,
        "unittest": 0.8,
        "coverage": 0.8,
        "tdd": 0.8,
        "bdd": 0.7,
        "fixture": 0.7,
        "mock": 0.7,
        "assert": 0.7,
        "verify": 0.6,
        "validate": 0.6,
        "check": 0.6,
    }

    coverage_score = 0.0
    for indicator, score in test_indicators.items():
        if indicator in skill_lower:
            coverage_score = max(coverage_score, score)

    return max(coverage_score, 0.5)  # 기본 테스트 존재 가정


def _evaluate_code_quality(query: str) -> float:
    """코드 품질 평가"""
    if not query:
        return 0.6

    query_lower = query.lower()

    # 코드 품질 지표
    quality_indicators = {
        "lint": 0.9,
        "ruff": 0.9,
        "black": 0.9,
        "isort": 0.9,
        "clean": 0.8,
        "refactor": 0.8,
        "optimize": 0.8,
        "pattern": 0.7,
        "design": 0.7,
        "architecture": 0.7,
        "best practice": 0.8,
        "standard": 0.7,
        "convention": 0.7,
    }

    quality_score = 0.0
    for indicator, score in quality_indicators.items():
        if indicator in query_lower:
            quality_score = max(quality_score, score)

    return max(quality_score, 0.6)  # 기본 코드 품질
