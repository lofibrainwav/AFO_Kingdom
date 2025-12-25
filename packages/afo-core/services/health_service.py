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
    from AFO.api.compat import TrinityMetrics

logger = logging.getLogger(__name__)


async def check_redis() -> dict[str, Any]:
    """心_Redis 상태 체크"""
    try:
        r = redis.from_url(get_redis_url())
        pong = await r.ping()
        await r.close()
        return {"healthy": pong, "output": f"PING -> {pong}"}
    except Exception as e:
        return {"healthy": False, "output": f"Error: {str(e)[:50]}"}


async def check_postgres() -> dict[str, Any]:
    """肝_Postgres 상태 체크"""
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


async def get_comprehensive_health() -> dict[str, Any]:
    """종합 건강 상태 진단 및 Trinity Score 계산"""
    current_time = datetime.now().isoformat()

    # 병렬 실행
    results = await asyncio.gather(
        check_redis(),
        check_postgres(),
        check_ollama(),
        check_self(),
        return_exceptions=True,
    )

    organ_names = ["心_Redis", "肝_PostgreSQL", "脾_Ollama", "肺_API_Server"]
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

    return {
        "status": trinity_metrics.balance_status,
        "health_percentage": round(trinity_metrics.trinity_score * 100, 2),
        "healthy_organs": healthy_count,
        "total_organs": total_organs,
        "trinity": trinity_metrics.to_dict(),
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
        "method": "bridge_perspective_v2_jiphyeonjeon",
        "timestamp": current_time,
    }
