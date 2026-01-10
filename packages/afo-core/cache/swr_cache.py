# Trinity Score: 90.0 (Established by Chancellor)
# packages/afo-core/cache/swr_cache.py
# (Stale-While-Revalidate 구현 - PDF 성능 최적화 기반)
# 🧭 Trinity Score: 眞85% 善95% 美99% 孝100%

import asyncio
import json
import logging
import time
from collections.abc import Callable
from typing import Any

# Assume AFO redis client wrapper or standard redis
try:
    import redis

    redis_client: redis.Redis | None = redis.Redis(
        host="localhost", port=6379, decode_responses=True
    )
except ImportError:
    redis_client = None
    print("⚠️ Redis not installed, SWR cache falling back to pass-through")

logger = logging.getLogger(__name__)


async def background_revalidate(
    key: str, fetch_func: Callable[[], Any], ttl: int, swr_grace: int
):
    """백그라운드 재검증 (SWR 핵심)
    Executes the fetch function and updates the cache.
    """
    try:
        logger.info(f"[SWR] Background revalidating key: {key}")
        data = (
            fetch_func()
        )  # This might be async in real app, keeping simple for pattern
        if asyncio.iscoroutine(data):
            data = await data

        # Update Cache
        if redis_client:
            payload = {"data": data, "timestamp": time.time()}
            redis_client.set(key, json.dumps(payload), ex=ttl + swr_grace)

        logger.info(f"[SWR] Revalidation complete for {key}")
    except Exception as e:
        logger.error(f"[SWR] Background revalidation failed for {key}: {e}")


def get_with_swr(
    key: str, fetch_func: Callable[[], Any], max_age: int = 60, swr: int = 300
) -> Any:
    """Stale-While-Revalidate: stale 허용 + 백그라운드 갱신 (PDF 캐싱 최적화)

    Args:
        key: Cache Key
        fetch_func: Function to retrieve data if missed or stale
        max_age: Duration in seconds to consider data 'fresh'
        swr: Duration in seconds to allow 'stale' data while revalidating

    Returns:
        The data (fresh, stale, or newly fetched)

    """
    if not redis_client:
        return fetch_func()

    cached_raw = redis_client.get(key)

    if cached_raw:
        try:
            cached_entry = json.loads(cached_raw)
            data = cached_entry.get("data")
            timestamp = cached_entry.get("timestamp", 0)

            age = time.time() - timestamp

            # Case 1: Fresh Hit
            if age < max_age:
                logger.debug(f"[SWR] Fresh Hit: {key} (Age: {age:.1f}s)")
                return data

            # Case 2: Stale Hit (within grace period)
            if age < max_age + swr:
                logger.info(
                    f"[SWR] Stale Hit: {key} (Age: {age:.1f}s) - Triggering Revalidation"
                )
                # Trigger background revalidation (assuming running in async loop context)
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(
                        background_revalidate(key, fetch_func, max_age, swr)
                    )
                except RuntimeError:
                    # Fallback for sync context or no loop (simple thread usage or skip)
                    pass
                return data  # Return stale data immediately

        except json.JSONDecodeError:
            pass  # Invalid cache, treat as miss

    # Case 3: Miss or Expired
    logger.info(f"[SWR] Cache Miss/Expired: {key} - Fetching synchronously")
    data = fetch_func()

    # Update Cache
    payload = {"data": data, "timestamp": time.time()}
    redis_client.set(key, json.dumps(payload), ex=max_age + swr)

    return data
