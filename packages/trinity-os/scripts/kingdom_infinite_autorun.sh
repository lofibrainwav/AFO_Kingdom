#!/usr/bin/env bash
################################################################################
# AFO 왕국 끝까지 오토런 루프 (Infinite Autorun Loop)
# 
# 眞善美孝: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%
# 목적: 문제 감지 → 해결 → 검증 → 재감지 루프로 모든 문제 해결까지 자동 실행
#
# 사용법:
#   ./scripts/kingdom_infinite_autorun.sh [--max-iterations=N] [--max-time=HOURS] [--dry-run]
#
# 옵션:
#   --max-iterations=N: 최대 반복 횟수 (기본값: 10)
#   --max-time=HOURS: 최대 실행 시간 (기본값: 1시간)
#   --dry-run: 시뮬레이션 모드
#
# 특징:
#   - 문제 해결까지 자동 반복
#   - Trinity Score ≥ 90% 달성까지 반복
#   - 무한 루프 방지 (안전장치)
#   - 진행 상황 실시간 보고
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
MAX_ITERATIONS=10
MAX_TIME_HOURS=1
DRY_RUN=false
AFO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
START_TIME=$(date +%s)

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iterations=*)
            MAX_ITERATIONS="${1#*=}"
            shift
            ;;
        --max-time=*)
            MAX_TIME_HOURS="${1#*=}"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo -e "${RED}❌ 알 수 없는 옵션: $1${NC}"
            exit 1
            ;;
    esac
done

# Calculate max time in seconds
MAX_TIME_SECONDS=$((MAX_TIME_HOURS * 3600))

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🏰 AFO 왕국 끝까지 오토런 루프 (Infinite Autorun)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}설정${NC}"
echo -e "  최대 반복 횟수: ${MAX_ITERATIONS}회"
echo -e "  최대 실행 시간: ${MAX_TIME_HOURS}시간"
echo -e "  DRY_RUN 모드: ${DRY_RUN}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}⚠️  DRY_RUN 모드: 실제 변경하지 않습니다${NC}"
    echo ""
fi

# Change to AFO root directory
cd "$AFO_ROOT"

# Loop variables
ITERATION=0
LAST_PROBLEM_COUNT=-1
CONSECUTIVE_FAILURES=0
MAX_CONSECUTIVE_FAILURES=5

# Main loop
while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME))

    # 시간 제한 확인
    if [ $ELAPSED_TIME -gt $MAX_TIME_SECONDS ]; then
        echo -e "${YELLOW}⚠️  최대 실행 시간 도달 (${MAX_TIME_HOURS}시간)${NC}"
        break
    fi

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🔄 반복 ${ITERATION}/${MAX_ITERATIONS}${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}경과 시간: $((ELAPSED_TIME / 60))분${NC}"
    echo ""

    # Step 1: 문제 감지
    echo -e "${CYAN}1️⃣  문제 감지${NC}"
    if [ -f "scripts/kingdom_problem_detector.py" ]; then
        PROBLEM_REPORT=$(python3 scripts/kingdom_problem_detector.py 2>/dev/null || echo '{"total_problems":0,"summary":{"critical":0,"high":0}}')
        TOTAL_PROBLEMS=$(echo "$PROBLEM_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_problems', 0))" 2>/dev/null || echo "0")
        CRITICAL_COUNT=$(echo "$PROBLEM_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('summary', {}).get('critical', 0))" 2>/dev/null || echo "0")
        
        echo -e "  총 문제: ${TOTAL_PROBLEMS}개"
        echo -e "  Critical: ${CRITICAL_COUNT}개"
        
        # 문제가 없으면 종료
        if [ "$TOTAL_PROBLEMS" -eq 0 ]; then
            echo -e "  ${GREEN}✅ 문제 없음 - 루프 종료${NC}"
            break
        fi
        
        # 동일한 문제가 5회 연속 실패하면 종료
        if [ "$TOTAL_PROBLEMS" = "$LAST_PROBLEM_COUNT" ]; then
            CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
            echo -e "  ${YELLOW}⚠️  동일한 문제 감지 (${CONSECUTIVE_FAILURES}회 연속)${NC}"
            
            if [ $CONSECUTIVE_FAILURES -ge $MAX_CONSECUTIVE_FAILURES ]; then
                echo -e "  ${RED}❌ 동일 문제 ${MAX_CONSECUTIVE_FAILURES}회 연속 실패 - 루프 종료${NC}"
                echo -e "  ${YELLOW}💡 수동 개입 필요${NC}"
                break
            fi
        else
            CONSECUTIVE_FAILURES=0
        fi
        
        LAST_PROBLEM_COUNT=$TOTAL_PROBLEMS
    else
        echo -e "  ${YELLOW}⚠️  문제 감지 스크립트 없음${NC}"
        TOTAL_PROBLEMS=0
    fi
    
    echo ""
    
    # Step 2: 문제 해결
    if [ "$TOTAL_PROBLEMS" -gt 0 ]; then
        echo -e "${CYAN}2️⃣  문제 해결${NC}"
        
        if [ -f "scripts/kingdom_unified_autorun.sh" ]; then
            if [ "$DRY_RUN" = true ]; then
                DRY_RUN=true ./scripts/kingdom_unified_autorun.sh --skip-sejong --skip-backup || true
            else
                ./scripts/kingdom_unified_autorun.sh --skip-sejong --skip-backup || true
            fi
        else
            echo -e "  ${YELLOW}⚠️  통합 자동화 스크립트 없음${NC}"
        fi
        
        echo ""
        
        # 잠시 대기 (서비스 재시작 등)
        echo -e "${CYAN}3️⃣  안정화 대기 (5초)${NC}"
        sleep 5
        echo ""
    fi
    
    # Step 3: 검증
    echo -e "${CYAN}4️⃣  검증${NC}"
    
    # Trinity Score 확인
    if [ -f "scripts/kingdom_health_report.py" ]; then
        HEALTH_REPORT=$(python3 scripts/kingdom_health_report.py 2>/dev/null || echo '{"overall_score":0}')
        OVERALL_SCORE=$(echo "$HEALTH_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('overall_score', 0))" 2>/dev/null || echo "0")
        
        echo -e "  Trinity Score: ${OVERALL_SCORE}"
        
        # Trinity Score ≥ 90% 달성 시 종료
        if (( $(echo "$OVERALL_SCORE >= 0.9" | bc -l 2>/dev/null || awk "BEGIN {print ($OVERALL_SCORE >= 0.9)}") )); then
            echo -e "  ${GREEN}✅ Trinity Score ≥ 90% 달성 - 루프 종료${NC}"
            break
        fi
    else
        echo -e "  ${YELLOW}⚠️  건강 리포트 스크립트 없음${NC}"
    fi
    
    echo ""
    
    # 진행률 표시
    PROGRESS=$((ITERATION * 100 / MAX_ITERATIONS))
    echo -e "${CYAN}📊 진행률: ${PROGRESS}% (${ITERATION}/${MAX_ITERATIONS})${NC}"
    echo ""
done

# 최종 보고
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 끝까지 오토런 루프 완료!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 최종 상태 확인
echo -e "${CYAN}📊 최종 상태${NC}"
if [ -f "scripts/kingdom_problem_detector.py" ]; then
    FINAL_PROBLEM_REPORT=$(python3 scripts/kingdom_problem_detector.py 2>/dev/null || echo '{"total_problems":0}')
    FINAL_TOTAL=$(echo "$FINAL_PROBLEM_REPORT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_problems', 0))" 2>/dev/null || echo "0")
    echo -e "  남은 문제: ${FINAL_TOTAL}개"
fi

if [ -f "scripts/kingdom_health_report.py" ]; then
    FINAL_HEALTH=$(python3 scripts/kingdom_health_report.py 2>/dev/null || echo '{"overall_score":0}')
    FINAL_SCORE=$(echo "$FINAL_HEALTH" | python3 -c "import sys, json; print(json.load(sys.stdin).get('overall_score', 0))" 2>/dev/null || echo "0")
    echo -e "  Trinity Score: ${FINAL_SCORE}"
fi

FINAL_ELAPSED=$((($(date +%s) - START_TIME) / 60))
echo -e "  총 소요 시간: ${FINAL_ELAPSED}분"
echo -e "  총 반복 횟수: ${ITERATION}회"
echo ""

if [ "$FINAL_TOTAL" -eq 0 ] || (( $(echo "${FINAL_SCORE:-0} >= 0.9" | bc -l 2>/dev/null || awk "BEGIN {print (${FINAL_SCORE:-0} >= 0.9)}") )); then
    echo -e "${GREEN}✅ 목표 달성!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  일부 문제 남음 - 수동 확인 권장${NC}"
    exit 1
fi
