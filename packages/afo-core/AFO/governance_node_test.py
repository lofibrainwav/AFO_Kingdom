import asyncio
import json
import logging
from typing import Any

from AFO.agents.governance_agent import RiskLevel
from api.chancellor_v2.graph.nodes.governance_node import governance_node
from api.chancellor_v2.graph.state import GraphState

# Configure logging
logging.basicConfig(level=logging.INFO)


async def test_governance_node():
    print("=== Testing Governance Node (AFO Kingdom) ===")

    # Case 1: Allowed Action
    state_allowed = GraphState(
        trace_id="test_allowed",
        request_id="req_allowed",
        input={"command": "list files in docs"},
    )
    state_allowed.outputs["MERGE"] = {
        "action": "list_files",
        "agent": "Chancellor",
        "target_path": "docs",
        "trinity_score": 90.0,
    }

    print("\n[Case 1] Evaluating Allowed Action: list_files in docs")
    result_allowed = await governance_node(state_allowed)
    gov_output = result_allowed.outputs.get("GOVERNANCE", {})
    print(f"Decision: {gov_output.get('decision')}")
    print(f"Risk Level: {gov_output.get('risk_level')}")
    assert gov_output.get("decision") == "approved"

    # Case 2: Forbidden Action
    state_forbidden = GraphState(
        trace_id="test_forbidden",
        request_id="req_forbidden",
        input={"command": "delete production database"},
    )
    state_forbidden.outputs["MERGE"] = {
        "action": "delete_production_data",
        "agent": "Chancellor",
        "trinity_score": 10.0,
    }

    print("\n[Case 2] Evaluating Forbidden Action: delete_production_data")
    result_forbidden = await governance_node(state_forbidden)
    gov_output = result_forbidden.outputs.get("GOVERNANCE", {})
    print(f"Decision: {gov_output.get('decision')}")
    print(f"Risk Level: {gov_output.get('risk_level')}")
    print(f"Reasoning: {gov_output.get('reasoning')}")
    assert gov_output.get("decision") == "escalated"
    assert gov_output.get("risk_level") == RiskLevel.CRITICAL.value
    assert "governance_blocked" in result_forbidden.outputs.get("_meta", {})

    # Case 3: Restricted Directory
    state_restricted = GraphState(
        trace_id="test_restricted",
        request_id="req_restricted",
        input={"command": "edit sensitive file in /etc/shadow"},
    )
    state_restricted.outputs["MERGE"] = {
        "action": "write_file",
        "agent": "Chancellor",
        "target_path": "/etc/shadow",
        "trinity_score": 88.0,
    }

    print("\n[Case 3] Evaluating Restricted Directory: /etc/shadow")
    result_restricted = await governance_node(state_restricted)
    gov_output = result_restricted.outputs.get("GOVERNANCE", {})
    print(f"Decision: {gov_output.get('decision')}")
    print(f"Reasoning: {gov_output.get('reasoning')}")
    assert gov_output.get("decision") == "denied"

    print("\n✅ All Governance Node tests passed!")


if __name__ == "__main__":
    asyncio.run(test_governance_node())
