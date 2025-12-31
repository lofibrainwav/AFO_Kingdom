import os

import pytest

# Import from AFO package
from AFO.mipro_optimizer import MiproOptimizer
from AFO.trinity_metric_wrapper import TrinityMetricWrapper


def test_mipro_disabled_raises():
    metric = TrinityMetricWrapper(lambda prompt, target: 0.5)
    opt = MiproOptimizer(metric)
    os.environ.pop("AFO_MIPRO_ENABLED", None)
    with pytest.raises(RuntimeError):
        opt.optimize(["p1"], "t")


def test_mipro_selects_best():
    metric = TrinityMetricWrapper(lambda prompt, target: 1.0 if prompt == "best" else 0.1)
    opt = MiproOptimizer(metric)
    os.environ["AFO_MIPRO_ENABLED"] = "1"
    res = opt.optimize(["bad", "best"], "t")
    assert res.best_prompt == "best"
    assert res.best_score == 1.0


def test_mipro_node_noop_when_disabled():
    """Test that MIPRO node is truly NO-OP when flags are disabled."""
    from AFO.chancellor_graph import ChancellorGraph

    # Mock state to track changes
    class MockState:
        def __init__(self):
            self.outputs = {}
            self.trace_id = "test-noop"
            self.step = "MIPRO"

    # Test with flags OFF
    os.environ.pop("AFO_MIPRO_ENABLED", None)
    os.environ.pop("AFO_MIPRO_CHANCELLOR_ENABLED", None)

    # Create ChancellorGraph instance to access mipro_node
    cg = ChancellorGraph()
    # Access the mipro_node function via internal method
    nodes_dict = {
        "CMD": lambda s: s,
        "PARSE": lambda s: s,
        "TRUTH": lambda s: s,
        "GOODNESS": lambda s: s,
        "BEAUTY": lambda s: s,
        "MERGE": lambda s: s,
        "EXECUTE": lambda s: s,
        "VERIFY": lambda s: s,
        "REPORT": lambda s: s,
    }

    # Trigger node creation (this adds MIPRO to nodes_dict)
    cg.run_v2({"command": "test"})

    # Get the MIPRO node
    mipro_node = nodes_dict.get("MIPRO")
    assert mipro_node is not None, "MIPRO node should always be registered"

    # Test NO-OP behavior
    initial_outputs = {"existing": "data"}
    state = MockState()
    state.outputs = initial_outputs.copy()

    # Call MIPRO node with flags OFF
    result_state = mipro_node(state)

    # Verify NO-OP: outputs should be unchanged
    assert result_state.outputs == initial_outputs, "MIPRO node should be NO-OP when disabled"
    assert "_mipro" not in result_state.outputs, "No MIPRO output should be added when disabled"
