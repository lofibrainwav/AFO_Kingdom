from __future__ import annotations

from fastapi import APIRouter

try:
    from AFO.api.routers.users import router as router  # type: ignore
except Exception:
    router = APIRouter(prefix="/api/users", tags=["Users"])

    @router.get("/health")
    async def users_health() -> dict[str, str]:
        return {
            "status": "degraded",
            "message": "Users router fallback (no persistence connected)",
        }
