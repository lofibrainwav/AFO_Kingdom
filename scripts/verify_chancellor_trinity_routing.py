# scripts/verify_chancellor_trinity_routing.py
"""
Verification script for Trinity-Driven Routing in Chancellor Graph.
Tests AUTO_RUN and ASK_COMMANDER scenarios.
"""

import asyncio
import os
import sys

# Ensure AFO package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

from langchain_core.messages import HumanMessage


async def verify_trinity_routing():
    """Test Trinity-Driven Routing logic."""
    print("=== Trinity-Driven Routing Verification ===")

    from AFO.chancellor_graph import chancellor_graph
    from AFO.domain.metrics.trinity_manager import trinity_manager

    # Test 1: High Trinity Score (AUTO_RUN)
    print("\n[Test 1] High Trinity Score (AUTO_RUN expected)")

    # Ensure scores are high
    trinity_manager.deltas = {
        "truth": 0,
        "goodness": 0,
        "beauty": 0,
        "filial_serenity": 0,
        "eternity": 0,
    }

    initial_state = {
        "messages": [HumanMessage(content="Simple status check")],
        "kingdom_context": {"llm_context": {"quality_tier": "STANDARD"}},
        "analysis_results": {},
    }

    config = {"configurable": {"thread_id": "test_auto_run"}}
    result = await chancellor_graph.ainvoke(initial_state, config=config)

    auto_run = result.get("auto_run_eligible", False)
    print(f"  auto_run_eligible: {auto_run}")
    print(f"  trinity_score: {result.get('trinity_score', 'N/A')}")
    print(f"  risk_score: {result.get('risk_score', 'N/A')}")

    if auto_run:
        print("  ✅ AUTO_RUN correctly triggered")
    else:
        print("  ⚠️ ASK_COMMANDER (Trinity Score may be < 0.9 or Risk > 0.1)")

    # Test 2: Low Trinity Score (ASK_COMMANDER)
    print("\n[Test 2] Low Trinity Score (ASK_COMMANDER expected)")

    # Apply multiple negative triggers to lower score significantly
    for _ in range(5):
        trinity_manager.apply_trigger("VERIFICATION_FAIL")  # -10 Truth each
        trinity_manager.apply_trigger("MANUAL_INTERVENTION")  # -5 Serenity each

    config2 = {"configurable": {"thread_id": "test_ask_commander"}}
    result2 = await chancellor_graph.ainvoke(initial_state, config=config2)

    auto_run2 = result2.get("auto_run_eligible", False)
    print(f"  auto_run_eligible: {auto_run2}")
    print(f"  trinity_score: {result2.get('trinity_score', 'N/A')}")
    print(f"  risk_score: {result2.get('risk_score', 'N/A')}")

    if not auto_run2:
        print("  ✅ ASK_COMMANDER correctly triggered")
    else:
        print("  ❌ AUTO_RUN triggered unexpectedly")

    print("\n=== Verification Complete ===")


if __name__ == "__main__":
    asyncio.run(verify_trinity_routing())
