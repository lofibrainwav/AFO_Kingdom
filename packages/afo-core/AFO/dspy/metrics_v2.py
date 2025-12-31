from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any, Optional


def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return float(SequenceMatcher(None, a, b).ratio())


def _risk_penalty(text: str) -> float:
    t = (text or "").lower()
    hits = 0
    for w in (
        "i think",
        "maybe",
        "might be",
        "not sure",
        "guess",
        "probably",
        "hallucinat",
        "unverified",
    ):
        if w in t:
            hits += 1
    for w in ("http://", "https://"):
        if w in t:
            hits += 1
    return min(hits * 0.08, 0.40)


def calculate_trinity_objective(example: Any, pred: Any, trace: Any | None = None) -> float:
    expected = getattr(example, "expected", "") or getattr(example, "answer", "") or ""
    got = getattr(pred, "briefing", "") or ""

    sim = _ratio(str(expected), str(got))

    structure_hits = 0
    for token in ("Summary", "Next Steps", "Risks"):
        if token.lower() in str(got).lower():
            structure_hits += 1
    structure = structure_hits / 3.0

    length_score = min(len(str(got)) / 900.0, 1.0)

    risk = _risk_penalty(str(got))

    score = (0.55 * sim) + (0.30 * structure) + (0.15 * length_score)
    score = max(score - risk, 0.0)
    return float(score)
