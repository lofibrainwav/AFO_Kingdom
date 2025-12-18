"""
MCP Server Verification Script
Verify AFO Ultimate MCP Server via JSON-RPC 2.0 (stdio)
"""

import json
import subprocess

SERVER_PATH = "packages/trinity-os/trinity_os/servers/afo_ultimate_mcp_server.py"


def verify_mcp():
    print("🔌 Starting AFO Ultimate MCP Server Verification...")

    # Start the server process
    process = subprocess.Popen(
        ["python", SERVER_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,  # Unbuffered
    )

    try:
        # 1. Initialize
        print("\n🔹 Requesting Initialize...")
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "Verifier", "version": "1.0"},
            },
        }
        process.stdin.write(json.dumps(init_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        if not response_line:
            print("❌ No response from server.")
            return

        print(f"Server Response: {response_line.strip()}")
        resp = json.loads(response_line)
        assert resp["result"]["serverInfo"]["name"] == "AfoUltimate"
        print("✅ Initialize Success")

        # 2. List Tools
        print("\n🔹 Requesting tools/list...")
        list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        process.stdin.write(json.dumps(list_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Server Response: {response_line.strip()}")
        resp = json.loads(response_line)
        tools = resp["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        print(f"Tools Found: {tool_names}")

        assert "shell_execute" in tool_names
        assert "kingdom_health" in tool_names
        assert "calculate_trinity_score" in tool_names
        assert "verify_fact" in tool_names
        print("✅ Tools List Success")

        # 3. Test Trinity Score
        print("\n🔹 Testing calculate_trinity_score...")
        trinity_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "calculate_trinity_score",
                "arguments": {
                    "truth_base": 90,
                    "goodness_base": 85,
                    "beauty_base": 80,
                    "friction": 0,
                    "eternity_base": 90,
                },
            },
        }
        process.stdin.write(json.dumps(trinity_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        content = json.loads(resp["result"]["content"][0]["text"])
        assert content["trinity_score"] > 80
        print("✅ Trinity Score Calculation Success")

        # 4. Test Fact Verification
        print("\n🔹 Testing verify_fact...")
        fact_req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "verify_fact",
                "arguments": {"claim": "The sky is blue", "context": "General knowledge"},
            },
        }
        process.stdin.write(json.dumps(fact_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        content = json.loads(resp["result"]["content"][0]["text"])
        assert content["verdict"] == "PLAUSIBLE"
        print("✅ Fact Verification Success")
        # Print stderr if any
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"STDERR: {stderr_output}")

    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

    print("\n🎉 MCP Verification Complete!")


if __name__ == "__main__":
    verify_mcp()
