#!/bin/bash
# 30초 진단: Grafana/Pushgateway 포트 확인
# Hetzner 서버에서 실행

set -euo pipefail

echo "== LISTEN PORTS (3000/3100/9091) =="
sudo ss -lntp | grep -E ':3000|:3100|:9091' || echo "해당 포트에서 리스닝하는 프로세스 없음"

echo
echo "== DOCKER PS (grafana/pushgateway/cloudflared) =="
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}" | grep -E "grafana|pushgateway|cloudflared" || echo "해당 컨테이너 없음"

echo
echo "== LOCAL CURL =="
curl -sS -I --max-time 2 http://127.0.0.1:3000 | head -n 1 || echo "3000 NO"
curl -sS -I --max-time 2 http://127.0.0.1:3100 | head -n 1 || echo "3100 NO"
curl -sS -I --max-time 2 http://127.0.0.1:9091/-/ready | head -n 1 || echo "9091 NO"

