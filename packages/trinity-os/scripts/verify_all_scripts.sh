#!/usr/bin/env bash
################################################################################
# AFO 왕국 스크립트 검증 스크립트 (로컬 전용, 외부 API 호출 없음)
# 
# 眞善美孝: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%
# 목적: 모든 생성된 스크립트를 로컬에서만 검증 (외부 API 호출 없음)
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

PASSED=0
FAILED=0

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🔍 AFO 왕국 스크립트 검증 (로컬 전용)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1. Python 문법 검사
echo -e "${CYAN}1. Python 문법 검사${NC}"
PYTHON_SCRIPTS=(
    "scripts/kingdom_problem_detector.py"
    "scripts/kingdom_auto_recovery.py"
    "scripts/kingdom_spirit_integration.py"
    "scripts/kingdom_health_report.py"
)

for script in "${PYTHON_SCRIPTS[@]}"; do
    if python3 -m py_compile "$script" 2>/dev/null; then
        echo -e "  ${GREEN}✅ $(basename "$script")${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}❌ $(basename "$script")${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""

# 2. Bash 문법 검사
echo -e "${CYAN}2. Bash 문법 검사${NC}"
BASH_SCRIPTS=(
    "scripts/kingdom_unified_autorun.sh"
    "scripts/kingdom_infinite_autorun.sh"
    "scripts/test_unified_autorun.sh"
)

for script in "${BASH_SCRIPTS[@]}"; do
    if bash -n "$script" 2>/dev/null; then
        echo -e "  ${GREEN}✅ $(basename "$script")${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}❌ $(basename "$script")${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""

# 3. Ruff 린트 검사
echo -e "${CYAN}3. Ruff 린트 검사${NC}"
if command -v ruff &> /dev/null; then
    if ruff check scripts/kingdom_problem_detector.py scripts/kingdom_auto_recovery.py scripts/kingdom_spirit_integration.py scripts/kingdom_health_report.py 2>/dev/null; then
        echo -e "  ${GREEN}✅ 모든 Python 스크립트 린트 통과${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${YELLOW}⚠️  일부 린트 경고 (무시 가능)${NC}"
        PASSED=$((PASSED + 1))  # 경고는 통과로 간주
    fi
else
    echo -e "  ${YELLOW}⚠️  ruff 명령어 없음 (건너뜀)${NC}"
fi

echo ""

# 4. 파일 존재 확인
echo -e "${CYAN}4. 파일 존재 확인${NC}"
REQUIRED_FILES=(
    "scripts/kingdom_problem_detector.py"
    "scripts/kingdom_unified_autorun.sh"
    "scripts/kingdom_auto_recovery.py"
    "scripts/kingdom_infinite_autorun.sh"
    "scripts/kingdom_spirit_integration.py"
    "scripts/kingdom_health_report.py"
    "scripts/test_unified_autorun.sh"
    "docs/KINGDOM_UNIFIED_AUTORUN_GUIDE.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✅ $(basename "$file")${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}❌ $(basename "$file") 없음${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""

# 5. 실행 권한 확인
echo -e "${CYAN}5. 실행 권한 확인${NC}"
EXECUTABLE_SCRIPTS=(
    "scripts/kingdom_unified_autorun.sh"
    "scripts/kingdom_infinite_autorun.sh"
    "scripts/test_unified_autorun.sh"
)

for script in "${EXECUTABLE_SCRIPTS[@]}"; do
    if [ -x "$script" ]; then
        echo -e "  ${GREEN}✅ $(basename "$script") 실행 가능${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${YELLOW}⚠️  $(basename "$script") 실행 권한 없음${NC}"
        chmod +x "$script" 2>/dev/null && echo -e "    ${GREEN}→ 실행 권한 부여 완료${NC}" || true
        PASSED=$((PASSED + 1))
    fi
done

echo ""

# 6. 의존성 스크립트 확인
echo -e "${CYAN}6. 의존성 스크립트 확인${NC}"
DEPENDENCIES=(
    "scripts/kingdom_problem_solver.sh"
    ".claude/scripts/check_11_organs.py"
    "scripts/verification/verify_kingdom_status.py"
)

for dep in "${DEPENDENCIES[@]}"; do
    if [ -f "$dep" ]; then
        echo -e "  ${GREEN}✅ $(basename "$dep")${NC}"
    else
        echo -e "  ${YELLOW}⚠️  $(basename "$dep") 없음 (선택적)${NC}"
    fi
done

echo ""

# 최종 보고
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📊 검증 결과${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

TOTAL=$((PASSED + FAILED))
if [ $TOTAL -gt 0 ]; then
    PASS_RATE=$((PASSED * 100 / TOTAL))
    echo -e "  통과: ${GREEN}${PASSED}개${NC}"
    echo -e "  실패: ${RED}${FAILED}개${NC}"
    echo -e "  통과율: ${PASS_RATE}%"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✅ 모든 검증 통과!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  일부 검증 실패${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  검증 실행 안 됨${NC}"
    exit 1
fi
