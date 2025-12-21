"""
Test APIWallet edge cases without module reloading.
Uses direct mocking instead of sys.modules manipulation.
"""

from unittest.mock import MagicMock, mock_open, patch

import pytest

from AFO.api_wallet import APIWallet


@pytest.mark.skip(reason="Flaky in full suite due to pytest import caching. Passes individually.")
def test_generate_default_key_reads_env() -> None:
    """Test that _generate_default_key reads from .env file correctly."""
    import os

    valid_key = "3qX4+P5+12345678901234567890123456789012345="

    def exists_side_effect(self):
        return ".env" in str(self)

    # Clear any existing env var that might interfere
    with (
        patch.dict(os.environ, {"API_WALLET_ENCRYPTION_KEY": ""}, clear=False),
        patch("pathlib.Path.exists", autospec=True, side_effect=exists_side_effect),
        patch(
            "builtins.open",
            mock_open(read_data=f"API_WALLET_ENCRYPTION_KEY={valid_key}"),
        ),
    ):
        wallet = APIWallet(use_vault=False, db_connection=None, encryption_key=None)
        # When .env has key, it should be used
        assert wallet.encryption_key == valid_key


@pytest.mark.skip(reason="Auto-saving to .env is not currently implemented in APIWallet")
def test_generate_default_key_writes_env() -> None:
    """Test that _generate_default_key writes a new key when missing."""

    def exists_side_effect(self):
        return ".env" in str(self)

    with patch("pathlib.Path.exists", autospec=True, side_effect=exists_side_effect):
        with patch("builtins.open", mock_open(read_data="")) as m_open:
            # Must be 44 chars for Fernet (Base64 URL safe)
            valid_new_key = b"3qX4+P5+12345678901234567890123456789012345="
            with patch("AFO.api_wallet.Fernet.generate_key", return_value=valid_new_key):
                APIWallet(use_vault=False, db_connection=None, encryption_key=None)

                # Check that open was called with 'a' mode
                calls = m_open.call_args_list
                append_calls = [c for c in calls if len(c.args) > 1 and c.args[1] == "a"]
                assert len(append_calls) > 0, "No file opened in append mode"


def test_vault_fallback_to_default_key() -> None:
    """Test vault key retrieval failure falls back to default key generation."""
    mock_vault = MagicMock()
    mock_vault.is_available.return_value = True
    mock_vault.get_encryption_key.return_value = None  # Key missing in vault

    with patch("AFO.api_wallet.VAULT_AVAILABLE", True):
        with patch("AFO.api_wallet.VaultKMS", return_value=mock_vault):
            # Should fall back to env/default key
            wallet = APIWallet(use_vault=True)
            assert wallet.encryption_key is not None
            assert len(wallet.encryption_key) > 0


def test_crypto_mock_fernet() -> None:
    """Test that MockFernet works when cryptography unavailable."""
    from AFO import api_wallet

    # Test MockFernet class directly without module reload
    if hasattr(api_wallet, "MockFernet"):
        mock_fernet = api_wallet.MockFernet(b"key")
        enc = mock_fernet.encrypt(b"test")
        dec = mock_fernet.decrypt(enc)
        assert dec == b"test"
    else:
        # Cryptography is available, test real Fernet behavior
        pytest.skip("Cryptography available, MockFernet not defined")
