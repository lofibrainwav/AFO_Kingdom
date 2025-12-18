#!/usr/bin/env bash
set -euo pipefail

echo "=========================================="
echo "🔐 SixXon: codex 재캡처 (수동 로그인 필요)"
echo "=========================================="
echo
echo "원칙:"
echo "- 세션/쿠키/토큰은 Git에 커밋 금지"
echo "- 실패해도 Receipt + raw/ 증거는 남겨서(SSOT) 원인 추적"
echo "- 브라우저는 system-chrome만(혼선 제거)"
echo

echo "1) 현재 상태(doctor)"
./scripts/sixxon auth doctor --json || true
echo

echo "2) 세션 재캡처 (브라우저가 뜨면 로그인하고 완료될 때까지 기다리세요)"
./scripts/sixxon auth capture --provider codex --browser system-chrome --keep-open --refresh --json || true
echo

echo "3) 복호화 가능 여부 확인"
./scripts/sixxon auth status --json || true
echo

echo "DONE"

