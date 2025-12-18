import os
import sys

# 프로젝트 루트 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

from AFO.security.vault_manager import vault, VaultManager

def verify_vault_manager():
    print("=== VaultManager Verification ===")
    
    # Check Singleton
    v1 = VaultManager.get_instance()
    v2 = VaultManager.get_instance()
    assert v1 is v2, "Singleton check failed"
    print("✅ Singleton Pattern Verified")
    
    # Check Fallback (Since we don't have Vault, it should use Env)
    print("\n[Step 1] Verifying Get Secret (Fallback)...")
    os.environ["TEST_SECRET_KEY"] = "EnvValue123"
    
    val = vault.get_secret("TEST_SECRET_KEY", default="DefaultValue")
    print(f"Result: {val}")
    
    assert val == "EnvValue123", "Fallback to Env failed"
    print("✅ Fallback to Environment Verified")
    
    # Check Default
    val_default = vault.get_secret("NON_EXISTENT_KEY", default="MyDefault")
    assert val_default == "MyDefault", "Default value failed"
    print("✅ Default Value Verified")

    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    verify_vault_manager()
