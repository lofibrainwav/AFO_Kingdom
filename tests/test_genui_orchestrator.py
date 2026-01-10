import pathlib
import shutil
from unittest.mock import AsyncMock, patch

import pytest

from AFO.domain.serenity.genui_orchestrator import GenUISpec, genui_orchestrator


@pytest.mark.asyncio
async def test_create_sub_app_flow():
    # Mock Jwaja response to avoid real model call
    mock_code = """
    ```tsx
    import React from 'react';
    export default function Page() {
        return <div>Hello GenUI</div>;
    }
    ```
    """

    # Patch yeongdeok.consult_jwaja
    with patch(
        "AFO.scholars.yeongdeok.yeongdeok.consult_jwaja", new_callable=AsyncMock
    ) as mock_consult:
        mock_consult.return_value = mock_code

        spec = GenUISpec(
            app_id="test-app-001",
            description="Test Dashboard",
            requirements=["Simple div"],
        )

        # Execute
        result = await genui_orchestrator.create_sub_app(spec)

        # Verify
        assert result["status"] == "deployed"
        assert result["url"] == "/genui/test-app-001"
        assert pathlib.Path(result["path"]).exists()

        # Check Content
        with pathlib.Path(result["path"]).open(encoding="utf-8") as f:
            content = f.read()
            assert "export default function Page()" in content
            assert "```" not in content  # Markdown stripped

        # Cleanup
        shutil.rmtree("packages/dashboard/src/app/genui/test-app-001")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_create_sub_app_flow())
