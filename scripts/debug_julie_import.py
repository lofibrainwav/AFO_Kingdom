import sys
import os

# Add package root to path
sys.path.append("/Users/brnestrm/AFO_Kingdom/packages/afo-core")

try:
    print("Attempting to import Julie Royal Router...")
    from AFO.api.routers.julie_royal import router
    print("✅ Success! Router imported.")
    for route in router.routes:
        print(f" - {route.path} {route.methods}")
except Exception as e:
    print(f"❌ Import Failed: {e}")
    import traceback
    traceback.print_exc()
