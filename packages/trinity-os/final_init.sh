#!/bin/bash
# TRINITY-OS 최종 초기화 스크립트

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 TRINITY-OS 완전 구축 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 작업 디렉터리 확인
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 TRINITY-OS 위치: $SCRIPT_DIR"
echo ""

# 권한 설정
echo "🔧 최종 권한 설정 중..."
chmod +x *.sh
chmod +x scripts/*.sh
chmod +x scripts/*.py

echo "✅ 권한 설정 완료"
echo ""

# 시스템 테스트
echo "🧪 최종 시스템 테스트 실행..."
./test_trinity_os.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TRINITY-OS 완전 준비 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 이제 TRINITY-OS를 사용하세요:"
echo ""
echo "  🎯 인터랙티브 모드:"
echo "     ./run_trinity_os.sh"
echo ""
echo "  🐍 Python 인터페이스:"
echo "     python3 run_trinity_os.py"
echo ""
echo "  ⚙️ 통합 자동화:"
echo "     ./scripts/kingdom_unified_autorun.sh"
echo ""
echo "  🔍 문제 감지:"
echo "     python3 scripts/kingdom_problem_detector.py"
echo ""
echo "  📊 건강 리포트:"
echo "     python3 scripts/kingdom_health_report.py"
echo ""
echo "  🧠 정신 통합:"
echo "     python3 scripts/kingdom_spirit_integration.py"
echo ""
echo "  🚀 끝까지 오토런:"
echo "     ./scripts/kingdom_infinite_autorun.sh"
echo ""
echo "🧠 철학: 眞善美孝永 (Truth, Goodness, Beauty, Serenity, Eternity)"
echo ""
echo "🏰 왕국의 새로운 시작을 축하합니다!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"