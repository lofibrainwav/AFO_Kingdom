"""
Root Router
Phase 2 리팩토링: Root 엔드포인트 분리
Phase 3: 타입 힌트 강화
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter(tags=["Root"])


@router.get("/")
async def read_root() -> dict[str, Any]:
    """
    Root endpoint - Expose API metadata for dashboards and automated checks.

    Returns:
        dict[str, Any]: API 메타데이터 (name, version, status, message)
    """
    try:
        from config.settings import get_settings

        settings = get_settings()
        version: str = settings.AFO_API_VERSION
    except ImportError:
        try:
            from AFO.config.settings import get_settings

            settings = get_settings()
            version = settings.AFO_API_VERSION
        except ImportError:
            version = "v1"

    return {
        "name": "AFO Soul Engine API",
        "version": version,
        "status": "operational",
        "message": "AFO Ultimate General Command Post is operational!",
    }
