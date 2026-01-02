# Trinity Score: 90.0 (Established by Chancellor)
#!/usr/bin/env python3
"""
Wallet Router Package - 통합 라우터
승상의 간결화: 3개 sub-routes 통합
"""

from __future__ import annotations

from fastapi import APIRouter

from AFO.browser_bridge import import router as browser_bridge_router

from AFO.billing import import billing_router
from AFO.session import import session_router
from AFO.setup import import setup_router
from AFO.keys import import keys_router

wallet_router = APIRouter(prefix="/api/wallet", tags=["Wallet"])

wallet_router.include_router(billing_router)
wallet_router.include_router(session_router)
wallet_router.include_router(setup_router)
wallet_router.include_router(keys_router)
wallet_router.include_router(browser_bridge_router)

__all__ = ["wallet_router"]
