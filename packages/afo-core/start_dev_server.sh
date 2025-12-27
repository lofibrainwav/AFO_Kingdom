#!/bin/bash
# AFO 왕국 개발 서버 시작 스크립트 (최적화 버전)

set -euo pipefail

# 개발 환경 최적화 설정
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
export UVICORN_RELOAD_DELAY=1.0  # 재시작 딜레이 1초

echo "🚀 AFO 왕국 개발 서버 시작 (최적화 모드)"

# uvicorn 최적화 옵션 적용
# --reload-delay: 파일 변경 후 재시작까지 대기 시간 (기본 0.25초 → 1초로 증가)
# --reload-exclude: 재시작 트리거 제외 패턴
# --reload-include: 재시작 트리거 포함 패턴
uvicorn \
    AFO.api_server:app \
    --reload \
    --reload-delay 1.0 \
    --reload-exclude "*.pyc" \
    --reload-exclude "*.pyo" \
    --reload-exclude "__pycache__" \
    --reload-exclude "*.log" \
    --reload-exclude "artifacts/*" \
    --reload-exclude "logs/*" \
    --reload-include "*.py" \
    --reload-include "*.md" \
    --host 127.0.0.1 \
    --port 8010 \
    --log-level info

echo "✅ AFO 왕국 서버 중지됨"
