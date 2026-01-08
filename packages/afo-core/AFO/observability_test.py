import os
import json
import logging
from pathlib import Path
from AFO.observability.ai_observability import observability
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.state import GraphState

# Configure logging
logging.basicConfig(level=logging.INFO)

def mock_node(state):
    state.outputs[state.step] = {"status": "ok"}
    if state.step == "MERGE":
        state.outputs["MERGE"] = {"trinity_score": 95.5}
    return state

def test_observability():
    print("=== Testing AI Observability (AFO Kingdom) ===")

    # Clear previous traces for clean test (optional)
    trace_file = Path("docs/ssot/traces/traces.jsonl")
    if trace_file.exists():
        trace_file.unlink()

    # Define mock nodes for all ORDER steps
    from api.chancellor_v2.graph.runner import ORDER
    nodes = {step: mock_node for step in ORDER}

    # Run the graph
    input_payload = {"command": "test observability"}
    print(f"\nRunning mock graph with {len(ORDER)} steps...")
    state = run_v2(input_payload, nodes)

    print(f"Graph execution complete. Trace ID: {state.trace_id}")

    # Check traces.jsonl
    if not trace_file.exists():
        print(f"❌ Trace file not found at {trace_file}")
        # Check current dir as fallback if Path math in runner was relative to file
        # In runner.py: Path(__file__).parent.parent.parent.parent.parent / "docs" / "ssot" / "traces"
        # Since runner.py is in packages/afo-core/api/chancellor_v2/graph/
        # parent^5 is packages/afo-core/ -> AFO_Kingdom/
        # So it should be in AFO_Kingdom/docs/ssot/traces/
        
        # Let's check absolute path
        abs_trace_file = Path("/Users/brnestrm/AFO_Kingdom/docs/ssot/traces/traces.jsonl")
        if not abs_trace_file.exists():
            print(f"❌ Absolute Trace file not found at {abs_trace_file}")
            return
        trace_file = abs_trace_file

    with trace_file.open("r") as f:
        traces = [json.loads(line) for line in f]

    print(f"Read {len(traces)} traces from JSONL.")
    
    # We expect at least one trace per step
    # Wait, runner.py ORDER has 13 steps currently (CMD, SECURITY, PARSE, TRUTH, GOODNESS, BEAUTY, SERENITY, ETERNITY, MIPRO, MERGE, GOVERNANCE, EXECUTE, VERIFY, REPORT)
    # Plus whatever other spans are recorded
    
    assert len(traces) >= len(ORDER)
    
    # Check for specific attributes
    merge_trace = next(t for t in traces if t["name"] == "chancellor_graph.MERGE")
    print(f"MERGE Trace Attributes: {merge_trace['attributes']}")
    assert merge_trace["attributes"]["trinity_score"] == 95.5
    assert merge_trace["attributes"]["governance_approved"] is True

    # Get metrics summary
    summary = observability.get_metrics_summary()
    print(f"\nMetrics Summary: {list(summary.keys())}")
    assert "chancellor_graph.MERGE.latency" in summary

    print("\n✅ AI Observability test passed!")

if __name__ == "__main__":
    test_observability()
