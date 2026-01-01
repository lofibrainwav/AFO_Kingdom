"""BEAUTY Node - UX/beauty evaluation (美: Beauty)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


def beauty_node(state: GraphState) -> GraphState:
    """Evaluate UX and aesthetic aspects.

    美 (Beauty) - 구조적 단순함, 모듈화, 일관된 API/UI 평가

    Args:
        state: Current graph state

    Returns:
        Updated graph state with beauty evaluation
    """
    skill_id = state.plan.get("skill_id", "")
    query = state.plan.get("query", "")

    # 실제 UX/구조/일관성 평가 로직
    ux_score = _evaluate_ux_friendliness(query)
    simplicity_score = _evaluate_structural_simplicity(skill_id)
    consistency_score = _evaluate_api_consistency(skill_id, query)
    modularity_score = _evaluate_modularity(skill_id)

    # 종합 Beauty 점수 (가중 평균)
    beauty_score = (
        ux_score * 0.3  # UX 우선
        + simplicity_score * 0.3  # 구조적 단순함
        + consistency_score * 0.25  # API 일관성
        + modularity_score * 0.15  # 모듈화
    )

    evaluation = {
        "skill_id": skill_id,
        "ux_friendly": ux_score >= 0.7,
        "simple_design": simplicity_score >= 0.7,
        "consistent_api": consistency_score >= 0.7,
        "modular_design": modularity_score >= 0.7,
        "documentation_quality": _evaluate_documentation_quality(query),
        "score": beauty_score,
        "issues": [],
    }

    # Store evaluation results
    if "BEAUTY" not in state.outputs:
        state.outputs["BEAUTY"] = {}

    state.outputs["BEAUTY"] = evaluation

    return state


def _evaluate_ux_friendliness(query: str) -> float:
    """UX 친화성 평가"""
    if not query:
        return 0.6

    query_lower = query.lower()

    # UX 관련 키워드 평가
    ux_indicators = {
        "user experience": 0.9,
        "ux": 0.9,
        "ui": 0.9,
        "interface": 0.8,
        "usability": 0.8,
        "accessible": 0.8,
        "responsive": 0.8,
        "intuitive": 0.8,
        "user-friendly": 0.8,
        "ergonomic": 0.7,
        "design": 0.7,
        "aesthetic": 0.7,
        "visual": 0.6,
    }

    ux_score = 0.0
    for indicator, score in ux_indicators.items():
        if indicator in query_lower:
            ux_score = max(ux_score, score)

    return max(ux_score, 0.6)  # 기본 UX 수준


def _evaluate_structural_simplicity(skill_id: str) -> float:
    """구조적 단순함 평가"""
    if not skill_id:
        return 0.6

    skill_lower = skill_id.lower()

    # 단순함 관련 키워드 평가
    simplicity_indicators = {
        "simple": 0.9,
        "clean": 0.9,
        "minimal": 0.9,
        "straightforward": 0.9,
        "refactor": 0.8,
        "simplify": 0.8,
        "optimize": 0.8,
        "readable": 0.7,
        "maintainable": 0.7,
        "elegant": 0.7,
        "concise": 0.7,
        "clear": 0.7,
        "intuitive": 0.6,
    }

    simplicity_score = 0.0
    for indicator, score in simplicity_indicators.items():
        if indicator in skill_lower:
            simplicity_score = max(simplicity_score, score)

    return max(simplicity_score, 0.6)  # 기본 구조적 단순함


def _evaluate_api_consistency(skill_id: str, query: str) -> float:
    """API 일관성 평가"""
    combined_text = f"{skill_id} {query}".lower()

    # API 일관성 관련 키워드 평가
    consistency_indicators = {
        "consistent": 0.9,
        "standard": 0.9,
        "convention": 0.9,
        "pattern": 0.8,
        "rest": 0.8,
        "restful": 0.8,
        "graphql": 0.8,
        "openapi": 0.8,
        "swagger": 0.7,
        "schema": 0.7,
        "contract": 0.7,
        "interface": 0.6,
        "protocol": 0.6,
        "specification": 0.6,
    }

    consistency_score = 0.0
    for indicator, score in consistency_indicators.items():
        if indicator in combined_text:
            consistency_score = max(consistency_score, score)

    return max(consistency_score, 0.7)  # 기본 API 일관성


def _evaluate_modularity(skill_id: str) -> float:
    """모듈화 평가"""
    if not skill_id:
        return 0.6

    skill_lower = skill_id.lower()

    # 모듈화 관련 키워드 평가
    modularity_indicators = {
        "modular": 0.9,
        "module": 0.9,
        "component": 0.8,
        "service": 0.8,
        "microservice": 0.8,
        "plugin": 0.8,
        "extension": 0.8,
        "separation": 0.7,
        "concern": 0.7,
        "layer": 0.7,
        "architecture": 0.6,
        "design pattern": 0.6,
        "solid": 0.6,
    }

    modularity_score = 0.0
    for indicator, score in modularity_indicators.items():
        if indicator in skill_lower:
            modularity_score = max(modularity_score, score)

    return max(modularity_score, 0.6)  # 기본 모듈화 수준


def _evaluate_documentation_quality(query: str) -> float:
    """문서화 품질 평가 (보조 메트릭)"""
    if not query:
        return 0.6

    query_lower = query.lower()

    # 문서화 관련 키워드 평가
    doc_indicators = {
        "docs": 0.9,
        "documentation": 0.9,
        "readme": 0.9,
        "guide": 0.8,
        "tutorial": 0.8,
        "example": 0.8,
        "reference": 0.7,
        "comment": 0.6,
        "docstring": 0.6,
        "javadoc": 0.6,
    }

    doc_score = 0.0
    for indicator, score in doc_indicators.items():
        if indicator in query_lower:
            doc_score = max(doc_score, score)

    return max(doc_score, 0.6)  # 기본 문서화 수준
