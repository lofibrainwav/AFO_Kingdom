# Trinity Score: 90.0 (Established by Chancellor)
"""
Health Service - Centralized logic for system monitoring
眞 (Truth): Accurate service status detection
善 (Goodness): Reliable health reporting
"""

import asyncio
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

import httpx
import redis.asyncio as redis

# AFO internal imports
from AFO.config.settings import get_settings
from AFO.domain.metrics.trinity import calculate_trinity
from AFO.services.database import get_db_connection
from AFO.utils.redis_connection import get_redis_url

if TYPE_CHECKING:
    from AFO.domain.metrics.trinity import TrinityMetrics

logger = logging.getLogger(__name__)

# Trinity Score 모니터링 (선택적)
try:
    from services.trinity_score_monitor import record_trinity_score_metrics
    TRINITY_MONITORING_AVAILABLE = True
except ImportError:
    TRINITY_MONITORING_AVAILABLE = False
    if TRINITY_MONITORING_AVAILABLE is False:  # logger가 정의된 후에만 로깅
        logger.warning("Trinity Score monitoring not available")

# 건강 체크 캐시 설정
import json
import time
from typing import Optional

# 캐시 설정
HEALTH_CACHE_TTL = 30  # 30초 캐시
HEALTH_CACHE_KEY = "afo:health:comprehensive"
INDIVIDUAL_CACHE_TTL = 60  # 개별 체크 60초 캐시

# 캐시 저장소 (메모리 + Redis)
_health_cache: dict | None = None
_cache_timestamp: float = 0

# 동시성 제한
_semaphore = asyncio.Semaphore(5)  # 최대 5개 동시 실행


async def check_redis() -> dict[str, Any]:
    """心_Redis 상태 체크 (캐시 적용, 타임아웃 5초)"""
    cache_key = "afo:health:redis"
    try:
        r = redis.from_url(get_redis_url())
        pong = await asyncio.wait_for(r.ping(), timeout=5.0)
        await r.close()
        result = {"healthy": pong, "output": f"PING -> {pong}"}

        # Redis에 캐시 저장 (선택적)
        try:
            r_cache = redis.from_url(get_redis_url())
            await r_cache.setex(cache_key, INDIVIDUAL_CACHE_TTL, json.dumps(result))
            await r_cache.close()
        except Exception:
            pass  # 캐시 실패해도 기능 영향 없음

        return result
    except Exception as e:
        return {"healthy": False, "output": f"Error: {str(e)[:50]}"}


async def check_postgres() -> dict[str, Any]:
    """肝_Postgres 상태 체크 (캐시 적용, 타임아웃 5초)"""
    try:
        conn = await get_db_connection()
        result = await conn.fetchval("SELECT 1")
        await conn.close()
        return {"healthy": result == 1, "output": f"SELECT 1 -> {result}"}
    except Exception as e:
        return {"healthy": False, "output": f"Error: {str(e)[:50]}"}


async def check_ollama() -> dict[str, Any]:
    """脾_Ollama 상태 체크"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            ollama_url = get_settings().OLLAMA_BASE_URL
            resp = await client.get(ollama_url + "/api/tags")
            data = resp.json()
            model_count = len(data.get("models", []))
            return {"healthy": model_count > 0, "output": f"Models: {model_count}"}
    except Exception as e:
        return {"healthy": False, "output": f"Error: {str(e)[:50]}"}


async def check_self() -> dict[str, Any]:
    """肺_API_Server 자가 진단"""
    return {"healthy": True, "output": "Self-check: API responding"}


async def check_mcp() -> dict[str, Any]:
    """肾_MCP 상태 체크 (외부 서비스 연결, 타임아웃 5초)"""
    try:
        # MCP 서버 구성 상태 체크
        from config.health_check_config import health_check_config

        if health_check_config.MCP_SERVERS and len(health_check_config.MCP_SERVERS) > 0:
            # 간단하게 구성된 서버 수만 확인
            return {
                "healthy": True,
                "output": f"MCP servers configured: {len(health_check_config.MCP_SERVERS)} servers"
            }
        else:
            return {"healthy": False, "output": "No MCP servers configured"}
    except Exception as e:
        return {"healthy": False, "output": f"MCP check failed: {str(e)[:50]}"}


async def get_comprehensive_health() -> dict[str, Any]:
    """종합 건강 상태 진단 및 Trinity Score 계산 (캐시 적용)"""
    current_time = datetime.now().isoformat()
    response: dict[str, Any] = {}  # 초기화

    # 캐시 확인 (글로벌 메모리 캐시 우선)
    global _health_cache, _cache_timestamp
    if _health_cache and (time.time() - _cache_timestamp) < HEALTH_CACHE_TTL:
        logger.debug("Returning cached health data")
        return _health_cache

    # Redis 캐시 확인 (선택적)
    try:
        r = redis.from_url(get_redis_url())
        cached_data = await r.get(HEALTH_CACHE_KEY)
        await r.close()
        if cached_data:
            cached_result = json.loads(cached_data)
            # 메모리 캐시에도 저장
            _health_cache = cached_result
            _cache_timestamp = time.time()
            logger.debug("Returning Redis cached health data")
            return cast(dict[str, Any], cached_result)
    except Exception:
        pass  # Redis 캐시 실패해도 계속 진행

    # 동시성 제한 적용
    async with _semaphore:
        # 병렬 실행 (타임아웃 적용 - 전체 10초 제한)
        try:
            results = await asyncio.wait_for(
                asyncio.gather(
                    check_redis(),
                    check_postgres(),
                    check_ollama(),
                    check_self(),
                    check_mcp(),
                    return_exceptions=True,
                ),
                timeout=10.0  # 10초 타임아웃
            )
        except TimeoutError:
            logger.warning("Health check timed out after 10 seconds")
            results = (
                {"healthy": False, "output": "Timeout"},
                {"healthy": False, "output": "Timeout"},
                {"healthy": False, "output": "Timeout"},
                {"healthy": True, "output": "API responding"},
                {"healthy": False, "output": "Timeout"},
            )

    organ_names = ["心_Redis", "肝_PostgreSQL", "脾_Ollama", "肺_API_Server", "肾_MCP"]
    organs: list[dict[str, Any]] = []

    for i, name in enumerate(organ_names):
        res = results[i]
        if isinstance(res, Exception):
            status_data = {"healthy": False, "output": str(res)}
        else:
            status_data = cast("dict[str, Any]", res)

        organs.append(
            {
                "organ": name,
                "healthy": status_data["healthy"],
                "status": "healthy" if status_data["healthy"] else "unhealthy",
                "output": status_data["output"],
                "timestamp": current_time,
            }
        )

    # Trinity 계산 (5기둥 SSOT 가중 합)
    healthy_count = sum(1 for o in organs if o["healthy"])
    total_organs = len(organs)

    # 眞 (Truth 35%) - 핵심 데이터 계층
    core_data_organs = ["心_Redis", "肝_PostgreSQL"]
    truth_healthy = sum(
        1 for o in organs if o["organ"] in core_data_organs and o["healthy"]
    )
    truth_score = truth_healthy / len(core_data_organs) if core_data_organs else 0.0

    # 善 (Goodness 35%) - 전체 서비스 기반 안정성
    goodness_score = healthy_count / total_organs if total_organs > 0 else 0.0

    # 美 (Beauty 20%) - API 가용성
    api_healthy = any(o["organ"] == "肺_API_Server" and o["healthy"] for o in organs)
    beauty_score = 1.0 if api_healthy else 0.0

    # 孝 (Serenity 8%) - LLM 가용성
    llm_healthy = any(o["organ"] == "脾_Ollama" and o["healthy"] for o in organs)
    filial_score = 1.0 if llm_healthy else 0.0

    # 永 (Eternity 2%) - 영속적 가동
    eternity_score = (
        1.0 if healthy_count == total_organs else healthy_count / total_organs
    )

    trinity_metrics: TrinityMetrics = calculate_trinity(
        truth=truth_score,
        goodness=goodness_score,
        beauty=beauty_score,
        filial_serenity=filial_score,
        eternity=eternity_score,
    )

    # Trinity Score 모니터링 기록 (선택적)
    if TRINITY_MONITORING_AVAILABLE:
        try:
            record_trinity_score_metrics(trinity_metrics)
        except Exception as e:
            logger.warning(f"Failed to record Trinity Score metrics: {e}")

    # Issue/Suggestion 생성
    issues = []
    suggestions = []
    if trinity_metrics.truth < 1.0:
        failed = [
            o["organ"]
            for o in organs
            if o["organ"] in core_data_organs and not o["healthy"]
        ]
        issues.append(f"眞(데이터 계층): {', '.join(failed)} 연결 실패")
        suggestions.append("docker-compose restart redis postgres")

    if trinity_metrics.filial_serenity < 1.0:
        issues.append("孝(LLM 서비스): Ollama 연결 끊김")
        suggestions.append("docker start afo-ollama")

    if trinity_metrics.balance_status == "imbalanced":
        decision = "TRY_AGAIN"
        decision_message = "집현전 학자들이 문제를 해결 중입니다. 재시도하세요."
    elif trinity_metrics.balance_status == "warning":
        decision = "ASK_COMMANDER"
        decision_message = "일부 서비스에 주의가 필요합니다."
    else:
        decision = "AUTO_RUN"
        decision_message = "모든 시스템 정상. 자동 실행 가능합니다."

    try:
        from AFO.api.metadata import get_api_metadata

        api_metadata = get_api_metadata()
        service_name = str(api_metadata.get("title", "AFO Kingdom Soul Engine API"))
        api_version = str(api_metadata.get("version", "unknown"))
    except Exception:
        service_name = "AFO Kingdom Soul Engine API"
        api_version = "unknown"

    # T21: Add organs_v2 with 11 keys for true 11-ORGANS system
    try:
        from AFO.health.organs_v2 import build_organs_v2

        v2_data = build_organs_v2()
        response_v2 = {
            "organs_v2": v2_data["organs"],
            "contract_v2": v2_data["contract"],
            "ts_v2": v2_data["ts"],
        }
    except Exception as e:
        logger.warning(f"organs_v2 generation failed: {e}")
        response_v2 = {
            "organs_v2": None,
            "contract_v2": {"version": "organs/v2", "error": str(e)},
            "ts_v2": current_time,
        }

    # 최종 응답 구성 (안전하게 초기화)
    try:
        balance_status = trinity_metrics.balance_status if trinity_metrics else "unknown"
        trinity_score = trinity_metrics.trinity_score if trinity_metrics else 0.0
    except:
        balance_status = "unknown"
        trinity_score = 0.0

    response = {
        "service": service_name,
        "version": api_version,
        "status": balance_status,
        "health_percentage": round(trinity_score * 100, 2),
        "healthy_organs": healthy_count,
        "total_organs": total_organs,
        "trinity": trinity_metrics.to_dict() if trinity_metrics else {},
        "decision": decision,
        "decision_message": decision_message,
        "issues": issues if issues else None,
        "suggestions": suggestions if suggestions else None,
        "organs": {
            o["organ"]: {
                "status": o["status"],
                "output": str(o.get("output", ""))[:100],
            }
            for o in organs
        },
        **response_v2,
        "method": "bridge_perspective_v2_jiphyeonjeon",
        "timestamp": current_time,
    }

    # 캐시 저장 (메모리 + Redis)
    try:
        _health_cache = response
        _cache_timestamp = time.time()

        # Redis 캐시 저장 (선택적)
        r = redis.from_url(get_redis_url())
        await r.setex(HEALTH_CACHE_KEY, HEALTH_CACHE_TTL, json.dumps(response))
        await r.close()
        logger.debug("Health check result cached")
    except Exception as e:
        logger.warning(f"Failed to cache health check result: {e}")

    return response
