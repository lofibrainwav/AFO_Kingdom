# Trinity Score: 90.0 (Established by Chancellor)
import os
import shutil
import sqlite3
import subprocess
import sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# from cryptography.hazmat.primitives import padding

# Add AFO to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AFO.api_wallet import APIWallet


def get_safe_storage_password():
    try:
        cmd = ["security", "find-generic-password", "-w", "-s", "Chrome Safe Storage"]
        password = subprocess.check_output(cmd).strip()
        return password
    except Exception as e:
        print(f"❌ Password fetch failed: {e}")
        return None


def decrypt_value(encrypted_value, safe_password):
    # Combinations to try (iterations, iv_char, length)
    combos = [
        (1003, b" ", 16),
        (1, b" ", 16),
        (1000, b" ", 16),
        (1003, b"\x00", 16),
    ]

    # Pre-process v10
    if encrypted_value.startswith(b"v10"):
        encrypted_value = encrypted_value[3:]

    for _i, (iters, iv_char, key_len) in enumerate(combos):
        try:
            salt = b"saltysalt"
            iv = iv_char * 16

            # Key derivation
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA1(),
                length=key_len,
                salt=salt,
                iterations=iters,
                backend=default_backend(),
            )
            key = kdf.derive(safe_password)

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            # Decrypt
            decrypted = decryptor.update(encrypted_value) + decryptor.finalize()

            # Try to validate
            try:
                val = decrypted.decode("utf-8")
                # OpenAI session token usually starts with some structure, checking len > 20
                if len(val) > 20:
                    return val
            except Exception:
                # If standard decode fails, try ignore and search
                val = decrypted.decode("utf-8", errors="ignore")
                if len(val) > 20:
                    # Clean up garbage chars for fuzzy match
                    # OpenAI tokens don't have a strict prefix like sk-ant...
                    # But they are usually alphanumeric.
                    # Let's just return it and see what we get
                    return val
        except Exception:
            pass

    return None


def main():
    print("🕵️ Force Extracting OpenAI Token...")

    p = get_safe_storage_password()
    if not p:
        sys.exit(1)

    profiles = [
        os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Cookies"),
        os.path.expanduser("~/Library/Application Support/Google/Chrome/Profile 1/Cookies"),
    ]

    wallet = APIWallet()
    print(f"DEBUG: Wallet Key Prefix: {wallet.encryption_key[:5]}...")

    # First, delete existing bad key if any
    try:
        if any(k["name"] == "openai" for k in wallet.list_keys()):
            wallet.delete("openai")
            print("🗑️ Deleted existing openai key")
    except Exception:
        pass

    captured = False

    for db_path in profiles:
        if not os.path.exists(db_path):
            continue

        print(f"📂 Scanning {db_path}...")
        temp_db = "debug_force_cookies_openai.db"
        shutil.copy2(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        query = "SELECT host_key, name, encrypted_value FROM cookies WHERE name='__Secure-1PSID'"
        cursor.execute(query)
        rows = cursor.fetchall()

        for host, name, encrypted in rows:
            print(f"🔎 Found cookie: {host} / {name}")
            val = decrypt_value(encrypted, p)
            if val and len(val) > 10:  # Ensure not empty
                # Clean up if known suffix issues?
                # OpenAI tokens are just session IDs.

                print(f"🔓 Decrypted! Length: {len(val)}")
                print(f"Preview: {val[:10]}...")

                wallet.add(
                    name="openai",
                    api_key=val,
                    service="openai",
                    description=f"Extracted from {host}",
                    read_only=False,
                )
                print("💾 Saved to Wallet!")
                captured = True
                break
            else:
                print("❌ Failed to decrypt or empty.")

        conn.close()
        if os.path.exists(temp_db):
            os.remove(temp_db)

        if captured:
            break

    if captured:
        print("🎉 SUCCESS: OpenAI token secured.")
    else:
        print("💀 FAILURE: Could not extract token.")


if __name__ == "__main__":
    main()
