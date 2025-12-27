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

    Contract: If MCP fails for any reason, raises RuntimeError.
    NO BYPASS. NO PASSTHROUGH.
    """
    from AFO.services.mcp_stdio_client import call_tool

    server_name = "sequential-thinking"
    resp = call_tool(
        server_name,
        tool_name="sequentialthinking",
        arguments={
            "thought": thought,
            "thoughtNumber": thought_number,
            "totalThoughts": total_thoughts,
            "nextThoughtNeeded": next_thought_needed,
        },
    )

    if "error" in resp:
        raise RuntimeError(f"MCP sequential_thinking failed: {resp['error']}")

    return resp.get("result", {"thought": thought, "processed": True})


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
