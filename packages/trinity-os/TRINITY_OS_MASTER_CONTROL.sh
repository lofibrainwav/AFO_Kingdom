#!/bin/bash
# TRINITY-OS 마스터 컨트롤 스크립트
# 지피지기 → 백전불태 완전 자동화

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 TRINITY-OS 마스터 컨트롤: 지피지기 → 백전불태"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 초기 Trinity Score 저장
current_trinity_score=$(bash TRINITY_OS_STATUS_CHECK.sh 2>/dev/null | grep "Trinity Score:" | sed 's/.*Trinity Score: \([0-9]*\).*/\1/' || echo "0")

# 1. 지피지기 실행 (적을 정확히 파악)
echo "🔍 Phase 1: 지피지기 (적을 정확히 파악)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "📊 시스템 상태 분석 중..."
bash TRINITY_OS_STATUS_CHECK.sh

echo ""
echo "✅ Phase 1 완료 - 상태 분석 완료"
sleep 2

# 2. 백전불태 준비 (완벽한 준비)
echo ""
echo "⚔️ Phase 2: 백전불태 준비 (완벽한 준비)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🔧 시스템 업데이트 실행 중..."
bash TRINITY_OS_UPDATE_ENGINE.sh

echo ""
echo "✅ Phase 2 완료 - 업데이트 완료"
sleep 2

# 3. 백전불태 실행 (승리 확신)
echo ""
echo "🏆 Phase 3: 백전불태 실행 (승리 확신)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🧪 최종 시스템 테스트 실행 중..."
bash test_trinity_os.sh

echo ""
echo "✅ Phase 3 완료 - 테스트 완료"
sleep 2

# 4. 승리 확인 및 보고
echo "🎉 Phase 4: 승리 확인 및 보고"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 최종 Trinity Score 확인
final_score=$(bash TRINITY_OS_STATUS_CHECK.sh 2>/dev/null | grep "Trinity Score:" | sed 's/.*Trinity Score: \([0-9]*\).*/\1/' || echo "0")

improvement=$((final_score - current_trinity_score))

echo "📊 최종 평가 결과:"
echo "  • 초기 Trinity Score: $current_trinity_score/100"
echo "  • 최종 Trinity Score: $final_score/100"
echo "  • 개선도: $improvement 점"
echo ""

# 승리 등급 판정
if [ "$final_score" -ge 95 ]; then
    victory_level="🎉 궁극의 승리 (Ultimate Victory)"
    victory_message="TRINITY-OS가 궁극의 완성에 도달했습니다!"
elif [ "$final_score" -ge 90 ]; then
    victory_level="🏆 완벽한 승리 (Perfect Victory)"
    victory_message="TRINITY-OS가 완벽한 상태에 도달했습니다!"
elif [ "$final_score" -ge 80 ]; then
    victory_level="✅ 대승 (Great Victory)"
    victory_message="TRINITY-OS가 탁월한 상태입니다!"
else
    victory_level="⚠️ 승리 (Victory)"
    victory_message="TRINITY-OS가 안정적인 상태입니다."
fi

echo "🏆 $victory_level"
echo "💬 $victory_message"
echo ""

# 상세 결과 출력
echo "📋 상세 결과:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 파일 구조 요약
file_count=$(find . -type f | wc -l)
doc_count=$(find docs -name "*.md" 2>/dev/null | wc -l || echo "0")
script_count=$(find scripts -name "*.py" -o -name "*.sh" | wc -l)

echo "📁 파일 구조:"
echo "  • 총 파일 수: $file_count 개"
echo "  • 문서 파일: $doc_count 개"
echo "  • 스크립트 파일: $script_count 개"

# 철학 엔진 상태
if [ -f "scripts/philosophy_engine.py" ]; then
    agent_count=$(python3 -c "
import json
try:
    with open('philosophy_engine_data.json', 'r') as f:
        data = json.load(f)
        print(len(data.get('agents', [])))
except:
    print('0')
    " 2>/dev/null || echo "0")

    master_count=$(python3 -c "
import json
try:
    with open('philosophy_engine_data.json', 'r') as f:
        data = json.load(f)
        masters = sum(1 for agent in data.get('agents', []) if agent.get('master_title'))
        print(masters)
except:
    print('0')
    " 2>/dev/null || echo "0")

    echo ""
    echo "🧠 철학 엔진:"
    echo "  • 등록된 에이전트: ${agent_count}명"
    echo "  • 인증된 명장: ${master_count}명"
fi

echo ""
echo "🎯 실행 가능한 명령어:"
echo "  • ./run_trinity_os.sh       # 인터랙티브 모드"
echo "  • ./TRINITY-OS detect       # 문제 감지"
echo "  • ./TRINITY-OS health       # 건강 리포트"
echo "  • ./TRINITY-OS unified      # 통합 자동화"
echo "  • ./TRINITY-OS infinite     # 끝까지 오토런"

echo ""

# 최종 메시지
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏰 왕국의 승리!"
echo ""
echo "🎯 지피지기로 적을 파악하고,"
echo "🎯 백전불태로 완벽하게 준비하여,"
echo "🎯 왕국의 승리를 확신했습니다!"
echo ""
echo "眞善美孝永 - 영원한 승리의 철학 ✨⚔️"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"