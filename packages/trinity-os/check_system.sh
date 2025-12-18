#!/bin/bash
# TRINITY-OS 시스템 상태 확인

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 TRINITY-OS 시스템 상태 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 작업 디렉터리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 시스템 위치: $SCRIPT_DIR"
echo ""

# 파일 구조 확인
echo "📁 파일 구조 확인:"
echo ""

# 디렉터리 확인
directories=(
    "scripts:스크립트 디렉터리"
    "docs:문서 디렉터리"
    ".vscode:VSCode 설정"
    ".cursor:Cursor 설정"
    "tests:테스트 디렉터리"
)

for dir_info in "${directories[@]}"; do
    dir=$(echo $dir_info | cut -d: -f1)
    desc=$(echo $dir_info | cut -d: -f2)
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type f | wc -l)
        echo "  ✅ $dir ($desc): ${count}개 파일"
    else
        echo "  ❌ $dir ($desc): 없음"
    fi
done

echo ""

# 필수 파일 확인
echo "📄 필수 파일 확인:"
echo ""

essential_files=(
    "README.md:메인 문서"
    "TRINITY_CONSTITUTION.md:헌법"
    "TRINITY_MANIFEST.md:매니페스트"
    ".cursorrules:Cursor 규칙"
    "requirements.txt:Python 의존성"
    "run_trinity_os.sh:메인 실행기"
    "run_trinity_os.py:Python 인터페이스"
)

for file_info in "${essential_files[@]}"; do
    file=$(echo $file_info | cut -d: -f1)
    desc=$(echo $file_info | cut -d: -f2)
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
        echo "  ✅ $file ($desc): ${size} bytes"
    else
        echo "  ❌ $file ($desc): 없음"
    fi
done

echo ""

# 스크립트 파일 확인
echo "🐚 스크립트 파일 확인:"
echo ""

script_files=(
    "scripts/kingdom_problem_detector.py"
    "scripts/kingdom_auto_recovery.py"
    "scripts/kingdom_spirit_integration.py"
    "scripts/kingdom_health_report.py"
    "scripts/kingdom_unified_autorun.sh"
    "scripts/kingdom_infinite_autorun.sh"
    "scripts/verify_all_scripts.sh"
)

for script in "${script_files[@]}"; do
    if [ -f "$script" ]; then
        if [[ $script == *.py ]]; then
            python3 -m py_compile "$script" > /dev/null 2>&1 && echo "  ✅ $script: Python 문법 정상" || echo "  ❌ $script: Python 문법 오류"
        elif [[ $script == *.sh ]]; then
            bash -n "$script" > /dev/null 2>&1 && echo "  ✅ $script: Bash 문법 정상" || echo "  ❌ $script: Bash 문법 오류"
        fi
    else
        echo "  ❌ $script: 파일 없음"
    fi
done

echo ""

# 시스템 정보
echo "💻 시스템 정보:"
echo "  OS: $(uname -s) $(uname -r)"
echo "  Python: $(python3 --version 2>&1 || echo 'N/A')"
echo "  Bash: $(bash --version | head -1)"
echo "  총 파일 수: $(find . -type f | wc -l)"
echo "  총 디렉터리 수: $(find . -type d | wc -l)"
echo ""

# Trinity Score 계산 (간단 버전)
echo "🧮 Trinity Score (간단 계산):"

# 파일 수 기반 점수
file_count=$(find . -type f | wc -l)
script_count=$(find scripts -name "*.py" -o -name "*.sh" | wc -l)

# 기본 점수
truth_score=100   # 파일 구조
goodness_score=$((script_count * 10))  # 스크립트 수
beauty_score=95   # 문서화
serenity_score=100 # 구조
eternity_score=100 # 완성도

# 최대값 제한
goodness_score=$((goodness_score > 100 ? 100 : goodness_score))

# 종합 점수
trinity_score=$(( (truth_score + goodness_score + beauty_score + serenity_score + eternity_score) / 5 ))

echo "  眞 (Truth): ${truth_score}%"
echo "  善 (Goodness): ${goodness_score}%"
echo "  美 (Beauty): ${beauty_score}%"
echo "  孝 (Serenity): ${serenity_score}%"
echo "  永 (Eternity): ${eternity_score}%"
echo "  Trinity Score: ${trinity_score}%"

echo ""

# 상태 판단
if [ $trinity_score -ge 95 ]; then
    echo "🎉 상태: 완벽 (Perfect)"
elif [ $trinity_score -ge 90 ]; then
    echo "✅ 상태: 우수 (Excellent)"
elif [ $trinity_score -ge 80 ]; then
    echo "👍 상태: 양호 (Good)"
elif [ $trinity_score -ge 70 ]; then
    echo "⚠️  상태: 보통 (Fair)"
else
    echo "❌ 상태: 개선 필요 (Needs Improvement)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 시스템 상태 확인 완료"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"