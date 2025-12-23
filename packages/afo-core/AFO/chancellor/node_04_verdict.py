from __future__ import annotations

from typing import TYPE_CHECKING, Any

from AFO.observability.verdict_event import (Decision, VerdictEvent,
                                             VerdictFlags)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from AFO.observability.verdict_logger import VerdictLogger


def build_verdict_event(
    *,
    trace_id: str,
    decision: Decision,
    rule_id: str,
    trinity_score: float,
    risk_score: float,
    dry_run_default: bool,
    residual_doubt: bool,
    graph_node_id: str = "node_04_verdict",
    step: int = 41,
    extra: Mapping[str, Any] | None = None,
) -> VerdictEvent:
    flags: VerdictFlags = {
        "dry_run": bool(dry_run_default),
        "residual_doubt": bool(residual_doubt),
    }
    return VerdictEvent(
        trace_id=trace_id,
        graph_node_id=graph_node_id,
        step=int(step),
        decision=decision,
        rule_id=rule_id,
        trinity_score=float(trinity_score),
        risk_score=float(risk_score),
        flags=flags,
        timestamp=VerdictEvent.now_iso(),
        extra=extra,
    )


def emit_verdict(
    logger: VerdictLogger,
    *,
    trace_id: str,
    decision: Decision,
    rule_id: str,
    trinity_score: float,
    risk_score: float,
    dry_run_default: bool,
    residual_doubt: bool,
    graph_node_id: str = "node_04_verdict",
    step: int = 41,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ev = build_verdict_event(
        trace_id=trace_id,
        decision=decision,
        rule_id=rule_id,
        trinity_score=trinity_score,
        risk_score=risk_score,
        dry_run_default=dry_run_default,
        residual_doubt=residual_doubt,
        graph_node_id=graph_node_id,
        step=step,
        extra=extra,
    )
    return logger.emit(ev)
