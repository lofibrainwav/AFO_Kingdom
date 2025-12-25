# Trinity Score: 90.0 (Established by Chancellor)
"""
Grok Interactive Auth - Stealth Mode (CDP)
Phase 15: The Grok Singularity

Description:
    Launches Google Chrome via Subprocess with Debugging Port (9222).
    Connects Playwright via CDP to bypass "Browser not secure" checks.
    Allows user to login via Google/TouchID without detection.
"""

import json
import os
import shutil
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

SESSION_FILE = "secrets/grok_session.json"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
USER_DATA_DIR = "/tmp/grok-stealth-profile"


def find_chrome():
    """Finds the confirmed Chrome executable on macOS"""
    if os.path.exists(CHROME_PATH):
        return CHROME_PATH
    # Fallback search
    for app in ["Google Chrome", "Chrome"]:
        path = f"/Applications/{app}.app/Contents/MacOS/{app}"
        if os.path.exists(path):
            return path
    return None


def interactive_login_stealth():
    print("🕵️‍♂️ [StealthAuth] Preparing Stealth Environment...")

    chrome_bin = find_chrome()
    if not chrome_bin:
        print("❌ Google Chrome not found in /Applications. Please install it.")
        return

    # 1. Launch Chrome as a separate process (Not controlled by Playwright yet)
    # This prevents the 'Navigator.webdriver' flag from being set initially in some cases,
    # or allows us to attach loosely.
    print("🚀 Launching Chrome (CDP Mode) on port 9222...")

    # Clean prev profile for fresh start logic, or keep it?
    # User wants 'auth saved', but if we error out, fresh is safer.
    # Let's try to keep it if exists to save partial progress, but likely empty.
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    cmd = [
        chrome_bin,
        "--remote-debugging-port=9222",
        f"--user-data-dir={USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        # Flags to help bypass detection
        "--disable-blink-features=AutomationControlled",
        "https://x.com/i/grok",
    ]

    # Launch detached
    proc = subprocess.Popen(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Give it time to spin up
    print("⏳ Waiting for Chrome to warm up (5s)...")
    time.sleep(5)

    try:
        with sync_playwright() as p:
            print("🔗 Connecting to Chrome via CDP...")
            max_connect_retries = 5
            browser = None

            for _attempt in range(max_connect_retries):
                try:
                    browser = p.chromium.connect_over_cdp("http://localhost:9222")
                    break
                except Exception:
                    time.sleep(1)

            if not browser:
                print("❌ Failed to connect to Chrome. Port 9222 blocked?")
                proc.kill()
                return

            context = browser.contexts[0]

            print("\n🔒 [StealthAuth] Browser Connected!")
            print("👉 Please log in to x.com inside the opened Chrome window.")
            print("👉 'Google Sign-In' should work now.")

            # Polling for auth_token
            max_retries = 600  # 10 minutes (give ample time for MFA)
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

                # Feedback
                if i % 5 == 0:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                time.sleep(1)

            if found_token:
                print("\n🎉 SUCCESS! Closing stealth browser...")
            else:
                print("\n❌ Login Timed Out.")

            browser.close()

    except Exception as e:
        print(f"\n⚠️ Unexpected Error: {e}")
    finally:
        # Cleanup the subprocess
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()
        print("🧹 Cleanup complete.")


if __name__ == "__main__":
    interactive_login_stealth()
