# tests/test_trinity_manager.py (TrinityManager unit tests)
import pytest
import sys
import os

# Ensure AFO package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

from AFO.domain.metrics.trinity_manager import trinity_manager

@pytest.fixture(autouse=True)
def reset_trinity():
    """Reset accumulated deltas before each test."""
    trinity_manager.deltas = {
        "truth": 0.0,
        "goodness": 0.0,
        "beauty": 0.0,
        "filial_serenity": 0.0,
        "eternity": 0.0
    }
    yield

def test_initial_score():
    """Test initial score is perfect (100%)."""
    metrics = trinity_manager.get_current_metrics()
    assert metrics.trinity_score == pytest.approx(1.0)
    assert metrics.balance_status == "balanced"

def test_dry_run_action():
    """Test DRY_RUN trigger action (Goodness +10, Risk -5)."""
    # Note: Logic in Manager: "goodness" delta += 10. Risk -5 (means Goodness delta -= -5 -> +5?)
    # Wait, check trinity_manager.py logic.
    # "DRY_RUN_ACTIVE": {"goodness": 10.0, "risk": -5.0},
    # if key == "risk": self.deltas["goodness"] -= value
    # So: Goodness += 10. Risk (-5) -> Goodness -= (-5) -> Goodness += 5.
    # Total Goodness Delta = 15.
    
    trinity_manager.apply_trigger("DRY_RUN_ACTIVE")
    metrics = trinity_manager.get_current_metrics()
    
    # 1.0 + 0.15 = 1.15 -> Clamped to 1.0
    assert metrics.goodness == pytest.approx(1.0)
    assert metrics.trinity_score == pytest.approx(1.0)

def test_manual_intervention():
    """Test MANUAL_INTERVENTION trigger (-Serenity)."""
    # "MANUAL_INTERVENTION": {"filial_serenity": -5.0} -> -0.05
    trinity_manager.apply_trigger("MANUAL_INTERVENTION")
    metrics = trinity_manager.get_current_metrics()
    
    # Initial 1.0 - 0.05 = 0.95
    assert round(metrics.filial_serenity, 2) == 0.95
    # Trinity Score affects weighted sum.
    # weights: T(.35) + G(.35) + B(.20) + S(.08) + E(.02)
    # Delta S (-0.05) * Weight S (0.08) = -0.004
    # Expected Score: 1.0 - 0.004 = 0.996
    assert round(metrics.trinity_score, 3) == 0.996

def test_verification_pass():
    """Test VERIFICATION_SUCCESS trigger."""
    # "VERIFICATION_SUCCESS": {"truth": 5.0, "goodness": 2.0} -> +0.05 T, +0.02 G
    trinity_manager.apply_trigger("VERIFICATION_SUCCESS")
    metrics = trinity_manager.get_current_metrics()
    
    assert metrics.truth == 1.0 # Clamped
    assert metrics.goodness == 1.0 # Clamped

def test_multiple_actions():
    """Test accumulated deltas over multiple actions."""
    # 1. Manual Intervention (-0.05 S)
    trinity_manager.apply_trigger("MANUAL_INTERVENTION")
    
    # 2. Verification Fail (-0.10 T, +0.05 Risk -> -0.05 G)
    # "VERIFICATION_FAIL": {"truth": -10.0, "risk": 5.0}
    # risk handles as: self.deltas["goodness"] -= value -> G -= 5.0 (-0.05)
    trinity_manager.apply_trigger("VERIFICATION_FAIL")
    
    metrics = trinity_manager.get_current_metrics()
    
    # Truth: 1.0 - 0.10 = 0.90
    assert round(metrics.truth, 2) == 0.90
    
    # Goodness: 1.0 - 0.05 = 0.95
    assert round(metrics.goodness, 2) == 0.95
    
    # Serenity: 1.0 - 0.05 = 0.95
    assert round(metrics.filial_serenity, 2) == 0.95
