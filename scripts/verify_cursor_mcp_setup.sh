#!/usr/bin/env bash
################################################################################
# Cursor MCP 설정 검증 스크립트
# 
# 목적: Cursor IDE의 MCP 서버 설정이 올바르게 되어 있는지 검증
################################################################################

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

AFO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$AFO_ROOT"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🔍 Cursor MCP 설정 검증${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1. MCP 설정 파일 확인
echo -e "${CYAN}1. MCP 설정 파일 확인${NC}"

MCP_FILE=".cursor/mcp.json"
if [ -f "$MCP_FILE" ]; then
    SIZE=$(stat -f%z "$MCP_FILE" 2>/dev/null || stat -c%s "$MCP_FILE" 2>/dev/null || echo "0")
    echo -e "  ${GREEN}✅ $MCP_FILE (${SIZE} bytes)${NC}"
    
    # JSON 형식 검증
    if python3 -m json.tool "$MCP_FILE" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅ JSON 형식 검증 통과${NC}"
    else
        echo -e "  ${RED}❌ JSON 형식 오류${NC}"
        exit 1
    fi
else
    echo -e "  ${RED}❌ $MCP_FILE 없음${NC}"
    exit 1
fi

echo ""

# 2. 등록된 MCP 서버 확인
echo -e "${CYAN}2. 등록된 MCP 서버${NC}"

python3 << 'PYTHON'
import json
import sys
from pathlib import Path

try:
    mcp_file = Path(".cursor/mcp.json")
    if not mcp_file.exists():
        print("  ❌ MCP 설정 파일 없음")
        sys.exit(1)
    
    data = json.loads(mcp_file.read_text())
    servers = data.get("mcpServers", {})
    
    print(f"  총 {len(servers)}개 서버 등록됨:")
    print()
    
    # 외부 서버
    external_servers = ["memory", "filesystem", "sequential-thinking", "brave-search", "context7"]
    afo_servers = ["afo-ultimate-mcp", "afo-skills-mcp", "trinity-score-mcp"]
    
    print("  📦 외부 MCP 서버:")
    for server in external_servers:
        if server in servers:
            print(f"    ✅ {server}")
        else:
            print(f"    ⚠️  {server} (누락)")
    
    print()
    print("  🏰 AFO Kingdom MCP 서버:")
    for server in afo_servers:
        if server in servers:
            server_info = servers[server]
            desc = server_info.get("description", "No description")
            print(f"    ✅ {server}")
            print(f"       {desc}")
            
            # 파일 경로 확인
            args = server_info.get("args", [])
            if args:
                server_path = args[0] if args else None
                if server_path and Path(server_path).exists():
                    print(f"       📄 {server_path} ✅")
                elif server_path:
                    print(f"       📄 {server_path} ❌ (파일 없음)")
        else:
            print(f"    ❌ {server} (누락)")
    
    print()
    print("  📊 Skills:")
    skills = data.get("skills", {})
    for skill_name, skill_info in skills.items():
        endpoint = skill_info.get("endpoint", "N/A")
        print(f"    ✅ {skill_name}: {endpoint}")
    
except Exception as e:
    print(f"  ❌ 오류: {e}")
    sys.exit(1)
PYTHON

echo ""

# 3. MCP 서버 파일 존재 확인
echo -e "${CYAN}3. MCP 서버 파일 존재 확인${NC}"

MCP_SERVERS=(
    "packages/trinity-os/trinity_os/servers/afo_ultimate_mcp_server.py"
    "packages/trinity-os/trinity_os/servers/afo_skills_mcp.py"
    "packages/trinity-os/trinity_os/servers/trinity_score_mcp.py"
)

for server_file in "${MCP_SERVERS[@]}"; do
    if [ -f "$server_file" ]; then
        echo -e "  ${GREEN}✅ $server_file${NC}"
    else
        echo -e "  ${RED}❌ $server_file (파일 없음)${NC}"
    fi
done

echo ""

# 4. 권장사항
echo -e "${CYAN}4. 권장사항${NC}"
echo -e "  ${YELLOW}💡 Cursor IDE를 재시작하면 새로운 MCP 서버가 활성화됩니다${NC}"
echo -e "  ${YELLOW}💡 MCP 서버 상태는 Cursor Settings → MCP Servers에서 확인할 수 있습니다${NC}"

echo ""
echo -e "${GREEN}✅ MCP 설정 검증 완료${NC}"
echo ""

