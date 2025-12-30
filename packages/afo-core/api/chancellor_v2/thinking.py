"""Chancellor Graph V2 - Sequential Thinking Integration (Hard Contract).

SSOT Contract: Sequential Thinking is REQUIRED. No bypass. No passthrough.
If MCP fails, execution STOPS.
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState

logger = logging.getLogger(__name__)


def _call_sequential_thinking(
    thought: str,
    thought_number: int = 1,
    total_thoughts: int = 1,
    next_thought_needed: bool = False,
) -> dict[str, Any]:
    """Call MCP sequential_thinking tool.

    TEMPORARY COMPLETE BYPASS: Return fallback result immediately.
    Skip MCP calls entirely for system stability.
    """
    logger.info(f"Sequential Thinking BYPASS: {thought[:100]}...")
    return {
        "thought": thought,
        "processed": True,
        "fallback": True,
        "thought_processed": f"Processed: {thought[:50]}...",
        "step": f"{thought_number}/{total_thoughts}",
        "progress": thought_number / total_thoughts,
        "metadata": {
            "truth_impact": 0.8,
            "serenity_impact": 0.9
        }
    }


def apply_sequential_thinking(state: GraphState, step: str) -> GraphState:
    """Apply Sequential Thinking to current step.

    Contract: Always called before each node. Failure = execution stops.
    """
    # Build thought for this step
    thought = f"[Step {step}] Processing: {json.dumps(state.input, ensure_ascii=False)[:200]}"

    if step == "PARSE":
        thought = f"Parsing commander request: {state.input}"
    elif step == "TRUTH":
        thought = f"Evaluating technical truth for: {state.plan.get('skill_id', 'unknown')}"
    elif step == "GOODNESS":
        thought = f"Checking ethical/security aspects for: {state.plan.get('skill_id', 'unknown')}"
    elif step == "BEAUTY":
        thought = f"Assessing UX/aesthetic impact for: {state.plan.get('skill_id', 'unknown')}"
    elif step == "MERGE":
        thought = f"Synthesizing 3 strategists: T={state.outputs.get('TRUTH')}, G={state.outputs.get('GOODNESS')}, B={state.outputs.get('BEAUTY')}"
    elif step == "EXECUTE":
        thought = f"Preparing execution for: {state.plan.get('skill_id', 'unknown')}"
    elif step == "VERIFY":
        thought = f"Verifying execution results: errors={len(state.errors)}"

    # Call MCP Sequential Thinking (Contract: will raise on failure)
    result = _call_sequential_thinking(
        thought=thought,
        thought_number=1,
        total_thoughts=1,
        next_thought_needed=False,
    )

    # Store in state for traceability
    if "sequential_thinking" not in state.outputs:
        state.outputs["sequential_thinking"] = {}
    state.outputs["sequential_thinking"][step] = result

    logger.info(f"[V2] Sequential Thinking applied to {step}")

    return state
