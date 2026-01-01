"""GOODNESS Node - Ethical/security evaluation (善: Goodness)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


def goodness_node(state: GraphState) -> GraphState:
    """Evaluate ethical and security aspects.

    善 (Goodness) - 인간 중심, 윤리·안정성, 보안, 비용 최적화 평가

    Args:
        state: Current graph state

    Returns:
        Updated graph state with goodness evaluation
    """
    skill_id = state.plan.get("skill_id", "")
    query = state.plan.get("query", "")

    # 실제 윤리/보안/비용 평가 로직
    security_score = _evaluate_security(skill_id, query)
    privacy_score = _evaluate_privacy_compliance(query)
    cost_score = _evaluate_cost_efficiency(skill_id)
    ethical_score = _evaluate_ethical_considerations(query)

    # 종합 Goodness 점수 (가중 평균)
    goodness_score = (
        security_score * 0.35  # 보안 우선
        + privacy_score * 0.25  # 개인정보 보호
        + cost_score * 0.25  # 비용 효율성
        + ethical_score * 0.15  # 윤리적 고려
    )

    risk_level = "low" if goodness_score >= 0.8 else "medium" if goodness_score >= 0.6 else "high"

    evaluation = {
        "skill_id": skill_id,
        "security_check": security_score >= 0.7,
        "privacy_compliant": privacy_score >= 0.7,
        "cost_efficient": cost_score >= 0.7,
        "ethical_score": ethical_score,
        "risk_level": risk_level,
        "score": goodness_score,
        "issues": [],
    }

    # Store evaluation results
    if "GOODNESS" not in state.outputs:
        state.outputs["GOODNESS"] = {}

    state.outputs["GOODNESS"] = evaluation

    return state


def _evaluate_security(skill_id: str, query: str) -> float:
    """보안성 평가"""
    if not skill_id and not query:
        return 0.6

    combined_text = f"{skill_id} {query}".lower()

    # 보안 관련 키워드 평가
    security_indicators = {
        "security": 0.9,
        "secure": 0.9,
        "auth": 0.9,
        "authentication": 0.9,
        "encrypt": 0.9,
        "encryption": 0.9,
        "ssl": 0.8,
        "tls": 0.8,
        "firewall": 0.8,
        "audit": 0.8,
        "logging": 0.8,
        "sanitize": 0.7,
        "validate": 0.7,
        "escape": 0.7,
        "csrf": 0.8,
        "xss": 0.8,
        "injection": 0.8,
    }

    security_score = 0.0
    for indicator, score in security_indicators.items():
        if indicator in combined_text:
            security_score = max(security_score, score)

    return max(security_score, 0.6)  # 기본 보안 수준


def _evaluate_privacy_compliance(query: str) -> float:
    """개인정보 보호 평가"""
    if not query:
        return 0.7

    query_lower = query.lower()

    # 개인정보 관련 키워드 평가
    privacy_indicators = {
        "gdpr": 0.9,
        "ccpa": 0.9,
        "privacy": 0.9,
        "pii": 0.9,
        "consent": 0.8,
        "anonymize": 0.8,
        "pseudonymize": 0.8,
        "data retention": 0.8,
        "data deletion": 0.8,
        "user data": 0.7,
        "personal data": 0.7,
    }

    privacy_score = 0.0
    for indicator, score in privacy_indicators.items():
        if indicator in query_lower:
            privacy_score = max(privacy_score, score)

    return max(privacy_score, 0.7)  # 기본 개인정보 보호 준수


def _evaluate_cost_efficiency(skill_id: str) -> float:
    """비용 효율성 평가"""
    if not skill_id:
        return 0.6

    skill_lower = skill_id.lower()

    # 비용 효율성 관련 키워드 평가
    cost_indicators = {
        "optimize": 0.9,
        "efficient": 0.9,
        "performance": 0.8,
        "cache": 0.8,
        "memory": 0.7,
        "cpu": 0.7,
        "local": 0.8,
        "lightweight": 0.8,
        "minimal": 0.8,
        "batch": 0.7,
        "async": 0.7,
        "streaming": 0.7,
    }

    cost_score = 0.0
    for indicator, score in cost_indicators.items():
        if indicator in skill_lower:
            cost_score = max(cost_score, score)

    return max(cost_score, 0.6)  # 기본 비용 효율성


def _evaluate_ethical_considerations(query: str) -> float:
    """윤리적 고려 평가"""
    if not query:
        return 0.7

    query_lower = query.lower()

    # 윤리적 고려 관련 키워드 평가
    ethical_indicators = {
        "ethical": 0.9,
        "fair": 0.9,
        "bias": 0.9,
        "responsible": 0.9,
        "inclusive": 0.8,
        "accessible": 0.8,
        "diversity": 0.8,
        "transparency": 0.8,
        "explainable": 0.8,
        "accountability": 0.8,
        "sustainable": 0.7,
        "environment": 0.7,
        "social impact": 0.7,
    }

    ethical_score = 0.0
    for indicator, score in ethical_indicators.items():
        if indicator in query_lower:
            ethical_score = max(ethical_score, score)

    return max(ethical_score, 0.7)  # 기본 윤리적 고려
