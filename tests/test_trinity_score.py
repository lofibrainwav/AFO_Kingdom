import os
import pathlib
import sys

import numpy as np
import pytest


# Ensure packages/afo-core is in python path
sys.path.append(
    pathlib.Path(
        os.path.join(pathlib.Path(__file__).parent, "../packages/afo-core")
    ).resolve()
)

from services.trinity_calculator import SSOT_WEIGHTS, trinity_calculator


def test_perfect_score_real():
    raw = [1.0, 1.0, 1.0, 1.0, 1.0]
    score = trinity_calculator.calculate_trinity_score(raw)
    assert score == 100.0, f"Expected 100.0, got {score}"
    assert np.isclose(sum(SSOT_WEIGHTS), 1.0), "SSOT Weights sum mismatch"


def test_risk_failure_real():
    # Truth=1.0, Goodness=0.0, Beauty=1.0, Serenity=1.0, Eternity=1.0
    # Score = 35 + 0 + 20 + 8 + 2 = 65.0
    raw = [1.0, 0.0, 1.0, 1.0, 1.0]
    score = trinity_calculator.calculate_trinity_score(raw)
    assert score == 65.0, f"Expected 65.0, got {score}"
    assert score < 70.0


def test_partial_score_real():
    # Partial Beauty (0.85)
    # Score = 35 + 35 + (20*0.85) + 8 + 2
    # = 35 + 35 + 17 + 8 + 2 = 97.0
    raw = [1.0, 1.0, 0.85, 1.0, 1.0]
    score = trinity_calculator.calculate_trinity_score(raw)
    assert score == 97.0, f"Expected 97.0, got {score}"


def test_edge_constraints_real():
    with pytest.raises(ValueError):
        trinity_calculator.calculate_trinity_score([1.0])
    with pytest.raises(AssertionError):
        trinity_calculator.calculate_trinity_score([1.5, 1.0, 1.0, 1.0, 1.0])
