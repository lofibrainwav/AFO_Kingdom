# Trinity Score: 90.0 (Established by Chancellor)
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

    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

router = APIRouter(prefix="/health", tags=["Health"])

# Comprehensive Health Check 통합
try:
    from AFO.api.routes.comprehensive_health import (
        router as comprehensive_health_router,
    )

    # comprehensive_health_router는 이미 prefix="/api/health"를 가지고 있으므로
    # health_router에 직접 통합하면 경로가 중복될 수 있음
    # 대신 api_server.py에서 별도로 등록하는 것이 좋음
    # 여기서는 주석 처리하고 api_server.py에서 처리
    # router.include_router(comprehensive_health_router)
except ImportError:
    pass  # comprehensive_health가 없어도 기본 health check는 작동


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
        return {"status": "error", "message": f"Health check failed: {e!s}"}
