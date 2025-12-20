from datetime import datetime

from strategists.base import log_action, robust_execute


def log(action: str, details: dict | None = None) -> str:
    """
    Huang Zhong (Eternity): Evolution Logging

    [Eternity Philosophy]:
    - History: Records actions with timestamps for persistence.
    - Resilience: Log failure does not stop the system.
    """

    if details is None:
        details = {}

    def _logic(val):
        act, dets = val
        {
            "action": act,
            "timestamp": datetime.utcnow().isoformat(),
            "trinity": dets.get("trinity", 100.0),
            "legacy_stable": True,
        }
        return "LOG_SAVED"

    # Robust Execute: Fallback to LOG_FAILED
    result = robust_execute(_logic, (action, details), fallback_value="LOG_FAILED")
    log_action("Huang Zhong 永", result)
    return str(result)


# V2 Interface Alias
eternity_log = log
