# Trinity Score: 95.0 (Established by Chancellor)
"""
AFO Domain Wallet Package (domain/wallet/__init__.py)

Strangler Fig Facade for the API Wallet system.
"""

from .core import APIWallet
from .crypto import Fernet, MockFernet, get_cipher
from .models import KeyMetadata, WalletSummary

__all__ = [
    "KeyMetadata",
    "WalletSummary",
    "Fernet",
    "MockFernet",
    "get_cipher",
    "APIWallet",
]
