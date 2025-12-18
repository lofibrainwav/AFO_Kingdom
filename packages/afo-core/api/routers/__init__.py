"""
AFO API Routers
Phase 2 리팩토링: 라우터 분리
"""

from .health import router as health_router
from .root import router as root_router

__all__ = ["health_router", "root_router"]
