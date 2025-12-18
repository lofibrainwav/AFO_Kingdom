#!/bin/bash
# TRINITY-OS 빠른 시작 가이드

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ TRINITY-OS 빠른 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 작업 디렉터리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 TRINITY-OS 위치: $SCRIPT_DIR"
echo ""

# 시스템 요구사항 확인
echo "🔍 시스템 요구사항 확인..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되어 있지 않습니다."
    echo "   설치 방법:"
    echo "   macOS: brew install python3"
    echo "   Ubuntu: sudo apt install python3"
    exit 1
fi

if ! command -v bash &> /dev/null; then
    echo "❌ Bash가 설치되어 있지 않습니다."
    exit 1
fi

echo "✅ Python3 버전: $(python3 --version)"
echo "✅ Bash 버전: $(bash --version | head -1)"
echo ""

# 권한 설정
echo "🔧 실행 권한 설정..."
chmod +x *.sh
chmod +x scripts/*.sh 2>/dev/null || true
echo "✅ 권한 설정 완료"
echo ""

# 기본 테스트
echo "🧪 기본 기능 테스트..."
if [ -f "scripts/kingdom_problem_detector.py" ]; then
    python3 scripts/kingdom_problem_detector.py > /dev/null 2>&1 && echo "✅ 문제 감지 엔진" || echo "❌ 문제 감지 엔진"
fi

if [ -f "scripts/kingdom_health_report.py" ]; then
    python3 scripts/kingdom_health_report.py > /dev/null 2>&1 && echo "✅ 건강 리포트" || echo "❌ 건강 리포트"
fi

if [ -f "run_trinity_os.sh" ]; then
    bash -n run_trinity_os.sh > /dev/null 2>&1 && echo "✅ 메인 인터페이스" || echo "❌ 메인 인터페이스"
fi

echo ""

# 사용법 안내
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 TRINITY-OS 사용법"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 인터랙티브 모드 (권장):"
echo "   ./run_trinity_os.sh"
echo ""
echo "2. Python 인터페이스:"
echo "   python3 run_trinity_os.py"
echo ""
echo "3. 단축 명령어:"
echo "   ./TRINITY-OS detect    # 문제 감지"
echo "   ./TRINITY-OS health    # 건강 리포트"
echo "   ./TRINITY-OS unified   # 통합 자동화"
echo "   ./TRINITY-OS infinite  # 끝까지 오토런"
echo ""
echo "4. 수동 실행:"
echo "   python3 scripts/kingdom_problem_detector.py"
echo "   python3 scripts/kingdom_health_report.py"
echo "   python3 scripts/kingdom_spirit_integration.py"
echo "   ./scripts/kingdom_unified_autorun.sh"
echo "   ./scripts/kingdom_infinite_autorun.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TRINITY-OS 준비 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🧠 철학: 眞善美孝永 (Truth, Goodness, Beauty, Serenity, Eternity)"
echo ""
echo "🏰 왕국의 새로운 운영체제를 만나보세요!"