import os
import sys
import importlib.util
import requests

def check_truth():
    print("Checking 眞 (Truth)...")
    # Check mypy.ini/pyproject.toml for strict mode (File presence)
    if os.path.exists("pyproject.toml") or os.path.exists("mypy.ini"):
        print("✅ Type Configuration Found")
    else:
        print("❌ Type Configuration Missing")
        return False
    return True

def check_goodness():
    print("Checking 善 (Goodness)...")
    try:
        from AFO.config.antigravity import antigravity
        if antigravity.DRY_RUN_DEFAULT:
            print("✅ AntiGravity DRY_RUN_DEFAULT = True")
        else:
            print("❌ AntiGravity DRY_RUN_DEFAULT = False (RISK!)")
            return False
    except ImportError:
         # Manually check file content if import fails due to path issues in script
         with open("packages/afo-core/AFO/config/antigravity.py", "r") as f:
             if "DRY_RUN_DEFAULT: bool = True" in f.read():
                 print("✅ AntiGravity DRY_RUN_DEFAULT = True (Static Check)")
             else:
                 print("❌ AntiGravity DRY_RUN_DEFAULT Check Failed")
                 return False
    return True

def check_beauty():
    print("Checking 美 (Beauty)...")
    layers = ["packages/afo-core/AFO/api", "packages/afo-core/AFO/domain", "packages/afo-core/AFO/services", "packages/dashboard/src/components"]
    all_exist = True
    for l in layers:
        if os.path.exists(l):
            print(f"✅ Layer Exists: {l}")
        else:
            print(f"❌ Layer Missing: {l}")
            all_exist = False
    return all_exist

def check_serenity():
    print("Checking 孝 (Serenity)...")
    # Check Matrix Stream Endpoint
    try:
        res = requests.get("http://localhost:8011/api/stream/health") # Assuming /health or similar exists or just check connection
        # Actually stream endpoint might be /api/stream/thoughts
        # Let's check the main health endpoint as proxy for Zero Friction
        res = requests.get("http://localhost:8011/api/health")
        if res.status_code == 200:
            print("✅ System Health Endpoint Active (Zero Friction)")
        else:
            print(f"❌ System Health Check Failed: {res.status_code}")
            return False
    except Exception as e:
        print(f"❌ Serenity Check Failed (Connection): {e}")
        return False
    return True

def check_eternity():
    print("Checking 永 (Eternity)...")
    try:
        from AFO.domain.metrics.trinity_ssot import TrinityWeights
        total = TrinityWeights.TRUTH + TrinityWeights.GOODNESS + TrinityWeights.BEAUTY + TrinityWeights.SERENITY + TrinityWeights.ETERNITY
        if 0.99 <= total <= 1.01:
            print(f"✅ SSOT Weights Sum to {total} (Perfect)")
            print(f"   Truth: {TrinityWeights.TRUTH}, Goodness: {TrinityWeights.GOODNESS}, Beauty: {TrinityWeights.BEAUTY}, Serenity: {TrinityWeights.SERENITY}, Eternity: {TrinityWeights.ETERNITY}")
        else:
            print(f"❌ SSOT Weights Sum Error: {total}")
            return False
    except ImportError:
         # Static check
         with open("packages/afo-core/AFO/domain/metrics/trinity_ssot.py", "r") as f:
             content = f.read()
             if "TRUTH: Final[float] = 0.35" in content and "ETERNITY: Final[float] = 0.02" in content:
                 print("✅ SSOT Weights Verified (Static Check)")
             else:
                 print("❌ SSOT Weights Check Failed")
                 return False
    return True

if __name__ == "__main__":
    print("🏛️  Foundation Integrity Re-Inspection Started")
    if all([check_truth(), check_goodness(), check_beauty(), check_serenity(), check_eternity()]):
        print("\n✨ ALL PILLARS SECURE. READY FOR PHASE 14.")
        sys.exit(0)
    else:
        print("\n⚠️  FOUNDATION CRACKS DETECTED.")
        sys.exit(1)
