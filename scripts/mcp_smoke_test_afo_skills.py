#!/usr/bin/env python3
"""
MCP Smoke Test for AFO Skills Server
Tests basic MCP protocol compliance and tool listing functionality.
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path


def run_mcp_server_test():
    """Test MCP server using subprocess and stdio"""
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "packages" / "afo-core")
    env.setdefault("AFO_API_BASE_URL", "http://127.0.0.1:8010")

    # Start MCP server process
    server_cmd = [
        sys.executable, "-m", "AFO.mcp.afo_skills_mcp"
    ]

    print("🚀 Starting AFO Skills MCP Server...")
    print(f"Command: {' '.join(server_cmd)}")
    print(f"PYTHONPATH: {env['PYTHONPATH']}")
    print(f"AFO_API_BASE_URL: {env['AFO_API_BASE_URL']}")
    print()

    try:
        # Start server process
        server_proc = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            bufsize=1
        )

        print("📋 Sending initialize request...")

        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        server_proc.stdin.write(json.dumps(init_request) + "\n")
        server_proc.stdin.flush()

        # Read initialize response
        init_response_line = server_proc.stdout.readline().strip()
        if init_response_line:
            init_response = json.loads(init_response_line)
            print(f"✅ Initialize response: {init_response['result']['serverInfo']['name']} v{init_response['result']['serverInfo']['version']}")
        else:
            print("❌ No initialize response received")
            return False

        print("📋 Sending tools/list request...")

        # Send tools/list request
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        server_proc.stdin.write(json.dumps(list_request) + "\n")
        server_proc.stdin.flush()

        # Read tools/list response
        list_response_line = server_proc.stdout.readline().strip()
        if list_response_line:
            list_response = json.loads(list_response_line)
            tools = list_response['result']['tools']
            tool_names = [tool['name'] for tool in tools]

            print(f"✅ Tools found: {len(tools)}개")
            print(f"   도구 목록: {', '.join(tool_names)}")

            # Verify expected tools
            expected_tools = ['skills_list', 'skills_detail', 'skills_execute', 'genui_generate', 'afo_api_health']
            missing_tools = [tool for tool in expected_tools if tool not in tool_names]
            extra_tools = [tool for tool in tool_names if tool not in expected_tools]

            if missing_tools:
                print(f"❌ 누락된 도구: {missing_tools}")
                return False
            if extra_tools:
                print(f"⚠️  추가된 도구: {extra_tools}")

            print("✅ 모든 예상 도구가 정상적으로 등록됨")
            return True

        else:
            print("❌ No tools/list response received")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        # Clean up server process
        if 'server_proc' in locals():
            try:
                server_proc.terminate()
                server_proc.wait(timeout=5)
            except:
                server_proc.kill()


def main():
    """Main test function"""
    print("🧪 AFO Skills MCP Server Smoke Test")
    print("=" * 50)

    success = run_mcp_server_test()

    print()
    print("=" * 50)
    if success:
        print("🎉 SMOKE TEST PASSED")
        print("✅ AFO Skills MCP Server is ready for Cursor IDE integration")
        return 0
    else:
        print("💥 SMOKE TEST FAILED")
        print("❌ AFO Skills MCP Server needs debugging")
        return 1


if __name__ == "__main__":
    sys.exit(main())