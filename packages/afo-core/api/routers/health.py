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
    Refactored to use centralized health_service.
    """
    try:
        from AFO.services.health_service import get_comprehensive_health
        return await get_comprehensive_health()
    except Exception as e:
        return {"status": "error", "message": f"Health check failed: {str(e)}"}
