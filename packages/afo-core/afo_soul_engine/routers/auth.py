# Trinity Score: 90.0 (Established by Chancellor)
from __future__ import annotations

from fastapi import APIRouter

try:
    # Prefer the canonical implementation if present.
    # [논어] 군자화이부동 - 조화롭되 다름을 인정함
    from afo.api.routers.auth import router as router
except Exception:
    router = APIRouter(prefix="/api/auth", tags=["Auth"])

    @router.get("/health")
    async def auth_health() -> dict[str, str]:
        return {
            "status": "degraded",
            "message": "Auth router fallback (no backing store connected)",
        }
