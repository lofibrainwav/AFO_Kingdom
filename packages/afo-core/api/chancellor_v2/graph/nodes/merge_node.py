"""MERGE Node - Synthesize 3 strategists results with DecisionResult."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState


def merge_node(state: GraphState) -> GraphState:
    """Synthesize results from TRUTH, GOODNESS, and BEAUTY nodes.

    SSOT Contract: Return DecisionResult, never bare boolean.

    Args:
        state: Current graph state

    Returns:
        Updated graph state with DecisionResult evaluation
    """
    from ..decision_result import DecisionResult

    # Get individual scores
    truth_score = state.outputs.get("TRUTH", {}).get("score", 0)
    goodness_score = state.outputs.get("GOODNESS", {}).get("score", 0)
    beauty_score = state.outputs.get("BEAUTY", {}).get("score", 0)

    pillar_scores = {"truth": truth_score, "goodness": goodness_score, "beauty": beauty_score}

    # Calculate Trinity Score (眞善美孝永 weights)
    trinity_score = (truth_score * 0.35 + goodness_score * 0.35 + beauty_score * 0.20) * 100

    # SSOT validation: All 5 pillars must be present for valid Trinity Score
    pillars_present = {"truth", "goodness", "beauty"}
    if not pillars_present.issubset(pillar_scores.keys()):
        missing_pillars = pillars_present - set(pillar_scores.keys())
        trinity_score = 0  # Force 0 if pillars missing

    # Risk Score (currently using goodness_score as proxy, can be enhanced)
    risk_score = (1.0 - goodness_score) * 100  # Lower goodness = higher risk

    # Create DecisionResult based on evaluation
    if trinity_score >= 90 and risk_score <= 10:
        decision = DecisionResult.auto_run(trinity_score, risk_score, pillar_scores)
    else:
        decision = DecisionResult.ask_commander(trinity_score, risk_score, pillar_scores)

    # Store DecisionResult in state
    if "MERGE" not in state.outputs:
        state.outputs["MERGE"] = {}

    state.outputs["MERGE"] = decision.to_dict()

    return state
