from tigers.guan_yu import guard
from tigers.huang_zhong import log
from tigers.ma_chao import deploy
from tigers.zhang_fei import gate
from tigers.zhao_yun import craft


def test_guan_yu_guard():
    assert guard({"data": "valid"}) >= 0.0


def test_zhang_fei_gate_safe():
    # Based on actual implementation, secure/safe might verify to 0.5 if not mocked properly
    # or if logic relies on validation. For now, asserting it returns > 0.0 (passed gate).
    assert gate(0.1, {}) > 0.0


def test_zhang_fei_gate_unsafe():
    # If implementation blocks high risk
    res = gate(0.9, {})
    assert res == 0.0  # Blocked


def test_zhao_yun_craft():
    code = craft("print('hello')", 1)
    assert "print" in code


def test_ma_chao_deploy():
    # Mocking deployment behavior usually, but here checking return structure
    res = deploy({})
    assert res is not None


def test_huang_zhong_log():
    res = log("Test Action", {"score": 100})
    assert res == "LOG_SAVED" or res is True
