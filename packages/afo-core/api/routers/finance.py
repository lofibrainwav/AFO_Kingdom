import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from AFO.julie_cpa.services.julie_service import JulieService

router = APIRouter(prefix="/api/finance", tags=["finance"])
logger = logging.getLogger(__name__)


# --- Dependencies ---
def get_julie_service() -> JulieService:
    return JulieService()


# --- Models ---
class TransactionRequest(BaseModel):
    account_id: str
    merchant: str
    amount: float
    currency: str = "KRW"
    category: str
    description: str | None = None


class DryRunResponse(BaseModel):
    success: bool
    mode: str
    friction_score: float
    reason: str | None = None


class FinanceDashboardResponse(BaseModel):
    financial_health_score: float
    monthly_spending: float
    budget_remaining: float
    recent_transactions: list[dict]
    risk_alerts: list[dict]
    advice: str


# --- Routes ---


@router.get("/dashboard", response_model=FinanceDashboardResponse)
async def get_finance_dashboard(julie: JulieService = Depends(get_julie_service)):
    """
    Get the Financial Guardian Dashboard data.
    """
    try:
        return await julie.get_financial_dashboard()
    except Exception as e:
        logger.error(f"Julie Dashboard Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transaction/dry-run", response_model=DryRunResponse)
async def dry_run_transaction(
    tx: TransactionRequest, julie: JulieService = Depends(get_julie_service)
):
    """
    Simulate a transaction to check against Friction (Warfare Deception).
    """
    try:
        # Convert Pydantic model to dict
        request_data = tx.dict()
        # Ensure transaction_id is present if required by model, or generate one
        if "transaction_id" not in request_data:
            import uuid

            request_data["transaction_id"] = str(uuid.uuid4())
            request_data["timestamp"] = "2024-01-01T00:00:00"  # Mock timestamp for dry run

        result = await julie.process_transaction(
            request_data=request_data, account_id=tx.account_id, dry_run=True
        )

        return {
            "success": result["success"],
            "mode": result.get("mode", "UNKNOWN"),
            "friction_score": result.get("friction_score", 0.0),
            "reason": result.get("reason"),
        }
    except Exception as e:
        logger.error(f"Julie Dry Run Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
