# Trinity Score: 90.0 (Established by Chancellor)
from AFO.api.routers.finance import (FinanceDashboardResponse, JulieService,
                                     get_finance_dashboard, get_julie_service)
from fastapi import APIRouter, Depends, HTTPException

# Separate router without prefix, or specific path
router = APIRouter(tags=["finance_root"])


@router.get("/finance/dashboard")
async def get_finance_dashboard_root(
    julie: JulieService = Depends(get_julie_service),
):
    """Alias for /api/finance/dashboard to support root-level access."""
    return await get_finance_dashboard(julie)


from pydantic import BaseModel


class TaxRequest(BaseModel):
    income: float
    filing_status: str


@router.post("/api/julie/calculate-tax")
async def calculate_tax(
    req: TaxRequest,
    julie: JulieService = Depends(get_julie_service),
):
    """Calculate tax scenario for Julie Tax Widget."""
    result = await julie.calculate_tax_scenario(req.income, req.filing_status)
    return result
