import os
import sys

sys.path.append("/AFO")
try:
    print("Attempting to import AFO.api.routes.skills...")
    from AFO.api.routes import skills

    print("Success!")
except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
