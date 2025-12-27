"""Chancellor Graph V2 - Context7 Integration.

Provides knowledge base context injection via MCP.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState

logger = logging.getLogger(__name__)

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


def _call_context7(query: str, domain: str = "technical") -> dict[str, Any]:
    """Call MCP retrieve_context tool for Context7 knowledge injection.

    Returns structured knowledge or error dict.
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

    except ImportError:
        logger.warning("[V2] mcp_stdio_client not available, context7 disabled")
        return {"context": "", "mode": "disabled"}
    except Exception as e:
        logger.error(f"[V2] Context7 error: {e}")
        return {"context": "", "error": str(e)}


def inject_context(state: GraphState, step: str) -> GraphState:
    """Inject Context7 knowledge for current step.

    Adds relevant context to state.plan based on step domain.
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

    # Call Context7
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


def wrap_with_context(node_fn):
    """Decorator to wrap a node function with Context7 injection.

    Usage:
        @wrap_with_context
        def my_node(state: GraphState) -> GraphState:
            ...
    """

    def _wrapped(state: GraphState) -> GraphState:
        step = state.step
        state = inject_context(state, step)
        return node_fn(state)

    _wrapped.__name__ = node_fn.__name__
    _wrapped.__doc__ = node_fn.__doc__
    return _wrapped
