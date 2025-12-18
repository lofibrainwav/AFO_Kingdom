# Redis 캐시 유틸리티
from __future__ import annotations

import json
import os
from functools import wraps
from typing import Any

import redis


class CacheManager:
    """Redis 기반 캐시 관리자"""

    def __init__(self):
        # Phase 2-4: settings 사용
        try:
            from AFO.utils.redis_connection import get_redis_url

            self.redis_url = get_redis_url()
        except ImportError:
            try:
                from config.settings import get_settings

                settings = get_settings()
                self.redis_url = settings.get_redis_url()
            except ImportError:
                try:
                    from AFO.config.settings import get_settings

                    settings = get_settings()
                    self.redis_url = settings.get_redis_url()
                except ImportError:
                    # Fallback
                    self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

        try:
            self.redis = redis.from_url(self.redis_url)
            self.redis.ping()  # 연결 테스트
            self.enabled = True
        except Exception:
            self.redis = None
            self.enabled = False

    def get(self, key: str) -> Any | None:
        """캐시에서 데이터 가져오기"""
        if not self.enabled:
            return None
        try:
            data = self.redis.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None

    def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """캐시에 데이터 저장"""
        if not self.enabled:
            return False
        try:
            self.redis.setex(key, expire, json.dumps(value))
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """캐시에서 데이터 삭제"""
        if not self.enabled:
            return False
        try:
            return bool(self.redis.delete(key))
        except Exception:
            return False


# 글로벌 캐시 인스턴스
cache = CacheManager()


def cached(expire: int = 300):
    """API 엔드포인트 캐싱 데코레이터"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 캐시 키 생성
            key = f"{func.__name__}:{str(args) + str(kwargs)}"

            # 캐시에서 먼저 확인
            cached_data = cache.get(key)
            if cached_data is not None:
                return cached_data

            # 실제 함수 실행
            result = await func(*args, **kwargs)

            # 결과 캐싱
            cache.set(key, result, expire)

            return result

        return wrapper

    return decorator
