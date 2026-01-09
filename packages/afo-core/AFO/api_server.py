# Trinity Score: 90.0 (Established by Chancellor)
"""AFO Kingdom API Server (아름다운 코드 적용)
FastAPI 기반 AFO 왕국 Soul Engine API 서버

이 파일은 AFO 왕국의 眞善美孝 철학을 구현합니다.
Trinity Score 기반 품질 관리 및 아름다운 코드 원칙 준수.
Debugging Super Agent (2026 Vision) Integrated (眞·永)

Author: AFO Kingdom Development Team
Date: 2025-12-24
Version: 1.0.0
"""

from __future__ import annotations

import asyncio
import importlib.util
import logging
import os  # Added for env check
import sys
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from fastapi import Header, HTTPException  # Added for security
from starlette.requests import Request
from starlette.responses import Response
from sse_starlette.sse import EventSourceResponse

# 2026 Debugging Super Agent
from services.debugging_agent import HealingAgent

ExceptionHandler = Callable[[Request, Exception], Response | Awaitable[Response]]


def _patch_typing_inspection_if_needed() -> None:
    """Self-heal for a known `typing-inspection` startup crash.

    In some environments, `typing_inspection.typing_objects` raises:
    `AttributeError: type object 'tuple' has no attribute '_name'` during import.
    That prevents FastAPI/Pydantic from importing and blocks the API server.

    This patch is safe and idempotent; it only rewrites the installed file when the
    buggy snippet is detected.
    """
    spec = importlib.util.find_spec("typing_inspection.typing_objects")
    if not spec or not spec.origin:
        return

    path = Path(spec.origin)
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return

    # Already patched.
    if "alias_name = getattr(alias" in text:
        return

    needle = "if (te_alias := getattr(typing_extensions, alias._name, None)) is not None:"
    if needle not in text:
        return

    replacement = (
        "alias_name = getattr(alias, '_name', None) or getattr(alias, '__name__', None)\n"
        "    if not alias_name:\n"
        "        continue\n"
        "    if (te_alias := getattr(typing_extensions, alias_name, None)) is not None:"
    )

    try:
        path.write_text(text.replace(needle, replacement, 1), encoding="utf-8")
    except Exception:
        return


_patch_typing_inspection_if_needed()

import uvicorn

# Core FastAPI imports with type hints
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# AFO Kingdom imports (clear and organized)
from AFO.api.config import get_app_config, get_server_config
from AFO.api.middleware import setup_middleware
from AFO.api.router_manager import setup_routers

if TYPE_CHECKING:
    from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AFOServer:
    """AFO Kingdom API Server Manager

    아름다운 코드 원칙을 준수하는 API 서버 관리 클래스.
    Trinity Score 기반 품질 관리를 통해 안정성과 확장성을 보장.

    Attributes:
        app: FastAPI 애플리케이션 인스턴스
        limiter: Rate limiting 인스턴스

    """

    def __init__(self) -> None:
        """Initialize AFO API Server with beautiful code principles."""
        self._setup_python_path()
        self._setup_sentry()
        self._setup_observability()  # Added: Observability Trinity
        self.app = self._create_app()
        self.limiter = self._create_limiter()
        self.healing_agent = HealingAgent()  # Initialize Super Agent
        self._background_tasks = set()  # Prevent GC of async tasks
        self._configure_app()
        self._setup_components()

        logger.info("AFO Kingdom API Server initialized with beautiful code principles")

    def _setup_sentry(self) -> None:
        """Initialize Sentry for error tracking and performance monitoring.

        Trinity Score: 善 (Goodness) - 실시간 에러 포착 및 시스템 안정성 강화
        """
        try:
            import sentry_sdk
            from sentry_sdk.integrations.fastapi import FastApiIntegration
            from sentry_sdk.integrations.logging import LoggingIntegration
            from sentry_sdk.integrations.starlette import StarletteIntegration

            # DSN should be configured via environment or config
            # Using a placeholder for now as per user request
            dsn = "${SENTRY_DSN:-}"

            sentry_sdk.init(
                dsn=dsn,
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
                environment="development",
                release="afo-core@1.0.0",
                integrations=[
                    FastApiIntegration(transaction_style="endpoint"),
                    StarletteIntegration(),
                    LoggingIntegration(level=logging.ERROR, event_level=logging.CRITICAL),
                ],
                send_default_pii=False,
            )
            logger.info("✅ Sentry initialized successfully")
        except ImportError:
            logger.warning("⚠️ Sentry SDK not installed, skipping initialization")
        except Exception:
            logger.exception("❌ Sentry initialization failed")

    def _setup_observability(self) -> None:
        """Initialize OpenTelemetry (Traces, Logs, Metrics).

        Trinity Score: 眞 (Truth) - 시스템의 투명한 관측 가능성 확보
        """
        try:
            # Local imports to prevent ModuleNotFoundError if dependencies are missing
            from opentelemetry import trace
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            from opentelemetry.instrumentation.logging import LoggingInstrumentor
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            # 1. Configure Resource (Service Name)
            resource = Resource.create(attributes={"service.name": "afo-soul-engine"})

            # 2. Configure Tracer Provider
            tracer_provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(tracer_provider)

            # 3. Configure OTLP Exporter (gRPC)
            # Default: http://localhost:4317 or env OTEL_EXPORTER_OTLP_ENDPOINT
            otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
            otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)

            # 4. Add Span Processor
            span_processor = BatchSpanProcessor(otlp_exporter)
            tracer_provider.add_span_processor(span_processor)

            # 5. Instrument Logging (Inject TraceContext)
            LoggingInstrumentor().instrument(set_logging_format=True)

            logger.info(f"✅ OpenTelemetry initialized (Endpoint: {otlp_endpoint})")
        except Exception as e:
            logger.warning(f"⚠️ OpenTelemetry setup failed: {e}")

    def _setup_python_path(self) -> None:
        """Setup Python path for AFO imports.

        Trinity Score: 眞 (Truth) - 정확한 경로 설정으로 import 안정성 보장
        """
        afo_root = str(Path(__file__).resolve().parent.parent)
        if afo_root not in sys.path:
            sys.path.insert(0, afo_root)
            logger.debug(f"Added AFO root to Python path: {afo_root}")

    def _create_app(self) -> FastAPI:
        """Create FastAPI application instance.

        Returns:
            Configured FastAPI application

        """
        app = get_app_config()
        logger.info("FastAPI application created")

        # Chancellor Router 직접 등록
        try:
            from AFO.api.routers.chancellor_router import router as chancellor_router

            app.include_router(chancellor_router)
            logger.info("Chancellor Router registered successfully")
        except Exception as e:
            logger.warning(f"Chancellor Router registration failed: {e}")

        # Multimodal Router 등록 (Vision, Audio, Video)
        try:
            from api.routers.multimodal import router as multimodal_router

            app.include_router(multimodal_router)
            logger.info("Multimodal Router registered successfully")
        except Exception as e:
            logger.warning(f"Multimodal Router registration failed: {e}")

        # RAG Router 등록
        try:
            from AFO.api.routers.rag_query import router as rag_router

            app.include_router(rag_router, prefix="/api")
            logger.info("RAG Router registered successfully")
        except Exception as e:
            logger.warning(f"RAG Router registration failed: {e}")

        # Auth Router 등록 (ACL 관리용)
        try:
            from AFO.api.routes.auth import router as auth_router

            app.include_router(auth_router)
            logger.info("Auth Router registered successfully")
        except Exception as e:
            logger.warning(f"Auth Router registration failed: {e}")

        return app

    def _create_limiter(self) -> Limiter:
        """Create rate limiter for API protection.

        Returns:
            Configured rate limiter

        """
        limiter = Limiter(key_func=get_remote_address)
        logger.info("Rate limiter configured")
        return limiter

    def _configure_app(self) -> None:
        """Configure FastAPI application with middleware and handlers.

        Trinity Score: 善 (Goodness) - 보안 및 에러 핸들링 강화
        """
        # Configure rate limiting
        self.app.state.limiter = self.limiter
        self.app.add_exception_handler(
            RateLimitExceeded, cast("ExceptionHandler", _rate_limit_exceeded_handler)
        )

        # Metrics 미들웨어 추가 (가장 먼저)
        try:
            from AFO.api.middleware.metrics import MetricsMiddleware

            self.app.add_middleware(MetricsMiddleware)
        except ImportError:
            logger.warning("⚠️ MetricsMiddleware not available")

        # ACL 미들웨어 추가 (rate limit 다음에)
        try:
            from AFO.api.middleware.authz import APIKeyAuthMiddleware

            self.app.add_middleware(APIKeyAuthMiddleware)
        except ImportError:
            logger.warning("⚠️ APIKeyAuthMiddleware not available")

        # ACL 초기화 (기본 엔드포인트 등록)
        try:
            from AFO.api.auth.api_key_acl import DEFAULT_ENDPOINT_SCOPES, acl

            for path, method, scopes in DEFAULT_ENDPOINT_SCOPES:
                acl.add_endpoint_scope(path, method, scopes)
        except ImportError:
            logger.warning("⚠️ API Key ACL not available")

        @self.app.on_event("startup")
        async def start_super_agent() -> None:
            """Start the Debugging Super Agent in the background."""
            if os.getenv("AFO_DEBUG_AGENT_ENABLED") != "1":
                logger.info("🛡️ Debugging Super Agent is DISABLED (Default Safe Mode).")
                return

            logger.info("🤖 Starting Debugging Super Agent (2026 Vision)...")
            # Fire-and-forget the infinite loop of the agent (Strong Reference Held)
            task = asyncio.create_task(self.healing_agent.start())
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)

        @self.app.on_event("shutdown")
        async def persist_acl_keys() -> None:
            """서버 종료 시 ACL 키 영속 저장"""
            try:
                from AFO.api.auth.api_key_acl import acl

                acl.persist_all_keys()
                logger.info("✅ ACL keys persisted on shutdown")
            except Exception as e:
                logger.warning(f"⚠️  ACL persistence failed on shutdown: {e}")

        @self.app.post("/api/debug/agent/simulate", tags=["Debugging Agent"])
        async def trigger_simulation(
            error_code: str = "DTZ005",
            x_afo_debug_secret: str | None = Header(None, alias="X-AFO-DEBUG-SECRET"),
        ) -> dict[str, Any]:
            """Trigger a self-healing simulation scenario (Protected)."""

            # 1. Gate: Feature Flag Check
            if os.getenv("AFO_DEBUG_AGENT_ENABLED") != "1":
                raise HTTPException(status_code=403, detail="Debugging Agent is disabled.")

            # 2. Gate: Secret Header Check (Simple protection for prototype)
            required_secret = os.getenv("AFO_DEBUG_SECRET", "default-dev-secret")
            if x_afo_debug_secret != required_secret:
                raise HTTPException(status_code=401, detail="Invalid Debug Secret.")

            await self.healing_agent.trigger_anomaly(error_code)
            return {
                "message": f"Anomaly {error_code} injected.",
                "agent_name": self.healing_agent.name,
                "current_entropy": self.healing_agent.state.entropy,
            }

        @self.app.get("/metrics")
        async def metrics():
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

        # SSE Log Stream for Chancellor Real-time Thoughts (眞·美)
        @self.app.get("/api/logs/stream", tags=["Logs"])
        async def logs_stream(request: Request):
            """Stream real-time chancellor thoughts via Server-Sent Events."""
            async def event_generator():
                """Generate SSE events for chancellor stream."""
                import datetime
                # Initial connection message
                yield {
                    "event": "connected",
                    "data": f'{{"message": "🏰 Chancellor Stream Connected", "timestamp": "{datetime.datetime.now(datetime.timezone.utc).isoformat()}"}}'
                }
                
                counter = 0
                while True:
                    # Check if client disconnected
                    if await request.is_disconnected():
                        break
                    
                    # Heartbeat every 15 seconds
                    await asyncio.sleep(15)
                    counter += 1
                    yield {
                        "event": "heartbeat", 
                        "data": f'{{"message": "💓 Chancellor Heartbeat #{counter}", "timestamp": "{datetime.datetime.now(datetime.timezone.utc).isoformat()}"}}'
                    }
            
            return EventSourceResponse(event_generator())

        logger.info("Application configured with security measures")

    def _setup_components(self) -> None:
        """Setup middleware and routers.

        Trinity Score: 美 (Beauty) - 모듈화된 컴포넌트 설정
        """
        try:
            setup_middleware(self.app)
            logger.info("Middleware setup completed")

            setup_routers(self.app)
            logger.info("Router setup completed")

            # Instrument FastAPI app with OpenTelemetry
            try:
                from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

                FastAPIInstrumentor.instrument_app(self.app)
                logger.info("OpenTelemetry FastAPI instrumentation applied")
            except ImportError:
                pass  # Already logged in _setup_observability
            except Exception as e:
                logger.warning(f"Failed to instrument FastAPI: {e}")

        except Exception:
            logger.exception("Component setup failed")
            raise

    def run_server(self, host: str = "127.0.0.1", port: int = 8010) -> None:
        """Run the API server.

        Args:
            host: Server host address
            port: Server port number

        """
        logger.info(f"🚀 Starting AFO Kingdom API Server on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


# Global server instance (Singleton pattern for beautiful code)
server = AFOServer()
app = server.app


# Main execution block with proper error handling
if __name__ == "__main__":
    try:
        host, port = get_server_config()
        server.run_server(host=host, port=port)
    except Exception:
        logger.exception("Failed to start server")
        sys.exit(1)
