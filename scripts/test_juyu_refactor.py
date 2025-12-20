import asyncio
import os
import sys

# Set path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

from AFO.agents.juyu_core import juyu


async def main():
    print("🎨 Awakening Juyu...")

    # 1. Setup: Create a "Rough" Widget (Low Beauty Score)
    target_path = "packages/dashboard/src/components/genui/SamahwiGeneratedWidget.tsx"

    # Read existing
    if os.path.exists(target_path):
        with open(target_path) as f:
            original = f.read()

    # Sabotage it (Remove Glassmorphism) to test Juyu
    rough_code = original.replace("glass-card", "bg-gray-500")
    with open(target_path, "w") as f:
        f.write(rough_code)
    print("\n[Setup] Sabotaged Widget (Removed 'glass-card' token)")

    # 2. Run Juyu
    print("\n[Action] Juyu Refactoring...")
    result = await juyu.run("Refactor genui/SamahwiGeneratedWidget.tsx")
    print(f"Result: {result}")

    # 3. Verify
    with open(target_path) as f:
        final_code = f.read()

    if "glass-card" in final_code:
        print("\n✅ Phase 16-3 COMPLETE: Juyu successfully injected 'glass-card' token.")
    else:
        print("\n❌ PHASE 16-3 FAILED: 'glass-card' token missing.")


if __name__ == "__main__":
    asyncio.run(main())
