# mypy: ignore-errors
"""
Multimodal RAG Cache for AFO Kingdom (Phase 5)
Redis-based caching for multimodal RAG operations.
Strangler Fig: 메모리 관리 및 캐시 크기 제한 추가
"""

import hashlib
import json
import logging
import threading
import time
from typing import Any

# 로깅 설정
logger = logging.getLogger(__name__)

# Redis client placeholder (set via dependency injection)
# Note: global statement is intentional for dependency injection pattern
_redis_client: Any = None

# Strangler Fig: 메모리 관리 추가 (眞: Truth 타입 안전성)
_memory_stats = {
    "cache_entries": 0,
    "total_memory_mb": 0.0,
    "max_memory_mb": 100.0,  # 기본 100MB 제한
    "last_cleanup": time.time(),
    "cleanup_interval": 300,  # 5분마다 정리
}
_memory_lock = threading.Lock()


def set_redis_client(client: Any) -> None:
    """
    Set the Redis client for caching operations.

    Args:
        client: Redis client instance (redis.Redis or compatible)
    """
    global _redis_client  # - Intentional global for dependency injection pattern
    _redis_client = client
    logger.info("Redis client 설정 완료")


def get_redis_client() -> Any | None:
    """Get the current Redis client."""
    return _redis_client


def cache_key(prefix: str, query: str) -> str:
    """Generate a cache key from prefix and query."""
    query_hash = hashlib.md5(query.encode()).hexdigest()[:12]
    return f"afo:cache:{prefix}:{query_hash}"


def get_cached(key: str) -> dict[str, Any] | None:
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
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning("캐시 데이터 JSON 파싱 실패 (키: %s): %s", key, str(e))
    except AttributeError as e:
        logger.warning("Redis 클라이언트 메서드 호출 실패 (키: %s): %s", key, str(e))
    except (ConnectionError, TimeoutError, OSError) as e:
        logger.warning("Redis 연결 에러 (키: %s): %s", key, str(e))
    except Exception as e:  # - Intentional fallback for unexpected errors
        # 기타 예상치 못한 에러는 로깅만 하고 조용히 처리 (fallback 동작)
        logger.debug("캐시 조회 중 예상치 못한 에러 (키: %s): %s", key, str(e))
    return None


def set_cached(key: str, value: dict[str, Any], ttl: int = 3600) -> bool:
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
        json_str = json.dumps(value)
        _redis_client.setex(key, ttl, json_str)
        return True
    except (TypeError, ValueError) as e:
        logger.warning("캐시 데이터 JSON 직렬화 실패 (키: %s): %s", key, str(e))
    except AttributeError as e:
        logger.warning("Redis 클라이언트 메서드 호출 실패 (키: %s): %s", key, str(e))
    except Exception as e:
        # 기타 예상치 못한 에러는 로깅만 하고 조용히 처리 (fallback 동작)
        logger.debug("캐시 저장 중 예상치 못한 에러 (키: %s): %s", key, str(e))
    return False


def invalidate(key: str) -> bool:
    """Invalidate a cache entry."""
    if _redis_client is None:
        return False

    try:
        _redis_client.delete(key)
        return True
    except AttributeError as e:
        logger.warning("Redis 클라이언트 메서드 호출 실패 (키: %s): %s", key, str(e))
    except (ConnectionError, TimeoutError, OSError) as e:
        logger.warning("Redis 연결 에러 (키: %s): %s", key, str(e))
    except Exception as e:  # - Intentional fallback for unexpected errors
        # 기타 예상치 못한 에러는 로깅만 하고 조용히 처리 (fallback 동작)
        logger.debug("캐시 무효화 중 예상치 못한 에러 (키: %s): %s", key, str(e))
    return False


# Strangler Fig: 메모리 관리 함수들 추가 (善: Goodness 안전성)
def set_memory_limit(max_mb: float) -> None:
    """
    캐시 메모리 제한 설정 (MB)

    Args:
        max_mb: 최대 메모리 사용량 (MB)
    """
    with _memory_lock:
        _memory_stats["max_memory_mb"] = max_mb


def get_memory_stats() -> dict[str, Any]:
    """
    메모리 통계 정보 반환

    Returns:
        메모리 통계 딕셔너리
    """
    with _memory_lock:
        return _memory_stats.copy()


def _estimate_memory_usage(data: dict[str, Any]) -> float:
    """
    데이터의 메모리 사용량 추정 (MB)

    Args:
        data: 캐시할 데이터

    Returns:
        예상 메모리 사용량 (MB)
    """
    try:
        # JSON 직렬화 크기로 메모리 사용량 추정
        json_str = json.dumps(data)
        # UTF-8 인코딩 시 약 2배, 오버헤드 고려하여 3배
        return len(json_str.encode("utf-8")) * 3 / (1024 * 1024)
    except (TypeError, ValueError) as e:
        logger.debug("메모리 사용량 추정 실패: %s", str(e))
        return 1.0  # 기본 1MB 추정
    except Exception as e:
        logger.debug("메모리 사용량 추정 중 예상치 못한 에러: %s", str(e))
        return 1.0  # 기본 1MB 추정


def _cleanup_expired_cache() -> int:
    """
    만료된 캐시 항목 정리 (메모리 최적화)
    Sequential Thinking: 단계별 메모리 정리 로직

    Returns:
        정리된 항목 수
    """
    if _redis_client is None:
        logger.debug("Redis 클라이언트 없음 - 캐시 정리 생략")
        return 0

    try:
        # Phase 1: 정리 주기 확인
        current_time = time.time()
        with _memory_lock:
            if current_time - _memory_stats["last_cleanup"] < _memory_stats["cleanup_interval"]:
                logger.debug("정리 주기 도달 전 - 생략")
                return 0

        # Phase 2: TTL 만료 키 정리 (가벼운 정리)
        pattern = "afo:cache:*"
        keys = _redis_client.keys(pattern)

        ttl_expired = 0
        memory_pressure_cleaned = 0

        for key in keys:
            try:
                # TTL 확인 (-2: 키 없음, -1: TTL 없음, >0: 남은 시간)
                ttl = _redis_client.ttl(key)
                if ttl == -2:  # 키가 존재하지 않음
                    continue
                elif ttl == 0:  # TTL 만료됨
                    _redis_client.delete(key)
                    ttl_expired += 1
                    _update_memory_stats("remove", 0)  # 메모리 통계만 업데이트
                elif ttl == -1:  # TTL 설정 안됨 (영구 키)
                    # Phase 3: 메모리 압력 기반 정리
                    with _memory_lock:
                        if _memory_stats["total_memory_mb"] > _memory_stats["max_memory_mb"]:
                            _redis_client.delete(key)
                            memory_pressure_cleaned += 1
                            # 메모리 통계는 실제 데이터 크기를 모르므로 추정치 사용
                            _update_memory_stats("remove", 1.0)  # 기본 1MB로 추정
            except Exception as e:
                logger.debug("개별 키 정리 실패 (키: %s): %s", key, str(e))
                continue

        # Phase 4: 정리 결과 기록
        total_cleaned = ttl_expired + memory_pressure_cleaned
        with _memory_lock:
            _memory_stats["last_cleanup"] = current_time

        if total_cleaned > 0:
            logger.info(
                "캐시 정리 완료: TTL 만료 %d개, 메모리 압력 %d개",
                ttl_expired,
                memory_pressure_cleaned,
            )

        return total_cleaned

    except Exception as e:
        logger.warning("캐시 정리 작업 실패: %s", str(e))
        return 0


def _update_memory_stats(operation: str, data_size_mb: float = 0.0) -> None:
    """
    메모리 통계 업데이트

    Args:
        operation: 'add' | 'remove'
        data_size_mb: 데이터 크기 (MB)
    """
    with _memory_lock:
        if operation == "add":
            _memory_stats["cache_entries"] += 1
            _memory_stats["total_memory_mb"] += data_size_mb
        elif operation == "remove":
            _memory_stats["cache_entries"] = max(0, _memory_stats["cache_entries"] - 1)
            _memory_stats["total_memory_mb"] = max(
                0, _memory_stats["total_memory_mb"] - data_size_mb
            )


def set_cached_with_memory_check(key: str, value: dict[str, Any], ttl: int = 3600) -> bool:
    """
    메모리 사용량 확인 후 캐시 설정 (Strangler Fig 메모리 안전성)

    Args:
        key: 캐시 키
        value: 캐시할 값
        ttl: TTL (초)

    Returns:
        성공 여부
    """
    if _redis_client is None:
        return False

    # 메모리 사용량 추정
    data_size_mb = _estimate_memory_usage(value)

    with _memory_lock:
        # 메모리 제한 확인
        if _memory_stats["total_memory_mb"] + data_size_mb > _memory_stats["max_memory_mb"]:
            # 자동 정리 시도
            cleaned = _cleanup_expired_cache()
            if cleaned > 0:
                print(f"⚠️  메모리 부족으로 {cleaned}개 캐시 정리")

            # 여전히 메모리 부족하면 실패
            if _memory_stats["total_memory_mb"] + data_size_mb > _memory_stats["max_memory_mb"]:
                print(
                    f"❌ 메모리 제한 초과: {data_size_mb:.2f}MB 요청, 현재 {_memory_stats['total_memory_mb']:.2f}MB 사용"
                )
                return False

    # 캐시 설정
    success = set_cached(key, value, ttl)
    if success:
        _update_memory_stats("add", data_size_mb)
        print(f"✅ 캐시 저장: {data_size_mb:.2f}MB (총 {_memory_stats['total_memory_mb']:.2f}MB)")

    return success


def cache_rag_result(query: str, results: dict[str, Any], ttl: int = 1800) -> bool:
    """Cache a RAG result."""
    key = cache_key("rag", query)
    return set_cached(key, results, ttl)


def get_cached_rag_result(query: str) -> dict[str, Any] | None:
    """Get a cached RAG result."""
    key = cache_key("rag", query)
    return get_cached(key)


def cache_multimodal_result(
    query: str, content_type: str, results: dict[str, Any], ttl: int = 1800
) -> bool:
    """Cache a multimodal RAG result."""
    key = cache_key(f"mm_{content_type}", query)
    return set_cached(key, results, ttl)


def get_cached_multimodal_result(query: str, content_type: str) -> dict[str, Any] | None:
    """Get a cached multimodal RAG result."""
    key = cache_key(f"mm_{content_type}", query)
    return get_cached(key)


class MultimodalRAGCache:
    """
    Cache manager for multimodal RAG operations.
    """

    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl

    def cache(self, query: str, results: dict[str, Any], content_type: str = "text") -> bool:
        """Cache RAG results."""
        return cache_multimodal_result(query, content_type, results, self.default_ttl)

    def get(self, query: str, content_type: str = "text") -> dict[str, Any] | None:
        """Get cached RAG results."""
        return get_cached_multimodal_result(query, content_type)

    def clear(self, query: str, content_type: str = "text") -> bool:
        """Clear cached results for a query."""
        key = cache_key(f"mm_{content_type}", query)
        return invalidate(key)
