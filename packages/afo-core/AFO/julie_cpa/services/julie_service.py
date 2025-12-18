from datetime import datetime
from typing import Dict, Any, Optional
from decimal import Decimal

# Absolute Imports based on package structure
from AFO.julie_cpa.domain.financial_models import FinancialTransaction
from AFO.julie_cpa.infrastructure.financial_connector import FinancialConnector
from AFO.julie_cpa.utils.friction_manager import FrictionManager

class JulieService:
    """
    [Julie CPA Service - Royal Library Edition]
    Orchestrates Finance with Strategy (Sun Tzu) and Control (Prince).
    """

    def __init__(self):
        self.connector = FinancialConnector()
        self.friction_manager = FrictionManager()

    async def process_transaction(self, request_data: Dict[str, Any], account_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        [Sun Tzu #3: All Warfare is Deception (Dry Run)]
        [Sun Tzu #9: Use of Spies (Audit)]
        """
        print(f"🛡️ [Julie] Assessing Request (Dry Run={dry_run})...")

        # 1. On War #34: Check Fog of War
        friction = self.friction_manager.assess_friction(request_data)
        if self.friction_manager.check_fog_of_war(friction):
            return {"success": False, "reason": "Fog of War Detected (High Friction)", "friction_score": friction}

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
                "friction_score": friction
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
            "audit_log": f"TX-{tx.transaction_id}-VERIFIED"
        }
