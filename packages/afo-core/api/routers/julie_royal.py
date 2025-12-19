from AFO.julie_cpa.services.julie_service import JulieService
from fastapi import APIRouter

# [Legacy Merger]
# This router exposes the same endpoints as the legacy 'julie.py'
# but powers them with the new 'JulieService' (Royal Edition).

router = APIRouter(prefix="/api/julie", tags=["Julie CPA (Royal)"])
julie_service = JulieService()


@router.get("/status")
async def get_status():
    """
    Legacy-compatible Status Endpoint.
    Used by: AICPA Julie Frontend (Port 3000)
    """
    return await julie_service.get_royal_status()


@router.get("/dashboard")
async def get_dashboard():
    """
    [GenUI Support]
    Full Financial Dashboard Data (Health, Alerts, Tx).
    """
    return await julie_service.get_financial_dashboard()
