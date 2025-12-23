"""
Cache Backends (Protocol & Implementation)

Defines the interface for cache backends and concrete implementations.
- Protocol: CacheBackend
- L1: MemoryBackend (LRU)
- L2: RedisBackend (Redis)
"""

import json
import logging
from typing import Any, Protocol, TypeVar

from config.settings import settings

T = TypeVar("T")

logger = logging.getLogger(__name__)


class CacheBackend(Protocol):
    """
    Protocol for Cache Backends.
    Ensures consistent interface for Memory, Redis, etc.
    """

    async def get(self, key: str) -> Any | None:
        """Retrieve value by key"""
        ...

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value with optional TTL (seconds)"""
        ...

    async def delete(self, key: str) -> None:
        """Delete value by key"""
        ...

    async def clear(self) -> None:
        """Clear all keys in this namespace"""
        ...


class MemoryBackend:
    """
    L1 Cache: In-Memory (LRU via pylru or simple dict for now)
    Extremely fast (microseconds), ephemeral.
    """

    def __init__(self, max_size: int = 1000):
        self._cache: dict[str, Any] = {}
        # Simple implementation for now. Production: use cachetools or pylru
        self._max_size = max_size

    async def get(self, key: str) -> Any | None:
        return self._cache.get(key)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        # Check size constraint
        if len(self._cache) >= self._max_size:
            # Simple eviction: remove arbitrary item (first one)
            # Ideal: LRU
            self._cache.pop(next(iter(self._cache)))

        self._cache[key] = value

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    async def clear(self) -> None:
        self._cache.clear()


class RedisBackend:
    """
    L2 Cache: Redis
    Fast (milliseconds), persistent, shared across instances.
    """

    def __init__(self, redis_url: str | None = None):
        self.redis = None
        self._url = redis_url or settings.get_redis_url()
        self._connected = False

    async def _ensure_connection(self) -> None:
        if not self._connected:
            try:
                import redis.asyncio as redis

                self.redis = redis.from_url(
                    self._url, encoding="utf-8", decode_responses=True
                )
                await self.redis.ping()
                self._connected = True
                logger.info(f"✅ L2 Cache Connected: {self._url}")
            except Exception as e:
                logger.error(f"❌ L2 Cache Connection Failed: {e}")
                self.redis = None  # Fallback mode

    async def get(self, key: str) -> Any | None:
        await self._ensure_connection()
        if not self.redis:
            return None

        try:
            val = await self.redis.get(key)
            if val:
                try:
                    return json.loads(val)
                except json.JSONDecodeError:
                    return val  # Return raw string if not JSON
            return None
        except Exception as e:
            logger.warning(f"L2 Get Error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        await self._ensure_connection()
        if not self.redis:
            return

        try:
            # Serialize
            val_str = (
                json.dumps(value) if isinstance(value, (dict, list)) else str(value)
            )

            if ttl:
                await self.redis.setex(key, ttl, val_str)
            else:
                await self.redis.set(key, val_str)
        except Exception as e:
            logger.warning(f"L2 Set Error: {e}")

    async def delete(self, key: str) -> None:
        await self._ensure_connection()
        if self.redis:
            try:
                await self.redis.delete(key)
            except Exception as e:
                logger.warning(f"L2 Delete Error: {e}")

    async def clear(self) -> None:
        # Warning: This flushes the DB. Use with caution or specific namespace.
        # For safety, maybe just log or implement namespace clearing.
        logger.warning("L2 Clear called but disabled for safety")
