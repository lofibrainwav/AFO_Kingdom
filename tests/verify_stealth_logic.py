import asyncio
import os
import pathlib
import sys
from unittest.mock import AsyncMock

# Add AFO to path
sys.path.append(
    os.path.join(
        pathlib.Path(pathlib.Path(pathlib.Path(__file__).resolve()).parent).parent,
        "AFO",
    )
)

from browser_auth.stealth_login import Stealther


async def verify_stealth_logic():
    mock_page = AsyncMock()
    await Stealther.apply_stealth(mock_page)

    scripts = [call.args[0] for call in mock_page.add_init_script.call_args_list]

    checks = {
        "webdriver": "navigator, 'webdriver'",
        "languages": "navigator, 'languages'",
        "plugins": "navigator, 'plugins'",
        "chrome": "window.chrome",
    }

    all_passed = True
    for substring in checks.values():
        if any(substring in s for s in scripts):
            pass
        else:
            all_passed = False

    if all_passed:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(verify_stealth_logic())
