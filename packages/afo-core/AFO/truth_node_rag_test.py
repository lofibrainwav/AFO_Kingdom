import asyncio
import json
import logging
from typing import Any

from api.chancellor_v2.graph.nodes.truth_node import truth_node
from api.chancellor_v2.graph.state import GraphState

# Configure logging
logging.basicConfig(level=logging.INFO)


async def test_truth_node_rag():
    print("=== Testing TRUTH Node with Agentic RAG (AFO Kingdom) ===")

    # Case 1: Complex Query (should invoke reasoning)
    state = GraphState(
        trace_id="test_rag_truth",
        request_id="req_rag_truth",
        input={"command": "How does specialized multimodal branch integration work?"},
    )
    state.plan = {"skill_id": "multimodal_fanout_join"}

    print("\nEvaluating query with Agentic RAG grounding...")
    result = await truth_node(state)
    
    truth_output = result.outputs.get("TRUTH", {})
    print(f"Truth Score: {truth_output.get('score'):.2f}")
    
    rag_grounding = truth_output.get("rag_grounding", {})
    print(f"RAG Confidence: {rag_grounding.get('confidence'):.2f}")
    print("\nDecision Path:")
    for step in rag_grounding.get("decision_path", []):
        print(f"  - {step}")

    assert "rag_grounding" in truth_output
    assert truth_output.get("score") > 0  # Should have a valid score

    print("\n✅ Agentic RAG Truth Node test passed!")


if __name__ == "__main__":
    asyncio.run(test_truth_node_rag())
