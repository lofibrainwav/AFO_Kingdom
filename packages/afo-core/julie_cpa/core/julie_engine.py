# Trinity Score: 90.0 (Established by Chancellor)
# packages/afo-core/julie_cpa/core/julie_engine.py
# Julie CPA AutoMate 메인 엔진 (Precision Upgrade)
# AntiGravity: 비용 최적화(Truth), 권한 검증(Goodness), 지속 아키텍처(Eternity)

from abc import ABC, abstractmethod
from decimal import Decimal, getcontext

from AFO.security.vault_manager import vault as vault_manager
from services.trinity_calculator import trinity_calculator

# Set Decimal Precision
getcontext().prec = 28

# Assuming llm_router import logic remains similar or we mock it
try:
    from services.llm_router import llm_router
except ImportError:

    class MockRouter:
        async def ask(self, prompt, context=None, model_priority=None):
            return "Mock LLM Response"

    llm_router = MockRouter()


# ==========================================
# Command Pattern for Financial Operations
# ==========================================


class FinancialCommand(ABC):
    @abstractmethod
    def execute(self) -> bool:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class AdjustBudgetCommand(FinancialCommand):
    def __init__(self, cpa: "JulieCPA", amount: Decimal):
        self.cpa = cpa
        self.amount = amount
        self.previous_limit = Decimal("0.00")

    def execute(self) -> bool:
        self.previous_limit = self.cpa.budget_limit
        self.cpa.budget_limit = self.amount
        print(f"💰 [Julie] Budget Adjusted: ${self.previous_limit} -> ${self.amount}")
        return True

    def undo(self) -> None:
        print(f"↩️ [Julie] Undo Budget Adjustment. Reverting to ${self.previous_limit}")
        self.cpa.budget_limit = self.previous_limit


# ==========================================
# Julie CPA Engine (Precision)
# ==========================================


class JulieCPA:
    """
    Julie CPA AutoMate - 의(義)의 기술
    재정적 자유와 절대적 정확성을 위한 자동 회계·세무 엔진
    """

    def __init__(self):
        # Vault 동적 조회
        self.openai_key = vault_manager.get_secret("OPENAI_API_KEY", "mock-key")

        # Financial State (Decimal for Precision)
        self.monthly_spending = Decimal("4200.00")
        self.budget_limit = Decimal("3500.00")
        self.tax_risk_score = 85

        self.command_history: list[FinancialCommand] = []

    async def execute_command(self, command: FinancialCommand) -> bool:
        """Trinity Gated Execution"""
        # 1. Calculate Trinity Score to approve action
        # Mocking raw scores for this action context - ideally dynamic
        raw_scores = [1.0, 1.0, 1.0, 1.0, 1.0]
        # Check Risk Gate (Goodness)
        if self.tax_risk_score > 90:
            # If too risky, Goodness pillar might fail
            raw_scores[1] = 0.0

        trinity_score = trinity_calculator.calculate_trinity_score(raw_scores)

        if trinity_score < 70.0:
            print(
                f"⛔ [Julie] Trinity Score Too Low ({trinity_score}). Action Blocked."
            )
            return False

        # 2. Execute
        success = command.execute()
        if success:
            self.command_history.append(command)
            return True
        return False

    async def undo_last_command(self):
        if self.command_history:
            cmd = self.command_history.pop()
            cmd.undo()
        else:
            print("⚠️ [Julie] No commands to undo.")

    async def risk_alert(self) -> list[str]:
        """초과 지출·세금 위험 실시간 알림"""
        alerts = []
        if self.monthly_spending > self.budget_limit * Decimal("1.2"):
            alerts.append("⚠️ Monthly burn rate > 20% over budget (LA Life)")
        if self.tax_risk_score > 80:
            alerts.append("🔴 IRS Audit Risk High - Check 1099s immediately")
        return alerts


# Singleton Instance
julie = JulieCPA()
