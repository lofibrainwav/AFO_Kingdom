# Trinity Score: 90.0 (Established by Chancellor)
"""Grok Safari Connect - The Apple Link
Phase 15: The Grok Singularity

Description:
    Tries to extract cookies from Safari (Cookies.binarycookies).
    Requires Full Disk Access for Terminal/Python on macOS.
"""

import json
import os

import browser_cookie3

SESSION_FILE = "secrets/grok_session.json"


def extract_safari_token():
    print("🍎 [GrokLink] Scanning Safari for x.com keys...")

    try:
        # Load Safari Cookies
        cj = browser_cookie3.safari(domain_name="x.com")

        auth_token = None
        ct0 = None

        for cookie in cj:
            if cookie.name == "auth_token":
                auth_token = cookie.value
                print(f"✅ Found auth_token: {auth_token[:6]}...")
            elif cookie.name == "ct0":
                ct0 = cookie.value

        if not auth_token:
            print("🔄 Checking twitter.com domain...")
            cj = browser_cookie3.safari(domain_name="twitter.com")
            for cookie in cj:
                if cookie.name == "auth_token":
                    auth_token = cookie.value
                    print(f"✅ Found auth_token: {auth_token[:6]}...")
                elif cookie.name == "ct0":
                    ct0 = cookie.value

        if auth_token:
            os.makedirs("secrets", exist_ok=True)
            secrets = {"auth_token": auth_token}
            if ct0:
                secrets["ct0"] = ct0

            with open(SESSION_FILE, "w") as f:
                json.dump(secrets, f, indent=2)
            print(f"💾 Grok Session saved to {SESSION_FILE}")
            print("🎉 Safari Connection Successful!")
        else:
            print("❌ 'auth_token' not found in Safari.")
            print("   Note: Safari requires Full Disk Access for your terminal to read cookies.")

    except Exception as e:
        print(f"⚠️ Extraction Failed: {e}")
        if "Operation not permitted" in str(e):
            print("   🔴 PERMISSION DENIED: Please grant Full Disk Access to Terminal/Python.")


if __name__ == "__main__":
    extract_safari_token()
