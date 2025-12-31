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
