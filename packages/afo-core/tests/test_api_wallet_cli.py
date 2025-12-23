from unittest.mock import MagicMock, patch

import pytest
from AFO.api_wallet import main as cli


def test_cli_add_key():
    with patch("sys.argv", ["api_wallet.py", "add", "test_key", "sk-123"]):
        # Verify cli function object
        assert hasattr(cli, "__globals__")

        MockWallet = MagicMock()
        MockInstance = MockWallet.return_value
        MockInstance.add.return_value = 1

        # Patch the APIWallet class in the function's global scope
        with patch.dict(cli.__globals__, {"APIWallet": MockWallet}):
            cli()

            # CLI passes service="" by default
            MockInstance.add.assert_called_with("test_key", "sk-123", service="")


def test_cli_add_key_failure():
    with patch("sys.argv", ["api_wallet.py", "add", "test_key", "sk-123"]):
        MockWallet = MagicMock()
        MockInstance = MockWallet.return_value
        MockInstance.add.side_effect = ValueError("Duplicate")

        with patch.dict(cli.__globals__, {"APIWallet": MockWallet}):
            # CLI catches error and system exits
            with pytest.raises(SystemExit):
                cli()


def test_cli_get_key():
    # CLI doesn't seem to parse --decrypt flag in the code we saw?
    # It just calls get(name).
    with patch("sys.argv", ["api_wallet.py", "get", "test_key"]):
        MockWallet = MagicMock()
        MockInstance = MockWallet.return_value
        MockInstance.get.return_value = "decrypted_sk"

        with patch.dict(cli.__globals__, {"APIWallet": MockWallet}):
            cli()

            # Called without keyword arg if code is just wallet.get(name)
            MockInstance.get.assert_called_with("test_key")


def test_cli_list_keys():
    with patch("sys.argv", ["api_wallet.py", "list"]):
        MockWallet = MagicMock()
        MockInstance = MockWallet.return_value
        MockInstance.list_keys.return_value = [{"name": "k1", "created_at": "now"}]

        with patch.dict(cli.__globals__, {"APIWallet": MockWallet}):
            cli()

            MockInstance.list_keys.assert_called()


def test_cli_delete_key():
    with patch("sys.argv", ["api_wallet.py", "delete", "test_key"]):
        MockWallet = MagicMock()
        MockInstance = MockWallet.return_value
        MockInstance.delete.return_value = True

        with patch.dict(cli.__globals__, {"APIWallet": MockWallet}):
            cli()

            MockInstance.delete.assert_called_with("test_key")


def test_cli_no_args():
    # Calling without args prints help and sys.exit(1)
    with patch("sys.argv", ["api_wallet.py"]):
        with patch.dict(cli.__globals__, {"APIWallet": MagicMock()}):
            with pytest.raises(SystemExit) as e:
                cli()
            assert e.value.code == 1
