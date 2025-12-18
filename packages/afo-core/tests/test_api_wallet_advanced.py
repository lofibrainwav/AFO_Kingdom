import importlib
import os
import runpy
import sys
from unittest.mock import MagicMock, patch

import pytest

from AFO.api_wallet import APIWallet, create_wallet

# Load wallet-specific fixtures
pytest_plugins = ["tests.conftest_wallet"]


# 1. Vault KMS Integration Tests
def test_wallet_init_vault_success():
    mock_vault = MagicMock()
    mock_vault.is_available.return_value = True
    mock_vault.get_encryption_key.return_value = "vault_key_44_chars_encoded_here__"

    with patch("AFO.api_wallet.VaultKMS", return_value=mock_vault):
        with patch.dict(os.environ, {"VAULT_ENABLED": "true"}):
            wallet = APIWallet(use_vault=True)
            # It should try to get key from vault
            assert wallet.encryption_key == "vault_key_44_chars_encoded_here__"
            assert wallet.use_vault is True


def test_wallet_init_vault_failure_fallback():
    mock_vault = MagicMock()
    mock_vault.is_available.return_value = False  # Vault enabled but not reachable

    with patch("AFO.api_wallet.VaultKMS", return_value=mock_vault):
        with patch.dict(os.environ, {"VAULT_ENABLED": "true"}):
            # Should disable vault use and fallback to env/default
            wallet = APIWallet(use_vault=True)
            assert wallet.use_vault is False
            assert len(wallet.encryption_key) > 0


# 3. Cryptography Missing (MockFernet)
def test_mock_fernet_fallback():
    # Force reload api_wallet with CRYPTO_AVAILABLE=False logic
    # We cheat by importing, then mocking the global variable if it was already True,
    # OR we use the reload technique.
    # Since we are in the same process, reloading is safer.

    with patch.dict(sys.modules):
        # Remove it so we can re-import
        if "AFO.api_wallet" in sys.modules:
            del sys.modules["AFO.api_wallet"]
        if "api_wallet" in sys.modules:
            del sys.modules["api_wallet"]

        # We also need to ensure Fernet doesn't import properly or we force disable it
        # The code checks: try: from cryptography.fernet import Fernet ... except ImportError: ...

        # Let's force ImportError for cryptography
        sys.modules["cryptography"] = None
        sys.modules["cryptography.fernet"] = None

        # Now import
        # Use import_module to ensure it loads freshly and registers in sys.modules
        api_wallet = importlib.import_module("AFO.api_wallet")

        assert api_wallet.CRYPTO_AVAILABLE is False
        assert api_wallet.Fernet.__name__ == "MockFernet"

        # Now test the MockFernet class logic
        wallet = api_wallet.APIWallet(encryption_key="x" * 44)
        enc = wallet.cipher.encrypt(b"test")
        # MockFernet returns base64 string of data
        # Wait, the MockFernet implementation in api_wallet.py:
        # return base64.urlsafe_b64encode(data)
        import base64

        expected = base64.urlsafe_b64encode(b"test")
        assert enc == expected

        dec = wallet.cipher.decrypt(enc)
        assert dec == b"test"


# 3. CLI Tests using main()
def test_cli_execution():
    from AFO.api_wallet import main

    # Mock create_wallet to return a mock wallet
    mock_wallet_instance = MagicMock()
    mock_wallet_instance.add.return_value = 1
    mock_wallet_instance.get.return_value = "API_KEY"
    mock_wallet_instance.list_keys.return_value = [{"name": "test", "service": "test"}]
    mock_wallet_instance.delete.return_value = True

    # We must patch create_wallet in the exact module main() looks for it.
    # main() is in AFO.api_wallet, and it calls create_wallet() from global scope of AFO.api_wallet.
    # So patching AFO.api_wallet.create_wallet is correct.

    with patch("AFO.api_wallet.create_wallet", return_value=mock_wallet_instance):
        # Test ADD
        with patch.object(
            sys, "argv", ["api_wallet.py", "add", "test_key", "secret_val", "openai"]
        ):
            main()
            mock_wallet_instance.add.assert_called_with("test_key", "secret_val", service="openai")

        # Test GET
        with patch.object(sys, "argv", ["api_wallet.py", "get", "test_key"]):
            main()
            mock_wallet_instance.get.assert_called_with("test_key")

        # Test LIST
        with patch.object(sys, "argv", ["api_wallet.py", "list"]):
            main()
            mock_wallet_instance.list_keys.assert_called()

        # Test DELETE
        with patch.object(sys, "argv", ["api_wallet.py", "delete", "test_key"]):
            main()
            mock_wallet_instance.delete.assert_called_with("test_key")


# 4. DB Method Tests (Directly calling them to ensure SQL construction works)
def test_db_methods_sql_construction():
    mock_db = MagicMock()
    wallet = APIWallet(db_connection=mock_db)
    # Patch PSYCOPG2_AVAILABLE to True for this instance logic (it uses self.use_db)

    # We set db_connection, so self.use_db depends on PSYCOPG2_AVAILABLE global
    # Let's force it
    wallet.use_db = True

    # Test _ensure_table_exists
    wallet._ensure_table_exists()
    mock_db.getconn.return_value.cursor.return_value.__enter__.return_value.execute.assert_called()

    # Test _add_to_database
    mock_db.getconn.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value = [
        10
    ]
    key_id = wallet._add_to_database(
        {
            "name": "n",
            "encrypted_key": "k",
            "key_type": "t",
            "read_only": True,
            "service": "s",
            "description": "d",
            "key_hash": "h",
            "created_at": "now",
            "last_accessed": "now",
            "access_count": 0,
        }
    )
    assert key_id == 10
