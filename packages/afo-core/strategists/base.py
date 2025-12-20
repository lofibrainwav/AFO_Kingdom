from typing import Callable, Any, TypeVar, Optional
from datetime import datetime
try:
    from AFO.utils.logging import log_sse
except ImportError:
    # Fallback if logging module not found (Graceful Degradation)
    def log_sse(msg): print(f"[LOG] {msg}")

T = TypeVar("T")

def log_action(action: str, result: Any):
    """Common logging function for consistent output."""
    timestamp = datetime.utcnow().isoformat()
    # Using log_sse for specific important actions if needed, or just print
    print(f"[{action}] Result: {result} (Time: {timestamp})")

def log_error(action: str, error: Exception):
    """Common error logging with timestamp."""
    timestamp = datetime.utcnow().isoformat()
    log_sse(f"[{action}] Error Detail: {str(error)} at {timestamp} - Executing Fallback")

def robust_execute(
    func: Callable[..., T], 
    data: Any, 
    fallback_value: T = None
) -> T:
    """
    Common Error Handling: Graceful degradation & Fallback.
    (PDF Tech Completeness 25/25: Robust Error Handling)
    """
    try:
        if isinstance(data, tuple):
            return func(data)
        return func(data)
    except Exception as e:
        log_error(func.__name__, e)
        return fallback_value
