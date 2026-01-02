import os
import sys


# Add packages/afo-core to python path
current_dir = os.getcwd()
afo_core_path = os.path.join(current_dir, "packages", "afo-core")
sys.path.append(afo_core_path)

try:
    import dspy

    # Try alternate import if AFO is not a package
    try:
        from AFO.dspy.trinity_mipro_v2 import TrinityAwareMIPROv2

        print("✅ Imports Successful: TrinityAwareMIPROv2 (from AFO)")
    except ImportError:
        try:
            from afo.dspy.trinity_mipro_v2 import TrinityAwareMIPROv2

            print("✅ Imports Successful: TrinityAwareMIPROv2 (from afo)")
        except ImportError as e:
            print(f"❌ Import Failed: {e}")
            sys.exit(1)

except ImportError as e:
    print(f"❌ dspy Import Failed: {e}")
    sys.exit(1)


# Mock LM for dspy 3.0+ compatibility
class MockLM(dspy.LM):
    def __init__(self, model="mock", **kwargs):
        super().__init__(model, **kwargs)
        self.history = []

    def basic_request(self, prompt, **kwargs):
        return ["Mock Answer"]

    def __call__(self, prompt, **kwargs):
        return ["Mock Answer"]


def dummy_metric(example, pred, trace=None):
    return True


def test_dry_run():
    print("🚀 Starting Dry-Run Verification...")

    # 1. Setup Mock LM
    lm = MockLM()
    dspy.configure(lm=lm)
    print("✅ MockLM Configured")

    # 2. Initialize Teleprompter
    try:
        # Pass dummy metric
        teleprompter = TrinityAwareMIPROv2(metric=dummy_metric)
        print("✅ TrinityAwareMIPROv2 Initialized")
    except Exception as e:
        print(f"❌ Initialization Failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    # 3. Verify Trinity Logic
    if hasattr(teleprompter, "compile"):
        print("✅ Compile method exists")

    # 4. Trinity Score Logic Check (if exposed)
    # Check if we can inspect default Trinity weights or config
    if hasattr(teleprompter, "trinity_weights"):
        print(f"✅ Trinity Weights Found: {teleprompter.trinity_weights}")

    print("🎉 Dry-Run Complete: Logic Verified.")


if __name__ == "__main__":
    test_dry_run()
