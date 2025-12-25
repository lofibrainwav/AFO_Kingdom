from __future__ import annotations

import os

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse


def _redis_url() -> str:
    """Get Redis URL from environment or default."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = os.getenv("REDIS_PORT", "6379")
    db = os.getenv("REDIS_DB", "0")
    return f"redis://{host}:{port}/{db}"


def _rps() -> int:
    """Get RPS limit from environment."""
    return int(os.getenv("AFO_RATE_LIMIT_RPS", "10"))


def _enabled() -> bool:
    """Check if rate limiting is enabled."""
    return os.getenv("AFO_RATE_LIMIT_ENABLED", "true").lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


def create_redis_limiter() -> Limiter:
    """
    Create Redis-backed rate limiter using slowapi.

    External references (2025):
    - slowapi PyPI: https://pypi.org/project/slowapi/
    - FastAPI integration: https://github.com/laurentS/slowapi
    - Redis Token Bucket: https://redis.io/commands/EVAL
    """
    if not _enabled():
        # Return dummy limiter when disabled
        return Limiter(key_func=get_remote_address, strategy="fixed-window")

    redis_url = _redis_url()
    rps = _rps()

    # Create Redis-backed limiter
    limiter = Limiter(
        key_func=get_remote_address,  # IP-based rate limiting
        default_limits=[f"{rps}/minute"],  # RPS converted to per-minute
        storage_uri=redis_url,
        strategy="fixed-window",  # Redis-backed with fixed window
        auto_check=False,  # Manual checking for better control
    )

    return limiter


def create_rate_limit_middleware(limiter: Limiter):
    """
    Create FastAPI middleware from slowapi limiter.

    For now, return None to disable rate limiting middleware.
    TODO: Implement proper FastAPI middleware integration.
    """
    # Temporarily disable rate limiting to avoid middleware issues
    return None