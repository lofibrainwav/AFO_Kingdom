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

        # 5. Test Shell Execute
        print("\n🔹 Testing shell_execute...")
        shell_req = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "shell_execute",
                "arguments": {"command": "echo 'Hello AFO'"},
            },
        }
        process.stdin.write(json.dumps(shell_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        content = resp["result"]["content"][0]["text"]
        assert "Hello AFO" in content
        print("✅ Shell Execute Success")

        # 6. Test Write File
        print("\n🔹 Testing write_file...")
        test_file_path = "temp_test_mcp.txt"
        write_req = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "write_file",
                "arguments": {"path": test_file_path, "content": "AFO Verification Content"},
            },
        }
        process.stdin.write(json.dumps(write_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        assert not resp["result"]["isError"]
        print("✅ Write File Success")

        # 7. Test Read File
        print("\n🔹 Testing read_file...")
        read_req = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "read_file",
                "arguments": {"path": test_file_path},
            },
        }
        process.stdin.write(json.dumps(read_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        content = resp["result"]["content"][0]["text"]
        assert "AFO Verification Content" in content
        print("✅ Read File Success")

        # Cleanup temp file
        import os

        if os.path.exists(test_file_path):
            os.remove(test_file_path)

        # 8. Test CuPy Weighted Sum
        print("\n🔹 Testing cupy_weighted_sum...")
        math_req = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {
                "name": "cupy_weighted_sum",
                "arguments": {"data": [1.0, 2.0, 3.0], "weights": [0.5, 0.5, 0.5]},
            },
        }
        process.stdin.write(json.dumps(math_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        # Result should be 1*0.5 + 2*0.5 + 3*0.5 = 0.5 + 1.0 + 1.5 = 3.0
        content = resp["result"]["content"][0]["text"]
        assert float(content) == 3.0
        print("✅ CuPy Weighted Sum Success")

        # 9. Test Sequential Thinking
        print("\n🔹 Testing sequential_thinking...")
        think_req = {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "tools/call",
            "params": {
                "name": "sequential_thinking",
                "arguments": {
                    "thought": "Analysis of Trinity Score architecture shows hybrid engine is optimal.",
                    "thought_number": 1,
                    "total_thoughts": 3,
                    "next_thought_needed": True,
                },
            },
        }
        process.stdin.write(json.dumps(think_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        content = json.loads(resp["result"]["content"][0]["text"])
        assert content["status"] == "THINKING"
        print("✅ Sequential Thinking Success")

        # 10. Test Context7 (Retrieve Context)
        print("\n🔹 Testing retrieve_context...")
        ctx_req = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "retrieve_context",
                "arguments": {"query": "AFO Architecture", "domain": "technical"},
            },
        }
        process.stdin.write(json.dumps(ctx_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        content = json.loads(resp["result"]["content"][0]["text"])
        assert content["found"] is True
        assert "Chancellor" in content["context"]
        print("✅ Context7 Retrieval Success")

        # 11. Test Context7 (Soul & Body)
        print("\n🔹 Testing retrieve_context (Soul & Body)...")
        soul_req = {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "tools/call",
            "params": {
                "name": "retrieve_context",
                "arguments": {"query": "Sixxon Body Trinity Soul", "domain": "philosophy"},
            },
        }
        process.stdin.write(json.dumps(soul_req) + "\n")
        process.stdin.flush()

        response_line = process.stdout.readline()
        print(f"Tool Response: {response_line.strip()}")
        resp = json.loads(response_line)
        content = json.loads(resp["result"]["content"][0]["text"])
        assert content["found"] is True
        assert "Sixxon (The Physical Manifestation)" in content["context"]
        assert "Trinity 5 Pillars (The Soul)" in content["context"]
        print("✅ Context7 Soul & Body Retrieval Success")

        # 12. Test Playwright Bridge (Navigate & Scrape)
        print("\n🔹 Testing Playwright Bridge...")
        try:
            # Navigate
            nav_req = {
                "jsonrpc": "2.0",
                "id": 12,
                "method": "tools/call",
                "params": {
                    "name": "browser_navigate",
                    "arguments": {"url": "http://example.com"},
                },
            }
            process.stdin.write(json.dumps(nav_req) + "\n")
            process.stdin.flush()

            response_line = process.stdout.readline()
            print(f"Tool Response (Navigate): {response_line.strip()}")
            resp = json.loads(response_line)
            content = json.loads(resp["result"]["content"][0]["text"])

            if content.get("success"):
                print("✅ Browser Navigation Success")

                # Scrape
                scrape_req = {
                    "jsonrpc": "2.0",
                    "id": 13,
                    "method": "tools/call",
                    "params": {
                        "name": "browser_scrape",
                        "arguments": {"selector": "h1"},
                    },
                }
                process.stdin.write(json.dumps(scrape_req) + "\n")
                process.stdin.flush()

                response_line = process.stdout.readline()
                print(f"Tool Response (Scrape): {response_line.strip()}")
                resp = json.loads(response_line)
                content = json.loads(resp["result"]["content"][0]["text"])
                assert "Example Domain" in content["content"]
                print("✅ Browser Scrape Success")
            else:
                print(f"⚠️ Browser Navigation Failed: {content.get('error')}")
                print("Skipping Scrape Test due to Navigation Failure")

        except Exception as e:
            print(f"⚠️ Playwright Test Skipped/Failed: {e}")

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
