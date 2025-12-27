"""Chancellor Graph V2 Runner.

Orchestrates node execution with checkpoint/event logging.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Callable
from typing import Any

from .state import GraphState
from .store import append_event, save_checkpoint

NodeFn = Callable[[GraphState], GraphState]

# Canonical node execution order
ORDER = [
    "CMD",
    "PARSE",
    "TRUTH",
    "GOODNESS",
    "BEAUTY",
    "MERGE",
    "EXECUTE",
    "VERIFY",
    "REPORT",
]


def _now() -> float:
    """Get current Unix timestamp."""
    return time.time()


def _emit(
    state: GraphState,
    step: str,
    event: str,
    ok: bool,
    detail: dict[str, Any] | None = None,
) -> None:
    """Emit event to trace log."""
    payload: dict[str, Any] = {
        "ts": _now(),
        "trace_id": state.trace_id,
        "step": step,
        "event": event,
        "ok": ok,
    }
    if detail is not None:
        payload["detail"] = detail
    append_event(state.trace_id, payload)


def _checkpoint(state: GraphState, step: str) -> None:
    """Save checkpoint for current state."""
    payload = {
        "trace_id": state.trace_id,
        "request_id": state.request_id,
        "step": step,
        "input": state.input,
        "plan": state.plan,
        "outputs": state.outputs,
        "errors": state.errors,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
    }
    save_checkpoint(state.trace_id, step, payload)


def run_v2(
    input_payload: dict[str, Any],
    nodes: dict[str, NodeFn],
    *,
    enable_thinking: bool = True,
    enable_context7: bool = True,
) -> GraphState:
    """Execute graph with provided nodes.

    Args:
        input_payload: Input from commander
        nodes: Dict mapping step names to node functions
        enable_thinking: Enable Sequential Thinking MCP integration
        enable_context7: Enable Context7 knowledge injection

    Returns:
        Final GraphState after execution
    """
    # Import thinking/context modules lazily to avoid circular imports
    thinking_apply = None
    context7_inject = None

    if enable_thinking:
        try:
            from api.chancellor_v2.thinking import apply_sequential_thinking

            thinking_apply = apply_sequential_thinking
        except ImportError:
            pass

    if enable_context7:
        try:
            from api.chancellor_v2.context7 import inject_context

            context7_inject = inject_context
        except ImportError:
            pass

    trace_id = uuid.uuid4().hex
    state = GraphState(
        trace_id=trace_id,
        request_id=uuid.uuid4().hex,
        input=input_payload,
        started_at=_now(),
        updated_at=_now(),
    )

    # Track thinking/context7 status
    state.outputs["_meta"] = {
        "thinking_enabled": thinking_apply is not None,
        "context7_enabled": context7_inject is not None,
    }

    for step in ORDER:
        state.step = step
        _emit(state, step, "enter", True)

        # Apply Sequential Thinking before node (眞: step-by-step reasoning)
        if thinking_apply is not None:
            try:
                state = thinking_apply(state, step)
            except Exception as e:
                _emit(state, step, "thinking_error", False, {"error": str(e)})

        # Inject Context7 knowledge before node (眞: knowledge grounding)
        if context7_inject is not None:
            try:
                state = context7_inject(state, step)
            except Exception as e:
                _emit(state, step, "context7_error", False, {"error": str(e)})

        fn = nodes.get(step)
        if fn is None:
            state.errors.append(f"missing node: {step}")
            _emit(state, step, "missing_node", False)
            _checkpoint(state, step)
            return state

        try:
            state = fn(state)
            state.updated_at = _now()
            _emit(state, step, "exit", True)
            _checkpoint(state, step)
        except Exception as e:
            state.errors.append(f"{step} failed: {type(e).__name__}: {e}")
            _emit(state, step, "error", False, {"error": f"{type(e).__name__}: {e}"})
            _checkpoint(state, step)
            return state

    return state
