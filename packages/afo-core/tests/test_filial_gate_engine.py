import os
import shutil

import pytest

from AFO.filial_gate_engine import filial_gate


@pytest.fixture(autouse=True)
def cleanup():
    # Setup
    if filial_gate.LOG_DIR.exists():
        shutil.rmtree(filial_gate.LOG_DIR)
    yield
    # No teardown needed to keep logs for CI step if running locally


def test_serenity_check_pass():
    op = {"disruption_level": 2, "manual_steps_required": 1}
    res = filial_gate.check_serenity(op)
    assert res["passed"] is True
    assert res["friction_score"] == 0.1
    # Check if seal exists
    seals = list(filial_gate.LOG_DIR.glob("ssot_filial_seal_*.json"))
    assert len(seals) == 1


def test_serenity_check_fail_disruption():
    op = {"disruption_level": 7, "manual_steps_required": 1}
    res = filial_gate.check_serenity(op)
    assert res["passed"] is False
    assert res["gates"]["serenity_first"] is False


def test_serenity_check_fail_friction():
    op = {"disruption_level": 2, "manual_steps_required": 5}
    res = filial_gate.check_serenity(op)
    assert res["passed"] is False
    assert res["gates"]["friction_check"] is False
