#!/bin/bash
# AFO Kingdom API Server Quick Start

cd "$(dirname "$0")/packages/afo-core"

echo "🚀 AFO Kingdom API Server 시작 중..."
echo "📍 포트: 8010"
echo ""

# 가상환경 활성화 (있는 경우)
if [ -f "../../.venv/bin/activate" ]; then
    source ../../.venv/bin/activate
fi

# PYTHONPATH 설정
export PYTHONPATH="$(pwd):$PYTHONPATH"

# API 서버 시작
if [ -f "../../.venv/bin/python" ]; then
    ../../.venv/bin/python api_server.py
else
    python3 api_server.py
fi
