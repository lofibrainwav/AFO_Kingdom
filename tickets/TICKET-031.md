# 🎫 TICKET-031: AICPA/Tax AI 실전 배포 - Julie CPA 세금 시뮬레이션 위젯 구현

**우선순위**: HIGH
**상태**: PENDING
**담당**: 승상 + AI팀
**의존성**: TICKET-030 (DSPy MIPROv2 완성)
**예상 소요시간**: 20시간

## 🎯 목표 (Goal)

Julie CPA 세금 시뮬레이션 위젯을 AFO 왕국에 실전 배포하여 전문 도메인 AI 적용 사례 구축.

## 📋 작업 내용

### 1. 세금 계산 엔진 구현 (Tax Engine Core)
```python
# packages/afo-core/afo/tax_engine.py
class TaxEngine:
    """연방 + 캘리포니아 세금 계산 엔진"""

    def __init__(self):
        self.federal_brackets_2025 = {
            "single": [
                (0, 11600, 0.10),      # 10%
                (11600, 47150, 0.12),  # 12%
                (47150, 100525, 0.22), # 22%
                # ... 2025 최신 세율
            ]
        }
        self.ca_brackets_2025 = {
            "single": [
                (0, 10099, 0.01),      # 1%
                (10099, 23942, 0.02),  # 2%
                # ... 9브래킷 + Mental Health 1% 추가세
            ]
        }

    def calculate_federal_tax(self, taxable_income: float, filing_status: str) -> float:
        """연방 소득세 계산"""
        brackets = self.federal_brackets_2025.get(filing_status, self.federal_brackets_2025["single"])
        return self._calculate_bracket_tax(taxable_income, brackets)

    def calculate_ca_tax(self, taxable_income: float, filing_status: str) -> float:
        """캘리포니아 주세 계산 + Mental Health surtax"""
        base_tax = self._calculate_bracket_tax(
            taxable_income,
            self.ca_brackets_2025.get(filing_status, self.ca_brackets_2025["single"])
        )

        # Mental Health Services 1% surtax (> $1M taxable)
        if taxable_income > 1000000:
            mental_health_tax = (taxable_income - 1000000) * 0.01
            return base_tax + mental_health_tax

        return base_tax
```

### 2. Julie CPA 위젯 API 구현
```python
# packages/afo-core/api/routes/tax.py
from fastapi import APIRouter
from pydantic import BaseModel
from afo.tax_engine import TaxEngine

router = APIRouter(prefix="/tax", tags=["Tax Simulation"])

class TaxCalculationRequest(BaseModel):
    filing_status: str = "single"
    gross_income: float
    deductions: float = 0
    credits: float = 0
    state: str = "CA"
    retirement_contributions: float = 0
    self_employment_income: float = 0

class TaxCalculationResponse(BaseModel):
    federal_tax: float
    state_tax: float
    total_tax: float
    effective_rate: float
    net_income: float
    marginal_rate: float

@router.post("/calculate", response_model=TaxCalculationResponse)
async def calculate_tax(request: TaxCalculationRequest):
    """세금 계산 API"""
    engine = TaxEngine()

    # AGI 계산
    agi = request.gross_income - request.retirement_contributions

    # 표준공제 적용 (2025)
    standard_deduction = 15750 if request.filing_status == "single" else 31500
    taxable_income = max(0, agi - standard_deduction - request.deductions)

    # QBI 공제 (단순화)
    qbi_deduction = min(taxable_income * 0.20, 100000)  # 임시 값
    taxable_income -= qbi_deduction

    # 세금 계산
    federal_tax = engine.calculate_federal_tax(taxable_income, request.filing_status)
    state_tax = engine.calculate_ca_tax(taxable_income, request.filing_status)

    total_tax = federal_tax + state_tax - request.credits
    net_income = request.gross_income - total_tax
    effective_rate = (total_tax / request.gross_income) * 100 if request.gross_income > 0 else 0

    # Marginal rate (단순화)
    marginal_rate = 0.22  # 임시 값

    return TaxCalculationResponse(
        federal_tax=round(federal_tax, 2),
        state_tax=round(state_tax, 2),
        total_tax=round(total_tax, 2),
        effective_rate=round(effective_rate, 2),
        net_income=round(net_income, 2),
        marginal_rate=round(marginal_rate * 100, 2)
    )
```

### 3. DSPy MIPROv2 통합 절세 조언
```python
# packages/afo-core/afo/tax_advisor.py
from afo.api.routes.dspy import MIPROv2Optimizer

class TaxAdvisor:
    """DSPy MIPROv2 기반 세무 조언 엔진"""

    def __init__(self):
        self.optimizer = MIPROv2Optimizer()

    async def get_tax_advice(self, tax_data: dict) -> list[str]:
        """절세 조언 생성"""
        task = f"""
        Analyze this tax situation and provide 3 specific tax-saving recommendations:
        - Filing Status: {tax_data.get('filing_status', 'single')}
        - Gross Income: ${tax_data.get('gross_income', 0):,}
        - Effective Tax Rate: {tax_data.get('effective_rate', 0):.1f}%
        - State: {tax_data.get('state', 'CA')}

        Focus on retirement contributions, deductions, and tax credits.
        """

        # DSPy MIPROv2로 최적화된 조언 생성
        dataset = [
            {"question": "What tax-saving strategies should I consider?", "answer": "Maximize retirement contributions and itemize deductions if beneficial."},
            {"question": "How can I reduce my effective tax rate?", "answer": "Contribute to tax-advantaged accounts and consider tax-loss harvesting."}
        ]

        # API 호출 시뮬레이션
        advice_request = {
            "task": task,
            "dataset": dataset,
            "num_candidates": 3,
            "max_bootstrapped_demos": 2,
            "num_trials": 5
        }

        # 실제로는 API 호출
        # response = await self.optimizer.optimize_with_mipro(advice_request)

        # 임시 응답
        return [
            f"Contribute up to $23,000 to 401(k) to reduce taxable income by ${min(tax_data.get('gross_income', 0) * 0.22, 23000 * 0.22):,.0f}",
            "Consider converting traditional IRA to Roth IRA if in lower tax bracket",
            "Maximize HSA contributions ($4,150 single/$8,300 family) for triple tax benefits"
        ]
```

### 4. 대시보드 컴포넌트 통합
```typescript
// packages/dashboard/src/components/TaxCalculatorCard.tsx
'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Slider } from '@/components/ui/slider'

interface TaxData {
  federal_tax: number
  state_tax: number
  total_tax: number
  effective_rate: number
  net_income: number
  marginal_rate: number
}

export function TaxCalculatorCard() {
  const [grossIncome, setGrossIncome] = useState(75000)
  const [deductions, setDeductions] = useState(0)
  const [retirement, setRetirement] = useState(0)
  const [taxData, setTaxData] = useState<TaxData | null>(null)
  const [loading, setLoading] = useState(false)

  const calculateTax = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/tax/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          gross_income: grossIncome,
          deductions: deductions,
          retirement_contributions: retirement,
          filing_status: 'single',
          state: 'CA'
        })
      })
      const data = await response.json()
      setTaxData(data)
    } catch (error) {
      console.error('Tax calculation failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Julie CPA Tax Calculator</CardTitle>
        <p className="text-sm text-muted-foreground">
          2025 Federal + California Tax Simulation
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-sm font-medium">Gross Income</label>
            <Input
              type="number"
              value={grossIncome}
              onChange={(e) => setGrossIncome(Number(e.target.value))}
              placeholder="75000"
            />
          </div>
          <div>
            <label className="text-sm font-medium">Additional Deductions</label>
            <Input
              type="number"
              value={deductions}
              onChange={(e) => setDeductions(Number(e.target.value))}
              placeholder="0"
            />
          </div>
          <div>
            <label className="text-sm font-medium">Retirement Contributions</label>
            <Input
              type="number"
              value={retirement}
              onChange={(e) => setRetirement(Number(e.target.value))}
              placeholder="0"
            />
          </div>
        </div>

        <Button onClick={calculateTax} disabled={loading} className="w-full">
          {loading ? 'Calculating...' : 'Calculate Tax'}
        </Button>

        {taxData && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="font-semibold">Tax Breakdown</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Federal Tax:</span>
                  <span>${taxData.federal_tax.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span>State Tax:</span>
                  <span>${taxData.state_tax.toLocaleString()}</span>
                </div>
                <div className="flex justify-between font-semibold">
                  <span>Total Tax:</span>
                  <span>${taxData.total_tax.toLocaleString()}</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-semibold">Key Metrics</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Effective Rate:</span>
                  <span>{taxData.effective_rate}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Marginal Rate:</span>
                  <span>{taxData.marginal_rate}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Net Income:</span>
                  <span>${taxData.net_income.toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="text-xs text-muted-foreground">
          * This is a simulation for educational purposes. Consult a tax professional for actual tax advice.
        </div>
      </CardContent>
    </Card>
  )
}
```

## ✅ Acceptance Criteria

- [ ] Tax Engine 코어 구현 (연방 + CA 세율 계산)
- [ ] Julie CPA 위젯 API 구현 및 테스트
- [ ] DSPy MIPROv2 기반 절세 조언 통합
- [ ] 대시보드 컴포넌트 구현 및 통합
- [ ] 2025 세법 정확성 검증 (표준공제, QBI, Mental Health surtax)

## 🔒 제약사항

- **SSOT 유지**: 모든 세금 계산은 2025 최신 세법 기반
- **안전 우선**: 세무 조언은 "교육용 시뮬레이션"으로 한정
- **컴플라이언스**: 실제 세무 자문 아님 명시

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| 세법 변경 | 중간 | 중간 | 버전 관리된 세율 테이블 |
| 계산 정확성 | 높음 | 높음 | 전문 CPA 검토 + 테스트 |
| 법적 책임 | 높음 | 높음 | 명확한 disclaimer |

## 🔄 롤백 계획

1. 위젯 비활성화 → 기본 계산만 유지
2. API 제거 → 수동 계산으로 전환
3. 대시보드 컴포넌트 제거

## 📊 Trinity Score 영향

- **眞 (Truth)**: +9 (세법 정확성 + 실시간 계산)
- **善 (Goodness)**: +8 (절세 전략 최적화)
- **美 (Beauty)**: +9 (직관적 인터랙션 UI)
- **孝 (Serenity)**: +8 (CPA 업무 자동화)
- **永 (Eternity)**: +9 (세법 업데이트 자동화)

**예상 총점**: 78.3 → **97.7** (전문 도메인 AI 적용 성공)

## 📝 작업 로그

- **시작일**: 2025-12-31 (LoRA + DSPy MIPROv2 완성 후)
- **완료일**: 예정
- **실제 소요시간**: 예정

## 🔗 관련 문서

- `AICPA/AFO AICPA_JULIE 122125.md` - Julie CPA 위젯 상세 설계
- `docs/MIPROv2_123025_standard.md` - DSPy MIPROv2 표준
- `packages/afo-core/afo/tax_engine.py` - 세금 계산 엔진
- `packages/dashboard/src/components/TaxCalculatorCard.tsx` - 대시보드 컴포넌트
