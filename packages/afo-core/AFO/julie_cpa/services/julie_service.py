from typing import Any, Dict, List
import logging

# Absolute Imports based on package structure
from AFO.julie_cpa.domain.financial_models import FinancialTransaction
from AFO.julie_cpa.infrastructure.financial_connector import FinancialConnector
from AFO.julie_cpa.utils.friction_manager import FrictionManager

# AI Router (Truth & Goodness)
try:
    from AFO.llm_router import llm_router
except ImportError:
    # Fallback for direct testing
    from llm_router import llm_router

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

    async def get_royal_status(self) -> Dict[str, Any]:
        """
        [Legacy Merger]
        Replicates the '3-line summary' from legacy julie.py but backed by Royal metrics.
        """
        # Calculate Risk based on Friction logic
        friction_score = 15.0 # Mocking current friction
        
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
            "dry_run_tx_count": 42
        }

    async def get_financial_dashboard(self) -> Dict[str, Any]:
        """
        [GenUI Support]
        Returns detailed financial health data for the AICPA Dashboard.
        Uses LLM Router for dynamic advice (Server-Side AI Shift).
        """
        # 1. Fetch real-time bank data (Mock for now)
        bank_data = await self.connector.fetch_bank_data("KB-1234")
        
        # 2. Risk Analysis
        friction_score = 15.0 
        financial_health_score = max(0, 100 - friction_score * 2) # e.g. 70
        
        # 3. Dynamic Advice via LLM Router (Server-Side AI Shift)
        # VaultManager already secures keys inside llm_router
        context_data = {
            "health": financial_health_score,
            "spending": 2450000,
            "budget": 550000
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
                {"id": "t1", "merchant": "Netflix", "amount": 17000, "date": "2024-04-25", "category": "Subscription"},
                {"id": "t2", "merchant": "Starbucks", "amount": 9800, "date": "2024-04-24", "category": "Food"},
                {"id": "t3", "merchant": "AWS", "amount": 45000, "date": "2024-04-23", "category": "Infrastructure"}
            ],
            "risk_alerts": [
                {"level": "warning", "message": "Subscription cost increased by 15% vs last month"},
                {"level": "info", "message": "Budget utilization at 82%"}
            ],
            "advice": advice
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
        print(f"💰 [Julie] Transaction Processed: {tx.amount} {tx.currency}")
        return {
            "success": True,
            "mode": "LIVE",
            "transaction": tx.model_dump(),
            "bank_sync": bank_status,
            "audit_log": f"TX-{tx.transaction_id}-VERIFIED",
        }
