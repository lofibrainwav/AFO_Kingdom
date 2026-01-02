#!/usr/bin/env python3
"""Debug script for Chancellor Graph testing."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "packages", "afo-core"))

print("=== Chancellor Graph Debug Test ===")

try:
    print("1. Importing Chancellor Graph...")
    from AFO.chancellor_graph import chancellor_graph

    print("✅ Import successful")

    print("2. Testing basic invoke...")
    result = chancellor_graph.invoke("test")
    print("✅ Invoke completed")

    print("3. Checking DecisionResult...")
    decision = result.get("decision", {})
    if decision:
        print("✅ DecisionResult found")
        print(f"   Mode: {decision.get('mode')}")
        print(".2f")
        print(".2f")
        print(f"   Reasons: {decision.get('reasons')}")
    else:
        print("❌ DecisionResult missing")

    print("4. Checking Sequential Thinking...")
    outputs = result.get("outputs", {})
    if "sequential_thinking" in outputs:
        print("✅ Sequential Thinking applied")
    else:
        print("❌ Sequential Thinking missing")

    print("5. Checking Context7...")
    if "context7" in outputs:
        print("✅ Context7 injected")
        context7 = outputs["context7"]
        if "KINGDOM_DNA" in context7:
            print("✅ Kingdom DNA injected")
        else:
            print("❌ Kingdom DNA missing")
    else:
        print("❌ Context7 missing")

    print("=== Test Complete ===")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
