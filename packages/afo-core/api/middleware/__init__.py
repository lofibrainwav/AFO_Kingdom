# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Kingdom API Middleware Package (眞善美孝永)

Trinity Score 기반 아름다운 코드로 구현된 미들웨어 패키지.
시스템의 안정성과 관측성을 보장하기 위한 미들웨어 관리 기능을 제공합니다.
"""

from __future__ import annotations

import logging

from .audit import audit_middleware
from .prometheus import PrometheusMiddleware, metrics_endpoint
from .setup import setup_middleware

# Configure logging
logger = logging.getLogger(__name__)

__all__ = [
    "PrometheusMiddleware",
    "audit_middleware",
    "metrics_endpoint",
    "setup_middleware",
]

logger.info("AFO Kingdom Middleware Package initialized with beautiful code principles")
