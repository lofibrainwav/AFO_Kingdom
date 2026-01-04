from __future__ import annotations

from dataclasses import dataclass
from typing import Any

W = {"truth": 0.35, "goodness": 0.35, "beauty": 0.20, "serenity": 0.08, "eternity": 0.02}

@dataclass(frozen=True)
class TrinityEval:
    score_total: float          # 0~100
    score_breakdown: dict[str, float]  # 5 pillars, 0~25 each

_LAST: TrinityEval | None = None

def _norm(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x.strip().lower()
    return str(x).strip().lower()

def _get_text(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    for k in ("answer", "output", "prediction", "text", "response"):
        v = getattr(obj, k, None)
        if isinstance(v, str):
            return v
        if v is not None:
            try:
                return str(v)
            except Exception:
                pass
    try:
        return str(obj)
    except Exception:
        return ""

def trinity_score(example: Any, pred: Any) -> TrinityEval:
    # 眞: exact match (보수적 기본형)
    gold = _norm(getattr(example, "answer", None) or getattr(example, "gold", None) or getattr(example, "label", None))
    out = _norm(_get_text(pred))

    truth_25 = 25.0 if (gold and out and gold == out) else (12.5 if not gold else 0.0)

    # 善: 시크릿/위험 흔적 감점(보수적)
    bad = ("slack webhook", "api_key", "private key", "password=", "-----begin", "token=")
    goodness_25 = 25.0 if not any(b in out for b in bad) else 10.0

    # 美: 장황함 감점(150단어 기준)
    words = len(out.split())
    beauty_25 = 25.0 if words <= 150 else max(10.0, 25.0 - (words - 150) * 0.1)

    # 孝: 사족/변명 패턴 감점(가벼운 휴리스틱)
    fatigue = ("as an ai", "i can't", "i cannot", "i'm unable", "sorry")
    serenity_25 = 25.0 if not any(f in out for f in fatigue) else 18.0

    # 永: 재현성/구조성(지금은 만점 유지)
    eternity_25 = 25.0

    bd = {
        "truth": float(truth_25),
        "goodness": float(goodness_25),
        "beauty": float(beauty_25),
        "serenity": float(serenity_25),
        "eternity": float(eternity_25),
    }

    total_0_100 = (
        bd["truth"] * W["truth"]
        + bd["goodness"] * W["goodness"]
        + bd["beauty"] * W["beauty"]
        + bd["serenity"] * W["serenity"]
        + bd["eternity"] * W["eternity"]
    ) * 4.0

    return TrinityEval(score_total=float(total_0_100), score_breakdown=bd)

def trinity_metric(example: Any, pred: Any, trace: Any = None) -> float:
    global _LAST
    ev = trinity_score(example, pred)
    _LAST = ev
    return ev.score_total

def get_last_eval() -> dict[str, Any] | None:
    if _LAST is None:
        return None
    return {"score_total": _LAST.score_total, "score_breakdown": _LAST.score_breakdown}
