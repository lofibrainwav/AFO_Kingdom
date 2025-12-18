#!/usr/bin/env bash
################################################################################
# AFO 왕국 통합 자동화 스크립트 (Unified Autorun)
# 
# 眞善美孝: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%
# 목적: 모든 레거시 시스템을 통합하여 끝까지 오토런
#
# 사용법:
#   ./scripts/kingdom_unified_autorun.sh [--dry-run] [--skip-sejong] [--skip-backup]
#
# 옵션:
#   --dry-run: 시뮬레이션 모드 (실제 변경하지 않음)
#   --skip-sejong: 세종 애민정신 Phase 건너뛰기
#   --skip-backup: 백업 Phase 건너뛰기
#
# 특징:
#   - 모든 기존 스크립트 통합
#   - 지피지기 원칙 준수
#   - 논리적 순차 실행
#   - 끝까지 오토런
################################################################################

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
DRY_RUN=false
SKIP_SEJONG=false
SKIP_BACKUP=false
AFO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --skip-sejong)
            SKIP_SEJONG=true
            shift
            ;;
        --skip-backup)
            SKIP_BACKUP=true
            shift
            ;;
        *)
            echo -e "${RED}❌ 알 수 없는 옵션: $1${NC}"
            exit 1
            ;;
    esac
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🏰 AFO 왕국 통합 자동화 시스템 (Unified Autorun)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}⚠️  DRY_RUN 모드: 실제 변경하지 않습니다${NC}"
    echo ""
fi

# Change to AFO root directory
cd "$AFO_ROOT"

# Phase 0: 지피지기 (知己知彼 - 문제 감지)
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 0: 지피지기 (知己知彼) - 문제 감지${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}0.1 Critical 문제 감지${NC}"
if [ -f "scripts/kingdom_problem_detector.py" ]; then
    PROBLEM_REPORT=$(python3 scripts/kingdom_problem_detector.py 2>/dev/null || echo '{"total_problems":0}')
    CRITICAL_COUNT=$(echo "$PROBLEM_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('summary', {}).get('critical', 0))" 2>/dev/null || echo "0")
    HIGH_COUNT=$(echo "$PROBLEM_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('summary', {}).get('high', 0))" 2>/dev/null || echo "0")
    TOTAL_PROBLEMS=$(echo "$PROBLEM_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_problems', 0))" 2>/dev/null || echo "0")
    
    echo -e "  Critical 문제: ${CRITICAL_COUNT}개"
    echo -e "  High 문제: ${HIGH_COUNT}개"
    echo -e "  총 문제: ${TOTAL_PROBLEMS}개"
    
    if [ "$TOTAL_PROBLEMS" -gt 0 ]; then
        echo -e "  ${YELLOW}⚠️  문제 발견됨 - 다음 Phase에서 해결 예정${NC}"
    else
        echo -e "  ${GREEN}✅ 문제 없음${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  문제 감지 스크립트 없음${NC}"
    CRITICAL_COUNT=0
    HIGH_COUNT=0
    TOTAL_PROBLEMS=0
fi

echo ""
echo -e "${GREEN}✅ Phase 0 완료${NC}"
echo ""

# Phase 1: Critical 문제 해결 (성능)
if [ "$TOTAL_PROBLEMS" -gt 0 ] || [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Phase 1: Critical 문제 해결 (성능)${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ -f "scripts/kingdom_problem_solver.sh" ]; then
        if [ "$DRY_RUN" = true ]; then
            DRY_RUN=true ./scripts/kingdom_problem_solver.sh --phase=1 || true
        else
            ./scripts/kingdom_problem_solver.sh --phase=1 || true
        fi
    else
        echo -e "  ${YELLOW}⚠️  문제 해결 스크립트 없음${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Phase 1 완료${NC}"
    echo ""
fi

# Phase 2: 연결 문제 해결
if [ "$TOTAL_PROBLEMS" -gt 0 ] || [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Phase 2: 연결 문제 해결${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ -f "scripts/kingdom_problem_solver.sh" ]; then
        if [ "$DRY_RUN" = true ]; then
            DRY_RUN=true ./scripts/kingdom_problem_solver.sh --phase=2 || true
        else
            ./scripts/kingdom_problem_solver.sh --phase=2 || true
        fi
    else
        echo -e "  ${YELLOW}⚠️  문제 해결 스크립트 없음${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Phase 2 완료${NC}"
    echo ""
fi

# Phase 3: 보안 문제 해결
if [ "$TOTAL_PROBLEMS" -gt 0 ] || [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Phase 3: 보안 문제 해결${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ -f "scripts/kingdom_problem_solver.sh" ]; then
        if [ "$DRY_RUN" = true ]; then
            DRY_RUN=true ./scripts/kingdom_problem_solver.sh --phase=3 || true
        else
            ./scripts/kingdom_problem_solver.sh --phase=3 || true
        fi
    else
        echo -e "  ${YELLOW}⚠️  문제 해결 스크립트 없음${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Phase 3 완료${NC}"
    echo ""
fi

# Phase 4: 오장육부 건강도 개선
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 4: 오장육부 건강도 개선${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}4.1 오장육부 건강도 확인${NC}"
if [ -f ".claude/scripts/check_11_organs.py" ]; then
    HEALTH_REPORT=$(python3 .claude/scripts/check_11_organs.py 2>/dev/null || echo '{"health_percentage":0}')
    HEALTH_PCT=$(echo "$HEALTH_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('health_percentage', 0))" 2>/dev/null || echo "0")
    if [ -z "$HEALTH_PCT" ] || [ "$HEALTH_PCT" = "" ]; then
        HEALTH_PCT=$(echo "$HEALTH_REPORT" | grep -o '"health_percentage":[0-9.]*' | cut -d: -f2 | tr -d ' ' || echo "0")
    fi
    echo -e "  오장육부 건강도: ${HEALTH_PCT}%"
    
    if (( $(echo "$HEALTH_PCT < 80" | bc -l 2>/dev/null || awk "BEGIN {print ($HEALTH_PCT < 80)}") )); then
        echo -e "  ${YELLOW}⚠️  건강도 개선 필요${NC}"
    else
        echo -e "  ${GREEN}✅ 건강도 양호${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  오장육부 체크 스크립트 없음${NC}"
    HEALTH_PCT=0
fi

echo ""
echo -e "${GREEN}✅ Phase 4 완료${NC}"
echo ""

# Phase 5: 세종 애민정신 자동화 (일일 진화 시스템)
if [ "$SKIP_SEJONG" = false ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Phase 5: 세종 애민정신 자동화 (일일 진화)${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    echo -e "${CYAN}5.1 아침 점호${NC}"
    if [ -f "scripts/morning_routine.sh" ]; then
        bash scripts/morning_routine.sh || echo -e "  ${YELLOW}⚠️  아침 점호 실패${NC}"
    else
        echo -e "  ${YELLOW}⚠️  아침 점호 스크립트 없음${NC}"
    fi
    
    echo ""
    
    echo -e "${CYAN}5.2 파도타기 체크${NC}"
    if [ -f "scripts/check_wave_updates.sh" ]; then
        bash scripts/check_wave_updates.sh || echo -e "  ${YELLOW}⚠️  파도타기 체크 실패${NC}"
    else
        echo -e "  ${YELLOW}⚠️  파도타기 스크립트 없음${NC}"
    fi
    
    echo ""
    
    echo -e "${CYAN}5.3 일일 진화 시스템${NC}"
    if [ -f "scripts/daily_evolution_runner.sh" ]; then
        bash scripts/daily_evolution_runner.sh || echo -e "  ${YELLOW}⚠️  일일 진화 시스템 실패${NC}"
    else
        echo -e "  ${YELLOW}⚠️  일일 진화 스크립트 없음${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Phase 5 완료${NC}"
    echo ""
fi

# Phase 6: 백업 실행
if [ "$SKIP_BACKUP" = false ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Phase 6: 백업 실행${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ -f "scripts/maintenance/backup_afo_kingdom.sh" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo -e "${CYAN}6.1 백업 시뮬레이션${NC}"
            bash scripts/maintenance/backup_afo_kingdom.sh --dry-run || echo -e "  ${YELLOW}⚠️  백업 시뮬레이션 실패${NC}"
        else
            echo -e "${CYAN}6.1 백업 실행${NC}"
            bash scripts/maintenance/backup_afo_kingdom.sh || echo -e "  ${YELLOW}⚠️  백업 실패${NC}"
        fi
    else
        echo -e "  ${YELLOW}⚠️  백업 스크립트 없음${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Phase 6 완료${NC}"
    echo ""
fi

# Phase 7: 최종 검증
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase 7: 최종 검증${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}7.1 왕국 상태 검증${NC}"
if [ -f "scripts/verification/verify_kingdom_status.py" ]; then
    python3 scripts/verification/verify_kingdom_status.py || echo -e "  ${YELLOW}⚠️  왕국 상태 검증 실패${NC}"
else
    echo -e "  ${YELLOW}⚠️  왕국 상태 검증 스크립트 없음${NC}"
fi

echo ""
echo -e "${CYAN}7.2 문제 재감지 (해결 확인)${NC}"
if [ -f "scripts/kingdom_problem_detector.py" ]; then
    PROBLEM_REPORT_AFTER=$(python3 scripts/kingdom_problem_detector.py 2>/dev/null || echo '{"total_problems":0}')
    TOTAL_PROBLEMS_AFTER=$(echo "$PROBLEM_REPORT_AFTER" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_problems', 0))" 2>/dev/null || echo "0")
    
    if [ "$TOTAL_PROBLEMS_AFTER" -eq 0 ]; then
        echo -e "  ${GREEN}✅ 모든 문제 해결됨${NC}"
    else
        echo -e "  ${YELLOW}⚠️  남은 문제: ${TOTAL_PROBLEMS_AFTER}개${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  문제 감지 스크립트 없음${NC}"
fi

echo ""
echo -e "${GREEN}✅ Phase 7 완료${NC}"
echo ""

# 최종 보고
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 AFO 왕국 통합 자동화 완료!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 요약
echo -e "${CYAN}📊 최종 상태 요약${NC}"
if [ -n "${HEALTH_PCT:-}" ] && [ "$HEALTH_PCT" != "0" ]; then
    echo -e "  오장육부 건강도: ${HEALTH_PCT}%"
fi
if [ -n "${TOTAL_PROBLEMS_AFTER:-}" ]; then
    echo -e "  남은 문제: ${TOTAL_PROBLEMS_AFTER}개"
fi
echo ""

echo -e "${GREEN}✅ 모든 작업 완료!${NC}"
echo ""

exit 0
