import logging
from typing import Any

# Absolute Imports based on package structure
from AFO.julie_cpa.domain.financial_models import FinancialTransaction
from AFO.julie_cpa.infrastructure.financial_connector import FinancialConnector
from AFO.julie_cpa.utils.friction_manager import FrictionManager

# AI Router (Truth & Goodness)
try:
    from AFO.llm_router import llm_router
except ImportError:
    llm_router = None  # type: ignore

logger = logging.getLogger(__name__)


class JulieService:
    """
    [Julie CPA Service - Royal Library Edition]
    Orchestrates Finance with Strategy (Sun Tzu) and Control (Prince).
    Legacy Merged: Incorporates 'Advice' and 'Alerts' from legacy code.
    """

    def __init__(self):
        self.connector = FinancialConnector()
        self.friction_manager = FrictionManager()

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
        # 1. Fetch real-time bank data (Mock for now)
        await self.connector.fetch_bank_data("KB-1234")

        # 2. Risk Analysis
        friction_score = 15.0
        financial_health_score = max(0, 100 - friction_score * 2)  # e.g. 70

        # 3. Dynamic Advice via LLM Router (Server-Side AI Shift)
        # VaultManager already secures keys inside llm_router
        context_data = {
            "health": financial_health_score,
            "spending": 2450000,
            "budget": 550000,
        }

        try:
            # Simple prompt for advice
            ai_response = await llm_router.execute_with_routing(
                f"As a Royal CPA, give 1 sentence of strategic financial advice based on: Health={financial_health_score}/100, Budget Remaining={context_data['budget']}. Keep it elegant."
            )
            advice = ai_response.get("response", "Financial data analysis unavailable.")
        except Exception as e:
            logger.warning(f"AI Advice Generation Failed: {e}")
            advice = "Review cloud infrastructure costs (AWS) for potential savings via consolidated instances."

        return {
            "financial_health_score": financial_health_score,
            "monthly_spending": 2450000,
            "budget_remaining": 550000,
            "recent_transactions": [
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
            ],
            "risk_alerts": [
                {
                    "level": "warning",
                    "message": "Subscription cost increased by 15% vs last month",
                },
                {"level": "info", "message": "Budget utilization at 82%"},
            ],
            "advice": advice,
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
            return {
                "success": True,
                "mode": "DRY_RUN",
                "transaction": tx.model_dump(),
                "friction_score": friction,
            }

        # 4. Three Kingdoms #14: External Connect
        # Dynamic Account Sync
        bank_status = await self.connector.fetch_bank_data(account_id)

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
            (23200 if filing_status == "mfj" else 11600, 0.10),
            (94300 if filing_status == "mfj" else 47150, 0.12),
            (201050 if filing_status == "mfj" else 100525, 0.22),
            (383900 if filing_status == "mfj" else 191950, 0.24),
            (487450 if filing_status == "mfj" else 243725, 0.32),
            (731200 if filing_status == "mfj" else 609350, 0.35),
            (float("inf"), 0.37),
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
            qbi_tax_value = qbi_deduction * fed_marginal_rate  # QBI is Fed only deduction
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
