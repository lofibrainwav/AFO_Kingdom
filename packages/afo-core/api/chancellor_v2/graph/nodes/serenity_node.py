"""SERENITY Node - Automation and failure recovery evaluation (孝: Serenity)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


def serenity_node(state: GraphState) -> GraphState:
    """Evaluate automation, error recovery, and user friction reduction aspects.

    孝 (Serenity) - 평온·연속성, 자동화, 실패 복구 용이성 (8% 가중치)

    Args:
        state: Current graph state

    Returns:
        Updated graph state with serenity evaluation
    """
    skill_id = state.plan.get("skill_id", "")
    query = state.plan.get("query", "")

    # Evaluate automation potential
    automation_score = _evaluate_automation_potential(query)

    # Evaluate error recovery capabilities
    recovery_score = _evaluate_error_recovery(skill_id)

    # Evaluate user friction reduction
    friction_score = _evaluate_friction_reduction(state)

    # Overall serenity score (평균)
    serenity_score = (automation_score + recovery_score + friction_score) / 3.0

    evaluation = {
        "skill_id": skill_id,
        "automation_score": automation_score,
        "recovery_score": recovery_score,
        "friction_score": friction_score,
        "serenity_score": serenity_score,
        "issues": [],
    }

    # Store evaluation results
    if "SERENITY" not in state.outputs:
        state.outputs["SERENITY"] = {}

    state.outputs["SERENITY"] = evaluation

    return state


def _evaluate_automation_potential(query: str) -> float:
    """평온(孝): 자동화 잠재력 평가 - AFO 왕국 특화"""
    if not query:
        return 0.7  # AFO 왕국은 기본적으로 고도 자동화 지향

    query_lower = query.lower()

    # AFO 왕국 자동화 키워드 확장 (CI/CD, MCP, Chancellor Graph 등 고려)
    automation_keywords = {
        # 기존 키워드
        "auto": 0.9,
        "automate": 0.9,
        "automatic": 0.9,
        "batch": 0.8,
        "script": 0.8,
        "pipeline": 0.8,
        "schedule": 0.7,
        "cron": 0.7,
        "workflow": 0.7,
        "deploy": 0.6,
        "build": 0.6,
        "test": 0.6,
        # AFO 왕국 특화 키워드 (고점수)
        "mcp": 0.95,
        "chancellor": 0.95,
        "graph": 0.95,
        "trinity": 0.95,
        "orchestrate": 0.9,
        "coordinate": 0.9,
        "parallel": 0.9,
        "async": 0.85,
        "concurrent": 0.85,
        "distributed": 0.85,
        "ci/cd": 0.85,
        "webhook": 0.85,
        "trigger": 0.85,
        "event-driven": 0.85,
        "reactive": 0.85,
        # 일반 자동화 키워드 (중간 점수)
        "integration": 0.75,
        "stream": 0.75,
        "queue": 0.75,
        "cache": 0.7,
        "optimize": 0.7,
        "scale": 0.7,
        "monitor": 0.65,
        "alert": 0.65,
        "dashboard": 0.65,
    }

    max_score = 0.0
    keyword_count = 0

    for keyword, score in automation_keywords.items():
        if keyword in query_lower:
            max_score = max(max_score, score)
            keyword_count += 1

    # 다중 키워드 보너스 (자동화 복합성이 높을수록 점수 상승)
    if keyword_count >= 3:
        max_score = min(max_score + 0.1, 1.0)
    elif keyword_count >= 2:
        max_score = min(max_score + 0.05, 1.0)

    return max_score if max_score > 0 else 0.8  # AFO 왕국 기본 자동화 수준 향상


def _evaluate_error_recovery(skill_id: str) -> float:
    """연속성(孝): 오류 복구 용이성 평가"""
    if not skill_id:
        return 0.5

    skill_lower = skill_id.lower()

    # 복구 용이한 스킬 평가
    recovery_indicators = {
        "backup": 0.9,
        "restore": 0.9,
        "rollback": 0.9,
        "retry": 0.8,
        "fallback": 0.8,
        "circuit": 0.8,
        "health": 0.7,
        "monitor": 0.7,
        "alert": 0.7,
    }

    recovery_score = 0.0
    for indicator, score in recovery_indicators.items():
        if indicator in skill_lower:
            recovery_score = max(recovery_score, score)

    # 기본 복구 용이성 (대부분의 작업은 어느 정도 복구 가능)
    return max(recovery_score, 0.7)


def _evaluate_friction_reduction(state: GraphState) -> float:
    """마찰 제거(孝): 사용자 경험 개선 평가"""
    # 기존 outputs 확인으로 마찰 감소 평가
    outputs = state.outputs or {}

    friction_score = 0.0

    # 다른 노드들의 평가가 있는지 확인 (협력적 평가)
    if "TRUTH" in outputs:
        friction_score += 0.2  # 타입 안전성으로 인지 부하 감소

    if "GOODNESS" in outputs:
        friction_score += 0.2  # 보안 검증으로 신뢰성 향상

    if "BEAUTY" in outputs:
        friction_score += 0.2  # 일관된 UX로 학습 비용 감소

    # 기본 마찰 감소 점수 (어떤 자동화든 어느 정도 도움)
    base_friction = 0.4

    return min(friction_score + base_friction, 1.0)
