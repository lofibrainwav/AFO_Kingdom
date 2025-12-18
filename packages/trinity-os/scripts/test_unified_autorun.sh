#!/usr/bin/env bash
################################################################################
# AFO 왕국 통합 자동화 테스트 스크립트
# 
# 眞善美孝: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%
# 목적: DRY_RUN 모드로 전체 워크플로우 테스트 및 검증
#
# 사용법:
#   ./scripts/test_unified_autorun.sh
#
# 특징:
#   - DRY_RUN 모드로 안전하게 테스트
#   - 각 Phase별 검증
#   - 통합 스크립트 호환성 확인
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
echo -e "${GREEN}🧪 AFO 왕국 통합 자동화 테스트${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 테스트 결과 추적
TESTS_PASSED=0
TESTS_FAILED=0
TEST_RESULTS=()

# 테스트 함수
test_script_exists() {
    local script_path="$1"
    local test_name="$2"
    
    if [ -f "$script_path" ]; then
        echo -e "  ${GREEN}✅ ${test_name}: 존재함${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("✅ $test_name")
        return 0
    else
        echo -e "  ${RED}❌ ${test_name}: 없음${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("❌ $test_name")
        return 1
    fi
}

test_script_executable() {
    local script_path="$1"
    local test_name="$2"
    
    if [ -x "$script_path" ]; then
        echo -e "  ${GREEN}✅ ${test_name}: 실행 가능${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("✅ $test_name (executable)")
        return 0
    else
        echo -e "  ${YELLOW}⚠️  ${test_name}: 실행 권한 없음${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("⚠️ $test_name (not executable)")
        return 1
    fi
}

test_script_runs() {
    local script_path="$1"
    local test_name="$2"
    local timeout="${3:-30}"
    
    if [ ! -f "$script_path" ]; then
        echo -e "  ${RED}❌ ${test_name}: 스크립트 없음${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("❌ $test_name (script missing)")
        return 1
    fi
    
    # Python 스크립트인지 확인
    if [[ "$script_path" == *.py ]]; then
        if timeout "$timeout" python3 "$script_path" --help >/dev/null 2>&1 || \
           timeout "$timeout" python3 "$script_path" >/dev/null 2>&1; then
            echo -e "  ${GREEN}✅ ${test_name}: 실행 성공${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            TEST_RESULTS+=("✅ $test_name (runs)")
            return 0
        else
            echo -e "  ${YELLOW}⚠️  ${test_name}: 실행 실패 (타임아웃 또는 오류)${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            TEST_RESULTS+=("⚠️ $test_name (run failed)")
            return 1
        fi
    else
        # Bash 스크립트
        if bash -n "$script_path" 2>/dev/null; then
            echo -e "  ${GREEN}✅ ${test_name}: 문법 검사 통과${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            TEST_RESULTS+=("✅ $test_name (syntax OK)")
            return 0
        else
            echo -e "  ${RED}❌ ${test_name}: 문법 오류${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            TEST_RESULTS+=("❌ $test_name (syntax error)")
            return 1
        fi
    fi
}

# Phase 1: 필수 스크립트 존재 확인
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 1: 필수 스크립트 존재 확인${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

test_script_exists "scripts/kingdom_problem_detector.py" "문제 감지 엔진"
test_script_exists "scripts/kingdom_unified_autorun.sh" "통합 자동화 스크립트"
test_script_exists "scripts/kingdom_auto_recovery.py" "자동 복구 메커니즘"
test_script_exists "scripts/kingdom_infinite_autorun.sh" "끝까지 오토런 루프"
test_script_exists "scripts/kingdom_spirit_integration.py" "왕국 정신 통합"
test_script_exists "scripts/kingdom_health_report.py" "통합 건강 리포트"

echo ""
echo -e "${GREEN}✅ Phase 1 완료${NC}"
echo ""

# Phase 2: 실행 권한 확인
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 2: 실행 권한 확인${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

test_script_executable "scripts/kingdom_unified_autorun.sh" "통합 자동화 스크립트"
test_script_executable "scripts/kingdom_infinite_autorun.sh" "끝까지 오토런 루프"

echo ""
echo -e "${GREEN}✅ Phase 2 완료${NC}"
echo ""

# Phase 3: 스크립트 실행 테스트 (DRY_RUN)
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 3: 스크립트 실행 테스트 (DRY_RUN)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}3.1 문제 감지 엔진 테스트${NC}"
test_script_runs "scripts/kingdom_problem_detector.py" "문제 감지 엔진" 60

echo ""
echo -e "${CYAN}3.2 통합 건강 리포트 테스트${NC}"
test_script_runs "scripts/kingdom_health_report.py" "통합 건강 리포트" 120

echo ""
echo -e "${CYAN}3.3 왕국 정신 통합 테스트${NC}"
test_script_runs "scripts/kingdom_spirit_integration.py" "왕국 정신 통합" 30

echo ""
echo -e "${CYAN}3.4 통합 자동화 스크립트 문법 검사${NC}"
test_script_runs "scripts/kingdom_unified_autorun.sh" "통합 자동화 스크립트"

echo ""
echo -e "${CYAN}3.5 끝까지 오토런 루프 문법 검사${NC}"
test_script_runs "scripts/kingdom_infinite_autorun.sh" "끝까지 오토런 루프"

echo ""
echo -e "${GREEN}✅ Phase 3 완료${NC}"
echo ""

# Phase 4: 통합 워크플로우 테스트 (DRY_RUN)
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 4: 통합 워크플로우 테스트 (DRY_RUN)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}4.1 통합 자동화 스크립트 DRY_RUN${NC}"
if [ -f "scripts/kingdom_unified_autorun.sh" ]; then
    if DRY_RUN=true bash scripts/kingdom_unified_autorun.sh --skip-sejong --skip-backup >/dev/null 2>&1; then
        echo -e "  ${GREEN}✅ DRY_RUN 성공${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("✅ 통합 자동화 DRY_RUN")
    else
        echo -e "  ${YELLOW}⚠️  DRY_RUN 실패 (일부 오류 가능)${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("⚠️ 통합 자동화 DRY_RUN")
    fi
else
    echo -e "  ${RED}❌ 스크립트 없음${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TEST_RESULTS+=("❌ 통합 자동화 DRY_RUN (script missing)")
fi

echo ""
echo -e "${GREEN}✅ Phase 4 완료${NC}"
echo ""

# Phase 5: 의존성 확인
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 5: 의존성 확인${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}5.1 필수 스크립트 의존성 확인${NC}"

# kingdom_unified_autorun.sh가 호출하는 스크립트들 확인
DEPENDENCIES=(
    "scripts/kingdom_problem_solver.sh"
    ".claude/scripts/check_11_organs.py"
    "scripts/verification/verify_kingdom_status.py"
    "scripts/maintenance/backup_afo_kingdom.sh"
    "scripts/morning_routine.sh"
    "scripts/check_wave_updates.sh"
    "scripts/daily_evolution_runner.sh"
)

for dep in "${DEPENDENCIES[@]}"; do
    if [ -f "$dep" ]; then
        echo -e "  ${GREEN}✅ $(basename "$dep")${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "  ${YELLOW}⚠️  $(basename "$dep") 없음 (선택적 의존성일 수 있음)${NC}"
    fi
done

echo ""
echo -e "${GREEN}✅ Phase 5 완료${NC}"
echo ""

# 최종 보고
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📊 테스트 결과 요약${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
if [ $TOTAL_TESTS -gt 0 ]; then
    PASS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))
    echo -e "  총 테스트: ${TOTAL_TESTS}개"
    echo -e "  통과: ${GREEN}${TESTS_PASSED}개${NC}"
    echo -e "  실패: ${RED}${TESTS_FAILED}개${NC}"
    echo -e "  통과율: ${PASS_RATE}%"
    echo ""
    
    echo -e "${CYAN}상세 결과:${NC}"
    for result in "${TEST_RESULTS[@]}"; do
        echo -e "  $result"
    done
    echo ""
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}✅ 모든 테스트 통과!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  일부 테스트 실패${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  테스트 실행 안 됨${NC}"
    exit 1
fi
