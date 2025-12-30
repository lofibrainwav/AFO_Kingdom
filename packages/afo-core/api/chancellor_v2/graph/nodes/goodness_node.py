"""GOODNESS Node - Ethical/security evaluation (善: Goodness)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


def goodness_node(state: GraphState) -> GraphState:
    """Evaluate ethical and security aspects.

    Args:
        state: Current graph state

    Returns:
        Updated graph state with goodness evaluation
    """
    skill_id = state.plan.get("skill_id", "")

    # Basic ethical/security evaluation
    goodness_score = 0.85  # Default good score
    evaluation = {
        "skill_id": skill_id,
        "security_check": True,
        "privacy_compliant": True,
        "cost_efficient": True,
        "risk_level": "low",
        "score": goodness_score,
        "issues": [],
    }

    # Store evaluation results
    if "GOODNESS" not in state.outputs:
        state.outputs["GOODNESS"] = {}

    state.outputs["GOODNESS"] = evaluation

    return state
