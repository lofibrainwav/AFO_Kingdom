#!/usr/bin/env python3
"""
Chrome Cookie Decryptor for macOS
Breaking the seal of 'Safe Storage' to retrieve the User's Session.
"""

import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

# Crypto libraries (try to import)
try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("❌ 'cryptography' library not found. Install with: pip install cryptography")


def get_safe_storage_password(service="Chrome Safe Storage"):
    """Get the Safe Storage password from Keychain"""
    try:
        cmd = ["security", "find-generic-password", "-w", "-s", service]
        password = subprocess.check_output(cmd).strip()
        return password
    except Exception:
        # print(f"⚠️ Could not fetch {service} password: {e}")
        return None


def decrypt_value(encrypted_value, safe_password):
    """Decrypt the macOS Chrome Cookie value"""
    if not encrypted_value or not safe_password:
        return ""

    try:
        # PBKDF2 derivation
        salt = b"saltysalt"
        iv = b" " * 16
        length = 16
        iterations = 1003

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            length=length,
            salt=salt,
            iterations=iterations,
            backend=default_backend(),
        )
        key = kdf.derive(safe_password)

        # AES-128-CBC Decryption
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Strip v10 prefix if present (Chrome v10+)
        if encrypted_value[:3] == b"v10":
            encrypted_value = encrypted_value[3:]

        decrypted = decryptor.update(encrypted_value) + decryptor.finalize()

        # Remove padding
        return decrypted.decode("utf-8").strip()
    except Exception:
        # print(f"Decryption error: {e}")
        return ""


def main():
    if not CRYPTO_AVAILABLE:
        sys.exit(1)

    print("🔓 Unlocking Cookies (Chrome/Chromium)...")

    # Try Chrome then Chromium password
    password = get_safe_storage_password("Chrome Safe Storage")
    if not password:
        print("ℹ️ Chrome Safe Storage not found, trying Chromium...")
        password = get_safe_storage_password("Chromium Safe Storage")

    if not password:
        print("❌ Failed to access Keychain (Chrome/Chromium). Aborting.")
        sys.exit(1)

    print("🔑 Keychain Access Granted.")

    profiles: list[Path] = []

    # Check for arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--scan-playwright":
        import glob

        print("👻 Scanning Playwright Temp Profiles...")
        # Hardcoded for this environment based on investigation
        temp_profiles = glob.glob(
            "/var/folders/mp/7m5m295d1jb17rnk1j9761xh0000gn/T/playwright_chromiumdev_profile-*"
        )
        for p in temp_profiles:
            path = Path(p)
            # Playwright often puts Cookies in 'Default' or root depending on launch
            if (path / "Default" / "Cookies").exists():
                profiles.append(path / "Default")
            elif (path / "Cookies").exists():
                profiles.append(path)
    else:
        # Default Real Chrome
        base_path = Path.home() / "Library/Application Support/Google/Chrome"
        all_profiles = [p.name for p in base_path.glob("*") if p.is_dir()]
        print(f"📂 Found {len(all_profiles)} directories in Chrome root: {all_profiles}")

        for p in base_path.glob("*"):
            if (p / "Cookies").exists():
                profiles.append(p)  # type: ignore[arg-type]
            elif (p / "Default" / "Cookies").exists():
                print(f"📂 Detected User Data Dir: {p.name}")
                for sub in p.glob("*"):
                    if (sub / "Cookies").exists():
                        profiles.append(sub)

    total_found = 0

    import api_wallet
    from api_wallet import APIWallet

    print(f"🐛 Loaded api_wallet from: {api_wallet.__file__}")
    wallet = APIWallet()

    for profile in profiles:
        print(f"\n📂 Scanning Profile: {profile.name}")
        cookie_path = profile / "Cookies"

        # Copy DB
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            shutil.copy2(cookie_path, tmp.name)
            tmp_db = tmp.name

        try:
            conn = sqlite3.connect(tmp_db)
            cursor = conn.cursor()

            # Query OpenAI AND Claude
            query = """
                SELECT name, encrypted_value, host_key
                FROM cookies
                WHERE (host_key LIKE '%openai%' OR host_key LIKE '%claude%' OR host_key LIKE '%anthropic%')
                -- AND (name LIKE '%session%' OR name LIKE '%auth%' OR name LIKE 'sessionKey')
            """
            cursor.execute(query)

            print(f"   🔍 Scanning {profile.name} for matching cookies...")
            print(f"   🔍 Scanning {profile.name} for matching cookies...")
            for name, enc_val, host in cursor.fetchall():
                decrypted = decrypt_value(enc_val, password)
                # print(f"      Found cookie: {name} in {host} (len={len(decrypted)})")

                # Loose filter for saving
                if len(decrypted) > 20 and any(
                    k in name.lower() for k in ["session", "auth", "key", "token"]
                ):
                    service = "openai" if "openai" in host else "anthropic"
                    print(f"      ✅ CAPTURED: {name} ({host})")

                    wallet.add(
                        name=f"{service}_{name}_{profile.name}",
                        api_key=decrypted,
                        key_type="session_token",
                        service=service,
                        description=f"Decrypted from Real Chrome ({profile.name})",
                        read_only=False,
                    )
                    print("         💾 Saved to API Wallet")
                    total_found += 1
                elif len(decrypted) > 20:
                    print(
                        f"      👀 Ignored: {name} ({host}) - didn't match 'session/auth/key/token'"
                    )

        except Exception as e:
            print(f"      ⚠️ Error scanning profile: {e}")
        finally:
            if os.path.exists(tmp_db):
                os.unlink(tmp_db)

    if total_found == 0:
        print("\n⚠️ No valid sessions found in ANY Chrome profile.")
        print("💡 Suggestion: Please login to OpenAI/Claude in your Chrome first.")
    else:
        print(f"\n🎉 Successfully imported {total_found} tokens from Real Chrome.")


if __name__ == "__main__":
    # Add AFO to path to find api_wallet
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        from AFO.api_wallet import APIWallet
    except ImportError:
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

    main()
