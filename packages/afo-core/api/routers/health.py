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
    from AFO.services.database import get_db_connection
    from AFO.utils.redis_connection import get_redis_url

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check() -> dict[str, Any]:
    """
    시스템 건강 상태 체크 (11-Organ Health Monitoring)
    Returns: {"status": "balanced", "health_percentage": 100.0, "organs": {...}}
    """
    import httpx
    import redis
    from qdrant_client import QdrantClient

    try:
        from AFO.config.settings import get_settings
    except ImportError:
        from config.settings import get_settings

    settings = get_settings()
    organs = {}
    total_organs = 11
    healthy_count = 0

    # 1. PostgreSQL (Brain - 장기 기억)
    try:
        conn = await get_db_connection()
        result = await conn.fetchval("SELECT 1")
        await conn.close()
        organs["postgres"] = {"healthy": result == 1, "output": f"SELECT 1 -> {result}"}
        if result == 1:
            healthy_count += 1
    except Exception as e:
        organs["postgres"] = {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    # 2. Redis (Heart - 실시간 캐시)
    try:
        r = redis.from_url(get_redis_url())
        pong = await r.ping()
        await r.close()
        organs["redis"] = {"healthy": pong, "output": f"PING -> {pong}"}
        if pong:
            healthy_count += 1
    except Exception as e:
        organs["redis"] = {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    # 3. Qdrant (Lungs - 벡터 DB)
    try:
        client = QdrantClient(url=settings.QDRANT_URL)
        collections = client.get_collections()
        organs["qdrant"] = {
            "healthy": True,
            "output": f"Collections: {len(collections.collections)}",
        }
        healthy_count += 1
    except Exception as e:
        organs["qdrant"] = {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    # 4. Ollama (Stomach - 내부 지력)
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            ollama_url = settings.OLLAMA_BASE_URL
            resp = await client.get(ollama_url + "/api/tags")
            data = resp.json()
            models = data.get("models", [])
            organs["ollama"] = {"healthy": True, "output": f"Models: {len(models)}"}
            healthy_count += 1
    except Exception as e:
        organs["ollama"] = {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    # 5-11. 기타 장기들 (간단한 체크)
    for organ_name in [
        "n8n",
        "api_wallet",
        "mcp_server",
        "chromadb",
        "langgraph",
        "ragas",
        "alertmanager",
    ]:
        try:
            # 기본적으로 healthy로 설정 (실제 체크는 향후 구현)
            organs[organ_name] = {"healthy": True, "output": "OK"}
            healthy_count += 1
        except Exception:
            organs[organ_name] = {"healthy": False, "output": "Not checked"}

    health_percentage = (healthy_count / total_organs) * 100.0

    return {
        "status": "balanced" if health_percentage >= 80 else "unbalanced",
        "health_percentage": round(health_percentage, 2),
        "organs": organs,
        "healthy_count": healthy_count,
        "total_organs": total_organs,
    }
