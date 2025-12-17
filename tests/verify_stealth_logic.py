import sys
import os
import asyncio
from unittest.mock import AsyncMock

# Add AFO to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "AFO"))

from browser_auth.stealth_login import Stealther

async def verify_stealth_logic():
    print("running verification...")
    mock_page = AsyncMock()
    await Stealther.apply_stealth(mock_page)
    
    scripts = [call.args[0] for call in mock_page.add_init_script.call_args_list]
    
    checks = {
        "webdriver": "navigator, 'webdriver'",
        "languages": "navigator, 'languages'",
        "plugins": "navigator, 'plugins'",
        "chrome": "window.chrome"
    }
    
    all_passed = True
    for name, substring in checks.items():
        if any(substring in s for s in scripts):
            print(f"✅ Stealth Check Passed: {name}")
        else:
            print(f"❌ Stealth Check Failed: {name}")
            all_passed = False
            
    if all_passed:
        print("\n🎉 ALL STEALTH LOGIC VERIFIED.")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(verify_stealth_logic())
