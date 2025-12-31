from __future__ import annotations
from difflib import SequenceMatcher

def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return float(SequenceMatcher(None, a, b).ratio())

def _risk_penalty(text: str) -> float:
    t = (text or "").lower()
    hits = 0
    for w in ("i think", "maybe", "might be", "not sure", "guess", "probably", "hallucinat", "unverified"):
        if w in t:
            hits += 1
    return min(hits * 0.08, 0.32)

def _has_sections(text: str, required: tuple[str, ...]) -> float:
    t = (text or "").lower()
    hit = 0
    for s in required:
        if s.lower() in t:
            hit += 1
    return hit / max(len(required), 1)

def _count_sources(text: str) -> int:
    t = (text or "")
    for key in ("Sources:", "sources:", "Citations:", "citations:"):
        if key in t:
            tail = t.split(key, 1)[1]
            lines = [ln.strip() for ln in tail.splitlines() if ln.strip()]
            return min(len(lines), 10)
    return 0

def objective_factcard(example, pred, trace=None) -> float:
    expected = getattr(example, "expected", "") or ""
    got = getattr(pred, "fact_card", "") or ""

    sim = _ratio(str(expected), str(got))
    structure = _has_sections(str(got), ("As-of", "Key point", "Now do", "Sources"))
    sources = _count_sources(str(got))
    sources_score = min(sources / 2.0, 1.0)

    risk = _risk_penalty(str(got))

    score = (0.50 * sim) + (0.30 * structure) + (0.20 * sources_score)
    if sources < 2:
        score *= 0.4
    score = max(score - risk, 0.0)
    return float(score)

def objective_onepager(example, pred, trace=None) -> float:
    expected = getattr(example, "expected", "") or ""
    got = getattr(pred, "one_pager", "") or ""

    sim = _ratio(str(expected), str(got))
    structure = _has_sections(str(got), ("As-of", "Summary", "Key changes", "Risks", "Action items", "Sources"))
    sources = _count_sources(str(got))
    sources_score = min(sources / 2.0, 1.0)

    risk = _risk_penalty(str(got))

    score = (0.50 * sim) + (0.30 * structure) + (0.20 * sources_score)
    if sources < 2:
        score *= 0.4
    score = max(score - risk, 0.0)
    return float(score)
