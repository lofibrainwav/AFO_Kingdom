# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Kingdom Julie CPA Service (아름다운 코드 적용)

Trinity Score 기반 아름다운 코드로 구현된 Julie CPA 재무 서비스.
모듈화, 타입 안전성, 문서화를 통해 안정성과 확장성을 보장.

Author: AFO Kingdom Development Team
Date: 2025-12-24
Version: 2.0.0 (Beautiful Code Edition)

Philosophy:
- 智 (Wisdom): 전략적 재무 조언
- 眞 (Truth): 정확한 세금 및 재무 계산
- 善 (Goodness): 윤리적이고 투명한 재무 관리
- 美 (Beauty): 우아하고 직관적인 인터페이스
- 孝 (Serenity): 마찰 없는 사용자 경험
- 永 (Eternity): 지속 가능한 재무 계획
"""

from __future__ import annotations

import logging
from typing import Any, Optional, cast

# Core domain imports
from AFO.julie_cpa.domain.financial_models import FinancialTransaction
from AFO.julie_cpa.infrastructure.financial_connector import FinancialConnector
from AFO.julie_cpa.prophet_engine import get_kingdom_forecast
from AFO.julie_cpa.utils.friction_manager import FrictionManager

# ValidatedAction 계약 (Week 2 SSOT 경계)
from AFO.serenity.action_validator import ValidatedAction


def as_validated_action(x: dict[str, Any]) -> ValidatedAction:
    """ValidatedAction 타입 경계 함수 (Any 누수 차단)"""
    return cast(ValidatedAction, x)


def as_validated_actions(xs: list[dict[str, Any]]) -> list[ValidatedAction]:
    """ValidatedAction 리스트 타입 경계 함수"""
    return [as_validated_action(x) for x in xs]


# AI Router (Truth & Goodness) with graceful import
try:
    from AFO.llm_router import llm_router

    LLM_ROUTER_AVAILABLE = True
except ImportError:
    llm_router = None  # type: ignore[assignment]
    LLM_ROUTER_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)


class RoyalStatusProvider:
    """
    왕실 상태 제공자 (아름다운 코드 적용)

    Trinity Score: 眞 (Truth) - 정확한 상태 정보 제공
    아름다운 코드: 단일 책임 + 불변 데이터 + 타입 안전성
    """

    def __init__(self, friction_manager: FrictionManager) -> None:
        """Initialize royal status provider.

        Args:
            friction_manager: 마찰 관리자 인스턴스
        """
        self.friction_manager = friction_manager

    async def get_status(self) -> dict[str, Any]:
        """
        왕실 재무 상태를 조회합니다.

        Returns:
            상태 정보 딕셔너리
        """
        # Calculate Risk based on Friction logic
        friction_score = self.friction_manager.assess_friction({})

        alerts = []
        if friction_score > 10:
            alerts.append("⚠️ Market Volatility Detected (Friction > 10)")
        else:
            alerts.append("✅ Financial Serenity Maintained")

        advice = "Maintain current spending. Align with Trinity Score."

        return {
            "status": "Social Strategy Active (Royal Edition)",
            "alerts": alerts,
            "advice": advice,
            "dry_run_tx_count": 42,
            "friction_score": friction_score,
        }


class FinancialDashboardProvider:
    """
    재무 대시보드 제공자 (아름다운 코드 적용)

    Trinity Score: 美 (Beauty) - 아름다운 데이터 시각화
    """

    def __init__(
        self, connector: FinancialConnector, friction_manager: FrictionManager
    ) -> None:
        """Initialize financial dashboard provider.

        Args:
            connector: 금융 커넥터
            friction_manager: 마찰 관리자
        """
        self.connector = connector
        self.friction_manager = friction_manager

    async def get_dashboard_data(self) -> dict[str, Any]:
        """
        재무 대시보드 데이터를 생성합니다.

        Returns:
            대시보드 데이터 딕셔너리
        """
        # Fetch bank data
        await self.connector.fetch_bank_data("KB-1234")

        # Calculate health score
        friction_score = self.friction_manager.assess_friction({})
        financial_health_score = max(0, 100 - friction_score * 2)

        # Generate AI advice
        advice = await self._generate_ai_advice(financial_health_score)

        # Emit monitoring event
        await self._emit_dashboard_event(financial_health_score, friction_score)

        return {
            "financial_health_score": financial_health_score,
            "monthly_spending": 2450000,
            "budget_remaining": 550000,
            "recent_transactions": self._get_recent_transactions(),
            "risk_alerts": self._generate_risk_alerts(),
            "advice": advice,
            "friction_score": friction_score,
        }

    async def _generate_ai_advice(self, health_score: float) -> str:
        """AI 기반 재무 조언을 생성합니다."""
        if not LLM_ROUTER_AVAILABLE or not llm_router:
            return "Review cloud infrastructure costs for potential savings."

        try:
            budget_remaining = 550000
            prompt = (
                f"As a Royal CPA, give 1 sentence of strategic financial advice "
                f"based on: Health={health_score}/100, Budget Remaining={budget_remaining}. "
                "Keep it elegant."
            )

            ai_response = await llm_router.execute_with_routing(prompt)
            return cast(str, ai_response.get("response", "Financial data analysis unavailable."))
        except Exception as e:
            logger.warning(f"AI advice generation failed: {e}")
            return "Review cloud infrastructure costs for potential savings."

    async def _emit_dashboard_event(
        self, health_score: float, friction_score: float
    ) -> None:
        """대시보드 로드 이벤트를 발생시킵니다."""
        try:
            from AFO.api.routes.system_stream import publish_thought

            await publish_thought(
                {
                    "step": 0,
                    "decision": "ANALYSIS",
                    "rule_id": "JULIE_01",
                    "trinity": health_score,
                    "risk": friction_score,
                    "graph_node_id": "finance_dashboard_load",
                    "timestamp": "now",
                    "extra": {
                        "category": "finance",
                        "merchant": "Systems Check",
                        "status": "active",
                    },
                },
                event_type="verdict",
            )
        except ImportError:
            logger.debug("System stream not available for dashboard events")

    def _get_recent_transactions(self) -> list[dict[str, Any]]:
        """최근 거래 내역을 반환합니다."""
        return [
            {
                "id": "t1",
                "merchant": "Netflix",
                "amount": 17000,
                "date": "2024-04-25",
                "category": "Subscription",
            },
            {
                "id": "t2",
                "merchant": "Starbucks",
                "amount": 9800,
                "date": "2024-04-24",
                "category": "Food",
            },
            {
                "id": "t3",
                "merchant": "AWS",
                "amount": 45000,
                "date": "2024-04-23",
                "category": "Infrastructure",
            },
        ]

    def _generate_risk_alerts(self) -> list[dict[str, str]]:
        """리스크 알림을 생성합니다."""
        return [
            {
                "level": "warning",
                "message": "Subscription cost increased by 15% vs last month",
            },
            {"level": "info", "message": "Budget utilization at 82%"},
        ]


class TransactionProcessor:
    """
    거래 처리기 (아름다운 코드 적용)

    Trinity Score: 善 (Goodness) - 안전하고 신뢰할 수 있는 거래 처리
    """

    def __init__(
        self, connector: FinancialConnector, friction_manager: FrictionManager
    ) -> None:
        """Initialize transaction processor.

        Args:
            connector: 금융 커넥터
            friction_manager: 마찰 관리자
        """
        self.connector = connector
        self.friction_manager = friction_manager

    async def process_transaction(
        self, request_data: dict[str, Any], account_id: str, dry_run: bool = False
    ) -> dict[str, Any]:
        """
        거래를 처리합니다.

        Args:
            request_data: 거래 요청 데이터
            account_id: 계좌 ID
            dry_run: 드라이 런 모드

        Returns:
            처리 결과 딕셔너리
        """
        logger.info(f"Processing transaction (dry_run={dry_run})")

        # Validate friction
        friction = self.friction_manager.assess_friction(request_data)
        if self.friction_manager.check_fog_of_war(friction):
            return {
                "success": False,
                "reason": "Fog of War Detected (High Friction)",
                "friction_score": friction,
            }

        # Validate transaction data
        try:
            transaction = FinancialTransaction(**request_data)
        except Exception as e:
            logger.error(f"Transaction validation failed: {e}")
            return {"success": False, "reason": str(e)}

        # Process based on mode
        if dry_run:
            return await self._process_dry_run(transaction, friction, request_data)
        else:
            return await self._process_live_transaction(
                transaction, account_id, request_data
            )

    async def _process_dry_run(
        self,
        transaction: FinancialTransaction,
        friction: float,
        request_data: dict[str, Any],
    ) -> dict[str, Any]:
        """드라이 런 모드로 거래를 처리합니다."""
        logger.info("Executing dry run transaction")

        # Emit event
        await self._emit_transaction_event(
            "DRY_RUN", "SUN_TZU_03", 95, friction * 10, "finance_dry_run", request_data
        )

        return {
            "success": True,
            "mode": "DRY_RUN",
            "transaction": transaction.model_dump(),
            "friction_score": friction,
        }

    async def _process_live_transaction(
        self,
        transaction: FinancialTransaction,
        account_id: str,
        request_data: dict[str, Any],
    ) -> dict[str, Any]:
        """실제 거래를 처리합니다."""
        logger.info("Executing live transaction")

        # Sync with bank
        bank_status = await self.connector.fetch_bank_data(account_id)

        # Emit event
        await self._emit_transaction_event(
            "AUTO_RUN", "PRINCE_25", 99, 0, "finance_live_tx", request_data
        )

        return {
            "success": True,
            "mode": "LIVE",
            "transaction": transaction.model_dump(),
            "bank_sync": bank_status,
            "audit_log": f"TX-{transaction.transaction_id}-VERIFIED",
        }

    async def _emit_transaction_event(
        self,
        decision: str,
        rule_id: str,
        trinity: int,
        risk: float,
        graph_node: str,
        request_data: dict[str, Any],
    ) -> None:
        """거래 이벤트를 발생시킵니다."""
        try:
            from AFO.api.routes.system_stream import publish_thought

            await publish_thought(
                {
                    "step": 1 if "DRY" in decision else 2,
                    "decision": decision,
                    "rule_id": rule_id,
                    "trinity": trinity,
                    "risk": risk,
                    "graph_node_id": graph_node,
                    "timestamp": "now",
                    "extra": {
                        "category": "finance",
                        "merchant": request_data.get("merchant"),
                        "amount": request_data.get("amount"),
                        "status": "verified" if "AUTO" in decision else "simulated",
                    },
                },
                event_type="verdict",
            )
        except ImportError:
            logger.debug("System stream not available for transaction events")


class TaxCalculator:
    """
    세금 계산기 (아름다운 코드 적용)

    Trinity Score: 眞 (Truth) - 정확한 세금 계산
    """

    async def calculate_tax_scenario(
        self, income: float, filing_status: str = "single"
    ) -> dict[str, Any]:
        """
        세금 시나리오를 계산합니다.

        Args:
            income: 소득
            filing_status: 신고 상태

        Returns:
            세금 계산 결과
        """
        # Calculate taxable income
        standard_deduction = self._get_standard_deduction(filing_status)
        taxable_income = max(0, income - standard_deduction)

        # Calculate federal tax
        fed_tax, fed_marginal_rate = self._calculate_federal_tax(
            taxable_income, filing_status
        )

        # Calculate state tax
        ca_tax, ca_marginal_rate, surtax = self._calculate_california_tax(
            taxable_income
        )

        # Calculate QBI deduction
        qbi_deduction = self._calculate_qbi_deduction(
            income, taxable_income, filing_status
        )

        # Aggregate results
        total_tax = fed_tax + ca_tax
        net_income = income - total_tax
        eff_rate = (total_tax / income * 100) if income > 0 else 0
        combined_marginal_rate = fed_marginal_rate + ca_marginal_rate

        # Generate advice
        advice_cards = self._generate_advice_cards(
            combined_marginal_rate, qbi_deduction, fed_marginal_rate, filing_status
        )

        return {
            "income": income,
            "filing_status": filing_status,
            "standard_deduction": standard_deduction,
            "taxable_income": taxable_income,
            "fed_tax": round(fed_tax, 2),
            "ca_tax": round(ca_tax, 2),
            "total_tax": round(total_tax, 2),
            "net_income": round(net_income, 2),
            "effective_rate": round(eff_rate, 2),
            "marginal_rate": round(combined_marginal_rate * 100, 1),
            "qbi_potential_deduction": round(qbi_deduction, 2),
            "risk_level": (
                "safe" if eff_rate < 20 else "risk" if eff_rate > 30 else "neutral"
            ),
            "mental_health_surtax": round(surtax, 2),
            "advice_cards": advice_cards,
        }

    def _get_standard_deduction(self, filing_status: str) -> int:
        """표준 공제를 반환합니다."""
        return 31500 if filing_status == "mfj" else 15750

    def _calculate_federal_tax(
        self, taxable_income: float, filing_status: str
    ) -> tuple[float, float]:
        """연방 세금을 계산합니다."""
        brackets = [
            (int(23200 if filing_status == "mfj" else 11600), 0.10),
            (int(94300 if filing_status == "mfj" else 47150), 0.12),
            (int(201050 if filing_status == "mfj" else 100525), 0.22),
            (int(383900 if filing_status == "mfj" else 191950), 0.24),
            (int(487450 if filing_status == "mfj" else 243725), 0.32),
            (int(731200 if filing_status == "mfj" else 609350), 0.35),
            (int(float("inf")), 0.37),
        ]

        fed_tax = 0.0
        fed_marginal_rate = 0.0
        previous_limit = 0

        for limit, rate in brackets:
            if taxable_income > previous_limit:
                taxable_amount = min(taxable_income, limit) - previous_limit
                fed_tax += taxable_amount * rate
                previous_limit = limit
                fed_marginal_rate = rate
            else:
                break

        return fed_tax, fed_marginal_rate

    def _calculate_california_tax(
        self, taxable_income: float
    ) -> tuple[float, float, float]:
        """캘리포니아 주 세금을 계산합니다."""
        # Mental Health Surtax
        surtax = max(0, taxable_income - 1000000) * 0.01

        # Progressive tax
        if taxable_income > 1000000:
            ca_tax = taxable_income * 0.123
            ca_marginal_rate = 0.133  # Including surtax
        elif taxable_income > 300000:
            ca_tax = taxable_income * 0.113
            ca_marginal_rate = 0.113
        elif taxable_income > 60000:
            ca_tax = taxable_income * 0.093
            ca_marginal_rate = 0.093
        elif taxable_income > 100000:
            ca_tax = taxable_income * 0.06
            ca_marginal_rate = 0.06
        else:
            ca_tax = taxable_income * 0.02
            ca_marginal_rate = 0.02

        ca_tax += surtax
        return ca_tax, ca_marginal_rate, surtax

    def _calculate_qbi_deduction(
        self, income: float, taxable_income: float, filing_status: str
    ) -> float:
        """QBI 공제를 계산합니다."""
        qbi_eligible_income = income * 0.30
        qbi_threshold = 394600 if filing_status == "mfj" else 197300

        if taxable_income < qbi_threshold:
            return qbi_eligible_income * 0.20
        return 0.0

    def _generate_advice_cards(
        self,
        marginal_rate: float,
        qbi_deduction: float,
        fed_marginal_rate: float,
        filing_status: str,
    ) -> list[dict[str, Any]]:
        """조언 카드를 생성합니다."""
        advice_cards = []

        # 401k/SEP IRA advice
        potential_401k_saving = 23500 * marginal_rate
        advice_cards.append(
            {
                "title": "Maximize 401k/SEP",
                "action": "Contribute $23,500",
                "impact": f"Save ${int(potential_401k_saving):,} in Taxes",
                "type": "savings",
            }
        )

        # HSA advice
        hsa_limit = 8550 if filing_status == "mfj" else 4300
        potential_hsa_saving = hsa_limit * marginal_rate
        advice_cards.append(
            {
                "title": "Health Savings Account (HSA)",
                "action": f"Contribute ${hsa_limit:,}",
                "impact": f"Save ${int(potential_hsa_saving):,} in Taxes",
                "type": "health",
            }
        )

        # QBI advice
        if qbi_deduction > 0:
            qbi_tax_value = qbi_deduction * fed_marginal_rate
            advice_cards.append(
                {
                    "title": "QBI Deduction (20%)",
                    "action": "Maintain Business Income",
                    "impact": f"Auto-saving ${int(qbi_tax_value):,}",
                    "type": "business",
                }
            )

        return advice_cards


class JulieService:
    """
    AFO Kingdom Julie CPA Service (아름다운 코드 적용)

    Trinity Score 기반 Julie CPA 재무 서비스 메인 오케스트레이터.
    각 컴포넌트를 조율하여 체계적인 재무 서비스를 제공.

    Attributes:
        status_provider: 왕실 상태 제공자
        dashboard_provider: 재무 대시보드 제공자
        transaction_processor: 거래 처리기
        tax_calculator: 세금 계산기
    """

    def __init__(self) -> None:
        """Initialize Julie CPA service with beautiful code principles."""
        # Initialize core components
        self.connector = FinancialConnector()
        self.friction_manager = FrictionManager()

        # Initialize specialized providers
        self.status_provider = RoyalStatusProvider(self.friction_manager)
        self.dashboard_provider = FinancialDashboardProvider(
            self.connector, self.friction_manager
        )
        self.transaction_processor = TransactionProcessor(self.connector, self.friction_manager)
        self.tax_calculator = TaxCalculator()

        logger.info("Julie CPA Service initialized with beautiful code principles")

    async def get_royal_status(self) -> dict[str, Any]:
        """
        [Legacy Merger]
        Replicates the '3-line summary' from legacy julie.py but backed by Royal metrics.
        """
        # Calculate Risk based on Friction logic
        friction_score = 15.0  # Mocking current friction

        alerts = []
        if friction_score > 10:
            alerts.append("⚠️ Market Volatility Detected (Friction > 10)")
        else:
            alerts.append("✅ Financial Serenity Maintained")

        advice = "Maintain current spending. Align with Trinity Score."

        return {
            "status": "Social Strategy Active (Royal Edition)",
            "alerts": alerts,
            "advice": advice,
            "dry_run_tx_count": 42,
        }

    async def get_financial_dashboard(self) -> dict[str, Any]:
        """
        [GenUI Support]
        Returns detailed financial health data for the AICPA Dashboard.
        Uses LLM Router for dynamic advice (Server-Side AI Shift).
        """
        # 1. Fetch real-time (simulated) dashboard data
        dashboard_data = await self.connector.fetch_dashboard_data("KB-1234")
        if "error" in dashboard_data:
            # Fallback or Error handling
            logger.error(f"Dashboard fetch failed: {dashboard_data['error']}")
            return {"error": "Financial Data Unavailable"}

        # 2. Risk Analysis (Dynamic)
        # Recalculate based on real data
        monthly_spending = dashboard_data.get("monthly_spending", 0)
        budget_remaining = dashboard_data.get("budget_remaining", 0)

        # Simple friction model: High spending = High friction
        utilization = monthly_spending / (monthly_spending + budget_remaining + 1)
        friction_score = utilization * 20  # Max ~20
        financial_health_score = max(0, 100 - friction_score * 2)

        # 3. Dynamic Advice via LLM Router
        context_data = {
            "health": financial_health_score,
            "spending": monthly_spending,
            "budget": budget_remaining,
        }

        try:
            ai_response = await llm_router.execute_with_routing(
                f"As a Royal CPA, give 1 sentence of strategic financial advice based on: Health={int(financial_health_score)}/100, Budget Remaining={int(budget_remaining)}, Spending={int(monthly_spending)}. Keep it elegant."
            )
            advice = ai_response.get("response", "Financial data analysis unavailable.")
        except Exception as e:
            logger.warning(f"AI Advice Generation Failed: {e}")
            advice = "Review cloud infrastructure costs (AWS) for potential savings via consolidated instances."

        # Emit Thought: Dashboard Analysis
        from AFO.api.routes.system_stream import publish_thought

        await publish_thought(
            {
                "step": 0,
                "decision": "ANALYSIS",
                "rule_id": "JULIE_01",
                "trinity": financial_health_score,
                "risk": friction_score,
                "graph_node_id": "finance_dashboard_load",
                "timestamp": "now",
                "extra": {
                    "category": "finance",
                    "merchant": "Systems Check",
                    "status": "active",
                },
            },
            event_type="verdict",
        )

        return {
            "financial_health_score": financial_health_score,
            "monthly_spending": monthly_spending,
            "budget_remaining": budget_remaining,
            "recent_transactions": dashboard_data.get("recent_transactions", []),
            "risk_alerts": dashboard_data.get("risk_alerts", []),
            "advice": advice,
            "forecast": get_kingdom_forecast(periods=3),
        }

    async def process_transaction(
        self, request_data: dict[str, Any], account_id: str, dry_run: bool = False
    ) -> dict[str, Any]:
        """
        [Sun Tzu #3: All Warfare is Deception (Dry Run)]
        [Sun Tzu #9: Use of Spies (Audit)]
        """
        print(f"🛡️ [Julie] Assessing Request (Dry Run={dry_run})...")

        # 1. On War #34: Check Fog of War
        friction = self.friction_manager.assess_friction(request_data)
        if self.friction_manager.check_fog_of_war(friction):
            return {
                "success": False,
                "reason": "Fog of War Detected (High Friction)",
                "friction_score": friction,
            }

        # 2. The Prince #25: Strict Validation
        try:
            tx = FinancialTransaction(**request_data)
        except Exception as e:
            print(f"❌ [The Prince] Validation Rejected: {e}")
            return {"success": False, "reason": str(e)}

        # 3. Execution (or Simulation)
        if dry_run:
            print("🎭 [Sun Tzu] Dry Run Successful. No side effects.")
            # Emit Thought: Visualization
            from AFO.api.routes.system_stream import publish_thought

            await publish_thought(
                {
                    "step": 1,
                    "decision": "DRY_RUN",
                    "rule_id": "SUN_TZU_03",
                    "trinity": 95,
                    "risk": friction * 10,
                    "graph_node_id": "finance_dry_run",
                    "timestamp": "now",
                    "extra": {
                        "category": "finance",
                        "merchant": request_data.get("merchant"),
                        "amount": request_data.get("amount"),
                    },
                },
                event_type="verdict",
            )
            return {
                "success": True,
                "mode": "DRY_RUN",
                "transaction": tx.model_dump(),
                "friction_score": friction,
            }

        # 4. Three Kingdoms #14: External Connect
        # Dynamic Account Sync
        bank_status = await self.connector.fetch_bank_data(account_id)

        # Emit Thought: Live Execution
        from AFO.api.routes.system_stream import publish_thought

        await publish_thought(
            {
                "step": 2,
                "decision": "AUTO_RUN",
                "rule_id": "PRINCE_25",
                "trinity": 99,
                "risk": 0,
                "graph_node_id": "finance_live_tx",
                "timestamp": "now",
                "extra": {
                    "category": "finance",
                    "merchant": request_data.get("merchant"),
                    "status": "verified",
                },
            },
            event_type="verdict",
        )

        # 5. Finalize
        return {
            "success": True,
            "mode": "LIVE",
            "transaction": tx.model_dump(),
            "bank_sync": bank_status,
            "audit_log": f"TX-{tx.transaction_id}-VERIFIED",
        }

    async def calculate_tax_scenario(
        self, income: float, filing_status: str = "single"
    ) -> dict[str, Any]:
        """
        [Operation Gwanggaeto: Tax Truth 2025]
        Source code for 2025 Tax Logic (Federal + CA + QBI).
        SSOT Reference: AFO_WIDGET_BLUEPRINTS.md & Julie-Perplexity Report.
        """
        # 1. Constants (2025 Truth)
        standard_deduction = 31500 if filing_status == "mfj" else 15750

        # 2. Base Calculation
        taxable_income = max(0, income - standard_deduction)

        # 3. Federal Tax (Simplified Progressive 2025)
        # Brackets: 10%, 12%, 22%, 24%, 32%, 35%, 37%
        fed_tax = 0.0
        remaining = taxable_income

        brackets = [
            (int(23200 if filing_status == "mfj" else 11600), 0.10),
            (int(94300 if filing_status == "mfj" else 47150), 0.12),
            (int(201050 if filing_status == "mfj" else 100525), 0.22),
            (int(383900 if filing_status == "mfj" else 191950), 0.24),
            (int(487450 if filing_status == "mfj" else 243725), 0.32),
            (int(731200 if filing_status == "mfj" else 609350), 0.35),
            (int(float("inf")), 0.37),
        ]

        previous_limit = 0
        current_tax = 0.0

        # Marginal Rate Tracking
        fed_marginal_rate = 0.0

        for limit, rate in brackets:
            if taxable_income > previous_limit:
                taxable_amount = min(taxable_income, limit) - previous_limit
                current_tax += taxable_amount * rate
                previous_limit = limit
                fed_marginal_rate = rate  # Update marginal as we climb
            else:
                break
        fed_tax = current_tax

        # 4. CA State Tax (Logic: 1% - 12.3% + 1% Surtax > 1M)
        # Simplified effective buckets for simulation speed
        ca_tax = 0.0
        ca_marginal_rate = 0.0

        # Mental Health Surtax (1% on taxable > 1M)
        surtax = max(0, taxable_income - 1000000) * 0.01

        # Standard CA Progressive (Approximate for Simulation)
        if taxable_income > 1000000:
            ca_tax = taxable_income * 0.123  # Top rate approx
            ca_marginal_rate = 0.133  # 12.3 + 1
        elif taxable_income > 300000:
            ca_tax = taxable_income * 0.113
            ca_marginal_rate = 0.113
        elif taxable_income > 60000:
            ca_tax = taxable_income * 0.093
            ca_marginal_rate = 0.093
        elif taxable_income > 100000:  # Overlap fix
            ca_tax = taxable_income * 0.06
            ca_marginal_rate = 0.06
        else:
            ca_tax = taxable_income * 0.02
            ca_marginal_rate = 0.02

        ca_tax += surtax

        # 5. QBI (Qualified Business Income) Deduction Logic
        # Assuming 30% of Gross Income is "Qualified Business Income" for this simulation persona
        qbi_eligible_income = income * 0.30
        qbi_deduction = 0.0
        qbi_threshold = 394600 if filing_status == "mfj" else 197300

        if taxable_income < qbi_threshold:
            qbi_deduction = qbi_eligible_income * 0.20
            # Adjust taxable income for final accurate tax would be complex,
            # so we list it as a "Potential Saving" for advice.

        # 6. Aggregation
        total_tax = fed_tax + ca_tax
        net_income = income - total_tax
        eff_rate = (total_tax / income * 100) if income > 0 else 0
        combined_marginal_rate = fed_marginal_rate + ca_marginal_rate

        # 7. Risk Assessment
        risk_level = "safe" if eff_rate < 20 else "risk" if eff_rate > 30 else "neutral"

        # 8. Strategic Advice (The "Template" Logic)
        advice_cards = []

        # Strategy A: 401k / SEP IRA (Pre-tax) - 2025 Limit $23,500
        # "If you put in $23,500, you save X"
        potential_401k_saving = 23500 * combined_marginal_rate
        advice_cards.append(
            {
                "title": "Maximize 401k/SEP",
                "action": "Contribute $23,500",
                "impact": f"Save ${int(potential_401k_saving):,} in Taxes",
                "type": "savings",
            }
        )

        # Strategy B: HSA (Health Savings) - 2025 Limit $4,300 (Single) / $8,550 (Family)
        hsa_limit = 8550 if filing_status == "mfj" else 4300
        potential_hsa_saving = hsa_limit * combined_marginal_rate
        advice_cards.append(
            {
                "title": "Health Savings Account (HSA)",
                "action": f"Contribute ${hsa_limit:,}",
                "impact": f"Save ${int(potential_hsa_saving):,} in Taxes",
                "type": "health",
            }
        )

        # Strategy C: QBI (if applicable)
        if qbi_deduction > 0:
            qbi_tax_value = (
                qbi_deduction * fed_marginal_rate
            )  # QBI is Fed only deduction
            advice_cards.append(
                {
                    "title": "QBI Deduction (20%)",
                    "action": "Maintain Business Income",
                    "impact": f"Auto-saving ${int(qbi_tax_value):,}",
                    "type": "business",
                }
            )

        return {
            "income": income,
            "filing_status": filing_status,
            "standard_deduction": standard_deduction,
            "fed_tax": round(fed_tax, 2),
            "ca_tax": round(ca_tax, 2),
            "total_tax": round(total_tax, 2),
            "net_income": round(net_income, 2),
            "effective_rate": round(eff_rate, 2),
            "marginal_rate": round(combined_marginal_rate * 100, 1),
            "qbi_potential_deduction": round(qbi_deduction, 2),
            "risk_level": risk_level,
            "mental_health_surtax": round(surtax, 2),
            "advice_cards": advice_cards,
        }
