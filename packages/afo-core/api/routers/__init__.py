# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO API Routers
Phase 2 리팩토링: 라우터 분리
"""

from .health import router as health_router
from .rag_query import router as rag_query_router
from .root import router as root_router

__all__ = ["health_router", "root_router", "rag_query_router"]
