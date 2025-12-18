#!/usr/bin/env python3
import sys
import os
import time

# Add package root to path
sys.path.append(os.path.abspath("packages/afo-core"))
sys.path.append(os.path.abspath("packages/trinity-os"))

try:
    from AFO.genui.genui_orchestrator import GenUIOrchestrator
    print("✅ GenUI Orchestrator imported successfully.")
except ImportError as e:
    print(f"❌ Failed to import GenUI Orchestrator: {e}")
    sys.exit(1)

def main():
    print("==================================================")
    print(" 👁️  Operation Creator: GenUI Vision Loop Verification")
    print("==================================================")

    orchestrator = GenUIOrchestrator(workspace_root=os.getcwd())
    
    # Define a test project
    project_id = "verification_genui_v1"
    prompt = "Create a futuristic calculator for Julie CPA"

    print(f">> 1. Initiating Project Creation: {project_id}")
    print(f"   Prompt: '{prompt}'")

    try:
        result = orchestrator.create_project(project_id, prompt)
        
        print("\n>> 2. Result Analysis")
        print(f"   - Status: {result.get('status')}")
        print(f"   - Code Path: {result.get('code_path')}")
        
        vision = result.get('vision_result', {})
        if vision.get('success'):
            print(f"   ✅ Vision Success: {vision.get('message')}")
            print(f"   📸 Screenshot stored at: {vision.get('path')}")
        else:
            print(f"   ⚠️ Vision Warning: {vision.get('error') or vision.get('message')}")
            print("   (Note: Vision might fail if Dashboard port 3000 is not reachable or path is 404)")

        # Verify file existence
        if os.path.exists(result['code_path']):
            print(f"   ✅ Verified: Source code file exists at {result['code_path']}")
        else:
            print(f"   ❌ Error: Source code file missing!")

    except Exception as e:
        print(f"❌ Execution Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n==================================================")
    print("✨ Vision Loop Test Complete")
    print("==================================================")

if __name__ == "__main__":
    main()
