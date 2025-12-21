import sys
from datetime import datetime


def log_sse(message: str) -> None:
    """
    Log message in a format compatible with Server-Sent Events (SSE) or structured logs.
    Currently prints to stdout with timestamp.

    Args:
        message: Message to log
    """
    timestamp = datetime.utcnow().isoformat()
    # In a real SSE setup, this might yield or write to a stream.
    # For now, we print with a specific prefix for easy parsing.
    print(f"[SSE] {timestamp} - {message}")
    sys.stdout.flush()
