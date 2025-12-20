
import sys
import os
from decimal import Decimal
import asyncio

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages")))
# Also add packages/afo-core directly for internal imports if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

try:
    from julie_cpa.core.julie_engine import julie, AdjustBudgetCommand
except ImportError:
    # Fallback import strategy
    from packages.afo_core.julie_cpa.core.julie_engine import julie, AdjustBudgetCommand

async def verify_financial_precision():
    print("💰 [Julie CPA] Financial Precision Verification Start")
    
    # 1. Verify Decimal Types
    print(f"Checking types... Spending: {type(julie.monthly_spending)}, Budget: {type(julie.budget_limit)}")
    if not isinstance(julie.monthly_spending, Decimal):
        print("❌ FAILED: Monthly spending is not Decimal!")
        return
        
    # 2. Execute Command (Adjust Budget)
    new_budget = Decimal("5000.00")
    cmd = AdjustBudgetCommand(julie, new_budget)
    
    print("\n--- Executing AdjustBudgetCommand ---")
    await julie.execute_command(cmd)
    
    if julie.budget_limit == new_budget:
        print(f"✅ Budget updated to {julie.budget_limit}")
    else:
        print(f"❌ Failed to update budget. Current: {julie.budget_limit}")
        
    # 3. Undo Command
    print("\n--- Undo Last Command ---")
    await julie.undo_last_command()
    
    expected_original = Decimal("3500.00")
    if julie.budget_limit == expected_original:
        print(f"✅ Undo successful. Budget reverted to {julie.budget_limit}")
    else:
        print(f"❌ Undo failed. Current: {julie.budget_limit}")

    print("\n[Verification Complete] Financial Precision & Command Pattern Operational.")

if __name__ == "__main__":
    asyncio.run(verify_financial_precision())
