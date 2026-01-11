# Trinity Score: 92.0 (Established by Chancellor)
"""
AFO Wallet Core (domain/wallet/core.py)

Main logic for the API Wallet system.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from .crypto import get_cipher
from .models import WalletSummary

logger = logging.getLogger(__name__)


class APIWallet:
    """
    API Wallet - 암호화 키 관리 시스템 (Encrypted Key Management System)
    """

    def __init__(
        self,
        encryption_key: str | None = None,
        db_connection: Any | None = None,
        use_vault: bool | None = None,
    ) -> None:
        # Encryption Key initialization
        if not encryption_key:
            encryption_key = self._get_encryption_key_from_settings()

        if not encryption_key:
            encryption_key = self._generate_default_key()

        self.cipher = get_cipher(encryption_key)

        # Paths
        pkg_root = Path(__file__).parent.parent.parent
        self.storage_path = pkg_root / "data" / "api_wallet.json"
        self.audit_log_path = pkg_root / "logs" / "api_wallet_audit.log"

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Database
        self.db = db_connection
        self.use_db = db_connection is not None

        self._ensure_storage_file()

    def _get_encryption_key_from_settings(self) -> str | None:
        try:
            from AFO.config.settings import get_settings

            return cast(str | None, get_settings().API_WALLET_ENCRYPTION_KEY)
        except Exception:  # nosec
            return None

    def _generate_default_key(self) -> str:
        from .crypto import Fernet

        return str(Fernet.generate_key().decode())

    def _ensure_storage_file(self) -> None:
        if not self.storage_path.exists():
            self._save_storage({"keys": []})

    def _load_storage(self) -> dict[str, Any]:
        try:
            if not self.storage_path.exists():
                return {"keys": []}
            return cast(dict[str, Any], json.loads(self.storage_path.read_text()))
        except Exception:  # nosec
            return {"keys": []}

    def _save_storage(self, data: dict[str, Any]) -> None:
        self.storage_path.write_text(json.dumps(data, indent=2))

    def _audit_log(self, action: str, key_name: str, details: str = "") -> None:
        try:
            timestamp = datetime.now().isoformat()
            log_entry = f"{timestamp} | {action} | {key_name} | {details}\n"
            with open(self.audit_log_path, "a") as f:
                f.write(log_entry)
        except Exception:  # nosec
            pass

    def _hash_key(self, api_key: str) -> str:
        return hashlib.sha256(api_key.encode()).hexdigest()[:16]

    def add(
        self,
        name: str,
        api_key: str,
        key_type: str = "api",
        read_only: bool = True,
        service: str = "",
        description: str = "",
    ) -> int:
        """Add a new API key to wallet"""
        try:
            encrypted_key = self.cipher.encrypt(api_key.encode()).decode()
            key_hash = self._hash_key(api_key)

            storage = self._load_storage()
            if any(k["name"] == name for k in storage["keys"]):
                raise ValueError(f"Key with name '{name}' already exists")

            key_id = len(storage["keys"]) + 1
            key_data = {
                "id": key_id,
                "name": name,
                "encrypted_key": encrypted_key,
                "key_type": key_type,
                "read_only": read_only,
                "service": service,
                "description": description,
                "key_hash": key_hash,
                "created_at": datetime.now().isoformat(),
                "last_accessed": None,
                "access_count": 0,
            }

            storage["keys"].append(key_data)
            self._save_storage(storage)
            self._audit_log("ADD", name, f"type={key_type}, service={service}")
            return int(key_id)
        except Exception as e:
            self._audit_log("ADD_FAILED", name, str(e))
            raise

    def get(self, name: str, decrypt: bool = True) -> str | None:
        """Retrieve an API key by name"""
        storage = self._load_storage()
        for key in storage["keys"]:
            if key["name"] == name:
                self._update_access_stats(name)
                if decrypt:
                    return cast(
                        str,
                        self.cipher.decrypt(key["encrypted_key"].encode()).decode(),
                    )
                return cast(str, key["encrypted_key"])
        return None

    def list_keys(self) -> list[dict[str, Any]]:
        """List all keys in wallet (without decrypted values)"""
        storage = self._load_storage()
        return [
            {k: v for k, v in key.items() if k != "encrypted_key"}
            for key in storage["keys"]
        ]

    def delete(self, name: str) -> bool:
        """Delete a key from wallet"""
        storage = self._load_storage()
        original_count = len(storage["keys"])
        storage["keys"] = [k for k in storage["keys"] if k["name"] != name]

        if len(storage["keys"]) < original_count:
            self._save_storage(storage)
            self._audit_log("DELETE", name)
            return True
        return False

    def _update_access_stats(self, name: str) -> None:
        """Update access stats in local storage and Redis"""
        try:
            storage = self._load_storage()
            for key in storage["keys"]:
                if key["name"] == name:
                    key["last_accessed"] = datetime.now().isoformat()
                    key["access_count"] = key.get("access_count", 0) + 1
                    break
            self._save_storage(storage)
            # Redis sync logic could go here if needed, keeping it simple for now
        except Exception:  # nosec
            pass

    def get_summary(self) -> WalletSummary:
        """Get wallet state summary"""
        keys = self.list_keys()
        services = list({k.get("service") for k in keys if k.get("service")})
        return WalletSummary(
            total_keys=len(keys),
            active_services=services,
            total_token_usage={},
            last_backup=None,
        )
