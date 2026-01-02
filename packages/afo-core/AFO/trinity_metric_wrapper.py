from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TrinityMetricResult:
    score: float
    details: dict[str, Any]


class TrinityMetricWrapper:
    def __init__(self, metric_fn: Callable[[str, str], float]) -> None:
        self._metric_fn = metric_fn

    def score(self, prompt: str, target: str) -> TrinityMetricResult:
        s = float(self._metric_fn(prompt, target))
        if s < 0.0:
            s = 0.0
        if s > 1.0:
            s = 1.0
        return TrinityMetricResult(score=s, details={})
