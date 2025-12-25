import os
import sys


# Add package root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

try:
    from AFO.domain.janus.contract import VisualAction, VisualPlan
    from AFO.serenity.visual_agent import VisualAgent

    print("✅ Import Successful: Janus Contract & Visual Agent")
except ImportError as e:
    print(f"❌ Import Failed: {e}")
    sys.exit(1)

# Test Schema
try:
    # Test strict validation (Confidence < 0.7 logic is in Agent, but Schema is base)
    action = VisualAction(
        type="click",
        bbox={"x": 0.5, "y": 0.5, "w": 0.1, "h": 0.1},
        confidence=0.9,
        why="Test",
        safety="safe",
    )
    print("✅ Schema Validation Passed")
except Exception as e:
    print(f"❌ Schema Validation Failed: {e}")
    sys.exit(1)

# Test Agent Logic (Dry Run)
agent = VisualAgent()
print(f"✅ Visual Agent Initialized with model: {agent.model}")
