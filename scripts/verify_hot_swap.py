import os
import sys


# Ensure package root is in python path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "packages", "afo-core"))

import dspy

from AFO.dspy.commander_briefing import CommanderBriefing


def verify_hot_swap():
    # 1. Ensure Dummy Optimized File Exists
    optimized_path = "data/dspy/compiled_commander_briefing.v2.json"
    os.makedirs(os.path.dirname(optimized_path), exist_ok=True)

    # Create a mock valid DSPy state file if not exists
    # If it exists (from previous TICKET-003/023 runs), it will use that.
    # If not, we create a dummy one just to test the *loading logic*, not the validity of weights.
    # But dspy.load expects valid json structure.
    # Let's rely on the fact that we ran TICKET-023 check
    # But to be safe, let's create a minimal valid state if missing.
    # Create a mock valid DSPy state file using the module itself
    # This ensures the structure is exactly what dspy expects (metadata, etc.)
    if not os.path.exists(optimized_path):
        dummy_module = CommanderBriefing()
        # Save to the specific path
        dummy_module.save(optimized_path)
        print(f"🛠️ [Setup] Created dummy optimized state at {optimized_path}")

    # 2. Capture Stdout
    from io import StringIO

    old_stdout = sys.stdout
    captured = StringIO()
    sys.stdout = captured

    try:
        # 3. Instantiate Module
        module = CommanderBriefing()
    finally:
        sys.stdout = old_stdout

    output = captured.getvalue()
    print("CAPTURED OUTPUT:\n" + output)

    # 4. Verification
    if "HOT-SWAP: Loaded optimized intelligence" in output:
        print("✅ SUCCESS: Module detected and loaded optimized state.")
    else:
        print("❌ FAILURE: Module did not report loading optimized state.")
        sys.exit(1)


if __name__ == "__main__":
    verify_hot_swap()
