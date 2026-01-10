# Trinity Score: 90.0 (Established by Chancellor)
# Redis 캐시 유틸리티
from __future__ import annotations

import json
import logging
import os
from functools import wraps
from typing import TYPE_CHECKING, Any

import redis

if TYPE_CHECKING:
    from collections.abc import Callable

# 로깅 설정
logger = logging.getLogger(__name__)


class CacheManager:
    """Redis 기반 캐시 관리자"""

    def __init__(self) -> None:
        self.redis: redis.Redis | None = None
        self.enabled: bool = False
        # Phase 2 리팩터링: redis_connection 모듈 직접 사용 (간소화)
        try:
            from AFO.utils.redis_connection import get_redis_client

            self.redis = get_redis_client()
            self.enabled = True
        except ImportError:
            # 첫 번째 fallback: get_redis_url 사용
            try:
                from AFO.utils.redis_connection import get_redis_url

                redis_url = get_redis_url()
                self.redis = redis.from_url(redis_url)
                if self.redis is not None:
                    self.redis.ping()  # 연결 테스트
                self.enabled = True
            except (redis.ConnectionError, redis.TimeoutError, OSError) as e:
                logger.debug("Redis URL 연결 실패, 직접 연결 시도: %s", str(e))
                # 두 번째 fallback: 직접 연결 (독립 실행 시)
                try:
                    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
                    self.redis = redis.from_url(redis_url)
                    if self.redis is not None:
                        self.redis.ping()
                    self.enabled = True
                except (redis.ConnectionError, redis.TimeoutError, OSError) as e2:
                    logger.warning("Redis 직접 연결 실패: %s", str(e2))
                    self.redis = None
                    self.enabled = False
                except Exception as e2:  # - Intentional fallback
                    logger.warning("Redis 직접 연결 중 예상치 못한 에러: %s", str(e2))
                    self.redis = None
                    self.enabled = False
        except (ImportError, AttributeError) as e:
            logger.warning("Redis 연결 모듈 import 실패: %s", str(e))
            self.redis = None
            self.enabled = False
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("Redis 초기화 중 예상치 못한 에러: %s", str(e))
            self.redis = None
            self.enabled = False

    def get(self, key: str) -> Any | None:
        """캐시에서 데이터 가져오기"""
        if not self.enabled or self.redis is None:
            return None
        try:
            data = self.redis.get(key)
            if data and isinstance(data, (str, bytes, bytearray)):
                return json.loads(data)
            return None
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning("캐시 데이터 JSON 파싱 실패 (키: %s): %s", key, str(e))
            return None
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning("Redis 연결 에러 (키: %s): %s", key, str(e))
            return None
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.warning("캐시 조회 중 예상치 못한 에러 (키: %s): %s", key, str(e))
            return None

    def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """캐시에 데이터 저장"""
        if not self.enabled or self.redis is None:
            return False
        try:
            json_str = json.dumps(value)
            self.redis.setex(key, expire, json_str)
            return True
        except (TypeError, ValueError) as e:
            logger.warning("캐시 데이터 JSON 직렬화 실패 (키: %s): %s", key, str(e))
            return False
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning("Redis 연결 에러 (키: %s): %s", key, str(e))
            return False
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.warning("캐시 저장 중 예상치 못한 에러 (키: %s): %s", key, str(e))
            return False

    def delete(self, key: str) -> bool:
        """캐시에서 데이터 삭제"""
        if not self.enabled or self.redis is None:
            return False
        try:
            return bool(self.redis.delete(key))
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning("Redis 연결 에러 (키: %s): %s", key, str(e))
            return False
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("캐시 삭제 중 예상치 못한 에러 (키: %s): %s", key, str(e))
            return False


# 글로벌 캐시 인스턴스
cache = CacheManager()


def cached(expire: int = 300) -> Callable[[Callable], Callable]:
    """API 엔드포인트 캐싱 데코레이터"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
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
