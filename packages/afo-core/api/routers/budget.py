"""
AFO Julie CPA - Budget API Router
Phase 12 Extension: 실시간 예산 추적 및 리스크 알림

"금고 안전! Julie CPA가 왕국 부를 지켜요" 🛡️💰
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from AFO.julie_cpa.models.budget import (
    BudgetCategory,
    BudgetSummary,
    BudgetUpdate,
    MOCK_BUDGETS,
)

router = APIRouter(prefix="/api/julie/budget", tags=["Julie CPA - Budget"])
logger = logging.getLogger(__name__)


def calculate_risk_score(total_remaining: int, total_allocated: int) -> tuple[float, str]:
    """
    SSOT 연동 리스크 점수 계산
    
    善 (Goodness): 예산 잔여율에 따른 리스크 평가
    - 잔여율 > 30%: safe (risk 0-5)
    - 잔여율 20-30%: warning (risk 6-10)
    - 잔여율 < 20%: critical (risk 11-20)
    """
    if total_allocated == 0:
        return 0.0, "safe"
    
    remaining_rate = (total_remaining / total_allocated) * 100
    
    if remaining_rate >= 30:
        risk = 5.0 - (remaining_rate - 30) * 0.1  # 잔여 많을수록 낮은 리스크
        risk = max(0.0, min(5.0, risk))
        return risk, "safe"
    elif remaining_rate >= 20:
        risk = 6.0 + (30 - remaining_rate) * 0.4
        return min(10.0, risk), "warning"
    else:
        risk = 11.0 + (20 - remaining_rate) * 0.5
        return min(20.0, risk), "critical"


def generate_summary(risk_level: str, utilization_rate: float) -> str:
    """Julie의 한줄 평가 생성"""
    if risk_level == "safe":
        return f"✅ 예산 안정 – 사용률 {utilization_rate:.1f}%, Julie CPA 감시 중 🛡️"
    elif risk_level == "warning":
        return f"⚠️ 주의! 예산 {utilization_rate:.1f}% 사용 – 지출 조절 권장"
    else:
        return f"🚨 경고! 예산 {utilization_rate:.1f}% 소진 – 긴급 검토 필요"


@router.get("", response_model=BudgetSummary)
async def get_budget_summary():
    """
    예산 현황 조회
    
    Returns:
        BudgetSummary: 전체 예산 현황 및 리스크 점수
    """
    total_allocated = sum(b.allocated for b in MOCK_BUDGETS)
    total_spent = sum(b.spent for b in MOCK_BUDGETS)
    total_remaining = sum(b.remaining for b in MOCK_BUDGETS)
    
    utilization_rate = (total_spent / total_allocated * 100) if total_allocated > 0 else 0.0
    risk_score, risk_level = calculate_risk_score(total_remaining, total_allocated)
    
    return BudgetSummary(
        budgets=MOCK_BUDGETS,
        total_allocated=total_allocated,
        total_spent=total_spent,
        total_remaining=total_remaining,
        utilization_rate=round(utilization_rate, 2),
        risk_score=round(risk_score, 2),
        risk_level=risk_level,
        summary=generate_summary(risk_level, utilization_rate),
        timestamp=datetime.now().isoformat(),
    )


@router.get("/category/{category_name}")
async def get_category_budget(category_name: str):
    """특정 카테고리 예산 조회"""
    for budget in MOCK_BUDGETS:
        if budget.category.lower() == category_name.lower():
            return budget
    raise HTTPException(status_code=404, detail=f"카테고리 '{category_name}' 없음")


class SpendRequest(BaseModel):
    category: str
    amount: int
    description: Optional[str] = None
    dry_run: bool = True


@router.post("/spend")
async def record_spending(request: SpendRequest):
    """
    지출 기록 (DRY_RUN 기본)
    
    善 (Goodness): 안전 우선 - dry_run=True가 기본값
    """
    for budget in MOCK_BUDGETS:
        if budget.category.lower() == request.category.lower():
            new_spent = budget.spent + request.amount
            new_remaining = budget.allocated - new_spent
            
            # 리스크 체크
            if new_remaining < 0:
                return {
                    "success": False,
                    "mode": "DRY_RUN" if request.dry_run else "BLOCKED",
                    "reason": f"예산 초과! 잔여: ₩{budget.remaining:,}, 요청: ₩{request.amount:,}",
                    "suggestion": "예산 재할당 또는 지출 조정 필요",
                }
            
            if request.dry_run:
                return {
                    "success": True,
                    "mode": "DRY_RUN",
                    "preview": {
                        "category": budget.category,
                        "current_spent": budget.spent,
                        "new_spent": new_spent,
                        "new_remaining": new_remaining,
                    },
                    "message": "시뮬레이션 완료 – dry_run=False로 실제 반영",
                }
            else:
                # 실제 반영
                budget.spent = new_spent
                budget.calculate_remaining()
                logger.info(f"[Julie] 지출 기록: {request.category} +₩{request.amount:,}")
                return {
                    "success": True,
                    "mode": "EXECUTED",
                    "updated": budget.dict(),
                    "message": f"지출 기록 완료: {request.description or '(설명 없음)'}",
                }
    
    raise HTTPException(status_code=404, detail=f"카테고리 '{request.category}' 없음")


@router.get("/risk-alert")
async def get_risk_alerts():
    """
    리스크 알림 조회
    
    SSOT 연동: 위험 카테고리만 반환
    """
    alerts = []
    
    for budget in MOCK_BUDGETS:
        utilization = (budget.spent / budget.allocated * 100) if budget.allocated > 0 else 0
        
        if utilization >= 80:
            level = "critical" if utilization >= 90 else "warning"
            alerts.append({
                "level": level,
                "category": budget.category,
                "utilization": round(utilization, 1),
                "remaining": budget.remaining,
                "message": f"🚨 {budget.category}: {utilization:.1f}% 사용 (잔여 ₩{budget.remaining:,})",
            })
    
    return {
        "count": len(alerts),
        "alerts": alerts,
        "summary": "금고 문제? Julie가 자동 복구 중 – 조금만 기다려주세요!" if alerts else "✅ 모든 예산 안정",
    }
