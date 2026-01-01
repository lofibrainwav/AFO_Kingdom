import sys

sys.path.append("/AFO")
try:
    print("Attempting to import afo.api.routes.skills...")

    print("Success!")
except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
