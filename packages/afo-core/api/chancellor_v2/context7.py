"""Chancellor Graph V2 - Context7 Integration (Contract).

SSOT Contract: Context7 is REQUIRED, not optional.
MCP unavailable = execution fails (no passthrough).

Includes Kingdom DNA injection at trace start.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState

logger = logging.getLogger(__name__)

# Contract: MCP is REQUIRED by default (set to "0" only for emergency bypass)
MCP_REQUIRED = os.getenv("AFO_MCP_REQUIRED", "1") == "1"

# Context7 knowledge domains mapping
DOMAIN_MAP = {
    "PARSE": "afo-architecture",
    "TRUTH": "technical",
    "GOODNESS": "security",
    "BEAUTY": "ux-design",
    "MERGE": "afo-philosophy",
    "EXECUTE": "skills-registry",
    "VERIFY": "testing",
}

# Kingdom DNA query (Constitutional SSOT)
KINGDOM_DNA_QUERY = (
    "AFO Kingdom SSOT Constitution: "
    "眞善美孝永 5 Pillars Philosophy, "
    "Field Manual 41 Principles, "
    "Trinity Score Calculation, "
    "Historical Decisions and Precedents (Kingdom DNA)"
)


def _call_context7(query: str, domain: str = "technical") -> dict[str, Any]:
    """Call MCP retrieve_context tool for Context7 knowledge injection.

    Contract: If MCP_REQUIRED=1 and MCP unavailable, raises RuntimeError.
    """
    try:
        from AFO.services.mcp_stdio_client import call_tool

        server_name = "afo-ultimate-mcp"
        resp = call_tool(
            server_name,
            tool_name="retrieve_context",
            arguments={
                "query": query,
                "domain": domain,
            },
        )
        return resp.get("result", {"context": "", "source": "unknown"})

    except ImportError as e:
        if MCP_REQUIRED:
            raise RuntimeError(
                "MCP Context7 (retrieve_context) is REQUIRED but mcp_stdio_client not available. "
                "Set AFO_MCP_REQUIRED=0 to bypass (NOT RECOMMENDED)."
            ) from e
        logger.warning("[V2] mcp_stdio_client not available, context7 disabled")
        return {"context": "", "mode": "disabled"}

    except Exception as e:
        if MCP_REQUIRED:
            raise RuntimeError(f"MCP Context7 REQUIRED but failed: {e}") from e
        logger.error(f"[V2] Context7 error: {e}")
        return {"context": "", "error": str(e)}


def inject_kingdom_dna(state: GraphState) -> GraphState:
    """Inject Kingdom DNA at trace start (1-time constitutional injection).

    Contract: Always called at trace start before any node execution.
    """
    result = _call_context7(
        query=KINGDOM_DNA_QUERY,
        domain="afo-philosophy",
    )

    if "context7" not in state.outputs:
        state.outputs["context7"] = {}

    state.outputs["context7"]["KINGDOM_DNA"] = {
        "domain": "afo-philosophy",
        "query": KINGDOM_DNA_QUERY,
        "context": result.get("context", "")[:1500],  # Truncate for storage
        "injected": True,
    }

    # Also store in plan for node access
    state.plan["_kingdom_dna"] = result.get("context", "")[:1500]

    logger.info("[V2] Kingdom DNA injected at trace start")

    return state


def inject_context(state: GraphState, step: str) -> GraphState:
    """Inject Context7 knowledge for current step.

    Contract: Always called before each node (no bypass).
    """
    domain = DOMAIN_MAP.get(step, "technical")

    # Build query based on step
    query = f"AFO Kingdom {step} guidelines"

    if step == "PARSE":
        query = f"AFO command parsing: {state.input}"
    elif step == "TRUTH":
        query = f"Technical truth verification: {state.plan.get('skill_id', 'skill')}"
    elif step == "GOODNESS":
        query = f"Security and ethics: {state.plan.get('skill_id', 'skill')}"
    elif step == "BEAUTY":
        query = f"UX design principles for: {state.plan.get('skill_id', 'skill')}"
    elif step == "MERGE":
        query = "眞善美 trinity synthesis methodology"
    elif step == "EXECUTE":
        query = f"Skill execution: {state.plan.get('skill_id', 'skill')}"
    elif step == "VERIFY":
        query = "Verification and validation standards"

    # Call Context7 (Contract: will raise if MCP_REQUIRED and unavailable)
    result = _call_context7(query=query, domain=domain)

    # Store context in state
    if "context7" not in state.outputs:
        state.outputs["context7"] = {}
    state.outputs["context7"][step] = {
        "domain": domain,
        "query": query,
        "context": result.get("context", "")[:500],  # Truncate for storage
    }

    logger.info(f"[V2] Context7 injected for {step} (domain={domain})")

    return state
