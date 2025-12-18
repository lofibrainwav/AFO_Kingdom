from __future__ import annotations

# Re-export: canonical implementation lives in `api.routes.system_health`.
from api.routes.system_health import router

__all__ = ["router"]

