# Trinity Score: 90.0 (Established by Chancellor)
#!/usr/bin/env python3
"""
API Wallet - 모든 API 키를 안전하게 보관

三域 보안 체계:
- input.brnestrm.com: 입력 게이트웨이
- mcp.brnestrm.com: 암호화 저장소 (이 모듈)
- n8n.brnestrm.com: 워크플로우 실행

사마의 (善 - Goodness) 원칙:
- 최소 권한: 읽기 전용 키 우선
- 암호화: AES-256 (Fernet)
- 감사 로깅: 모든 접근 기록
- 비밀 스캔: 평문 금지
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

# Phase 8.3.3: Vault KMS 통합
try:
    from AFO.kms.vault_kms import VaultKMS

    VAULT_AVAILABLE = True
except ImportError:
    VAULT_AVAILABLE = False
    print("⚠️  Vault KMS 사용 불가 (ImportError)")

# PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor

    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

# Phase 2-4: settings 사용
try:
    from AFO.config.settings import get_settings

    settings = get_settings()
    FORCE_MOCK = settings.MOCK_MODE
except ImportError:
    FORCE_MOCK = os.getenv("MOCK_MODE", "false").lower() == "true"

# Try to import cryptography, fallback to mock mode
if not FORCE_MOCK:
    try:
        from cryptography.fernet import Fernet

        CRYPTO_AVAILABLE = True
    except Exception:
        CRYPTO_AVAILABLE = False
        FORCE_MOCK = True
else:
    CRYPTO_AVAILABLE = False

# Mock Fernet for environments without cryptography or in MOCK_MODE
if not CRYPTO_AVAILABLE:

    class MockFernet:
        def __init__(self, key: bytes) -> None:
            self.key = key

        def encrypt(self, data: bytes) -> bytes:
            # Simple base64 encoding (NOT secure, for testing only!)
            return base64.b64encode(data)

        def decrypt(self, data: bytes) -> bytes:
            return base64.b64decode(data)

        @staticmethod
        def generate_key() -> bytes:
            # Generate a fake 44-character key
            return base64.b64encode(b"mock_encryption_key_32_bytes_lo").decode().encode()

    Fernet = MockFernet  # type: ignore


class APIWallet:
    """
    API Wallet - 암호화 키 관리 시스템

    Features:
    - AES-256 encryption (Fernet)
    - PostgreSQL storage (fallback: JSON file)
    - Audit logging
    - Read-only key support
    """

    def __init__(
        self,
        encryption_key: str | None = None,
        db_connection: Any | None = None,
        use_vault: bool | None = None,
    ) -> None:
        """
        Initialize API Wallet

        Args:
            encryption_key: Base64-encoded Fernet key (44 chars)
            db_connection: PostgreSQL connection (optional)
            use_vault: Vault KMS 사용 여부 (기본: VAULT_ENABLED 환경 변수)
        """
        # Warn if using mock mode
        if not CRYPTO_AVAILABLE:
            print("⚠️  WARNING: cryptography module not available")
            print("   Using MOCK encryption (NOT SECURE!)")
            print("   Install cryptography for production: pip install cryptography")

        # Phase 8.3.3: Vault KMS 초기화
        # Phase 2-4: settings 사용 + TICKET W1: API_WALLET_KMS 환경변수 지원
        kms_type = os.getenv("API_WALLET_KMS", "local").strip().lower()
        if kms_type == "vault":
            # vault 모드: vault 강제 활성화
            vault_enabled_default = True
        elif kms_type == "local":
            # local 모드: vault 비활성화
            vault_enabled_default = False
        else:
            # 기타 값: 기존 로직 유지 (settings 우선)
            try:
                from AFO.config.settings import get_settings

                settings = get_settings()
                vault_enabled_default = settings.VAULT_ENABLED
            except ImportError:
                vault_enabled_default = os.getenv("VAULT_ENABLED", "false").lower() == "true"

        self.use_vault = use_vault if use_vault is not None else vault_enabled_default
        self.kms_type = kms_type  # TICKET W3.4: kms_type 저장 for fail-closed
        self.vault_kms = None

        if self.use_vault and VAULT_AVAILABLE:
            try:
                self.vault_kms = VaultKMS()
                if self.vault_kms.is_available():
                    print("✅ Vault KMS 활성화됨")
                else:
                    # TICKET W3: Fail-closed for vault mode
                    if self.kms_type == "vault":
                        raise RuntimeError(
                            "Vault KMS required but unavailable (토큰 또는 주소 없음)"
                        )
                    else:
                        print("⚠️  Vault KMS 사용 불가 (토큰 또는 주소 없음)")
                        self.use_vault = False
            except Exception as e:
                # TICKET W3: Fail-closed for vault mode - do not silently fallback
                if self.kms_type == "vault":
                    raise RuntimeError(f"Vault KMS required but failed to initialize: {e}") from e
                else:
                    print(f"⚠️  Vault KMS 초기화 실패 (local 모드로 fallback): {e}")
                    self.use_vault = False

        # Get encryption key (Vault 우선, 환경 변수, 기본값 순)
        if encryption_key:
            self.encryption_key = encryption_key
        elif self.use_vault and self.vault_kms:
            # Vault에서 키 가져오기
            vault_key = self.vault_kms.get_encryption_key()
            if vault_key:
                self.encryption_key = vault_key
                print("✅ Vault에서 암호화 키 로드 완료")
            else:
                key_from_settings = self._get_encryption_key_from_settings()
                self.encryption_key = (
                    key_from_settings
                    or os.getenv("API_WALLET_ENCRYPTION_KEY", self._generate_default_key())
                    or ""
                )
                # Vault에 저장 시도
                if self.vault_kms.is_available():
                    self.vault_kms.set_encryption_key(self.encryption_key)
        else:
            key_from_settings = self._get_encryption_key_from_settings()
            self.encryption_key = (
                key_from_settings
                or os.getenv("API_WALLET_ENCRYPTION_KEY", self._generate_default_key())
                or ""
            )

        # Validate key (only in real crypto mode)
        if CRYPTO_AVAILABLE and len(self.encryption_key) != 44:
            raise ValueError(
                "Encryption key must be 44 characters (Fernet key). "
                "Generate one with: "
                'python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"'
            )

        # Initialize cipher
        try:
            self.cipher = Fernet(self.encryption_key.encode())
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {e}") from e

        # Database connection (optional, fallback to JSON)
        self.db = db_connection
        self.use_db = db_connection is not None and PSYCOPG2_AVAILABLE

        if self.use_db:
            self._ensure_table_exists()

        # Fallback: JSON file storage
        if not self.use_db:
            # Determine data directory (AFO_DATA_DIR env var or tmp dir)
            base_dir = Path(os.getenv("AFO_DATA_DIR") or Path.home() / ".afo")
            base_dir.mkdir(parents=True, exist_ok=True)
            self.storage_path = base_dir / "api_wallet_storage.json"
            self._ensure_storage_file()

        # Audit log
        base_dir = Path(os.getenv("AFO_DATA_DIR") or Path.home() / ".afo")
        base_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log_path = base_dir / "api_wallet_audit.log"

    def _get_encryption_key_from_settings(self) -> str | None:
        """Helper to get encryption key from settings with fallback"""
        try:
            from AFO.config.settings import get_settings

            return get_settings().API_WALLET_ENCRYPTION_KEY
        except ImportError:
            return None

    def _generate_default_key(self) -> str:
        """Generate a default key for development (NOT for production!)"""
        # WARNING: This is for development only!
        # In production, always use a randomly generated key!

        try:
            env_path = Path(__file__).parent / ".env"

            # Check if key already exists in .env
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        if line.strip().startswith("API_WALLET_ENCRYPTION_KEY="):
                            # Extract existing key
                            existing_key = line.split("=", 1)[1].strip()
                            if existing_key and len(existing_key) == 44:
                                return existing_key

            # Generate new key if not found
            return str(Fernet.generate_key().decode())
        except Exception as e:
            # If filesystem is read-only or other error, return a reliable temporary key
            print(f"⚠️  Failed to generate/save default key: {e}")
            return str(Fernet.generate_key().decode())

    def _ensure_storage_file(self) -> None:
        """Ensure JSON storage file exists"""
        try:
            if not self.storage_path.exists():
                self.storage_path.write_text(json.dumps({"keys": []}, indent=2))
        except Exception as e:
            print(f"⚠️  Failed to create storage file: {e}")
            # Non-critical if we are just reading/using transiently

    def _load_storage(self) -> dict[str, list[dict[str, Any]]]:
        """Load from JSON storage"""
        try:
            if not self.storage_path.exists():
                return {"keys": []}
            # Explicit type cast for MyPy
            data: dict[str, list[dict[str, Any]]] = json.loads(self.storage_path.read_text())
            return data
        except Exception as e:
            print(f"⚠️  Failed to load failed storage: {e}")
            return {"keys": []}

    def _save_storage(self, data: dict[str, Any]) -> None:
        """Save to JSON storage"""
        try:
            self.storage_path.write_text(json.dumps(data, indent=2))
        except Exception as e:
            print(f"⚠️  Failed to save storage: {e}")
            raise OSError(f"Failed to persist wallet data: {e}") from e

    def _audit_log(self, action: str, key_name: str, details: str = "") -> None:
        """Write to audit log"""
        try:
            timestamp = datetime.now().isoformat()
            log_entry = f"{timestamp} | {action} | {key_name} | {details}\n"

            with open(self.audit_log_path, "a") as f:
                f.write(log_entry)
        except Exception as e:
            # Audit logging failure should not break the application
            print(f"⚠️  Audit Log Failed: {e}")

    def _hash_key(self, api_key: str) -> str:
        """Create SHA-256 hash of key for audit purposes"""
        return hashlib.sha256(api_key.encode()).hexdigest()[:16]

    def add(
        self,
        name: str,
        api_key: str,
        key_type: str = "api",
        read_only: bool = True,
        service: str = "",
        description: str = "",
        scopes: list[str] | None = None,
    ) -> int:
        """
        Add a new API key to wallet

        Args:
            name: Unique name for this key
            api_key: The actual API key (will be encrypted)
            key_type: Type of key (api, oauth, token, etc.)
            read_only: Whether this key has read-only permissions
            service: Service name (openai, anthropic, n8n, etc.)
            description: Optional description

        Returns:
            Key ID

        Raises:
            ValueError: If key name already exists or encryption fails
        """
        try:
            # Encrypt the API key
            try:
                encrypted_key = self.cipher.encrypt(api_key.encode()).decode()
            except Exception as e:
                raise ValueError(f"Encryption failed: {e}") from e

            # Create hash for audit
            key_hash = self._hash_key(api_key)

            # Prepare data
            key_data = {
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

            if self.use_db:
                # PostgreSQL storage
                key_id = self._add_to_database(key_data)
            else:
                # JSON file storage
                storage = self._load_storage()

                # Check if name exists
                if any(k["name"] == name for k in storage["keys"]):
                    raise ValueError(f"Key with name '{name}' already exists")

                # Add ID
                key_id_val = len(storage["keys"]) + 1
                key_data["id"] = key_id_val
                key_id = int(key_id_val)

                # Append and save
                storage["keys"].append(key_data)
                self._save_storage(storage)

            # Audit log
            self._audit_log("ADD", name, f"type={key_type}, service={service}, hash={key_hash}")

            return key_id

        except ValueError:
            raise
        except Exception as e:
            self._audit_log("ADD_FAILED", name, str(e))
            raise RuntimeError(f"Failed to add key '{name}': {e}") from e

    def get(self, name: str, decrypt: bool = True) -> str | None:
        """
        Retrieve an API key by name

        Args:
            name: Key name
            decrypt: Whether to decrypt the key (default: True)

        Returns:
            Decrypted API key or None if not found
        """
        try:
            if self.use_db:
                # PostgreSQL storage
                key_data = self._get_from_database(name)
            else:
                # JSON file storage
                storage = self._load_storage()
                key_data = next((k for k in storage["keys"] if k["name"] == name), None)

            if not key_data:
                self._audit_log("GET_FAILED", name, "Key not found")
                return None

            # Update access stats
            self._update_access_stats(name)

            # Decrypt if requested
            if decrypt:
                try:
                    encrypted_key = str(key_data["encrypted_key"])
                    decrypted_key = self.cipher.decrypt(encrypted_key.encode()).decode()

                    # Audit log (with hash only, not the actual key!)
                    key_hash = self._hash_key(decrypted_key)
                    self._audit_log("GET_SUCCESS", name, f"hash={key_hash}")

                    return str(decrypted_key)
                except Exception as e:
                    self._audit_log("DECRYPT_FAILED", name, str(e))
                    raise ValueError(f"Failed to decrypt key '{name}': {e}") from e
            else:
                # Return encrypted key
                return str(key_data["encrypted_key"])

        except Exception as e:
            self._audit_log("GET_ERROR", name, str(e))
            # Don't raise here, return None for safer failure mode in production
            print(f"⚠️  Error retrieving key '{name}': {e}")
            return None

    def list_keys(self, include_encrypted: bool = False) -> list[dict[str, Any]]:
        """
        List all keys in wallet

        Args:
            include_encrypted: Include encrypted keys in output

        Returns:
            List of key metadata (without decrypted keys)
        """
        try:
            if self.use_db:
                keys = self._list_from_database()
            else:
                storage = self._load_storage()
                keys = storage["keys"]

            # Filter out encrypted keys unless requested
            result = []
            for key in keys:
                key_info = {
                    "id": key.get("id"),
                    "name": key["name"],
                    "key_type": key["key_type"],
                    "read_only": key["read_only"],
                    "service": key["service"],
                    "description": key["description"],
                    "created_at": key["created_at"],
                    "last_accessed": key.get("last_accessed"),
                    "access_count": key.get("access_count", 0),
                }

                if include_encrypted:
                    key_info["encrypted_key"] = key["encrypted_key"]

                result.append(key_info)

            self._audit_log("LIST", "*", f"count={len(result)}")
            return result
        except Exception as e:
            print(f"⚠️  Failed to list keys: {e}")
            return []

    def delete(self, name: str) -> bool:
        """
        Delete a key from wallet

        Args:
            name: Key name

        Returns:
            True if deleted, False if not found
        """
        try:
            if self.use_db:
                success = self._delete_from_database(name)
            else:
                storage = self._load_storage()
                original_count = len(storage["keys"])
                storage["keys"] = [k for k in storage["keys"] if k["name"] != name]
                success = len(storage["keys"]) < original_count

                if success:
                    self._save_storage(storage)

            if success:
                self._audit_log("DELETE", name, "Success")
            else:
                self._audit_log("DELETE_FAILED", name, "Key not found")

            return success
        except Exception as e:
            self._audit_log("DELETE_ERROR", name, str(e))
            print(f"⚠️  Failed to delete key '{name}': {e}")
            return False

    def _update_access_stats(self, name: str) -> None:
        """Update access statistics for a key (Local + Redis Sync)"""
        service_name = "unknown"

        # 1. Update Local Storage
        try:
            if self.use_db:
                sql = """
                UPDATE api_keys
                SET last_accessed = %s, access_count = access_count + 1
                WHERE name = %s
                RETURNING service;
                """
                conn = None
                try:
                    conn = self._get_connection()
                    with conn.cursor() as cur:
                        cur.execute(sql, (datetime.now(), name))
                        result = cur.fetchone()
                        if result:
                            service_name = result[0] or "unknown"
                    conn.commit()
                except Exception as e:
                    print(f"⚠️  Failed to update access stats in DB: {e}")
                    if conn:
                        conn.rollback()
                finally:
                    if conn:
                        self._release_connection(conn)
            else:
                storage = self._load_storage()
                for key in storage["keys"]:
                    if key["name"] == name:
                        key["last_accessed"] = datetime.now().isoformat()
                        key["access_count"] = key.get("access_count", 0) + 1
                        service_name = key.get("service", "unknown")
                        break
                self._save_storage(storage)
        except Exception as e:
            print(f"⚠️  Local access stats update failed: {e}")

        # 2. Sync to Redis (Monitoring Service)
        try:
            import redis

            # 중앙 설정 사용 (Phase 1 리팩토링)
            try:
                from AFO.utils.redis_connection import get_redis_url

                redis_url = get_redis_url()
            except ImportError:
                redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

            client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            )

            # Use the same key format as Monitoring Service: wallet:usage:{provider}
            # If service name is empty, default to 'unknown'
            provider = service_name if service_name else "unknown"
            redis_key = f"wallet:usage:{provider}"

            pipe = client.pipeline()
            pipe.hincrby(redis_key, "requests_count", 1)
            pipe.hset(redis_key, "last_used", datetime.now().isoformat())
            pipe.execute()
        except Exception as e:
            # Fail silently for Redis sync to avoid breaking the wallet if Redis is down
            print(f"⚠️  Failed to sync wallet usage to Redis: {e}")

    def track_token_usage(self, provider: str, tokens: int) -> None:
        """Track token usage in Redis"""
        try:
            import redis

            # 중앙 설정 사용 (Phase 1 리팩토링)
            try:
                from AFO.utils.redis_connection import get_redis_url

                redis_url = get_redis_url()
            except ImportError:
                redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

            client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            )

            redis_key = f"wallet:usage:{provider}"
            client.hincrby(redis_key, "tokens_used", tokens)
        except Exception as e:
            print(f"⚠️  Failed to track token usage in Redis: {e}")

    # Additional API methods for compatibility
    def get_summary(self) -> dict[str, Any]:
        """Get wallet summary"""
        keys = self.list_keys(include_encrypted=False)
        return {
            "total_keys": len(keys),
            "keys": [{"name": k["name"], "service": k.get("service", "unknown")} for k in keys],
        }

    def get_all(self) -> list[dict[str, Any]]:
        """Get all APIs (alias for list_keys)"""
        return self.list_keys(include_encrypted=False)

    def get_all_apis(self) -> list[dict[str, Any]]:
        """Get all APIs (alias for list_keys)"""
        return self.list_keys(include_encrypted=False)

    def get_api(self, api_id: str) -> dict[str, Any] | None:
        """Get specific API by ID"""
        if self.use_db:
            # PostgreSQL storage
            return self._get_from_database(api_id)
        else:
            # JSON file storage
            storage = self._load_storage()
            return next((k for k in storage["keys"] if k["name"] == api_id), None)

    def remove_api(self, api_id: str) -> bool:
        """Remove API (alias for delete)"""
        return self.delete(api_id)

    def delete_api(self, api_id: str) -> bool:
        """Delete API (alias for delete)"""
        return self.delete(api_id)

    def save_wallet(self) -> None:
        """Save wallet (no-op since auto-save is implemented)"""
        pass

    def sync_to_env(self) -> None:
        """Sync keys to environment variables"""
        keys = self.list_keys(include_encrypted=False)
        for key_data in keys:
            name = key_data["name"]
            key = key_data.get("key")
            if key:
                os.environ[f"API_{name.upper()}"] = key

    def test_api(self, api_id: str) -> dict[str, Any]:
        """Test API connection"""
        try:
            api_info = self.get_api(api_id)
            if not api_info:
                return {"success": False, "error": "API not found"}

            # Basic test - just check if key exists and is accessible
            return {
                "success": True,
                "api_id": api_id,
                "service": api_info.get("service", "unknown"),
                "last_accessed": api_info.get("last_accessed"),
                "access_count": api_info.get("access_count", 0),
            }
        except Exception as e:
            print(f"⚠️  API test failed: {e}")
            return {"success": False, "error": str(e)}

    # Database methods
    def _get_connection(self) -> Any:
        """Get connection from pool or use single connection"""
        try:
            if self.db is None:
                raise RuntimeError("Database connection not initialized")
            if hasattr(self.db, "getconn"):
                return self.db.getconn()
            return self.db
        except Exception as e:
            print(f"⚠️  Database connection error: {e}")
            raise

    def _release_connection(self, conn: Any) -> None:
        """Release connection back to pool"""
        try:
            if self.db is None:
                # Should not happen if _get_connection was successful
                return
            if hasattr(self.db, "putconn"):
                self.db.putconn(conn)
        except Exception as e:
            print(f"⚠️  Database release error: {e}")

    def _ensure_table_exists(self) -> None:
        """Create api_keys table if not exists"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS api_keys (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            encrypted_key TEXT NOT NULL,
            key_type VARCHAR(50),
            read_only BOOLEAN DEFAULT TRUE,
            service VARCHAR(100),
            description TEXT,
            key_hash VARCHAR(64),
            created_at TIMESTAMP,
            last_accessed TIMESTAMP,
            access_count INTEGER DEFAULT 0
        );
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute(create_table_sql)
            conn.commit()
        except Exception as e:
            print(f"⚠️  Failed to create api_keys table: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                self._release_connection(conn)

    def _add_to_database(self, key_data: dict[str, Any]) -> int:
        """Add key to PostgreSQL"""
        sql = """
        INSERT INTO api_keys (
            name, encrypted_key, key_type, read_only, service,
            description, key_hash, created_at, last_accessed, access_count
        ) VALUES (
            %(name)s, %(encrypted_key)s, %(key_type)s, %(read_only)s, %(service)s,
            %(description)s, %(key_hash)s, %(created_at)s, %(last_accessed)s, %(access_count)s
        ) RETURNING id;
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute(sql, key_data)
                result = cur.fetchone()
                if result is None:
                    raise RuntimeError("Failed to retrieve ID after insert")
                key_id = result[0]
            conn.commit()
            return int(key_id)
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                self._release_connection(conn)

    def _get_from_database(self, name: str) -> dict[str, Any] | None:
        """Get key from PostgreSQL"""
        sql = "SELECT * FROM api_keys WHERE name = %s;"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (name,))
                result = cur.fetchone()

            if result:
                # Convert datetime objects to ISO format strings for consistency
                if result.get("created_at"):
                    result["created_at"] = result["created_at"].isoformat()
                if result.get("last_accessed"):
                    result["last_accessed"] = result["last_accessed"].isoformat()
                return dict(result)
            return None
        finally:
            if conn:
                self._release_connection(conn)

    def _list_from_database(self) -> list[dict[str, Any]]:
        """List keys from PostgreSQL"""
        sql = "SELECT * FROM api_keys;"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                results = cur.fetchall()

            keys = []
            for row in results:
                r = dict(row)
                if r.get("created_at") and hasattr(r["created_at"], "isoformat"):
                    r["created_at"] = r["created_at"].isoformat()
                elif r.get("created_at"):
                    r["created_at"] = str(r["created_at"])

                if r.get("last_accessed") and hasattr(r["last_accessed"], "isoformat"):
                    r["last_accessed"] = r["last_accessed"].isoformat()
                elif r.get("last_accessed"):
                    r["last_accessed"] = str(r["last_accessed"])

                keys.append(r)
            return keys
        except Exception as e:
            print(f"⚠️  Updated list from DB failed: {e}")
            raise
        finally:
            if conn:
                self._release_connection(conn)

    def _delete_from_database(self, name: str) -> bool:
        """Delete key from PostgreSQL"""
        sql = "DELETE FROM api_keys WHERE name = %s;"
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute(sql, (name,))
                deleted = cur.rowcount > 0
            conn.commit()
            return bool(deleted)
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                self._release_connection(conn)


# Convenience functions
def create_wallet(encryption_key: str | None = None) -> APIWallet:
    """Create a new API Wallet instance"""
    return APIWallet(encryption_key=encryption_key)


# CLI for testing
def main() -> None:
    import sys

    wallet = create_wallet()

    if len(sys.argv) < 2:
        print("API Wallet CLI")
        print("\nUsage:")
        print("  python api_wallet.py add <name> <key> [service]")
        print("  python api_wallet.py get <name>")
        print("  python api_wallet.py list")
        print("  python api_wallet.py delete <name>")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "add":
            if len(sys.argv) < 4:
                print("Usage: python api_wallet.py add <name> <key> [service]")
                sys.exit(1)

            name = sys.argv[2]
            key = sys.argv[3]
            service = sys.argv[4] if len(sys.argv) > 4 else ""

            key_id = wallet.add(name, key, service=service)
            print(f"✅ Added key '{name}' with ID {key_id}")

        elif command == "get":
            if len(sys.argv) < 3:
                print("Usage: python api_wallet.py get <name>")
                sys.exit(1)

            name = sys.argv[2]
            key = wallet.get(name) or ""
            if key:
                print(f"🔑 Key '{name}': {key}")
            else:
                print(f"❌ Key '{name}' not found")

        elif command == "list":
            keys = wallet.list_keys()
            print(f"📋 Wallet Keys ({len(keys)}):")
            for k in keys:
                print(f"  - {k['name']} ({k.get('service', 'unknown')})")

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Usage: python api_wallet.py delete <name>")
                sys.exit(1)

            name = sys.argv[2]
            if wallet.delete(name):
                print(f"🗑️  Deleted key '{name}'")
            else:
                print(f"❌ Key '{name}' not found")
                sys.exit(1)

        else:
            print(f"❌ Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error executing command '{command}': {e}")
        sys.exit(1)
