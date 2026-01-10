"""TRUTH Node - Technical truth evaluation (眞: Truth)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


async def truth_node(state: GraphState) -> GraphState:
    """Evaluate technical aspects of the planned execution.

    眞 (Truth) - 기술적 확실성, 타입 안전성, 테스트 무결성 평가
    Scholar: Zilong (Claude 3.5 Sonnet / Anthropic)
    """
    skill_id = state.plan.get("skill_id", "")
    query = state.plan.get("query", "")

    # 1. Heuristic Evaluation
    type_checking_score = _evaluate_type_safety(skill_id, query)
    test_coverage_score = _evaluate_test_coverage(skill_id)
    code_quality_score = _evaluate_code_quality(query)
    heuristic_score = (
        type_checking_score * 0.4
        + test_coverage_score * 0.35
        + code_quality_score * 0.25
    )

    # 2. Scholar Assessment (Zilong)
    import json

    from llm_router import llm_router

    prompt = f"""
    You are Zilong (眞), the Technical Strategist of the AFO Kingdom.
    Analyze the following execution plan for technical truth, type safety, and testability.

    Plan:
    - Skill: {skill_id}
    - Query/Target: {query}
    - Command: {state.input.get("command", "")}

    Guidelines:
    - Evaluate if the skill choice matches the query logic.
    - Assess type safety risks.
    - Check if the plan follows AFO Kingdom's technical standards (Python 3.12+, Pydantic).

    Provide your assessment in JSON:
    {{
      "score": float (0.0 to 1.0),
      "reasoning": string,
      "issues": list[string]
    }}
    """

    scholar_score = heuristic_score
    reasoning = "Heuristic assessment based on keyword mapping."
    issues = []
    assessment_mode = "Heuristic (Fallback)"
    scholar_model = "None"

    try:
        response = await llm_router.execute_with_routing(
            prompt, context={"provider": "anthropic", "quality_tier": "premium"}
        )
        if response and response.get("response"):
            try:
                # Basic JSON cleaning (in case of markdown blocks)
                text = (
                    response["response"]
                    .strip()
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )
                data = json.loads(text)
                scholar_score = data.get("score", heuristic_score)
                reasoning = data.get("reasoning", reasoning)
                issues = data.get("issues", [])
                assessment_mode = "LLM (Scholar)"
                scholar_model = response.get("model", "Anthropic/Zilong")
            except:
                pass
    except Exception as e:
        state.errors.append(f"Zilong (TRUTH) assessment failed: {e}")

    # Combine: 30% Heuristic + 70% Scholar
    final_score = (heuristic_score * 0.3) + (scholar_score * 0.7)

    evaluation = {
        "score": round(final_score, 3),
        "reasoning": reasoning,
        "issues": issues,
        "metadata": {
            "mode": assessment_mode,
            "scholar": "Zilong (眞)",
            "model": scholar_model,
        },
    }

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
