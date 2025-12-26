# Trinity Score: 90.0 (Established by Chancellor)
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
    return await julie_service.calculate_tax_scenario(
        request.income, request.filing_status
    )


class TransactionRequest(BaseModel):
    account_id: str
    merchant: str
    amount: float
    category: str
    date: str
    dry_run: bool = False


@router.post("/transaction")
async def process_transaction(request: TransactionRequest) -> dict[str, Any]:
    """
    [Action Endpoint]
    Trigger a financial transaction (or simulation).
    Emits thoughts to the Neural Stream (ToT).
    """
    return await julie_service.process_transaction(
        request_data={
            "transaction_id": f"tx-{request.merchant.lower()}-001",
            "merchant": request.merchant,
            "amount": request.amount,
            "category": request.category,
            "date": request.date,
        },
        account_id=request.account_id,
        dry_run=request.dry_run,
    )


@router.post("/transaction/approve")
async def approve_transaction(tx_id: str) -> dict[str, Any]:
    """
    [T26] Transaction Approval Action
    """
    # In Phase 2, this would trigger actual bank transfer or DB update.
    # For now, we simulate approval.
    return {
        "success": True,
        "message": f"Transaction {tx_id} approved",
        "tx_id": tx_id,
        "status": "APPROVED",
    }
