import pytest
from unittest.mock import Mock, AsyncMock
import sys
import os

# Ensure packages/afo-core is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

@pytest.fixture
def mock_antigravity():
    mock = Mock()
    mock.AUTO_DEPLOY = True
    mock.DRY_RUN_DEFAULT = False
    return mock

@pytest.fixture
def mock_strategists():
    zhuge = AsyncMock()
    sima = AsyncMock()
    zhou = AsyncMock()
    
    zhuge.evaluate.return_value = 1.0
    sima.review.return_value = 1.0
    zhou.optimize.return_value = 1.0
    
    return zhuge, sima, zhou

@pytest.fixture
def mock_tigers():
    guan = Mock()
    guan.guard.return_value = 1.0
    zhang = Mock()
    zhang.gate.return_value = 1.0
    zhao = Mock()
    zhao.craft.return_value = "<div>Code</div>"
    ma = Mock()
    ma.deploy.return_value = True
    huang = Mock()
    huang.log.return_value = True
    
    return guan, zhang, zhao, ma, huang
