"""
Grok Interactive Auth - The Biometric Handshake
Phase 15: The Grok Singularity

Description:
    Launches a VISIBLE Chrome window (System Chrome).
    Waits for the user to manually log in (supporting Touch ID/2FA).
    Automatically captures 'auth_token' once login is detected.
"""

import json
import os
import sys
import time

from playwright.sync_api import sync_playwright

SESSION_FILE = "secrets/grok_session.json"


def interactive_login():
    print("🔒 [GrokAuth] Initiating Secure Browser Session...")
    print("👉 Please log in to x.com when the browser opens.")
    print("👉 Use your Touch ID / Password / 2FA.")

    with sync_playwright() as p:
        try:
            # Launch System Chrome in Headed mode (Visible)
            # We use a temporary user data dir to avoid 'Profile Locked' errors
            # The user will need to login freshly, but this guarantees it works.
            browser = p.chromium.launch(
                channel="chrome",
                headless=False,
                args=["--no-sandbox", "--disable-infobars"],
            )

            # Create a context
            context = browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()

            print("🚀 Opening https://x.com/i/grok ...")
            page.goto("https://x.com/i/grok")

            print(
                "⏳ Waiting for authentication... (I am watching for the 'auth_token' cookie)"
            )

            # Polling for auth_token
            max_retries = 300  # Wait up to 5 minutes
            found_token = None

            for i in range(max_retries):
                cookies = context.cookies("https://x.com")
                auth_token = next(
                    (c["value"] for c in cookies if c["name"] == "auth_token"), None
                )
                ct0 = next((c["value"] for c in cookies if c["name"] == "ct0"), None)

                if auth_token:
                    print(f"\n✅ AUTHENTICATION DETECTED! Token: {auth_token[:6]}...")

                    # Save immediately
                    os.makedirs("secrets", exist_ok=True)
                    secrets = {"auth_token": auth_token, "ct0": ct0 or ""}
                    with open(SESSION_FILE, "w") as f:
                        json.dump(secrets, f, indent=2)

                    print(f"💾 Session saved to {SESSION_FILE}")
                    found_token = auth_token
                    break

                # Feedback every 5 seconds
                if i % 5 == 0:
                    sys.stdout.write(".")
                    sys.stdout.flush()

                time.sleep(1)

            if found_token:
                print("\n🎉 SUCCESS! You may close the browser now.")
                # Give user a moment to see the success
                time.sleep(5)
            else:
                print("\n❌ Timed out waiting for login.")

            browser.close()

        except Exception as e:
            print(f"\n⚠️ Browser Error: {e}")
            print("   Make sure Google Chrome is installed in the default location.")


if __name__ == "__main__":
    interactive_login()
