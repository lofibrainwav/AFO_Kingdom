#!/bin/bash
# TRINITY-OS 초기화 스크립트

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 TRINITY-OS 초기화"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 작업 디렉터리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 초기화 디렉터리: $SCRIPT_DIR"
echo ""

# 권한 설정
echo "🔧 실행 권한 설정 중..."
chmod +x run_trinity_os.sh
chmod +x test_trinity_os.sh
chmod +x init_trinity_os.sh
chmod +x scripts/*.sh

echo "✅ 실행 권한 설정 완료"
echo ""

# Python 환경 확인
echo "🐍 Python 환경 확인 중..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되어 있지 않습니다."
    echo "   brew install python3  # macOS"
    echo "   sudo apt install python3  # Ubuntu"
    exit 1
fi

echo "✅ Python3 버전: $(python3 --version)"
echo ""

# 가상환경 생성 (선택사항)
read -p "Python 가상환경을 생성하시겠습니까? (y/N): " create_venv

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv trinity_env
    echo "✅ 가상환경 생성 완료: trinity_env"
    echo ""
    echo "🔄 가상환경 활성화:"
    echo "   source trinity_env/bin/activate"
    echo ""
fi

# 의존성 설치 (선택사항)
read -p "Python 의존성을 설치하시겠습니까? (y/N): " install_deps

if [[ $install_deps =~ ^[Yy]$ ]]; then
    echo "📦 의존성 설치 중..."
    if [ -d "trinity_env" ]; then
        source trinity_env/bin/activate
    fi
    pip install -r requirements.txt
    echo "✅ 의존성 설치 완료"
    echo ""
fi

# 시스템 테스트 실행
echo "🧪 시스템 테스트 실행 중..."
./test_trinity_os.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TRINITY-OS 초기화 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 사용 방법:"
echo "   ./run_trinity_os.sh        # 인터랙티브 모드"
echo "   ./test_trinity_os.sh       # 시스템 테스트"
echo ""
echo "📚 주요 스크립트:"
echo "   python3 scripts/kingdom_problem_detector.py    # 문제 감지"
echo "   python3 scripts/kingdom_health_report.py       # 건강 리포트"
echo "   ./scripts/kingdom_unified_autorun.sh          # 통합 자동화"
echo "   ./scripts/kingdom_infinite_autorun.sh         # 끝까지 오토런"
echo ""
echo "🧠 철학: 眞善美孝永 (Truth, Goodness, Beauty, Serenity, Eternity)"