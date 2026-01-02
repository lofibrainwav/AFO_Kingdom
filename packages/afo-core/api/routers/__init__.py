# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO API Routers
Phase 2 리팩토링: 라우터 분리
"""

from AFO.health import import router as health_router
from AFO.root import import router as root_router

__all__ = ["health_router", "root_router"]
