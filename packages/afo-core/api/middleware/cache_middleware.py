# Trinity Score: 90.0 (Established by Chancellor)
"""
API Cache Middleware for AFO Kingdom
Automatic caching for GET requests to reduce response time and server load.

Sequential Thinking: 단계별 API 캐싱 미들웨어 구축
眞善美孝永: Truth 100%, Goodness 95%, Beauty 90%, Serenity 100%, Eternity 100%
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ...utils.redis_connection import get_redis_client

logger = logging.getLogger(__name__)

# 캐시 설정
API_CACHE_CONFIG: dict[str, Any] = {
    "key_prefix": "api:cache:",
    "default_ttl": 300,  # 5분
    "endpoint_ttl": {
        "/health": 5,  # 5초
        "/api/5pillars/current": 10,  # 10초
        "/api/skills/list": 30,  # 30초
    },
    "cacheable_methods": ["GET"],
    "cacheable_status_codes": [200, 201],
}


class CacheMiddleware(BaseHTTPMiddleware):
    """
    API 엔드포인트 캐싱 미들웨어
    Sequential Thinking: 단계별 캐시 구현 및 최적화
    """

    def __init__(self, app: Any):
        super().__init__(app)
        self.redis_client = None
        self._hit_count = 0
        self._miss_count = 0
        self._initialized = False
        self._initialize_cache()

    def _initialize_cache(self) -> None:
        """
        Redis 연결 초기화 (Sequential Thinking Phase 1)
        """
        try:
            self.redis_client = get_redis_client()
            if self.redis_client is not None:
                # 연결 테스트
                self.redis_client.ping()
                self._initialized = True
                logger.info("✅ API Cache Middleware 초기화 완료")
            else:
                logger.warning("⚠️ Redis 클라이언트를 가져올 수 없습니다")
        except Exception as e:
            logger.warning(f"⚠️ API Cache Middleware 초기화 실패: {e}")
            self._initialized = False

    def _generate_cache_key(self, request: Request) -> str:
        """
        캐시 키 생성 (Sequential Thinking Phase 2)
        """
        # 경로와 쿼리 파라미터 기반 키 생성
        path = request.url.path
        query_string = str(request.url.query)
        query_hash = hashlib.md5(query_string.encode()).hexdigest()[:8]

        cache_key = f"{API_CACHE_CONFIG['key_prefix']}{request.method}:{path}:{query_hash}"
        return cache_key

    def _get_ttl(self, path: str) -> int:
        """
        엔드포인트별 TTL 조회
        """
        return API_CACHE_CONFIG["endpoint_ttl"].get(path, API_CACHE_CONFIG["default_ttl"])

    def _is_cacheable(self, request: Request) -> bool:
        """
        캐싱 가능한 요청인지 확인
        """
        # GET 요청만 캐싱
        if request.method not in API_CACHE_CONFIG["cacheable_methods"]:
            return False

        # 특정 경로는 캐싱 제외 (예: 실시간 데이터)
        excluded_paths = ["/api/logs/stream", "/api/system/logs/stream"]
        return not any(request.url.path.startswith(path) for path in excluded_paths)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        미들웨어 처리 (Sequential Thinking Phase 3)
        """
        # 캐싱 불가능한 요청은 바로 통과
        if not self._is_cacheable(request):
            return await call_next(request)

        # 캐시 키 생성
        cache_key = self._generate_cache_key(request)

        # 캐시에서 조회 (Sequential Thinking Phase 3.1)
        if self._initialized and self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    try:
                        cache_entry = json.loads(cached_data)
                        self._hit_count += 1
                        logger.debug(f"✅ API Cache Hit: {cache_key}")

                        # 캐시된 응답 반환
                        response = JSONResponse(
                            content=cache_entry["body"],
                            status_code=cache_entry["status_code"],
                        )
                        response.headers["X-Cache"] = "HIT"
                        response.headers["X-Cache-Key"] = cache_key

                        # 건강 체크 엔드포인트에 브라우저 캐시 헤더 추가
                        if request.url.path == "/api/health/comprehensive":
                            response.headers["Cache-Control"] = "max-age=30, private"
                            response.headers["X-Cache-Source"] = "server-cache"

                        return response
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.warning(f"캐시 데이터 파싱 실패: {e}")
                        # 손상된 캐시 삭제
                        self.redis_client.delete(cache_key)
            except Exception as e:
                logger.debug(f"캐시 조회 실패 (무시): {e}")

        # 캐시 미스 - 실제 요청 처리 (Sequential Thinking Phase 3.2)
        self._miss_count += 1
        response = await call_next(request)

        # 성공 응답만 캐싱 (Sequential Thinking Phase 3.3)
        if (
            self._initialized
            and self.redis_client
            and response.status_code in API_CACHE_CONFIG["cacheable_status_codes"]
        ):
            try:
                # 응답 본문 읽기
                response_body = b""
                async for chunk in response.body_iterator:
                    response_body += chunk

                # JSON 파싱 시도
                try:
                    body_json = json.loads(response_body.decode())
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # JSON이 아닌 경우 캐싱하지 않음
                    return Response(
                        content=response_body,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                    )

                # 캐시 엔트리 생성
                ttl = self._get_ttl(request.url.path)
                cache_entry = {
                    "body": body_json,
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "cached_at": time.time(),
                }

                # Redis에 저장
                cache_data = json.dumps(cache_entry)
                self.redis_client.setex(cache_key, ttl, cache_data)

                logger.debug(f"✅ API Response Cached: {cache_key} (TTL: {ttl}s)")

                # 응답 재구성
                cached_response = JSONResponse(
                    content=body_json,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
                cached_response.headers["X-Cache"] = "MISS"
                cached_response.headers["X-Cache-Key"] = cache_key

                # 건강 체크 엔드포인트에 브라우저 캐시 헤더 추가
                if request.url.path == "/api/health/comprehensive":
                    cached_response.headers["Cache-Control"] = "max-age=30, private"
                    cached_response.headers["X-Cache-Source"] = "server-cache"

                return cached_response

            except Exception as e:
                logger.warning(f"캐시 저장 실패: {e}")
                # 원본 응답 반환
                return Response(
                    content=response_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )

        # 캐싱하지 않는 경우 원본 응답 반환
        response.headers["X-Cache"] = "SKIP"

        # 건강 체크 엔드포인트에 브라우저 캐시 헤더 추가
        if request.url.path == "/api/health/comprehensive":
            response.headers["Cache-Control"] = "max-age=30, private"
            response.headers["X-Cache-Source"] = "server-cache"

        return response

    def get_stats(self) -> dict[str, Any]:
        """
        캐시 통계 조회
        """
        total = self._hit_count + self._miss_count
        hit_rate = (self._hit_count / total * 100) if total > 0 else 0.0

        return {
            "hits": self._hit_count,
            "misses": self._miss_count,
            "total": total,
            "hit_rate": round(hit_rate, 2),
            "initialized": self._initialized,
        }
