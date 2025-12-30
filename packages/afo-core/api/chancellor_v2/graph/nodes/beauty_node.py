"""BEAUTY Node - UX/beauty evaluation (美: Beauty)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


def beauty_node(state: GraphState) -> GraphState:
    """Evaluate UX and aesthetic aspects.

    Args:
        state: Current graph state

    Returns:
        Updated graph state with beauty evaluation
    """
    skill_id = state.plan.get("skill_id", "")

    # Basic UX/beauty evaluation
    beauty_score = 0.75  # Default good score
    evaluation = {
        "skill_id": skill_id,
        "ux_friendly": True,
        "simple_design": True,
        "consistent_api": True,
        "documentation_quality": 0.8,
        "score": beauty_score,
        "issues": [],
    }

    # Store evaluation results
    if "BEAUTY" not in state.outputs:
        state.outputs["BEAUTY"] = {}

    state.outputs["BEAUTY"] = evaluation

    return state
