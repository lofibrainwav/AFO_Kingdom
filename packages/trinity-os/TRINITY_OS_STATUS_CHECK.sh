#!/bin/bash
# TRINITY-OS 지피지기 상태 점검 스크립트
# 적(시스템 상태)을 정확히 파악하고 아(목표)를 명확히 이해

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 TRINITY-OS 지피지기 상태 점검"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. 기본 시스템 상태 확인 (지피지기 - 적의 상태 파악)
echo "📊 1단계: 기본 시스템 상태 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 파일 구조 확인
echo "📁 파일 구조 분석:"
total_files=$(find . -type f | wc -l)
total_dirs=$(find . -type d | wc -l)
echo "  • 총 파일 수: $total_files"
echo "  • 총 디렉터리 수: $total_dirs"

# 주요 디렉터리별 파일 수
echo "  • docs/: $(find docs -type f 2>/dev/null | wc -l || echo 0)개"
echo "  • scripts/: $(find scripts -type f 2>/dev/null | wc -l || echo 0)개"
echo "  • .vscode/: $(find .vscode -type f 2>/dev/null | wc -l || echo 0)개"
echo "  • .cursor/: $(find .cursor -type f 2>/dev/null | wc -l || echo 0)개"
echo ""

# 2. 철학 엔진 상태 확인 (지피지기 - 핵심 기능 파악)
echo "🧠 2단계: 철학 엔진 상태 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "scripts/philosophy_engine.py" ]; then
    echo "✅ 철학 엔진 파일 존재"

    # Python 문법 체크
    if python3 -m py_compile scripts/philosophy_engine.py 2>/dev/null; then
        echo "✅ 철학 엔진 Python 문법 정상"
    else
        echo "❌ 철학 엔진 Python 문법 오류"
    fi

    # 철학 엔진 데이터 확인
    if [ -f "philosophy_engine_data.json" ]; then
        agent_count=$(python3 -c "
import json
try:
    with open('philosophy_engine_data.json', 'r') as f:
        data = json.load(f)
        print(len(data.get('agents', [])))
except:
    print('0')
        " 2>/dev/null || echo "0")
        echo "📈 등록된 에이전트: ${agent_count}명"

        if [ "$agent_count" -gt 0 ]; then
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
            echo "🏆 등록된 명장: ${master_count}명"
        fi
    else
        echo "📝 철학 엔진 데이터 파일 없음 (초기 상태)"
    fi
else
    echo "❌ 철학 엔진 파일 없음"
fi
echo ""

# 3. 코어 스크립트 상태 확인 (지피지기 - 실행 가능성 파악)
echo "⚙️ 3단계: 코어 스크립트 상태 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

core_scripts=(
    "scripts/kingdom_problem_detector.py"
    "scripts/kingdom_auto_recovery.py"
    "scripts/kingdom_spirit_integration.py"
    "scripts/kingdom_health_report.py"
    "scripts/kingdom_unified_autorun.sh"
    "scripts/kingdom_infinite_autorun.sh"
    "scripts/verify_all_scripts.sh"
)

for script in "${core_scripts[@]}"; do
    if [ -f "$script" ]; then
        if [[ $script == *.py ]]; then
            if python3 -m py_compile "$script" 2>/dev/null; then
                echo "✅ $script: Python 문법 정상"
            else
                echo "❌ $script: Python 문법 오류"
            fi
        elif [[ $script == *.sh ]]; then
            if bash -n "$script" 2>/dev/null; then
                echo "✅ $script: Bash 문법 정상"
            else
                echo "❌ $script: Bash 문법 오류"
            fi
        fi
    else
        echo "❌ $script: 파일 없음"
    fi
done
echo ""

# 4. 인터페이스 상태 확인 (지피지기 - 사용자 접근성 파악)
echo "💻 4단계: 인터페이스 상태 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

interfaces=(
    "run_trinity_os.sh"
    "run_trinity_os.py"
    "TRINITY-OS"
    "TRINITY-OS.bat"
)

for interface in "${interfaces[@]}"; do
    if [ -f "$interface" ]; then
        if [ -x "$interface" ] || [[ $interface == *.py ]] || [[ $interface == *.bat ]]; then
            echo "✅ $interface: 실행 가능"
        else
            echo "⚠️ $interface: 실행 권한 없음"
        fi
    else
        echo "❌ $interface: 파일 없음"
    fi
done
echo ""

# 5. 문서 상태 확인 (지피지기 - 지식 체계 파악)
echo "📚 5단계: 문서 상태 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# docs 구조 확인
if [ -d "docs" ]; then
    echo "📁 docs 디렉터리 구조:"
    find docs -type f -name "*.md" | head -10 | while read file; do
        if [ -f "$file" ]; then
            lines=$(wc -l < "$file")
            echo "  ✅ ${file#docs/}: ${lines}줄"
        fi
    done

    total_docs=$(find docs -name "*.md" | wc -l)
    echo "📊 총 문서 수: $total_docs 개"
else
    echo "❌ docs 디렉터리 없음"
fi
echo ""

# 6. Trinity Score 계산 (지피지기 - 종합 평가)
echo "📊 6단계: Trinity Score 종합 평가"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 각 요소별 점수 계산
file_score=0
philosophy_score=0
script_score=0
interface_score=0
docs_score=0

# 파일 구조 점수 (20%)
if [ "$total_files" -gt 70 ]; then
    file_score=20
elif [ "$total_files" -gt 50 ]; then
    file_score=15
elif [ "$total_files" -gt 30 ]; then
    file_score=10
else
    file_score=5
fi

# 철학 엔진 점수 (25%)
if [ -f "scripts/philosophy_engine.py" ] && python3 -m py_compile scripts/philosophy_engine.py 2>/dev/null; then
    philosophy_score=25
elif [ -f "scripts/philosophy_engine.py" ]; then
    philosophy_score=15
else
    philosophy_score=5
fi

# 스크립트 점수 (25%)
working_scripts=0
for script in "${core_scripts[@]}"; do
    if [ -f "$script" ]; then
        if [[ $script == *.py ]] && python3 -m py_compile "$script" 2>/dev/null; then
            ((working_scripts++))
        elif [[ $script == *.sh ]] && bash -n "$script" 2>/dev/null; then
            ((working_scripts++))
        fi
    fi
done
script_score=$((working_scripts * 25 / ${#core_scripts[@]}))

# 인터페이스 점수 (15%)
working_interfaces=0
for interface in "${interfaces[@]}"; do
    if [ -f "$interface" ]; then
        ((working_interfaces++))
    fi
done
interface_score=$((working_interfaces * 15 / ${#interfaces[@]}))

# 문서 점수 (15%)
if [ -d "docs" ]; then
    docs_score=$((total_docs * 15 / 20))  # 20개 문서 기준
    if [ "$docs_score" -gt 15 ]; then
        docs_score=15
    fi
else
    docs_score=0
fi

# 종합 Trinity Score 계산
trinity_score=$((file_score + philosophy_score + script_score + interface_score + docs_score))

echo "🔍 평가 상세:"
echo "  • 파일 구조 (20%): $file_score/20"
echo "  • 철학 엔진 (25%): $philosophy_score/25"
echo "  • 코어 스크립트 (25%): $script_score/25"
echo "  • 인터페이스 (15%): $interface_score/15"
echo "  • 문서화 (15%): $docs_score/15"
echo ""
echo "🎯 Trinity Score: $trinity_score/100"

# 등급 판정
if [ "$trinity_score" -ge 95 ]; then
    grade="완벽 (Perfect)"
    status="🎉 백전불태 준비 완료"
elif [ "$trinity_score" -ge 90 ]; then
    grade="우수 (Excellent)"
    status="✅ 전투 준비 완료"
elif [ "$trinity_score" -ge 80 ]; then
    grade="양호 (Good)"
    status="👍 추가 준비 필요"
elif [ "$trinity_score" -ge 70 ]; then
    grade="보통 (Fair)"
    status="⚠️ 개선 작업 필요"
else
    grade="개선 필요 (Needs Work)"
    status="❌ 즉각적 점검 필요"
fi

echo "📈 평가 등급: $grade"
echo "📋 상태: $status"
echo ""

# 7. 개선 권고사항 (지피지기 - 승리 전략 수립)
echo "🎯 7단계: 개선 권고사항 (지피지기 완성)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

recommendations=()

if [ "$file_score" -lt 15 ]; then
    recommendations+=("파일 구조 보강")
fi

if [ "$philosophy_score" -lt 20 ]; then
    recommendations+=("철학 엔진 강화")
fi

if [ "$script_score" -lt 20 ]; then
    recommendations+=("스크립트 품질 개선")
fi

if [ "$interface_score" -lt 12 ]; then
    recommendations+=("인터페이스 보완")
fi

if [ "$docs_score" -lt 12 ]; then
    recommendations+=("문서화 확대")
fi

if [ ${#recommendations[@]} -eq 0 ]; then
    echo "🎉 개선사항 없음 - 완벽한 상태!"
else
    echo "💡 권고사항:"
    for rec in "${recommendations[@]}"; do
        echo "  • $rec"
    done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 지피지기 완료: 적(시스템 상태)을 정확히 파악하였습니다"
echo ""
echo "🎯 다음 단계: 확인된 개선사항을 즉시 실행합니다"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"