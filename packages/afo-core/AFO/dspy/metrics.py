from __future__ import annotations

from difflib import SequenceMatcher


def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return float(SequenceMatcher(None, a, b).ratio())


def calculate_trinity_fidelity(example, pred, trace=None) -> float:
    expected = getattr(example, "expected", "") or getattr(example, "answer", "") or ""
    got = getattr(pred, "briefing", "") or ""
    sim = _ratio(expected, got)

    structure_hits = 0
    for token in ("Summary", "Next Steps", "Risks"):
        if token.lower() in got.lower():
            structure_hits += 1
    structure = structure_hits / 3.0

    length_score = min(len(got) / 800.0, 1.0)

    # Trinity Score Weighting
    return (0.55 * sim) + (0.30 * structure) + (0.15 * length_score)
