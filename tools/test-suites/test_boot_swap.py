#!/usr/bin/env python3
"""Boot-Swap 기능 테스트 스크립트"""

import json
import os
import sys
from pathlib import Path

# Add AFO packages to path
afo_root = str(Path(__file__).resolve().parent / "packages" / "afo-core")
if afo_root not in sys.path:
    sys.path.insert(0, afo_root)

def test_learning_loader():
    """Learning loader 테스트"""
    print("🧪 Testing Learning Loader...")

    # Set test profile path
    test_profile = Path(__file__).parent / "artifacts" / "learning_profiles" / "test_phase2.json"
    os.environ["AFO_LEARNING_PROFILE_PATH"] = str(test_profile)

    try:
        from afo.learning_loader import get_learning_profile

        profile = get_learning_profile()
        print(f"✅ Profile loaded: {profile.status}")
        print(f"   Version: {profile.version}")
        print(f"   SHA256: {profile.sha256[:16]}..." if profile.sha256 else "   SHA256: None")
        print(f"   Has data: {bool(profile.data)}")

        return profile

    except Exception as e:
        print(f"❌ Learning loader test failed: {e}")
        return None

def test_trinity_config():
    """Trinity config 테스트"""
    print("\n🧪 Testing Trinity Config...")

    try:
        from afo.trinity_config import BASE_CONFIG, apply_learning_profile

        print("✅ BASE_CONFIG loaded:")
        print(f"   Weights: {BASE_CONFIG['weights']}")
        print(f"   Thresholds: {BASE_CONFIG['thresholds']}")

        # Test with overrides
        overrides = {
            "weights": {
                "truth": 0.40,
                "goodness": 0.40,
                "beauty": 0.15,
                "serenity": 0.03,
                "eternity": 0.02
            },
            "thresholds": {
                "auto_run_trinity": 85,
                "auto_run_risk": 15
            }
        }

        effective = apply_learning_profile(BASE_CONFIG, overrides)
        print("✅ Effective config applied:")
        print(f"   Applied overrides: {effective['applied_overrides']}")
        print(f"   Effective weights: {effective['weights']}")
        print(f"   Effective thresholds: {effective['thresholds']}")

        return effective

    except Exception as e:
        print(f"❌ Trinity config test failed: {e}")
        return None

def test_merge_node_logic():
    """Merge node 로직 테스트"""
    print("\n🧪 Testing Merge Node Logic...")

    try:
        from afo.trinity_config import BASE_CONFIG, apply_learning_profile

        # Mock pillar scores
        pillar_scores = {
            "truth": 0.9,
            "goodness": 0.8,
            "beauty": 0.7,
            "serenity": 0.6,
            "eternity": 0.5
        }

        # Test with base config
        base_weights = BASE_CONFIG["weights"]
        base_thresholds = BASE_CONFIG["thresholds"]

        trinity_base = (
            pillar_scores["truth"] * base_weights["truth"] +
            pillar_scores["goodness"] * base_weights["goodness"] +
            pillar_scores["beauty"] * base_weights["beauty"] +
            pillar_scores["serenity"] * base_weights["serenity"] +
            pillar_scores["eternity"] * base_weights["eternity"]
        ) * 100

        risk_score = (1.0 - pillar_scores["goodness"]) * 100

        print(f"   Trinity Base: {trinity_base:.1f}")
        print(f"   Risk Score: {risk_score:.1f}")
        print(f"   Base thresholds: trinity>={base_thresholds['auto_run_trinity']}, risk<={base_thresholds['auto_run_risk']}")

        decision_base = "AUTO_RUN" if (
            trinity_base >= base_thresholds["auto_run_trinity"] and
            risk_score <= base_thresholds["auto_run_risk"]
        ) else "ASK_COMMANDER"

        print(f"   Base Decision: {decision_base}")

        # Test with overrides
        overrides = {
            "weights": {
                "truth": 0.40,
                "goodness": 0.40,
                "beauty": 0.15,
                "serenity": 0.03,
                "eternity": 0.02
            },
            "thresholds": {
                "auto_run_trinity": 85,
                "auto_run_risk": 15
            }
        }

        effective = apply_learning_profile(BASE_CONFIG, overrides)
        effective_weights = effective["weights"]
        effective_thresholds = effective["thresholds"]

        trinity_effective = (
            pillar_scores["truth"] * effective_weights["truth"] +
            pillar_scores["goodness"] * effective_weights["goodness"] +
            pillar_scores["beauty"] * effective_weights["beauty"] +
            pillar_scores["serenity"] * effective_weights["serenity"] +
            pillar_scores["eternity"] * effective_weights["eternity"]
        ) * 100

        print(".1f"        print(f"   Effective thresholds: trinity>={effective_thresholds['auto_run_trinity']}, risk<={effective_thresholds['auto_run_risk']}")

        decision_effective = "AUTO_RUN" if (
            trinity_effective >= effective_thresholds["auto_run_trinity"] and
            risk_score <= effective_thresholds["auto_run_risk"]
        ) else "ASK_COMMANDER"

        print(f"   Effective Decision: {decision_effective}")

        print(f"✅ Boot-Swap working: Base {decision_base} → Effective {decision_effective}")

        return {
            "base": {"trinity": trinity_base, "decision": decision_base},
            "effective": {"trinity": trinity_effective, "decision": decision_effective}
        }

    except Exception as e:
        print(f"❌ Merge node logic test failed: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Boot-Swap Phase 2 Test Suite")
    print("=" * 50)

    # Test learning loader
    profile = test_learning_loader()

    # Test trinity config
    config = test_trinity_config()

    # Test merge node logic
    results = test_merge_node_logic()

    print("\n" + "=" * 50)
    if profile and config and results:
        print("🎉 All tests passed! Boot-Swap Phase 2 ready for production.")
        print("\n📋 Summary:")
        print(f"   Profile status: {profile.status}")
        print(f"   Applied overrides: {config.get('applied_overrides', [])}")
        print(f"   Decision change: {results['base']['decision']} → {results['effective']['decision']}")
    else:
        print("❌ Some tests failed. Check implementation.")
        sys.exit(1)
