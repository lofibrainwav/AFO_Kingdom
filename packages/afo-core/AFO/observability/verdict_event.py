from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Mapping


class VerdictFlags(TypedDict):
    dry_run: bool
    residual_doubt: bool


Decision = Literal["AUTO_RUN", "ASK"]


@dataclass(frozen=True)
class VerdictEvent:
    trace_id: str
    graph_node_id: str
    step: int
    decision: Decision
    rule_id: str
    trinity_score: float
    risk_score: float
    flags: VerdictFlags
    timestamp: str
    extra: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "trace_id": self.trace_id,
            "graph_node_id": self.graph_node_id,
            "step": self.step,
            "decision": self.decision,
            "rule_id": self.rule_id,
            "trinity_score": round(float(self.trinity_score), 2),
            "risk_score": float(self.risk_score),
            "flags": dict(self.flags),
            "timestamp": self.timestamp,
        }
        if self.extra:
            payload["extra"] = dict(self.extra)
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"), ensure_ascii=False)

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
