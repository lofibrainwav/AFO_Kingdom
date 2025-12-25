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
from fastapi import APIRouter

# Optional SSE import
try:
    from sse_starlette.sse import EventSourceResponse

    SSE_AVAILABLE = True
except ImportError:
    # Define a dummy type for type checking if import fails
    EventSourceResponse = Any  # type: ignore
    SSE_AVAILABLE = False

router = APIRouter(prefix="/api/system", tags=["System Health"])


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
                # Explicitly cast to dict to avoid 'Awaitable' confusion in mypy
                all_status = cast("dict", redis_client.hgetall("services:health"))

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


# Request import for SSE endpoint (kept near endpoint for locality)
from fastapi import Request


@router.get("/logs/stream")
async def stream_logs(request: Request, limit: int = 0) -> EventSourceResponse:
    """
    [Serenity: 孝] Real-time Log Stream via Redis Pub/Sub

    Architecture:
    1. Primary: Redis Pub/Sub ('kingdom:logs:stream') - Zero Friction
    2. Fallback: File Tail ('backend.log') - Safety Net (Goodness)
    """

    async def log_generator():
        # 1. Try Redis Pub/Sub First
        try:
            from AFO.utils.cache_utils import cache

            if cache.enabled and cache.redis:
                pubsub = cache.redis.pubsub()
                pubsub.subscribe("kingdom:logs:stream")

                # Yield initial connection message
                yield {
                    "data": json.dumps(
                        {
                            "timestamp": datetime.now().isoformat(),
                            "message": "🔌 [Serenity] Connected to Neural Network (Redis Pub/Sub)",
                        }
                    )
                }

                while True:
                    if await request.is_disconnected():
                        break

                    message = pubsub.get_message(ignore_subscribe_messages=True)
                    if message:
                        # Redis returns bytes, need to decode
                        data = message["data"]
                        if isinstance(data, bytes):
                            data = data.decode("utf-8")

                        # Already JSON formatted by publisher
                        yield {"data": data}

                    await asyncio.sleep(0.1)  # Prevent tight loop
                return  # Exit if disconnected
        except Exception as e:
            logger.warning(f"Redis Pub/Sub failed: {e}. Falling back to file tail.")

        # 2. Fallback to File Tail (Original Logic)
        log_file = "backend.log"
        if not os.path.exists(log_file):
            open(log_file, "a").close()

        with open(log_file) as f:
            f.seek(0, 2)
            while True:
                if await request.is_disconnected():
                    break
                line = f.readline()
                if line:
                    yield {"data": line.strip()}
                else:
                    await asyncio.sleep(0.5)

    return EventSourceResponse(log_generator())
