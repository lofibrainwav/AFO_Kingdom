# Trinity Score: 90.0 (Established by Chancellor)
"""Grok Chrome Launch - Identity Verification
Phase 15: The Grok Singularity

Description:
    Launches User's ACTUAL Chrome Profile via Playwright.
    Navigates to x.com and extracts cookies from the live session.
"""

import json
import os
import time

from playwright.sync_api import sync_playwright

SESSION_FILE = "secrets/grok_session.json"
USER_DATA_DIR = os.path.expanduser("~/Library/Application Support/Google/Chrome")


def steal_identity():
    print("🕵️‍♂️ [GrokLink] Launching YOUR Chrome Profile...")

    with sync_playwright() as p:
        try:
            # Launch Persistent Context (Loads user profile)
            # channel="chrome" uses the installed Google Chrome
            context = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ],  # Try to hide automation
            )

            page = context.pages[0] if context.pages else context.new_page()

            print("🚀 Navigating to x.com...")
            page.goto("https://x.com/home")

            # Wait for load
            time.sleep(5)

            print("🍪 Extracting Cookies...")
            cookies = context.cookies("https://x.com")

            auth_token = None
            ct0 = None

            for c in cookies:
                if c["name"] == "auth_token":
                    auth_token = c["value"]
                    print(f"🔥 Found auth_token: {auth_token[:6]}...")
                elif c["name"] == "ct0":
                    ct0 = c["value"]

            if auth_token:
                os.makedirs("secrets", exist_ok=True)
                secrets = {"auth_token": auth_token}
                if ct0:
                    secrets["ct0"] = ct0

                with open(SESSION_FILE, "w") as f:
                    json.dump(secrets, f, indent=2)
                print(f"✅ Session saved to {SESSION_FILE}")
                print("🎉 SUCCESS! You can close this Chrome window now.")
            else:
                print("❌ auth_token NOT found in this profile.")
                print(
                    "   Note: If you use a specific profile (Profile 1, etc.), Playwright might load Default."
                )
                print("   Trying to navigate to /i/grok to verify...")
                page.goto("https://x.com/i/grok")
                time.sleep(5)

            # Keep open for a bit so user can see
            time.sleep(10)
            context.close()

        except Exception as e:
            print(f"⚠️ Launch Failed: {e}")
            print("   (Chrome must be COMPLETELY closed for this to work)")


if __name__ == "__main__":
    steal_identity()
