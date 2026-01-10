# Trinity Score: 90.0 (Established by Chancellor)
"""AFO Audit Module (眞善美孝永)

Stub module for audit middleware to unblock Gate.
Full implementation pending TICKET-XXX.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = logging.getLogger(__name__)


async def audit_middleware(request, call_next):
    """Audit middleware stub - passes through without logging.

    TODO: Implement full audit trail functionality.
    """
    return await call_next(request)


def setup_audit(app: FastAPI) -> None:
    """Setup audit middleware on FastAPI app.

    Args:
        app: FastAPI application instance
    """
    logger.info("Audit middleware stub initialized (full impl pending)")


__all__ = ["audit_middleware", "setup_audit"]
