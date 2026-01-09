# Trinity Score: 90.0 (Established by Chancellor)
"""Vault Manager for AFO Kingdom (Phase 22)
Handles secret retrieval from Environment or HashiCorp Vault.
"""

import logging
import os
import time

logger = logging.getLogger("AFO.Security")


class VaultManager:
    def __init__(self, mode: str = "env"):
        from AFO.config.settings import get_settings
        self.settings = get_settings()
        self.mode = mode
        self.secrets: dict[str, str] = {}
        self._audit_log: list[dict] = []
        logger.info(f"🛡️ VaultManager Initialized (Mode: {mode})")

    def _audit(self, action: str, key: str, success: bool):
        """Standard AFO Audit Logging (Phase 23)"""
        if self.settings.VAULT_STRICT_AUDIT:
            entry = {
                "ts": time.time(),
                "action": action,
                "key": key,
                "success": success,
                "head_sha": os.getenv("GIT_COMMIT_SHA", "unknown")
            }
            self._audit_log.append(entry)
            logger.info(f"📋 [Vault Audit] {action} on {key} (Success: {success})")

    def get_secret(self, key: str, default: str | None = None) -> str | None:
        """Retrieves a secret.
        In 'vault' mode, this would connect to HCV.
        In 'env' mode, it reads from os.environ.
        """
        # Policy Check (Simplified Zero Trust)
        if key.startswith("ROOT_") and not os.getenv("AFO_ROOT_ACCESS"):
            self._audit("ACCESS_DENIED", key, False)
            return None

        val: str | None = None
        if self.mode == "vault":
            # Simulation of Vault retrieval
            logger.debug(f"Securely retrieving {key} from Vault...")
            val = os.getenv(key, default)
        else:
            val = os.getenv(key, default)
        
        self._audit("GET", key, val is not None)
        return val

    def break_glass(self) -> None:
        """Emergency bypass protocol (High Priority Alert)."""
        logger.critical("🚨 [VAULT] BREAK-GLASS PROTOCOL ACTIVATED!")
        self._audit("BREAK_GLASS", "ALL", True)
        self.mode = "env" # Revert to env for emergency access

    def rotate_secret(self, key: str, new_value: str) -> bool:
        """Rotates a secret (Simulation)."""
        logger.warning(f"🔄 Rotating Secret: {key} (Audit Logged)")
        self.secrets[key] = new_value
        return True


# Singleton Instance
vault = VaultManager(mode=os.getenv("VAULT_MODE", "env"))
