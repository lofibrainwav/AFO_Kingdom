"""Governance Node - AFO Kingdom Chancellor Graph.
Enforces 2026 Policy Adherence and Bounded Autonomy (TICKET-084).
"""

import logging
from typing import Any

from AFO.agents.governance_agent import RiskLevel, evaluate_action
from api.chancellor_v2.graph.state import GraphState

logger = logging.getLogger(__name__)


async def governance_node(state: GraphState) -> GraphState:
    """Governance node: Enforce policy adherence before execution.

    Philosophical Alignment:
    - 眞 (Truth): Verified against SSOT policies
    - 善 (Goodness): Fail-closed on policy violations
    - 孝 (Serenity): Prevent high-risk actions without approval
    """
    plan = state.plan
    merge_output = state.outputs.get("MERGE", {})

    # Extract intended action and context from MERGE result
    action = merge_output.get("action", "unknown_action")
    agent_name = merge_output.get("agent", "Chancellor")
    context = {
        "command": state.input.get("command", ""),
        "plan_summary": plan or "No plan available",
        "trinity_score": merge_output.get("trinity_score", 0.0),
        "path": merge_output.get("target_path", ""),
    }

    # Evaluate action through Governance Agent (Sima Yi)
    decision = await evaluate_action(action, agent_name, **context)

    # Store governance results in state
    state.outputs["GOVERNANCE"] = {
        "decision": decision.decision,
        "risk_level": decision.risk_level.value,
        "reasoning": decision.reasoning,
        "policy_checks": [
            {
                "policy": pc.policy_name,
                "passed": pc.passed,
                "risk": pc.risk_level.value,
                "details": pc.details,
            }
            for pc in decision.policy_checks
        ],
    }

    # SSOT: Enforce "Escalated" or "Denied" decisions
    if decision.decision in ["denied", "escalated"]:
        logger.warning(
            f"🚨 GOVERNANCE {decision.decision.upper()}: {action} | {decision.reasoning}"
        )

        # Update MERGE output to block execution if necessary
        # We modify the state's knowledge so EXECUTE node knows it sits on restricted ground
        if "_meta" not in state.outputs:
            state.outputs["_meta"] = {}

        state.outputs["_meta"]["governance_blocked"] = True
        state.outputs["_meta"]["governance_decision"] = decision.decision

        # If denied, we append an error to stop the graph if the runner expects error-free flow
        if decision.decision == "denied":
            state.errors.append(f"Governance Denied: {decision.reasoning}")

    return state


def governance_node_sync(state: GraphState) -> GraphState:
    """Synchronous wrapper for governance_node (for graph runner compatibility)."""
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, governance_node(state))
                return future.result()
        else:
            return loop.run_until_complete(governance_node(state))
    except (RuntimeError, Exception):
        return asyncio.run(governance_node(state))
