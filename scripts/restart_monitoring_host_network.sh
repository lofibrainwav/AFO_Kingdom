#!/bin/bash
# AFO Kingdom Monitoring Stack - 호스트 네트워크 모드 재시작
# Hetzner 서버에서 실행: 컨테이너를 호스트 네트워크 모드로 재시작

set -euo pipefail

echo "==================================================="
echo "   🔄 AFO Kingdom Monitoring Stack 재시작           "
echo "   호스트 네트워크 모드 적용                        "
echo "==================================================="

# AFO Kingdom 프로젝트 디렉토리로 이동
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT/packages/afo-core" || {
    echo "❌ Error: packages/afo-core 디렉토리를 찾을 수 없습니다."
    exit 1
}

echo ""
echo "📂 작업 디렉토리: $(pwd)"

# 1. 현재 컨테이너 중지 (monitoring 프로파일만)
echo ""
echo "🛑 [1/3] Monitoring 컨테이너 중지 중..."
docker-compose --profile monitoring down || {
    echo "⚠️  일부 컨테이너가 이미 중지되었거나 존재하지 않습니다."
}

# 2. 호스트 네트워크 모드로 재시작
echo ""
echo "🚀 [2/3] 호스트 네트워크 모드로 재시작 중..."
docker-compose --profile monitoring up -d

# 3. 상태 확인
echo ""
echo "✅ [3/3] 컨테이너 상태 확인..."
sleep 3
docker ps | grep -E "(grafana|prometheus|pushgateway)" || echo "⚠️  일부 컨테이너가 실행되지 않았습니다."

echo ""
echo "==================================================="
echo "✅ 재시작 완료"
echo "==================================================="
echo ""
echo "📊 서비스 확인:"
echo "   - Grafana: http://localhost:3100 (호스트 네트워크)"
echo "   - Prometheus: http://localhost:9090"
echo ""
echo "🧪 로컬 테스트:"
echo "   curl -I http://localhost:3100  # HTTP 302 확인"
echo ""
echo "🌐 외부 테스트 (Tunnel 재시작 후):"
echo "   curl -I https://afo-grafana.brnestrm.com"
echo "   curl -s https://afo-metrics.brnestrm.com/-/ready"
echo ""

