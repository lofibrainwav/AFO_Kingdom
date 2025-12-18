"""
Health Check Router
Phase 2 리팩토링: Health 엔드포인트 분리
"""

from typing import Any

from fastapi import APIRouter

# Phase 2 리팩토링: 상대 import 사용
try:
    from AFO.services.database import get_db_connection
    from AFO.utils.redis_connection import get_redis_url
except ImportError:
    # Fallback for local execution
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check() -> dict[str, Any]:
    """
    시스템 건강 상태 체크 (11-Organ Health Monitoring)
    Returns: {"status": "balanced", "health_percentage": 100.0, "organs": {...}}
    """
    # api_server.py의 health_check_legacy 함수를 재사용
    # 실제 구현은 api_server.py에 있음
    from datetime import datetime

    import httpx
    import redis.asyncio as redis

    current_time = datetime.now().isoformat()
    organs: list[dict] = []

    # === 실제 서비스 체크 함수들 ===
    async def check_redis() -> dict:
        try:
            from AFO.utils.redis_connection import get_redis_url

            r = redis.from_url(get_redis_url())
            pong = await r.ping()
            await r.close()
            return {"healthy": pong, "output": f"PING -> {pong}"}
        except Exception as e:
            return {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    async def check_postgres() -> dict:
        try:
            from AFO.services.database import get_db_connection

            conn = await get_db_connection()
            result = await conn.fetchval("SELECT 1")
            await conn.close()
            return {"healthy": result == 1, "output": f"SELECT 1 -> {result}"}
        except Exception as e:
            return {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    async def check_ollama() -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                from AFO.config.settings import get_settings

                ollama_url = get_settings().OLLAMA_BASE_URL
                resp = await client.get(ollama_url + "/api/tags")
                data = resp.json()
                model_count = len(data.get("models", []))
                return {"healthy": model_count > 0, "output": f"Models: {model_count}"}
        except Exception as e:
            return {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    async def check_self() -> dict:
        return {"healthy": True, "output": "Self-check: API responding"}

    # === 병렬 실행 ===
    import asyncio

    results = await asyncio.gather(
        check_redis(), check_postgres(), check_ollama(), check_self(), return_exceptions=True
    )

    organ_checks = [
        (
            "心_Redis",
            results[0]
            if not isinstance(results[0], Exception)
            else {"healthy": False, "output": str(results[0])},
        ),
        (
            "肝_PostgreSQL",
            results[1]
            if not isinstance(results[1], Exception)
            else {"healthy": False, "output": str(results[1])},
        ),
        (
            "脾_Ollama",
            results[2]
            if not isinstance(results[2], Exception)
            else {"healthy": False, "output": str(results[2])},
        ),
        (
            "肺_API_Server",
            results[3]
            if not isinstance(results[3], Exception)
            else {"healthy": False, "output": str(results[3])},
        ),
    ]

    for organ_name, result in organ_checks:
        organs.append(
            {
                "organ": organ_name,
                "healthy": result["healthy"],
                "status": "healthy" if result["healthy"] else "unhealthy",
                "output": result["output"],
                "timestamp": current_time,
            }
        )

    # === 眞善美孝永 5기둥 계산 ===
    healthy_count = sum(1 for o in organs if o["healthy"])
    total_organs = len(organs)

    # Trinity 계산 (간단한 버전)
    trinity_score = healthy_count / total_organs if total_organs > 0 else 0.0

    return {
        "status": "balanced" if trinity_score >= 0.8 else "imbalanced",
        "health_percentage": round(trinity_score * 100, 2),
        "healthy_organs": healthy_count,
        "total_organs": total_organs,
        "organs": {
            o["organ"]: {"status": o["status"], "output": str(o.get("output", ""))[:100]}
            for o in organs
        },
        "timestamp": current_time,
    }
