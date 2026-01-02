# Trinity Score: 90.0 (Established by Chancellor)
"""Performance Monitoring Middleware for AFO Kingdom
Tracks response times and identifies slow endpoints.

Sequential Thinking: 단계별 성능 모니터링 미들웨어 구축
眞善美孝永: Truth 100%, Goodness 95%, Beauty 90%, Serenity 100%, Eternity 100%
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# 성능 임계값 설정
PERFORMANCE_THRESHOLDS = {
    "warning_ms": 1000,  # 1초 이상 시 경고
    "critical_ms": 2000,  # 2초 이상 시 위험
    "p95_target_ms": 1000,  # P95 목표: 1초 이하
}


class PerformanceMiddleware(BaseHTTPMiddleware):
    """성능 모니터링 미들웨어
    Sequential Thinking: 단계별 성능 측정 및 알림
    """

    def __init__(self, app: Any):
        super().__init__(app)
        self._request_times: list[float] = []
        self._endpoint_times: dict[str, list[float]] = {}
        self._max_history = 1000  # 최근 1000개 요청만 유지

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        """성능 측정 및 모니터링 (Sequential Thinking Phase 1)"""
        # 시작 시간 기록
        start_time = time.time()

        # 요청 처리
        response = await call_next(request)

        # 응답 시간 계산
        elapsed_ms = (time.time() - start_time) * 1000

        # 성능 데이터 수집 (Sequential Thinking Phase 1.1)
        self._record_performance(request, elapsed_ms)

        # 느린 엔드포인트 감지 (Sequential Thinking Phase 1.2)
        self._check_slow_endpoint(request, elapsed_ms)

        # Prometheus 메트릭 업데이트 (Sequential Thinking Phase 1.3)
        self._update_prometheus_metrics(request, elapsed_ms, response.status_code)

        # 응답 헤더에 성능 정보 추가
        response.headers["X-Response-Time"] = f"{elapsed_ms:.2f}ms"

        return response

    def _record_performance(self, request: Request, elapsed_ms: float) -> None:
        """성능 데이터 기록"""
        # 전체 요청 시간 기록
        self._request_times.append(elapsed_ms)
        if len(self._request_times) > self._max_history:
            self._request_times.pop(0)

        # 엔드포인트별 시간 기록
        endpoint = f"{request.method} {request.url.path}"
        if endpoint not in self._endpoint_times:
            self._endpoint_times[endpoint] = []
        self._endpoint_times[endpoint].append(elapsed_ms)
        if len(self._endpoint_times[endpoint]) > 100:  # 엔드포인트별 최근 100개만
            self._endpoint_times[endpoint].pop(0)

    def _check_slow_endpoint(self, request: Request, elapsed_ms: float) -> None:
        """느린 엔드포인트 감지 및 로깅"""
        if elapsed_ms >= PERFORMANCE_THRESHOLDS["critical_ms"]:
            logger.warning(
                f"🚨 CRITICAL: Slow endpoint detected - {request.method} {request.url.path} "
                f"took {elapsed_ms:.2f}ms (threshold: {PERFORMANCE_THRESHOLDS['critical_ms']}ms)"
            )
        elif elapsed_ms >= PERFORMANCE_THRESHOLDS["warning_ms"]:
            logger.info(
                f"⚠️ WARNING: Slow endpoint - {request.method} {request.url.path} "
                f"took {elapsed_ms:.2f}ms (threshold: {PERFORMANCE_THRESHOLDS['warning_ms']}ms)"
            )

    def _update_prometheus_metrics(
        self, request: Request, elapsed_ms: float, status_code: int
    ) -> None:
        """Prometheus 메트릭 업데이트"""
        try:
            from prometheus_client import Histogram

            # 메트릭이 없으면 생성 (첫 호출 시)
            if not hasattr(self, "_response_time_histogram"):
                self._response_time_histogram = Histogram(
                    "afo_api_response_time_seconds",
                    "API response time in seconds",
                    ["method", "endpoint", "status_code"],
                    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
                )

            # 메트릭 기록
            endpoint = request.url.path
            self._response_time_histogram.labels(
                method=request.method, endpoint=endpoint, status_code=status_code
            ).observe(elapsed_ms / 1000.0)  # 초 단위로 변환

        except (ImportError, Exception) as e:
            # Prometheus가 없으면 무시
            logger.debug(f"Prometheus 메트릭 업데이트 실패 (무시): {e}")

    def get_performance_stats(self) -> dict[str, Any]:
        """성능 통계 조회"""
        if not self._request_times:
            return {
                "total_requests": 0,
                "average_ms": 0.0,
                "p50_ms": 0.0,
                "p95_ms": 0.0,
                "p99_ms": 0.0,
                "slow_endpoints": [],
            }

        sorted_times = sorted(self._request_times)
        total = len(sorted_times)

        # 백분위수 계산
        p50_idx = int(total * 0.5)
        p95_idx = int(total * 0.95)
        p99_idx = int(total * 0.99)

        # 느린 엔드포인트 식별
        slow_endpoints = []
        for endpoint, times in self._endpoint_times.items():
            if times:
                avg_time = sum(times) / len(times)
                if avg_time >= PERFORMANCE_THRESHOLDS["p95_target_ms"]:
                    slow_endpoints.append(
                        {
                            "endpoint": endpoint,
                            "average_ms": round(avg_time, 2),
                            "count": len(times),
                        }
                    )

        return {
            "total_requests": total,
            "average_ms": round(sum(sorted_times) / total, 2),
            "p50_ms": round(sorted_times[p50_idx] if p50_idx < total else 0, 2),
            "p95_ms": round(sorted_times[p95_idx] if p95_idx < total else 0, 2),
            "p99_ms": round(sorted_times[p99_idx] if p99_idx < total else 0, 2),
            "slow_endpoints": sorted(slow_endpoints, key=lambda x: x["average_ms"], reverse=True),
        }
