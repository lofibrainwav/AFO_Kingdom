# packages/afo-core/conftest.py - Local pytest configuration
# 모든 테스트 활성화 (심볼릭 링크로 import 문제 해결됨)

from unittest.mock import MagicMock, patch

import pytest

# 테스트 제외 없음 - 모든 테스트 실행
collect_ignore: list[str] = []


@pytest.fixture(autouse=True)
def mock_workflow():
    """Global patch for workflow to ensure api_server lifespan starts correctly."""
    # We patch both potential import paths to be safe
    with patch("api_server.workflow", MagicMock()) as mock_wf:
        mock_wf.compile.return_value = MagicMock()
        yield mock_wf
