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


def run_v2(input_payload: dict[str, Any], nodes: dict[str, NodeFn]) -> GraphState:
    """Execute graph with provided nodes.

    Args:
        input_payload: Input from commander
        nodes: Dict mapping step names to node functions

    Returns:
        Final GraphState after execution
    """
    trace_id = uuid.uuid4().hex
    state = GraphState(
        trace_id=trace_id,
        request_id=uuid.uuid4().hex,
        input=input_payload,
        started_at=_now(),
        updated_at=_now(),
    )

    for step in ORDER:
        state.step = step
        _emit(state, step, "enter", True)

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
