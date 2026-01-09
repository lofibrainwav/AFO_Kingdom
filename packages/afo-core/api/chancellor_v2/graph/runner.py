"""Chancellor Graph V2 Runner (Contract Enforced).

Orchestrates node execution with checkpoint/event logging.
Contract: Sequential Thinking + Context7 are REQUIRED (no bypass).
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Any

from .state import GraphState
from .store import append_event, save_checkpoint

NodeFn = Callable[[GraphState], Awaitable[GraphState]]

# SSOT: Chancellor Graph V2 Execution Order (5기둥 Trinity 완전 평가)
# This is the SINGLE SOURCE OF TRUTH for Chancellor Graph node execution sequence
# Assessment Cluster (TRUTH to ETERNITY) will be executed in parallel
ORDER = [
    "CMD",
    "PARSE",
    "ASSESSMENT_CLUSTER",  # Pseudo-step for parallel Trinity assessment
    "MIPRO",
    "MERGE",
    "EXECUTE",
    "VERIFY",
    "REPORT",
]

TRINITY_PILLARS = ["TRUTH", "GOODNESS", "BEAUTY", "SERENITY", "ETERNITY"]


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


async def run_v2(input_payload: dict[str, Any], nodes: dict[str, NodeFn]) -> GraphState:
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
        "parallel_assessment": True,
    }

    for step in ORDER:
        state.step = step

        if step == "ASSESSMENT_CLUSTER":
            # Parallel execution of 眞善美孝永
            _emit(state, step, "enter_cluster", True)

            tasks = []
            for pillar in TRINITY_PILLARS:
                fn = nodes.get(pillar)
                if fn:
                    # Note: We pass copies of state or ensure nodes only update their own output keys
                    # Since GraphState is a dataclass, we must be careful.
                    # Each node will return a NEW state or modify one.
                    # We will collect all outputs.
                    tasks.append(_execute_node_safe(state, pillar, fn))

            # Execute all pillars in parallel
            pillar_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Merge results back to main state
            for pillar_res in pillar_results:
                if isinstance(pillar_res, GraphState):
                    # Merge outputs for that pillar
                    # Assumption: pillar nodes only update state.outputs[pillar]
                    for k, v in pillar_res.outputs.items():
                        if k in TRINITY_PILLARS:
                            state.outputs[k] = v
                    # Collect errors
                    state.errors.extend(pillar_res.errors)
                elif isinstance(pillar_res, Exception):
                    state.errors.append(f"Pillar execution failed: {pillar_res}")

            state.updated_at = _now()
            _emit(state, step, "exit_cluster", True)
            _checkpoint(state, step)
            continue

        _emit(state, step, "enter", True)

        # Contract: Apply Sequential Thinking BEFORE every node
        state = apply_sequential_thinking(state, step)

        # Contract: Inject Context7 knowledge BEFORE every node
        state = inject_context(state, step)

        fn = nodes.get(step)
        if fn is None:
            state.errors.append(f"missing node: {step}")
            _emit(state, step, "missing_node", False)
            _checkpoint(state, step)
            return state

        try:
            state = await fn(state)
            state.updated_at = _now()
            _emit(state, step, "exit", True)
            _checkpoint(state, step)
        except Exception as e:
            state.errors.append(f"{step} failed: {type(e).__name__}: {e}")
            _emit(state, step, "error", False, {"error": f"{type(e).__name__}: {e}"})
            _checkpoint(state, step)
            return state

    # Final Achievement: Save Evidence Pack (SSOT)
    await _save_evidence_pack(state)

    return state


async def _save_evidence_pack(state: GraphState) -> None:
    """Save the results of this run to the Council Evidence Pack (.jsonl)."""
    try:
        from AFO.config.settings import get_settings

        settings = get_settings()

        # Ensure artifacts directory exists
        evidence_dir = os.path.join(settings.ARTIFACTS_DIR, "council_runs")
        os.makedirs(evidence_dir, exist_ok=True)

        # Create run record
        record = {
            "timestamp": datetime.fromtimestamp(_now(), UTC).isoformat(),
            "trace_id": state.trace_id,
            "request_id": state.request_id,
            "command": state.input.get("command", ""),
            "outputs": state.outputs,
            "errors": state.errors,
            "decision": state.outputs.get("MERGE", {}),
        }

        # Append to daily evidence pack
        date_str = datetime.now(UTC).strftime("%Y%m%d")
        evidence_file = os.path.join(evidence_dir, f"council_{date_str}.jsonl")

        with open(evidence_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    except Exception as e:
        # Don't let evidence pack failure crash the command, but log it
        import logging

        logging.getLogger(__name__).error(f"Failed to save Council Evidence Pack: {e}")


async def _execute_node_safe(state: GraphState, step: str, fn: NodeFn) -> GraphState:
    """Helper to execute a node safely for parallel cluster."""
    import copy

    # Create a shallow copy of state for this parallel branch to avoid race conditions on dicts
    # Note: GraphState has fields like outputs, errors which are mutable.
    local_state = GraphState(
        trace_id=state.trace_id,
        request_id=state.request_id,
        input=state.input,
        plan=state.plan,
        outputs=copy.deepcopy(state.outputs),
        errors=[],  # Start with clean errors for this branch
        step=step,
        started_at=state.started_at,
        updated_at=state.updated_at,
    )

    from api.chancellor_v2.context7 import inject_context
    from api.chancellor_v2.thinking import apply_sequential_thinking

    local_state = apply_sequential_thinking(local_state, step)
    local_state = inject_context(local_state, step)

    try:
        return await fn(local_state)
    except Exception as e:
        local_state.errors.append(f"{step} failed: {e}")
        return local_state
