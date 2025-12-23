"""
AFO Kingdom API Middleware Configuration

Handles CORS, security, monitoring, and other middleware setup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware for the FastAPI application."""

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 모든 도메인 허용 (프로덕션에서는 특정 도메인으로 제한)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Cache middleware (Phase 1.2: API 엔드포인트 캐싱)
    _setup_cache_middleware(app)

    # Performance monitoring middleware (Phase 3.1: 성능 모니터링)
    _setup_performance_middleware(app)

    # Security middleware (audit logging)
    _setup_security_middleware(app)

    # Monitoring middleware (Prometheus)
    _setup_monitoring_middleware(app)


def _setup_security_middleware(app: FastAPI) -> None:
    """Setup security-related middleware."""
    try:
        from AFO.api.middleware.audit import audit_middleware
        from AFO.security.vault_manager import vault

        # Audit Middleware (Before Routes)
        app.middleware("http")(audit_middleware)

        # Initialize Vault (Log only)
        print(f"🛡️ Vault Manager Active (Mode: {vault.mode})")
        print("🛡️ Audit Middleware Active (Logging POST/PUT/DELETE)")

    except Exception as e:
        print(f"⚠️ Security Hardening 설정 실패: {e}")


def _setup_cache_middleware(app: FastAPI) -> None:
    """Setup cache middleware for API responses."""
    try:
        from AFO.api.middleware.cache_middleware import CacheMiddleware

        # Add cache middleware (before other middleware for optimal performance)
        app.add_middleware(CacheMiddleware)
        print("✅ API Cache Middleware 활성화")

    except Exception as e:
        print(f"⚠️ Cache Middleware 설정 실패: {e}")
        import traceback

        traceback.print_exc()


def _setup_performance_middleware(app: FastAPI) -> None:
    """Setup performance monitoring middleware."""
    try:
        from AFO.api.middleware.performance_middleware import \
            PerformanceMiddleware

        # Add performance middleware
        app.add_middleware(PerformanceMiddleware)
        print("✅ Performance Monitoring Middleware 활성화")

    except Exception as e:
        print(f"⚠️ Performance Middleware 설정 실패: {e}")
        import traceback

        traceback.print_exc()


def _setup_monitoring_middleware(app: FastAPI) -> None:
    """Setup monitoring and metrics middleware."""
    try:
        from AFO.api.middleware.prometheus import PrometheusMiddleware

        # Add Prometheus middleware
        app.add_middleware(PrometheusMiddleware, service_name="afo-kingdom-api")
        print("✅ Prometheus Metrics Middleware 활성화")

        # Add metrics endpoint
        from AFO.api.middleware.prometheus import metrics_endpoint
        from fastapi.routing import APIRouter

        metrics_router = APIRouter()
        metrics_router.get("/metrics")(metrics_endpoint)
        app.include_router(metrics_router)

        print("✅ Prometheus Metrics Endpoint 추가 (/metrics)")

    except Exception as e:
        print(f"⚠️ Prometheus Middleware 설정 실패: {e}")
        import traceback

        traceback.print_exc()
