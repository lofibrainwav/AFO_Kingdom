"""Chancellor Graph V2 Runner (Contract Enforced).

Orchestrates node execution with checkpoint/event logging.
Contract: Sequential Thinking + Context7 are REQUIRED (no bypass).
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Callable
from typing import Any

from .state import GraphState
from .store import append_event, save_checkpoint

NodeFn = Callable[[GraphState], GraphState]

# SSOT: Chancellor Graph V2 Execution Order (5기둥 Trinity 완전 평가)
# This is the SINGLE SOURCE OF TRUTH for Chancellor Graph node execution sequence
# Any changes to execution order MUST be made here and reflected in documentation
ORDER = [
    "CMD",
    "SECURITY",  # 2026 AI Threat Detection (TICKET-085)
    "PARSE",
    "TRUTH",  # 眞 (Truth) - 기술적 확실성
    "GOODNESS",  # 善 (Goodness) - 윤리·안정성
    "BEAUTY",  # 美 (Beauty) - 구조적 단순함
    "SERENITY",  # 孝 (Serenity) - 자동화·연속성
    "ETERNITY",  # 永 (Eternity) - 영속성·재현성
    "MIPRO",  # MIPRO optimization node (optional, feature-flag controlled)
    "MERGE",  # 5기둥 종합 평가
    "GOVERNANCE",  # 2026 Policy Adherence & Bounded Autonomy (TICKET-084)
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

    Contract: Sequential Thinking + Context7 are ALWAYS applied.
    No enable_* flags - this is enforced by design.

    Args:
        input_payload: Input from commander
        nodes: Dict mapping step names to node functions

    Returns:
        Final GraphState after execution
    """
    # Import thinking/context modules (Contract: these MUST be available)
    from api.chancellor_v2.context7 import inject_context, inject_kingdom_dna
    from api.chancellor_v2.thinking import apply_sequential_thinking

    trace_id = uuid.uuid4().hex
    state = GraphState(
        trace_id=trace_id,
        request_id=uuid.uuid4().hex,
        input=input_payload,
        started_at=_now(),
        updated_at=_now(),
    )

    # Contract: Always inject Kingdom DNA at trace start (Constitutional SSOT)
    _emit(state, "INIT", "kingdom_dna_start", True)
    state = inject_kingdom_dna(state)
    _emit(state, "INIT", "kingdom_dna_complete", True)

    # Track contract enforcement status
    state.outputs["_meta"] = {
        "thinking_enforced": True,
        "context7_enforced": True,
        "kingdom_dna_injected": True,
    }

    from AFO.observability.ai_observability import observability

    for step in ORDER:
        state.step = step
        _emit(state, step, "enter", True)

        # Contract: Trace every node execution (眞: transparency, 善: monitoring)
        with observability.trace(
            operation_name=f"chancellor_graph.{step}",
            trace_id=state.trace_id,
            request_id=state.request_id,
            agent="Chancellor",
        ) as span:
            # Contract: Apply Sequential Thinking BEFORE every node (眞: step-by-step reasoning)
            state = apply_sequential_thinking(state, step)

            # Contract: Inject Context7 knowledge BEFORE every node (眞: knowledge grounding)
            state = inject_context(state, step)

            fn = nodes.get(step)
            if fn is None:
                state.errors.append(f"missing node: {step}")
                _emit(state, step, "missing_node", False)
                span.status = "ERROR"
                span.attributes["error"] = f"missing node: {step}"
                _checkpoint(state, step)
                return state

            try:
                state = fn(state)
                state.updated_at = _now()
                _emit(state, step, "exit", True)

                # Record outcome in span
                span.status = "OK"
                if step == "MERGE":
                    merge_out = state.outputs.get("MERGE", {})
                    span.attributes["trinity_score"] = merge_out.get("trinity_score", 0.0)
                    span.attributes["governance_approved"] = True  # Mark for compliance check

                _checkpoint(state, step)

            except Exception as e:
                state.errors.append(f"{step} failed: {type(e).__name__}: {e}")
                _emit(state, step, "error", False, {"error": f"{type(e).__name__}: {e}"})
                span.status = "ERROR"
                span.attributes["error.type"] = type(e).__name__
                span.attributes["error.message"] = str(e)
                _checkpoint(state, step)
                return state

    return state

    return state
