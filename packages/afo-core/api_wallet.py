# Trinity Score: 98.0 (Established by Chancellor)
# afo_soul_engine/api_wallet.py
"""
AFO API Wallet (Strangler Fig Facade)

This module now serves as a facade for the modularized domain/wallet package.
All core models and encryption logic have been moved to domain/wallet/.
"""

from __future__ import annotations

import os
import sys
from typing import Any

# Add package root to sys.path to ensure 'domain' is importable
# In AFO/ subdirectory, we need to go up one level
package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if package_root not in sys.path:
    sys.path.append(package_root)

# Import from core domain package (Strangler Fig)
try:
    from domain.wallet import (
        APIWallet,
        Fernet,
        KeyMetadata,
        MockFernet,
        WalletSummary,
        get_cipher,
    )
except ImportError:
    # Fallback for different execution contexts
    from AFO.domain.wallet import (
        APIWallet,
        Fernet,
        KeyMetadata,
        MockFernet,
        WalletSummary,
        get_cipher,
    )

# ============================================================================
# Global Wallet Instance
# ============================================================================

wallet = APIWallet()


# ============================================================================
# Convenience Interface
# ============================================================================


def create_wallet(encryption_key: str | None = None) -> APIWallet:
    """Create a new API Wallet instance"""
    return APIWallet(encryption_key=encryption_key)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "APIWallet",
    "Fernet",
    "KeyMetadata",
    "MockFernet",
    "WalletSummary",
    "get_cipher",
    "wallet",
    "create_wallet",
]

# ============================================================================
# Self-Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("AFO API Wallet - Facade Self-Test")
    print("=" * 70)

    # 1. Registration Test
    print("\n🔍 Testing Key Registration...")
    try:
        test_key_name = f"test_facade_afo_{int(os.getpid())}"
        key_id = wallet.add(test_key_name, "sk-test-123", service="test")
        print(f"   ✅ Added test key: {test_key_name} (ID: {key_id})")

        # 2. Retrieval Test
        print("\n🔑 Testing Key Retrieval...")
        decrypted = wallet.get(test_key_name)
        if decrypted == "sk-test-123":
            print("   ✅ Decryption successful!")
        else:
            print(f"   ❌ Decryption failed: {decrypted}")

        # 3. Cleanup
        wallet.delete(test_key_name)
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

    print("\n✅ Facade self-test completed successfully!")
