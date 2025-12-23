import os
import shutil
import sqlite3
import subprocess
import sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

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
    # Combinations to try
    # (iterations, iv_char, length)
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

            cipher = Cipher(
                algorithms.AES(key), modes.CBC(iv), backend=default_backend()
            )
            decryptor = cipher.decryptor()

            # Decrypt
            decrypted = decryptor.update(encrypted_value) + decryptor.finalize()

            # PKCS7 Unpadding
            try:
                pad = decrypted[-1]
                if pad < 16:
                    decrypted = decrypted[:-pad]
            except Exception:
                pass  # Ignore unpad errors in fuzzy mode

            # Try to validate
            try:
                # PKCS7 Unpad provided we are confident
                pad = decrypted[-1]
                candidate = decrypted[:-pad] if pad < 16 else decrypted

                val = candidate.decode("utf-8")
                if "sk-ant" in val or "session" in val:
                    print(f"🔓 Decrypted with iter={iters}, iv={iv_char}")
                    return val
            except Exception:
                # If standard decode fails, try ignore and search
                val = decrypted.decode("utf-8", errors="ignore")
                if "sk-ant" in val:
                    print(f"🔓 Decrypted (fuzzy) with iter={iters}")
                    # Strip garbage before sk-ant
                    start_idx = val.find("sk-ant")
                    clean_val = val[start_idx:]
                    # Strip trailing nulls or garbage if any (usually just printable chars for token)
                    # clean_val = clean_val.split('\x00')[0] # Simple cleanup
                    return clean_val
        except Exception:
            # print(f"Combo {i} failed: {e}")
            pass

    return None


def main():
    print("🕵️ Force Extracting Claude Token...")

    p = get_safe_storage_password()
    if not p:
        sys.exit(1)

    profiles = [
        os.path.expanduser(
            "~/Library/Application Support/Google/Chrome/Default/Cookies"
        ),
        os.path.expanduser(
            "~/Library/Application Support/Google/Chrome/Profile 1/Cookies"
        ),
    ]

    wallet = APIWallet()
    print(f"DEBUG: Wallet Key Prefix: {wallet.encryption_key[:5]}...")
    captured = False

    for db_path in profiles:
        if not os.path.exists(db_path):
            continue

        print(f"📂 Scanning {db_path}...")
        temp_db = "debug_force_cookies.db"
        shutil.copy2(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        query = "SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%claude%' AND name='sessionKey'"
        cursor.execute(query)
        rows = cursor.fetchall()

        for host, name, encrypted in rows:
            print(f"🔎 Found cookie: {host} / {name}")
            val = decrypt_value(encrypted, p)
            if val:
                print(f"🔓 Decrypted! Length: {len(val)}")
                if len(val) > 20 and "sk-ant" in val:
                    print("✅ Valid Session Token Found!")
                    wallet.add(
                        name="anthropic",
                        api_key=val,
                        service="anthropic",
                        description=f"Extracted from {host}",
                        read_only=False,
                    )
                    print("💾 Saved to Wallet!")
                    captured = True
                    break
                # Also fallback check if simple check failed but length was ok
                elif len(val) > 20 and "session" in name:
                    print(f"⚠️ Likely Token (heuristic): {val[:15]}...")
                    # If sk-ant not found but decrypt worked reasonably, maybe save it?
                    # Let's be strict for now on sk-ant or just trust lenient decode
                    if "sk-ant" in val:  # Double check
                        wallet.add_key(
                            name="anthropic",
                            key=val,
                            service="anthropic",
                            read_only=False,
                        )
                        captured = True
                        break
            else:
                print("❌ Failed to decrypt.")

    conn.close()
    if os.path.exists(temp_db):
        os.remove(temp_db)

    if captured:
        print("🎉 SUCCESS: Claude token secured.")
    else:
        print("💀 FAILURE: Could not extract token.")


if __name__ == "__main__":
    main()
