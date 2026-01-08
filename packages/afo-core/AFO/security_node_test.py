import json
import logging
from typing import Any

from AFO.agents.security_agent import ThreatLevel, security_agent
from api.chancellor_v2.graph.nodes.security_node import security_node
from api.chancellor_v2.graph.state import GraphState

# Configure logging
logging.basicConfig(level=logging.INFO)


def test_security_node():
    print("=== Testing Security Node (AFO Kingdom) ===")

    # Case 1: Safe Action
    state_safe = GraphState(
        trace_id="test_safe",
        request_id="req_safe",
        input={"command": "list files", "source": "user_a"},
    )

    print("\n[Case 1] Evaluating Safe Action: list files")
    result_safe = security_node(state_safe)
    sec_output = result_safe.outputs.get("SECURITY", {})
    print(f"Status: {sec_output.get('status')}")
    assert sec_output.get("status") == "clear"

    # Case 2: Injection Attempt
    state_injection = GraphState(
        trace_id="test_injection",
        request_id="req_injection",
        input={"command": "'; DROP TABLE users; --", "source": "attacker"},
    )

    print("\n[Case 2] Evaluating Injection Attempt: SQL Injection")
    result_injection = security_node(state_injection)
    sec_output = result_injection.outputs.get("SECURITY", {})
    print(f"Status: {sec_output.get('status')}")
    print(f"Threat Level: {sec_output.get('threat_level')}")
    assert sec_output.get("status") == "threat_detected"
    assert len(result_injection.errors) > 0

    # Case 3: Blocked Entity
    security_agent.block_entity("bad_actor", "Repeated violations")
    state_blocked = GraphState(
        trace_id="test_blocked",
        request_id="req_blocked",
        input={"command": "list files", "source": "bad_actor"},
    )

    print("\n[Case 3] Evaluating Blocked Entity: bad_actor")
    result_blocked = security_node(state_blocked)
    sec_output = result_blocked.outputs.get("SECURITY", {})
    print(f"Status: {sec_output.get('status')}")
    assert sec_output.get("status") == "blocked"

    print("\n✅ All Security Node tests passed!")


if __name__ == "__main__":
    test_security_node()
