#!/bin/bash
# TRINITY-OS 테스트 스크립트

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 TRINITY-OS 시스템 테스트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 작업 디렉터리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 테스트 디렉터리: $SCRIPT_DIR"
echo ""

# 테스트 카운터
PASSED=0
FAILED=0

# 테스트 함수
test_file_exists() {
    local file=$1
    if [ -f "$file" ]; then
        echo "✅ $file 존재"
        ((PASSED++))
    else
        echo "❌ $file 없음"
        ((FAILED++))
    fi
}

test_directory_exists() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo "✅ $dir 디렉터리 존재"
        ((PASSED++))
    else
        echo "❌ $dir 디렉터리 없음"
        ((FAILED++))
    fi
}

test_python_syntax() {
    local file=$1
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "✅ $file Python 문법 정상"
        ((PASSED++))
    else
        echo "❌ $file Python 문법 오류"
        ((FAILED++))
    fi
}

test_bash_syntax() {
    local file=$1
    if bash -n "$file" 2>/dev/null; then
        echo "✅ $file Bash 문법 정상"
        ((PASSED++))
    else
        echo "❌ $file Bash 문법 오류"
        ((FAILED++))
    fi
}

echo "🔍 파일 존재 테스트..."
echo ""

# 디렉터리 테스트
test_directory_exists "scripts"
test_directory_exists "docs"
test_directory_exists ".vscode"
test_directory_exists ".cursor"

echo ""
echo "📄 파일 존재 테스트..."
echo ""

# 필수 파일들
test_file_exists "README.md"
test_file_exists ".gitignore"
test_file_exists "requirements.txt"
test_file_exists ".cursorrules"
test_file_exists "TRINITY_MANIFEST.md"
test_file_exists "run_trinity_os.sh"
test_file_exists "test_trinity_os.sh"

# 스크립트 파일들
test_file_exists "scripts/kingdom_problem_detector.py"
test_file_exists "scripts/kingdom_auto_recovery.py"
test_file_exists "scripts/kingdom_spirit_integration.py"
test_file_exists "scripts/kingdom_health_report.py"
test_file_exists "scripts/kingdom_unified_autorun.sh"
test_file_exists "scripts/kingdom_infinite_autorun.sh"
test_file_exists "scripts/test_unified_autorun.sh"
test_file_exists "scripts/verify_all_scripts.sh"

# 문서 파일들
test_file_exists "docs/KINGDOM_UNIFIED_AUTORUN_GUIDE.md"
test_file_exists "docs/CURSOR_REVIEW_DISABLE_GUIDE.md"

# 설정 파일들
test_file_exists ".vscode/settings.json"
test_file_exists ".cursor/environment.json"

echo ""
echo "🐍 Python 문법 테스트..."
echo ""

# Python 파일들 문법 검사
test_python_syntax "scripts/kingdom_problem_detector.py"
test_python_syntax "scripts/kingdom_auto_recovery.py"
test_python_syntax "scripts/kingdom_spirit_integration.py"
test_python_syntax "scripts/kingdom_health_report.py"

echo ""
echo "🐚 Bash 문법 테스트..."
echo ""

# Bash 파일들 문법 검사
test_bash_syntax "scripts/kingdom_unified_autorun.sh"
test_bash_syntax "scripts/kingdom_infinite_autorun.sh"
test_bash_syntax "scripts/test_unified_autorun.sh"
test_bash_syntax "scripts/verify_all_scripts.sh"
test_bash_syntax "run_trinity_os.sh"
test_bash_syntax "test_trinity_os.sh"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 테스트 결과"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 통과: $PASSED"
echo "❌ 실패: $FAILED"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "🎉 모든 테스트 통과! TRINITY-OS 준비 완료"
    echo ""
    echo "🚀 다음 단계:"
    echo "   ./run_trinity_os.sh  # 인터랙티브 모드 실행"
    echo "   python3 scripts/kingdom_problem_detector.py  # 문제 감지"
    echo "   ./scripts/kingdom_unified_autorun.sh  # 통합 자동화"
    exit 0
else
    echo ""
    echo "❌ $FAILED 개 테스트 실패. 시스템 점검 필요"
    exit 1
fi