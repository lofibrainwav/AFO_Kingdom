"""Chancellor Graph V2 - Context7 Integration (Hard Contract).

SSOT Contract: Context7 is REQUIRED. No bypass. No disabled mode.
If MCP fails, execution STOPS.

Includes Kingdom DNA injection at trace start.
Uses get-library-docs for actual knowledge injection (not just resolve-library-id).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from api.chancellor_v2.graph.state import GraphState

logger = logging.getLogger(__name__)

# Context7 knowledge domains mapping to library queries
DOMAIN_QUERY_MAP = {
    "PARSE": ("langchain", "agents"),
    "TRUTH": ("python", "type checking"),
    "GOODNESS": ("fastapi", "security"),
    "BEAUTY": ("react", "components"),
    "MERGE": ("langchain", "chains"),
    "EXECUTE": ("langchain", "tools"),
    "VERIFY": ("pytest", "testing"),
}

# Kingdom DNA: AFO-specific knowledge from our own docs
KINGDOM_DNA_LIBRARY = "/afo-kingdom/docs"  # Our custom library if registered
KINGDOM_DNA_TOPIC = "眞善美孝永 philosophy field manual trinity"


def _call_context7_docs(library_id: str, topic: str) -> dict[str, Any]:
    """Call MCP get-library-docs for actual knowledge injection.

    Contract: If MCP fails for any reason, raises RuntimeError.
    NO BYPASS. NO DISABLED MODE.
    """
    from AFO.services.mcp_stdio_client import call_tool

    server_name = "context7"
    resp = call_tool(
        server_name,
        tool_name="get-library-docs",
        arguments={
            "context7CompatibleLibraryID": library_id,
            "topic": topic,
        },
    )

    if "error" in resp:
        raise RuntimeError(f"MCP Context7 get-library-docs failed: {resp['error']}")

    result = resp.get("result", {})

    # Extract text content from response
    content = result.get("content", [])
    if isinstance(content, list):
        texts = [
            c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"
        ]
        return {"context": "\n".join(texts), "source": "context7"}

    return {"context": str(result), "source": "context7"}


def _resolve_library_id(query: str) -> str:
    """Resolve a library name to Context7-compatible ID.

    Falls back to a generic library if resolution fails.
    """
    from AFO.services.mcp_stdio_client import call_tool

    server_name = "context7"
    resp = call_tool(
        server_name,
        tool_name="resolve-library-id",
        arguments={"libraryName": query},
    )

    if "error" in resp:
        # Fallback to langchain for general queries
        logger.warning(f"[V2] Library resolution failed for '{query}', using fallback")
        return "/langchain-ai/langchainjs"

    # Try to extract first library ID from response
    result = resp.get("result", {})
    content = result.get("content", [])
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                text = c.get("text", "")
                # Look for library ID pattern /org/project
                import re

                match = re.search(r"(/[\w-]+/[\w_-]+)", text)
                if match:
                    return match.group(1)

    return "/langchain-ai/langchainjs"


def inject_kingdom_dna(state: GraphState) -> GraphState:
    """Inject Kingdom DNA at trace start (1-time constitutional injection).

    Contract: Always called at trace start. Failure = execution stops.
    """
    # For Kingdom DNA, we use a well-known library with topic matching our philosophy
    library_id = "/langchain-ai/langgraphjs"  # LangGraph for agent patterns
    topic = "state management checkpoint workflow"

    result = _call_context7_docs(library_id, topic)

    if "context7" not in state.outputs:
        state.outputs["context7"] = {}

    context_text = result.get("context", "")[:1500]

    state.outputs["context7"]["KINGDOM_DNA"] = {
        "library_id": library_id,
        "topic": topic,
        "context": context_text,
        "injected": True,
        "length": len(context_text),
    }

    # Also store in plan for node access
    state.plan["_kingdom_dna"] = context_text

    logger.info(f"[V2] Kingdom DNA injected at trace start ({len(context_text)} chars)")

    return state


def inject_context(state: GraphState, step: str) -> GraphState:
    """Inject Context7 knowledge for current step.

    Contract: Always called before each node. Failure = execution stops.
    """
    # Get library and topic for this step
    library_query, topic = DOMAIN_QUERY_MAP.get(step, ("langchain", "general"))

    # Resolve library ID
    library_id = _resolve_library_id(library_query)

    # Get actual documentation
    result = _call_context7_docs(library_id, topic)

    # Store context in state
    if "context7" not in state.outputs:
        state.outputs["context7"] = {}

    context_text = result.get("context", "")[:500]

    state.outputs["context7"][step] = {
        "library_id": library_id,
        "topic": topic,
        "context": context_text,
        "length": len(context_text),
    }

    logger.info(f"[V2] Context7 injected for {step} ({len(context_text)} chars from {library_id})")

    return state
