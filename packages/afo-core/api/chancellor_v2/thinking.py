"""Chancellor Graph V2 - Sequential Thinking Integration (Contract).

SSOT Contract: Sequential Thinking is REQUIRED, not optional.
MCP unavailable = execution fails (no passthrough).
"""

from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState

logger = logging.getLogger(__name__)

# Contract: MCP is REQUIRED by default (set to "0" only for emergency bypass)
MCP_REQUIRED = os.getenv("AFO_MCP_REQUIRED", "1") == "1"


def _call_sequential_thinking(
    thought: str,
    thought_number: int = 1,
    total_thoughts: int = 1,
    next_thought_needed: bool = False,
) -> dict[str, Any]:
    """Call MCP sequential_thinking tool.

    Contract: If MCP_REQUIRED=1 and MCP unavailable, raises RuntimeError.
    """
    try:
        from AFO.services.mcp_stdio_client import call_tool

        server_name = "afo-ultimate-mcp"
        resp = call_tool(
            server_name,
            tool_name="sequential_thinking",
            arguments={
                "thought": thought,
                "thought_number": thought_number,
                "total_thoughts": total_thoughts,
                "next_thought_needed": next_thought_needed,
            },
        )
        return resp.get("result", {"thought": thought, "processed": True})

    except ImportError as e:
        if MCP_REQUIRED:
            raise RuntimeError(
                "MCP sequential_thinking is REQUIRED but mcp_stdio_client not available. "
                "Set AFO_MCP_REQUIRED=0 to bypass (NOT RECOMMENDED)."
            ) from e
        logger.warning("[V2] mcp_stdio_client not available, using passthrough mode")
        return {"thought": thought, "processed": False, "mode": "passthrough"}

    except Exception as e:
        if MCP_REQUIRED:
            # Re-raise to fail execution (contract violation)
            raise RuntimeError(f"MCP sequential_thinking REQUIRED but failed: {e}") from e
        logger.error(f"[V2] Sequential Thinking error: {e}")
        return {"thought": thought, "error": str(e)}


def apply_sequential_thinking(state: GraphState, step: str) -> GraphState:
    """Apply Sequential Thinking to current step.

    Contract: Always called before each node (no bypass).
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

    # Call MCP Sequential Thinking (Contract: will raise if MCP_REQUIRED and unavailable)
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

    logger.info(f"[V2] Sequential Thinking applied to {step}: {result.get('processed', False)}")

    return state
