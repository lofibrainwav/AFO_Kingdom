import pytest
import os
import shutil
from unittest.mock import AsyncMock, patch
from AFO.domain.serenity.genui_orchestrator import genui_orchestrator, GenUISpec

@pytest.mark.asyncio
async def test_create_sub_app_flow():
    print("\n🎨 Testing GenUI Orchestrator...")
    
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
    with patch('AFO.scholars.yeongdeok.yeongdeok.consult_jwaja', new_callable=AsyncMock) as mock_consult:
        mock_consult.return_value = mock_code
        
        spec = GenUISpec(
            app_id="test-app-001",
            description="Test Dashboard",
            requirements=["Simple div"]
        )
        
        # Execute
        result = await genui_orchestrator.create_sub_app(spec)
        
        # Verify
        assert result["status"] == "deployed"
        assert result["url"] == "/genui/test-app-001"
        assert os.path.exists(result["path"])
        
        # Check Content
        with open(result["path"], "r") as f:
            content = f.read()
            assert "export default function Page()" in content
            assert "```" not in content  # Markdown stripped
            
        print("✅ GenUI Creation Verified")
        
        # Cleanup
        shutil.rmtree("packages/dashboard/src/app/genui/test-app-001")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_create_sub_app_flow())
