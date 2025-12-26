#!/bin/bash
# AFO Ultimate MCP Server Launcher
# MCP 공식 스펙에 따라 STDIO 기반 JSON-RPC 통신을 제공

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Python 경로 설정
export PYTHONPATH="$PROJECT_ROOT/packages/trinity-os:$PROJECT_ROOT/packages/afo-core:$PYTHONPATH"

# MCP 서버 실행
python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/packages/trinity-os')
sys.path.insert(0, '$PROJECT_ROOT/packages/afo-core')

from trinity_os.servers.afo_ultimate_mcp_server import AfoUltimateMCPServer
AfoUltimateMCPServer.run_loop()
"