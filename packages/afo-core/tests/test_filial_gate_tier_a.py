import os
from pathlib import Path

import pytest

from AFO.filial_gate_engine import filial_gate


def test_hard_lock_trigger_0_0_0_0(tmp_path):
    """Tier A should fail if 0.0.0.0 is present in code"""
    test_file = tmp_path / "app.py"
    test_file.write_text('app.run(host="0.0.0.0")')

    # We need to point the hard lock script to this tmp_path
    # In practice, filial_gate.ROOT_DIR is hardcoded, so we'll mock or adjust for test
    # For now, let's test the shell script directly or mock _run_hard_lock

    # Mocking op for test
    op = {"name": "test_op", "manual_steps_required": 0, "mypy_errors": 0}

    # Since ROOT_DIR is hardcoded in FilialGateEngine, we test the logic via subprocess
    script_path = Path("/Users/brnestrm/AFO_Kingdom/packages/afo-core/scripts/filial_hard_lock.sh")
    log_file = tmp_path / "scan.log"

    import subprocess

    result = subprocess.run([str(script_path), str(tmp_path), str(log_file)])
    assert result.returncode != 0
    assert "0.0.0.0 binding detected" in log_file.read_text()


def test_hard_lock_trigger_cors_wildcard(tmp_path):
    """Tier A should fail if CORS wildcard is used"""
    test_file = tmp_path / "settings.py"
    test_file.write_text('ALLOW_ORIGINS = ["*"]')

    script_path = Path("/Users/brnestrm/AFO_Kingdom/packages/afo-core/scripts/filial_hard_lock.sh")
    log_file = tmp_path / "scan.log"

    import subprocess

    result = subprocess.run([str(script_path), str(tmp_path), str(log_file)])
    assert result.returncode != 0
    assert "CORS Wildcard detected" in log_file.read_text()


def test_quality_gate_baseline_increment():
    """Tier B should fail if errors INCREASE, but pass if they STAY SAME or DECREASE"""
    # Create baseline
    engine = filial_gate
    engine.BASELINE_FILE.write_text("10")

    # Same count -> Pass
    op_same = {"mypy_errors": 10}
    assert engine._check_quality_baseline(op_same) is True

    # Lower count -> Pass
    op_lower = {"mypy_errors": 5}
    assert engine._check_quality_baseline(op_lower) is True

    # Higher count -> Fail
    op_higher = {"mypy_errors": 15}
    assert engine._check_quality_baseline(op_higher) is False


def test_dual_layer_sealing(tmp_path):
    """Check if mode=LOCAL vs SEAL impacts file location"""
    engine = filial_gate
    op = {"name": "test_seal"}
    results = {"passed": True, "gates": {}}

    # 1. LOCAL Mode
    engine._seal_operation(op, results, mode="LOCAL")
    local_files = list(engine.LOCAL_LOG_DIR.glob("FILIAL_GATE_*.json"))
    assert len(local_files) > 0

    # 2. SEAL Mode
    engine._seal_operation(op, results, mode="SEAL")
    ssot_files = list(engine.SSOT_LOG_DIR.glob("FILIAL_GATE_*.json"))
    assert len(ssot_files) > 0
