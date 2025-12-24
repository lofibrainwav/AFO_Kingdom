#!/bin/bash
# Hetzner VPS Pushgateway Setup Script
# AFO Kingdom - Phase 7 CI 실전 테스트용

set -euo pipefail

echo "🏰 AFO Kingdom - Hetzner Pushgateway Setup"
echo "==========================================="

# 1. 서버 기본 설정
echo "📋 서버 정보 확인..."
read -p "Hetzner 서버 IP: " SERVER_IP
read -p "서버 사용자 (기본: root): " SERVER_USER
SERVER_USER=${SERVER_USER:-root}

# 2. 도메인 설정 (선택)
read -p "도메인 (없으면 IP 사용): " DOMAIN
if [ -z "$DOMAIN" ]; then
    DOMAIN=$SERVER_IP
    USE_HTTPS=false
else
    USE_HTTPS=true
fi

# 3. Basic Auth 설정
read -p "Basic Auth 사용자명: " BASIC_USER
read -s -p "Basic Auth 비밀번호: " BASIC_PASS
echo ""

# 4. 서버 접속 테스트
echo "🔗 서버 접속 테스트..."
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP "echo '✅ 서버 접속 성공'" || {
    echo "❌ 서버 접속 실패"
    echo "Hetzner 콘솔에서 SSH 키를 추가했는지 확인하세요."
    exit 1
}

# 5. Docker 설치 확인 및 설치
echo "🐳 Docker 설치 확인..."
ssh $SERVER_USER@$SERVER_IP "
if ! command -v docker &> /dev/null; then
    echo '📦 Docker 설치...'
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
fi

if ! command -v docker-compose &> /dev/null; then
    echo '📦 Docker Compose 설치...'
    curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo '✅ Docker 환경 준비 완료'
"

# 6. Pushgateway 디렉토리 생성 및 파일 전송
echo "📁 설정 파일 생성..."
SETUP_DIR="pushgateway-setup"
mkdir -p $SETUP_DIR

# docker-compose.yml 생성
cat > $SETUP_DIR/docker-compose.yml << EOF
services:
  pushgateway:
    image: prom/pushgateway:latest
    restart: unless-stopped
    command:
      - --web.listen-address=127.0.0.1:9091
    network_mode: "host"

  caddy:
    image: caddy:latest
    restart: unless-stopped
    network_mode: "host"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config

volumes:
  caddy_data:
  caddy_config:
EOF

# Caddyfile 생성
if [ "$USE_HTTPS" = true ]; then
    cat > $SETUP_DIR/Caddyfile << EOF
$DOMAIN {
  encode gzip

  basicauth * {
    $BASIC_USER $(docker run --rm caddy:latest caddy hash-password --plaintext '$BASIC_PASS')
  }

  reverse_proxy 127.0.0.1:9091
}
EOF
else
    cat > $SETUP_DIR/Caddyfile << EOF
$DOMAIN {
  encode gzip

  basicauth * {
    $BASIC_USER $(docker run --rm caddy:latest caddy hash-password --plaintext '$BASIC_PASS')
  }

  reverse_proxy 127.0.0.1:9091
}
EOF
fi

# 7. 파일 서버로 전송
echo "📤 설정 파일 전송..."
scp -r $SETUP_DIR/* $SERVER_USER@$SERVER_IP:~

# 8. 서버에서 서비스 시작
echo "🚀 Pushgateway 서비스 시작..."
ssh $SERVER_USER@$SERVER_IP "
cd ~
docker-compose down 2>/dev/null || true
docker-compose up -d
echo '⏳ 서비스 시작 대기...'
sleep 10
"

# 9. 서비스 상태 확인
echo "🔍 서비스 상태 확인..."
if [ "$USE_HTTPS" = true ]; then
    TEST_CMD="curl -k -u '$BASIC_USER:$BASIC_PASS' https://$DOMAIN/-/ready"
else
    TEST_CMD="curl -u '$BASIC_USER:$BASIC_PASS' http://$DOMAIN/-/ready"
fi

ssh $SERVER_USER@$SERVER_IP "$TEST_CMD" && {
    echo "✅ Pushgateway 설정 완료!"
    echo ""
    echo "📋 GitHub Secrets 설정 정보:"
    echo "PUSHGATEWAY_URL: https://$DOMAIN"
    echo "PUSHGATEWAY_BASIC_AUTH: $BASIC_USER:$BASIC_PASS"
    echo ""
    echo "🧪 테스트 명령어:"
    echo "$TEST_CMD"
} || {
    echo "❌ 서비스 시작 실패"
    echo "서버 로그 확인:"
    ssh $SERVER_USER@$SERVER_IP "docker-compose logs"
    exit 1
}

# 10. 정리
rm -rf $SETUP_DIR

echo ""
echo "🎉 Hetzner Pushgateway 설정 완료!"
echo "이제 GitHub repo에서 CI 실전 테스트를 진행할 수 있습니다."