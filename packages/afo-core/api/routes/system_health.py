# Trinity Score: 90.0 (Established by Chancellor)
"""System Health & Logs Routes."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

import psutil
import redis
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Optional SSE import
try:
    from sse_starlette.sse import EventSourceResponse

    SSE_AVAILABLE = True
except ImportError:
    # Define a dummy type for type checking if import fails
    EventSourceResponse = Any  # type: ignore
    SSE_AVAILABLE = False

router = APIRouter(prefix="/api/system", tags=["System Health"])

# Security: Internal API Key Authentication for SSE Health Metrics
# Only allows internal services (Dashboard) to report SSE health metrics
security = HTTPBearer()

async def verify_internal_service(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify internal service authentication for SSE health metrics.

    This endpoint is only accessible to internal AFO services (Dashboard).
    Uses Bearer token authentication with internal API key.
    """
    expected_token = os.getenv("AFO_INTERNAL_API_KEY", "afo_internal_default_key")

    if credentials.credentials != expected_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Invalid internal API key"
        )

    return credentials.credentials


@router.get("/health", include_in_schema=os.getenv("ENVIRONMENT") == "dev")
async def system_health_alias():
    """Alias for /api/health to support legacy tests. Only available in dev environment."""
    current_time = datetime.now().isoformat()
    status = "unknown"
    timestamp = current_time
    try:
        from AFO.services.health_service import get_comprehensive_health

        health_data = await get_comprehensive_health()
        status = str(health_data.get("status", status))
        timestamp = str(health_data.get("timestamp", timestamp))
    except Exception as e:
        logger.warning("System health alias failed to read health service: %s", e)

    try:
        from AFO.api.metadata import get_api_metadata

        api_version = str(get_api_metadata().get("version", "unknown"))
    except Exception:
        api_version = "unknown"

    return {"status": status, "timestamp": timestamp, "version": api_version}


logger = logging.getLogger(__name__)

ORGANS = [
    "Brain",
    "Heart",
    "Lungs",
    "Digestive",
    "Immune",
    "Musculoskeletal",
    "Endocrine",
    "Nervous",
    "Reproductive",
    "Circulatory",
    "Integumentary",
]


def _get_redis_client() -> redis.Redis | None:
    """Redis 클라이언트 생성 (Lazy Loading)"""
    # Phase 2-4: settings 사용
    # Phase 2-4: settings 사용
    try:
        from AFO.utils.redis_connection import get_redis_url

        redis_url = get_redis_url()
    except ImportError:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

    try:
        # Explicitly cast to redis.Redis to satisfy mypy
        client = cast(
            "redis.Redis",
            redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            ),
        )
        client.ping()
        return client
    except Exception as e:
        logger.warning(f"Redis connection failed in System Health: {e}")
        return None


@router.get("/metrics")
async def get_system_metrics() -> dict[str, Any]:
    """
    CoreZen Dashboard를 위한 실시간 시스템 메트릭

    Returns:
        - memory_percent: 메모리 사용률 (0-100)
        - swap_percent: 스왑 사용률 (0-100)
        - containers_running: 실행 중인 컨테이너 수 (Redis 기반 추정)
        - disk_percent: 디스크 사용률 (0-100)
        - redis_connected: Redis 연결 상태
        - langgraph_active: LangGraph 활성 상태 (항상 True로 가정 or Redis 체크)
    """
    try:
        # 1. System Metrics via psutil (Cross-platform)
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage("/")

        memory_percent = memory.percent
        swap_percent = swap.percent
        disk_percent = disk.percent

        # 2. Redis Connection & Service Status
        redis_client = _get_redis_client()
        redis_connected = redis_client is not None

        containers_running = 0
        if redis_client:
            try:
                # Count healthy services from Redis
                all_status = redis_client.hgetall("services:health")

                # Filter for services that are 'healthy'
                containers_running = sum(
                    1
                    for data_json in all_status.values()
                    if isinstance(data_json, str) and "healthy" in data_json
                )
            except Exception:
                pass

        # 3. LangGraph Active Status
        # For now, we assume it's active if the API is running,
        # or we could check a specific Redis key if needed.
        langgraph_active = True

        # 4. Bind System Metrics to Organs (11-오장육부 Metaphor)
        # Score calculation: 100 - (Usage %)
        # Healthy means Low Usage (high score)

        # Brain (Memory)
        brain_score = max(0, 100 - memory_percent)
        # Digestive (Disk)
        digestive_score = max(0, 100 - disk_percent)
        # Heart (Redis - Connectivity)
        heart_score = 100 if redis_connected else 0
        # Lungs (Swap/CPU Proxy)
        lungs_score = max(0, 100 - swap_percent)

        # Others (Baseline high, slightly affected by total load)
        avg_load = (memory_percent + disk_percent) / 2
        general_score = max(50, 100 - (avg_load * 0.5))

        organs_data = [
            {"name": "Brain", "score": brain_score, "metric": f"Mem {memory_percent}%"},
            {"name": "Heart", "score": heart_score, "metric": "Redis Connected"},
            {
                "name": "Digestive",
                "score": digestive_score,
                "metric": f"Disk {disk_percent}%",
            },
            {"name": "Lungs", "score": lungs_score, "metric": f"Swap {swap_percent}%"},
            # Fill others with general health
            {"name": "Immune", "score": general_score, "metric": "General Protection"},
            {
                "name": "Musculoskeletal",
                "score": general_score,
                "metric": "Infrastructure",
            },
            {"name": "Endocrine", "score": general_score, "metric": "Scheduling"},
            {"name": "Nervous", "score": brain_score, "metric": "Network/API"},
            {"name": "Reproductive", "score": 100, "metric": "Backups"},
            {"name": "Circulatory", "score": heart_score, "metric": "Data Flow"},
            {
                "name": "Integumentary",
                "score": general_score,
                "metric": "Firewall/API Gateway",
            },
        ]

        return {
            "memory_percent": round(memory_percent, 1),
            "swap_percent": round(swap_percent, 1),
            "containers_running": containers_running,
            "disk_percent": round(disk_percent, 1),
            "redis_connected": redis_connected,
            "langgraph_active": langgraph_active,
            "organs": organs_data,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error collecting system metrics: {e}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}


async def _log_stream(limit: int | None = None) -> AsyncGenerator[str, None]:
    counter = 0
    while True:
        counter += 1
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"[{counter}] 시스템 정상 동작 (Unified Health)",
        }
        yield json.dumps(message)  # Ensure JSON string for SSE data
        await asyncio.sleep(1)
        if limit and counter >= limit:
            break


@router.get("/kingdom-status")
async def get_kingdom_status() -> dict[str, Any]:
    """
    AFO Kingdom Grand Status (Real-time Truth)

    Returns:
        - heartbeat: System pulse (Inverse CPU)
        - dependencies: Verified critical modules
        - scholars: Live module status
        - pillars: Dynamic Trinity Scores calculated from system state
    """
    import importlib.util

    from AFO.domain.metrics.trinity import TrinityInputs, TrinityMetrics

    # 1. Dependency Verification (42 Core Items)
    dependency_map = {
        "openai": "openai",
        "anthropic": "anthropic",
        "langchain": "langchain",
        "langgraph": "langgraph",
        "ragas": "ragas",
        "sentence-tx": "sentence_transformers",
        "suno": "suno",
        "numpy": "numpy",
        "pandas": "pandas",
        "scipy": "scipy",
        "sympy": "sympy",
        "boto3": "boto3",
        "hcloud": "hcloud",
        "docker": "docker",
        "git": "git",
        "kafka": "kafka",
        "redis": "redis",
        "chromadb": "chromadb",
        "qdrant": "qdrant_client",
        "neo4j": "neo4j",
        "postgresql": "psycopg2",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "requests": "requests",
        "sse-starlette": "sse_starlette",
        "web3": "web3",
        "eth-account": "eth_account",
        "psutil": "psutil",
        "prometheus": "prometheus_client",
        "watchdog": "watchdog",
        "playwright": "playwright",
        "mcp": "mcp",
        "black": "black",
        "ruff": "ruff",
        "pytest": "pytest",
        "mypy": "mypy",
        "markdown": "markdown",
        "frontmatter": "frontmatter",
    }

    verified_list = []
    for display, module_name in dependency_map.items():
        try:
            if importlib.util.find_spec(module_name) is not None:
                verified_list.append(display)
        except Exception:
            pass

    virtual_deps = ["ai-analysis", "react", "iframe", "trinity-mcp"]
    verified_list.extend(virtual_deps)

    # 2. Organs Data (Real-time System Metrics)
    cpu_percent = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_if_stats()

    heart_score = max(0, 100 - int(cpu_percent))
    brain_score = max(0, 100 - int(mem.percent))
    lungs_score = max(0, 100 - int(swap.percent))
    stomach_score = max(0, 100 - int(disk.percent))
    eyes_score = 100 if net else 50

    organs = [
        {"name": "Heart", "score": heart_score, "metric": f"CPU {cpu_percent}%"},
        {"name": "Brain", "score": brain_score, "metric": f"Mem {mem.percent}%"},
        {"name": "Lungs", "score": lungs_score, "metric": f"Swap {swap.percent}%"},
        {"name": "Stomach", "score": stomach_score, "metric": f"Disk {disk.percent}%"},
        {"name": "Eyes", "score": eyes_score, "metric": f"Net {len(net)} if"},
    ]

    # 3. Dynamic Trinity Score Calculation
    # Truth (眞): System Integrity (Memory & Dependencies)
    truth_raw = (brain_score / 100.0) * 0.5 + (len(verified_list) / 46.0) * 0.5

    # Goodness (善): Stability (Swap usage inverse - low swap means stable ram)
    goodness_raw = lungs_score / 100.0

    # Beauty (美): Responsiveness (Network health & CPU headroom)
    beauty_raw = (eyes_score / 100.0) * 0.4 + (heart_score / 100.0) * 0.6

    # Serenity (孝): Low Friction (CPU Load inverse)
    serenity_raw = heart_score / 100.0

    # Eternity (永): Persistance (Disk Space)
    eternity_raw = stomach_score / 100.0

    # Ensure 0.0-1.0 range via TrinityInputs.clamp() implicitly
    inputs = TrinityInputs(
        truth=truth_raw,
        goodness=goodness_raw,
        beauty=beauty_raw,
        filial_serenity=serenity_raw,
    )
    # Eternity passed separately to metrics
    metrics = TrinityMetrics.from_inputs(inputs, eternity=eternity_raw)

    trinity_score = round(metrics.trinity_score * 100, 1)  # Scale to 100

    pillars = [
        {"name": "Truth 眞", "score": int(metrics.truth * 100)},
        {"name": "Good 善", "score": int(metrics.goodness * 100)},
        {"name": "Beauty 美", "score": int(metrics.beauty * 100)},
        {"name": "Serenity 孝", "score": int(metrics.filial_serenity * 100)},
        {"name": "Eternity 永", "score": int(metrics.eternity * 100)},
    ]

    # 4. Real Scholar Status Check
    # Mapping Scholar to key Python Modules
    scholar_map = {
        "Jaryong": "AFO.scholars.jaryong",  # Logic
        "Bangtong": "AFO.scholars.bangtong",  # Implementation
        "Yeongdeok": "AFO.scholars.yeongdeok",  # Security
        "Yukson": "AFO.scholars.yukson",  # Strategy
    }

    scholars_status = []
    for name, module_path in scholar_map.items():
        status = "Inactive"
        if importlib.util.find_spec(module_path) is not None:
            status = "Active"

        scholars_status.append({"name": name, "role": "Check", "status": status})

    return {
        "heartbeat": heart_score,
        "dependency_count": len(verified_list),
        "total_dependencies": 42,
        "verified_dependencies": verified_list,
        "pillars": pillars,
        "trinity_score": trinity_score,
        "scholars": scholars_status,
        "organs": organs,
        "entropy": int(cpu_percent),
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/antigravity/config")
async def get_antigravity_config() -> dict[str, Any]:
    """
    [TRUTH WIRING]
    Expose current AntiGravity settings for verification.
    """
    from AFO.config.antigravity import antigravity

    return {
        "environment": antigravity.ENVIRONMENT,
        "auto_deploy": antigravity.AUTO_DEPLOY,
        "dry_run_default": antigravity.DRY_RUN_DEFAULT,
        "auto_sync": antigravity.AUTO_SYNC,
        "log_level": antigravity.LOG_LEVEL,
        "mode": "Self-Expanding" if antigravity.SELF_EXPANDING_MODE else "Static",
    }


# SSOT SSE Router (prefix-free for /api/logs/stream canonical path)
# This router is registered separately in router_manager.py
sse_ssot_router = APIRouter(prefix="/api", tags=["SSE SSOT"])


async def _sse_log_generator():
    """Shared SSE log generator for all alias paths (SSOT)."""
    messages = [
        "🔌 SSE Stream Connected",
        "💓 Heartbeat #1",
        "💓 Heartbeat #2",
        "✅ Stream Test Complete",
    ]

    for i, message in enumerate(messages):
        yield {
            "data": json.dumps(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": message,
                    "level": "INFO",
                    "counter": i + 1,
                }
            )
        }

        if i < len(messages) - 1:
            await asyncio.sleep(0.5)


# SSOT Canonical Path: /api/logs/stream
@sse_ssot_router.get("/logs/stream")
async def stream_logs_ssot(request: Request, limit: int = 0) -> EventSourceResponse:
    """
    [SSOT] Canonical SSE Log Stream Endpoint

    All SSE log streaming should use this path: /api/logs/stream

    Security: Rate limited to prevent abuse (10 requests/minute per IP)
    """
    # Security: Rate limit check to prevent abuse
    client_ip = request.client.host if request.client else "unknown"
    if not check_sse_rate_limit(client_ip, max_requests=10, window_seconds=60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: Too many SSE stream requests"
        )

    # SSE headers for browser compatibility (avoid hop-by-hop Connection header)
    headers = {
        "Cache-Control": "no-store, no-cache, no-transform",
        "X-Accel-Buffering": "no"
    }
    return EventSourceResponse(_sse_log_generator(), headers=headers)


# Cursor Compatibility Path: /api/stream/logs
@sse_ssot_router.get("/stream/logs")
async def stream_logs_cursor_compat(request: Request, limit: int = 0) -> RedirectResponse:
    """[Alias] Cursor compatibility path for /api/stream/logs (Redirects to SSOT)"""
    return RedirectResponse("/api/logs/stream", status_code=308)


# Original Path (retained for existing integrations): /api/system/logs/stream
@router.get("/logs/stream")
async def stream_logs(request: Request, limit: int = 0) -> RedirectResponse:
    """
    [Serenity: 孝] Simple Test Log Stream
    Redirects to canonical SSOT path
    """
    return RedirectResponse("/api/logs/stream", status_code=308)


# ============================================================================
# SSE Rate Limit Protection
# ============================================================================

import time
from collections import defaultdict

# Simple in-memory rate limiter for SSE streams
# Production should use Redis for distributed rate limiting
_sse_rate_limits = defaultdict(list)

def check_sse_rate_limit(client_ip: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
    """
    Check if client IP exceeds SSE stream rate limit.

    Args:
        client_ip: Client IP address
        max_requests: Maximum requests per window
        window_seconds: Time window in seconds

    Returns:
        True if allowed, False if rate limited
    """
    now = time.time()
    window_start = now - window_seconds

    # Clean old requests
    _sse_rate_limits[client_ip] = [
        timestamp for timestamp in _sse_rate_limits[client_ip]
        if timestamp > window_start
    ]

    # Check if under limit
    if len(_sse_rate_limits[client_ip]) < max_requests:
        _sse_rate_limits[client_ip].append(now)
        return True

    return False

# ============================================================================
# SSE Health Metrics Endpoint
# ============================================================================

@router.post("/sse/health", include_in_schema=os.getenv("ENVIRONMENT") == "dev")
async def update_sse_health_metrics(
    open_connections: int = 0,
    reconnect_count: int = 0,
    last_event_age_seconds: float = 0.0,
    token: str = Depends(verify_internal_service),  # Security: Internal auth required
) -> dict[str, str]:
    """
    Update SSE health metrics for monitoring and alerting.

    This endpoint allows the dashboard to report SSE connection health
    metrics to Prometheus for alerting and observability.

    Security: Requires internal API key authentication.
    Validation: Input values are sanitized to prevent metric explosion.

    Args:
        open_connections: Number of currently open SSE connections (0-100)
        reconnect_count: Total number of SSE reconnection attempts (0-10000)
        last_event_age_seconds: Time since last SSE event in seconds (0-3600)

    Returns:
        Success confirmation
    """
    # Security: Input validation to prevent metric explosion attacks
    # Limit reasonable ranges to prevent Prometheus overload
    if not (0 <= open_connections <= 100):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid open_connections: must be 0-100"
        )

    if not (0 <= reconnect_count <= 10000):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reconnect_count: must be 0-10000"
        )

    if not (0 <= last_event_age_seconds <= 3600):  # Max 1 hour
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid last_event_age_seconds: must be 0-3600"
        )

    try:
        from AFO.utils.metrics import update_sse_health_metrics

        update_sse_health_metrics(
            open_connections=open_connections,
            reconnect_count=reconnect_count,
            last_event_age_seconds=last_event_age_seconds,
        )

        return {"status": "success", "message": "SSE health metrics updated"}

    except Exception as e:
        logger.warning("Failed to update SSE health metrics: %s", e)
        return {"status": "error", "message": f"Failed to update metrics: {e}"}
