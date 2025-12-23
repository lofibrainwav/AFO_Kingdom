from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from AFO.julie_cpa.services.julie_service import JulieService

# [Legacy Merger]
# This router exposes the same endpoints as the legacy 'julie.py'
# but powers them with the new 'JulieService' (Royal Edition).

router = APIRouter(prefix="/api/julie", tags=["Julie CPA (Royal)"])
julie_service = JulieService()


@router.get("/status")
async def get_status() -> dict[str, Any]:
    """
    Legacy-compatible Status Endpoint.
    Used by: AICPA Julie Frontend (Port 3000)
    """
    return await julie_service.get_royal_status()


@router.get("/dashboard")
async def get_dashboard() -> dict[str, Any]:
    """
    [GenUI Support]
    Full Financial Dashboard Data (Health, Alerts, Tx).
    """
    return await julie_service.get_financial_dashboard()


class TaxCalcRequest(BaseModel):
    income: float
    filing_status: str = "single"


@router.post("/calculate-tax")
async def calculate_tax(request: TaxCalcRequest) -> dict[str, Any]:
    """
    [Operation Gwanggaeto]
    Performs real-time tax simulation (Federal + CA + QBI).
    Source: JuliePerplexity Report (2025 Rules).
    """
    return await julie_service.calculate_tax_scenario(request.income, request.filing_status)
