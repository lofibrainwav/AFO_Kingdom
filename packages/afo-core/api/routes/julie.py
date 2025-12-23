# packages/afo-core/api/routes/julie.py
# PDF 페이지 2: FastAPI 엔드포인트, 페이지 3: 권한 검증
from typing import Any

from AFO.julie_cpa.services.julie_service import JulieService
from fastapi import APIRouter

router = APIRouter(prefix="/api/julie", tags=["Julie CPA"])

# Singleton Instance (Goodness: Centralized Logic)
julie = JulieService()


@router.get("/status")
async def julie_status() -> dict[str, Any]:
    """형님께 드리는 3줄 요약 (PDF 페이지 2: 겸손 프로토콜)"""
    status_data = await julie.get_royal_status()
    # alerts = await julie.risk_alert() # Legacy
    # advice = await julie.personalized_advice() # Legacy

    # Simple transaction dry run check (using mock data)
    # txs = await julie.ingest_transactions("mock_bank")

    return {
        "status": status_data["status"],
        "alerts": status_data["alerts"],
        "advice": status_data["advice"],
        "dry_run_tx_count": status_data["dry_run_tx_count"],
    }
