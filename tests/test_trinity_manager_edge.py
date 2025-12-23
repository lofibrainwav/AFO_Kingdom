# tests/test_trinity_manager_edge.py (Edge Case Tests)
import os
import pathlib
import sys

import pytest

# Ensure AFO package is importable
sys.path.append(
    pathlib.Path(
        os.path.join(pathlib.Path(__file__).parent, "../packages/afo-core")
    ).resolve()
)

from AFO.domain.metrics.trinity_manager import trinity_manager


@pytest.fixture(autouse=True)
def reset_trinity():
    """Reset accumulated deltas before each test."""
    trinity_manager.deltas = {
        "truth": 0.0,
        "goodness": 0.0,
        "beauty": 0.0,
        "filial_serenity": 0.0,
        "eternity": 0.0,
    }


def test_upper_limit_cap():
    """Test delta accumulation exceeds 100% (should be clamped)."""
    # Trigger VERIFICATION_SUCCESS (+5 Truth) 25 times = +125%
    for _ in range(25):
        trinity_manager.apply_trigger("VERIFICATION_SUCCESS")

    metrics = trinity_manager.get_current_metrics()
    assert metrics.truth == 1.0  # Clamped, not 2.25
    assert metrics.trinity_score <= 1.0


def test_lower_limit_cap():
    """Test delta accumulation drops below 0% (should be clamped)."""
    # Trigger MANUAL_INTERVENTION (-5 Serenity) 25 times = -125%
    for _ in range(25):
        trinity_manager.apply_trigger("MANUAL_INTERVENTION")

    metrics = trinity_manager.get_current_metrics()
    assert metrics.filial_serenity == 0.0  # Clamped, not -0.25


def test_invalid_action():
    """Test invalid action string (should be ignored)."""
    initial = trinity_manager.get_current_metrics()
    trinity_manager.apply_trigger("INVALID_ACTION_NAME")
    after = trinity_manager.get_current_metrics()

    assert initial.trinity_score == after.trinity_score


def test_concurrent_updates_logic():
    """Simulate sequence of mixed updates to verify stable state."""
    # This isn't true threading concurrency, but logic sequence correctness.
    actions = [
        "VERIFICATION_SUCCESS",  # T+5, G+2
        "MANUAL_INTERVENTION",  # S-5
        "VERIFICATION_FAIL",  # T-10, G-5
        "INVALID",  # No change
        "DRY_RUN_ACTIVE",  # G+10, G+5 (Risk -5 -> G+5) -> G+15
    ]
    for action in actions:
        trinity_manager.apply_trigger(action)

    metrics = trinity_manager.get_current_metrics()

    # Truth: 0 + 5 - 10 = -5 (-0.05) -> 1.0 - 0.05 = 0.95
    assert round(metrics.truth, 2) == 0.95

    # Goodness: 0 + 2 - 5 + 15 = +12 (+0.12) -> 1.0 + 0.12 = 1.12 -> Clamped 1.0
    assert metrics.goodness == 1.0

    # Serenity: 0 - 5 = -5 (-0.05) -> 1.0 - 0.05 = 0.95
    assert round(metrics.filial_serenity, 2) == 0.95
