from __future__ import annotations

def get_current_risk_score() -> float:
    try:
        from trinity_os.core.risk_score import get_current_risk_score as _g
        return float(_g())
    except Exception:
        return 0.0
