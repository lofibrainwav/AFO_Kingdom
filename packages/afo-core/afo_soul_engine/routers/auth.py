from __future__ import annotations

from fastapi import APIRouter

try:
    # Prefer the canonical implementation if present.
    from AFO.api.routers.auth import router as router  # type: ignore
except Exception:
    router = APIRouter(prefix="/api/auth", tags=["Auth"])

    @router.get("/health")
    async def auth_health() -> dict[str, str]:
        return {
            "status": "degraded",
            "message": "Auth router fallback (no backing store connected)",
        }
