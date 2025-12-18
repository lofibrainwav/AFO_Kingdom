#!/usr/bin/env bash
################################################################################
# Cursor IDE 설정 체크 스크립트
# 
# 목적: "insufficient funds" 오류 원인 파악 및 해결
# 외부 API 호출 없이 로컬 설정만 확인
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
echo -e "${GREEN}🔍 Cursor IDE 설정 체크${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1. Cursor 설정 파일 확인
echo -e "${CYAN}1. Cursor 설정 파일 확인${NC}"

CURSOR_FILES=(
    ".cursor/environment.json"
    ".cursor/mcp.json"
    ".claude/settings.local.json"
    ".vscode/settings.json"
)

for file in "${CURSOR_FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
        echo -e "  ${GREEN}✅ $file (${SIZE} bytes)${NC}"
    else
        echo -e "  ${YELLOW}⚠️  $file 없음${NC}"
    fi
done

echo ""

# 2. environment.json 내용 확인
echo -e "${CYAN}2. .cursor/environment.json 내용${NC}"
if [ -f ".cursor/environment.json" ]; then
    cat .cursor/environment.json | python3 -m json.tool 2>/dev/null || cat .cursor/environment.json
else
    echo -e "  ${YELLOW}⚠️  파일 없음${NC}"
fi

echo ""

# 3. settings.local.json 내용 확인 (민감 정보 제외)
echo -e "${CYAN}3. .claude/settings.local.json 구조${NC}"
if [ -f ".claude/settings.local.json" ]; then
    python3 -c "
import json
with open('.claude/settings.local.json') as f:
    data = json.load(f)
    print('  Keys:', list(data.keys()))
    if 'permissions' in data:
        print('  Permissions count:', len(data['permissions'].get('allow', [])))
    if 'enabledMcpjsonServers' in data:
        print('  MCP Servers:', data['enabledMcpjsonServers'])
" 2>/dev/null || echo "  ${YELLOW}⚠️  파싱 실패${NC}"
else
    echo -e "  ${YELLOW}⚠️  파일 없음${NC}"
fi

echo ""

# 4. VSCode 설정 확인
echo -e "${CYAN}4. .vscode/settings.json 확인${NC}"
if [ -f ".vscode/settings.json" ]; then
    # review 관련 설정 찾기
    if grep -q -i "review" .vscode/settings.json 2>/dev/null; then
        echo -e "  ${YELLOW}⚠️  review 관련 설정 발견${NC}"
        grep -i "review" .vscode/settings.json | head -5
    else
        echo -e "  ${GREEN}✅ review 관련 설정 없음${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  파일 없음${NC}"
fi

echo ""

# 5. 권장사항
echo -e "${CYAN}5. 권장사항${NC}"
echo -e "  ${YELLOW}💡 'insufficient funds' 오류는 Cursor의 자동 리뷰 기능 때문일 수 있습니다${NC}"
echo -e "  ${YELLOW}💡 해결 방법:${NC}"
echo -e "    1. Cursor Settings → Features → Code Review 비활성화"
echo -e "    2. 또는 .vscode/settings.json에 다음 추가:"
echo -e "       {\"cursor.codeReview.enabled\": false}"
echo -e "    3. Cursor 재시작"

echo ""

# 6. 현재 Cursor 프로세스 확인
echo -e "${CYAN}6. Cursor 프로세스 확인${NC}"
if pgrep -f "Cursor" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅ Cursor 실행 중${NC}"
    echo -e "  ${YELLOW}💡 Cursor 재시작 권장 (설정 변경 후)${NC}"
else
    echo -e "  ${YELLOW}⚠️  Cursor 실행 안 됨${NC}"
fi

echo ""

echo -e "${GREEN}✅ 설정 체크 완료${NC}"
echo ""
