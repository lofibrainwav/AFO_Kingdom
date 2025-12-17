import pytest
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add AFO to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "AFO"))

from browser_auth.stealth_login import Stealther

@pytest.mark.asyncio
async def test_apply_stealth():
    """
    Verify that Stealther applies the necessary evasion scripts to the page.
    """
    mock_page = AsyncMock()
    
    await Stealther.apply_stealth(mock_page)
    
    # Check that add_init_script was called for the key evasions
    assert mock_page.add_init_script.call_count >= 4
    
    # Extract all scripts passed to add_init_script
    scripts = [call.args[0] for call in mock_page.add_init_script.call_args_list]
    
    # internal logic check: look for webdriver masking
    assert any("navigator, 'webdriver'" in s for s in scripts)
    # logic check: look for language mocking
    assert any("navigator, 'languages'" in s for s in scripts)
    # logic check: look for plugins mocking
    assert any("navigator, 'plugins'" in s for s in scripts)
    # logic check: look for chrome runtime
    assert any("window.chrome" in s for s in scripts)

    print("✅ Stealth Evasion Logic Verified: Webdriver, Languages, Plugins, Chrome Runtime masked.")
