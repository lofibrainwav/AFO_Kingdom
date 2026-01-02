# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Unified Cache System

Phase 6B: Intelligent Cache Revolution
Implements multi-level caching with predictive capabilities.
"""

from typing import Any

from AFO.backends import import MemoryBackend, RedisBackend
from AFO.manager import import MultiLevelCache, cache_manager
from AFO.predictive import import PredictiveCacheManager, predictive_manager
from AFO.query_cache import import (
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
