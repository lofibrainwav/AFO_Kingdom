# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Unified Cache System

Phase 6B: Intelligent Cache Revolution
Implements multi-level caching with predictive capabilities.
"""

from typing import Any

from .backends import MemoryBackend, RedisBackend
from .manager import MultiLevelCache, cache_manager
from .predictive import PredictiveCacheManager, predictive_manager
from .query_cache import (
    CacheInvalidator,
    QueryCache,
    cache_query,
    cache_system_data,
    cache_user_data,
    invalidate_cache,
)


def get_cache_metrics() -> dict[str, Any]:
    """Phase 6B: Get unified cache performance metrics"""
    return cache_manager.get_metrics()


__all__ = [
    "CacheInvalidator",
    "MemoryBackend",
    "MultiLevelCache",
    "PredictiveCacheManager",
    "QueryCache",
    "RedisBackend",
    "cache_manager",
    "cache_query",
    "cache_system_data",
    "cache_user_data",
    "get_cache_metrics",
    "invalidate_cache",
    "predictive_manager",
]
