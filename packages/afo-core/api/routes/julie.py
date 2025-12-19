# packages/afo-core/api/routes/julie.py
# PDF 페이지 2: FastAPI 엔드포인트, 페이지 3: 권한 검증
from fastapi import APIRouter

from julie_cpa.core.julie_engine import julie

router = APIRouter(prefix="/api/julie", tags=["Julie CPA"])


@router.get("/status")
async def julie_status():
    """형님께 드리는 3줄 요약 (PDF 페이지 2: 겸손 프로토콜)"""
    alerts = await julie.risk_alert()
    advice = await julie.personalized_advice()

    # Simple transaction dry run check
    txs = await julie.ingest_transactions("mock_bank")

    return {
        "status": "의(義)의 엔진 활성화",
        "alerts": alerts or ["✅ 모든 재정 안정"],
        "advice": advice,
        "dry_run_tx_count": len(txs),
    }
