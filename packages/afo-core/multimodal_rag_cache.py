"""
Multimodal RAG Cache for AFO Kingdom (Phase 5)
Redis-based caching for multimodal RAG operations.
"""
from typing import Any, Optional, Dict
import json
import hashlib

# Redis client placeholder (set via dependency injection)
_redis_client: Any = None

def set_redis_client(client: Any) -> None:
    """
    Set the Redis client for caching operations.
    
    Args:
        client: Redis client instance (redis.Redis or compatible)
    """
    global _redis_client
    _redis_client = client

def get_redis_client() -> Optional[Any]:
    """Get the current Redis client."""
    return _redis_client

def cache_key(prefix: str, query: str) -> str:
    """Generate a cache key from prefix and query."""
    query_hash = hashlib.md5(query.encode()).hexdigest()[:12]
    return f"afo:cache:{prefix}:{query_hash}"

def get_cached(key: str) -> Optional[Dict[str, Any]]:
    """
    Get a value from cache.
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None
    """
    if _redis_client is None:
        return None
    
    try:
        data = _redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception:
        pass
    return None

def set_cached(key: str, value: Dict[str, Any], ttl: int = 3600) -> bool:
    """
    Set a value in cache.
    
    Args:
        key: Cache key
        value: Value to cache (must be JSON serializable)
        ttl: Time to live in seconds (default 1 hour)
        
    Returns:
        True if successful
    """
    if _redis_client is None:
        return False
    
    try:
        _redis_client.setex(key, ttl, json.dumps(value))
        return True
    except Exception:
        return False

def invalidate(key: str) -> bool:
    """Invalidate a cache entry."""
    if _redis_client is None:
        return False
    
    try:
        _redis_client.delete(key)
        return True
    except Exception:
        return False

def cache_rag_result(query: str, results: Dict[str, Any], ttl: int = 1800) -> bool:
    """Cache a RAG result."""
    key = cache_key("rag", query)
    return set_cached(key, results, ttl)

def get_cached_rag_result(query: str) -> Optional[Dict[str, Any]]:
    """Get a cached RAG result."""
    key = cache_key("rag", query)
    return get_cached(key)

def cache_multimodal_result(query: str, content_type: str, 
                            results: Dict[str, Any], ttl: int = 1800) -> bool:
    """Cache a multimodal RAG result."""
    key = cache_key(f"mm_{content_type}", query)
    return set_cached(key, results, ttl)

def get_cached_multimodal_result(query: str, content_type: str) -> Optional[Dict[str, Any]]:
    """Get a cached multimodal RAG result."""
    key = cache_key(f"mm_{content_type}", query)
    return get_cached(key)

class MultimodalRAGCache:
    """
    Cache manager for multimodal RAG operations.
    """
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
    
    def cache(self, query: str, results: Dict[str, Any], 
              content_type: str = "text") -> bool:
        """Cache RAG results."""
        return cache_multimodal_result(query, content_type, results, self.default_ttl)
    
    def get(self, query: str, content_type: str = "text") -> Optional[Dict[str, Any]]:
        """Get cached RAG results."""
        return get_cached_multimodal_result(query, content_type)
    
    def clear(self, query: str, content_type: str = "text") -> bool:
        """Clear cached results for a query."""
        key = cache_key(f"mm_{content_type}", query)
        return invalidate(key)
