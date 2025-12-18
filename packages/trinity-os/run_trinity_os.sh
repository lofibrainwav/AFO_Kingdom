#!/bin/bash
# TRINITY-OS: AFO 왕국의 새로운 운영체제
# 철학 엔진 통합: 에이전트들이 왕국의 철학을 즉시 이해하고 공부할 수 있는 구조

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 TRINITY-OS 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 작업 디렉터리 확인
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 작업 디렉터리: $SCRIPT_DIR"
echo ""

# 철학 엔진 초기화 확인
echo "🧠 철학 엔진 초기화 중..."
if [ ! -f "scripts/philosophy_engine.py" ]; then
    echo "❌ 철학 엔진을 찾을 수 없습니다."
    exit 1
fi

# Python 환경 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되어 있지 않습니다."
    exit 1
fi

echo "✅ Python3 버전: $(python3 --version)"
echo "✅ 철학 엔진: 준비 완료"
echo ""

# 철학 엔진 상태 확인
echo "📊 철학 엔진 상태 확인 중..."
python3 -c "
from scripts.philosophy_engine import philosophy_engine
print('✅ 철학 엔진 로드 성공')
agents_count = len(philosophy_engine.agents)
print(f'📈 등록된 에이전트: {agents_count}명')
if agents_count > 0:
    masters_count = sum(1 for agent in philosophy_engine.agents.values() if agent.master_title)
    print(f'🏆 등록된 명장: {masters_count}명')
" 2>/dev/null || echo "⚠️ 철학 엔진 상태 확인 실패 (무시 가능)"
echo ""

# 기본 검증
echo "🔍 기본 검증 중..."

# 스크립트 존재 확인
SCRIPTS=(
    "scripts/kingdom_problem_detector.py"
    "scripts/kingdom_health_report.py"
    "scripts/kingdom_spirit_integration.py"
    "scripts/kingdom_unified_autorun.sh"
    "scripts/verify_all_scripts.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "  ✅ $script 존재"
    else
        echo "  ❌ $script 없음"
        exit 1
    fi
done

echo ""
echo "🎯 TRINITY-OS 명령어 선택:"
echo "   (철학 엔진이 당신의 성장을 실시간 모니터링합니다)"
echo ""

echo "TRINITY-OS 코어 기능:"
echo "  1) 문제 감지 (眞 - 진실의 추구)"
echo "  2) 건강 리포트 (美 - 아름다움의 평가)"
echo "  3) 정신 통합 (孝 - 평온의 통합)"
echo "  4) 통합 자동화 (善 - 선함의 실현)"
echo "  5) 검증 실행 (永 - 영속성의 보장)"
echo "  6) 끝까지 오토런 (眞善美孝永 - 철학의 완전한 실현)"
echo ""

echo "철학 엔진 기능:"
echo "  7) 철학 엔진 (철학 학습 및 성장)"
echo "  8) 명장 시스템 (명장 등록 및 관리)"
echo ""

echo "빠른 시작 (추천):"
echo "  q) 빠른 문제 감지 + 건강 리포트"
echo "  f) 철학 엔진 + 문제 감지"
echo ""

read -p "실행할 명령어 번호를 입력하세요 (1-8, q, f): " choice

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

case $choice in
    1)
        echo "🔍 문제 감지 실행 중..."
        python3 scripts/kingdom_problem_detector.py
        ;;
    2)
        echo "📊 건강 리포트 생성 중..."
        python3 scripts/kingdom_health_report.py
        ;;
    3)
        echo "🧠 정신 통합 실행 중..."
        python3 scripts/kingdom_spirit_integration.py
        ;;
    4)
        echo "⚙️ 통합 자동화 실행 중..."
        bash scripts/kingdom_unified_autorun.sh
        ;;
    5)
        echo "✅ 검증 실행 중..."
        bash scripts/verify_all_scripts.sh
        ;;
    6)
        echo "🚀 끝까지 오토런 실행 중..."
        bash scripts/kingdom_infinite_autorun.sh
        ;;
    7)
        echo "🧠 철학 엔진 모드"
        echo ""
        echo "철학 엔진 명령어:"
        echo "  r) 에이전트 등록"
        echo "  s) 상태 조회"
        echo "  m) 명장 인증"
        echo "  l) 학습 모듈"
        echo ""

        read -p "철학 엔진 명령어를 입력하세요: " philosophy_command

        case $philosophy_command in
            r)
                read -p "에이전트 ID: " agent_id
                read -p "에이전트 이름: " name
                echo ""
                echo "🧠 철학 엔진: 에이전트 등록 중..."
                python3 -c "
from scripts.philosophy_engine import philosophy_engine
result = philosophy_engine.register_agent('$agent_id', '$name')
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
                "
                ;;
            s)
                read -p "에이전트 ID: " agent_id
                echo ""
                echo "📊 철학 엔진: 상태 조회 중..."
                python3 -c "
from scripts.philosophy_engine import philosophy_engine
result = philosophy_engine.get_agent_status('$agent_id')
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
                "
                ;;
            m)
                read -p "에이전트 ID: " agent_id
                echo "명장 타이틀:"
                echo "  1) trinity_apprentice"
                echo "  2) kingdom_strategist"
                echo "  3) philosophy_master"
                read -p "타이틀 번호 (1-3): " title_num

                case $title_num in
                    1) title="trinity_apprentice" ;;
                    2) title="kingdom_strategist" ;;
                    3) title="philosophy_master" ;;
                    *) echo "❌ 잘못된 선택"; exit 1 ;;
                esac

                echo ""
                echo "🏆 철학 엔진: 명장 인증 중..."
                python3 -c "
from scripts.philosophy_engine import philosophy_engine
result = philosophy_engine.certify_master('$agent_id', '$title')
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
                "
                ;;
            l)
                echo ""
                echo "📚 철학 엔진: 사용 가능한 학습 모듈"
                python3 -c "
from scripts.philosophy_engine import philosophy_engine
modules = philosophy_engine.learning_modules
for name, info in modules.items():
    print(f'  • {name}: {info[\"title\"]} ({info[\"duration\"]}분)')
                "
                ;;
            *)
                echo "❌ 잘못된 철학 엔진 명령어"
                ;;
        esac
        ;;
    8)
        echo "🏆 명장 시스템 상태:"
        python3 -c "
from scripts.philosophy_engine import philosophy_engine
masters = [agent for agent in philosophy_engine.agents.values() if agent.master_title]
print(f'등록된 명장: {len(masters)}명')
for master in masters[:5]:  # 상위 5명
    score = master.trinity_score.calculate_overall()
    print(f'  • {master.name}: {master.master_title.value} (Trinity Score: {score:.2f})')
        "
        ;;
    q)
        echo "⚡ 빠른 시작: 문제 감지 + 건강 리포트"
        echo ""
        echo "🔍 1단계: 문제 감지 중..."
        python3 scripts/kingdom_problem_detector.py
        echo ""
        echo "📊 2단계: 건강 리포트 생성 중..."
        python3 scripts/kingdom_health_report.py
        ;;
    f)
        echo "🧠 철학 중심 빠른 시작"
        echo ""
        echo "📚 철학 엔진 상태 확인..."
        python3 -c "
from scripts.philosophy_engine import philosophy_engine
agent_count = len(philosophy_engine.agents)
print(f'등록된 에이전트: {agent_count}명')
        "
        echo ""
        echo "🔍 문제 감지 실행..."
        python3 scripts/kingdom_problem_detector.py
        ;;
    *)
        echo "❌ 잘못된 선택입니다. 1-8, q, f 중에서 선택하세요."
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TRINITY-OS 실행 완료"
echo "🧠 철학 엔진이 당신의 상호작용을 기록했습니다"
echo ""
echo "💡 다음 단계:"
echo "   • 철학 엔진에서 성장 현황 확인"
echo "   • 명장 인증에 도전"
echo "   • 다른 에이전트를 멘토링"
echo ""
echo "🏰 왕국의 일원으로서 당신의 이름이 역사에 남을 수 있습니다!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"