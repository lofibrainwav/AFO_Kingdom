#!/usr/bin/env bash
set -euo pipefail

SOUL_URL="${SOUL_URL:-http://127.0.0.1:8010}"
DASH_URL="${DASH_URL:-http://127.0.0.1:3000}"

curl4() {
  curl -4 -sf --retry 20 --retry-connrefused --retry-delay 1 "$@"
}

echo "[1/4] soul /health"
curl4 "${SOUL_URL}/health" >/dev/null

echo "[2/4] soul /metrics (head)"
curl4 "${SOUL_URL}/metrics" | head -n 5 >/dev/null

echo "[3/4] dashboard"
curl4 -I "${DASH_URL}" | head -n 1 >/dev/null

echo "[4/4] sse stream (need 2+ lines)"
TMP="$(mktemp)"
set +e
curl -4 -N --max-time 6 "${DASH_URL}/api/logs/stream" >"$TMP" 2>/dev/null
RC=$?
set -e

LINES="$(wc -l <"$TMP" | tr -d ' ')"
if [ "$LINES" -lt 2 ]; then
  echo "[fail] sse lines=${LINES}"
  cat "$TMP" || true
  exit 1
fi

if [ "$RC" -ne 0 ] && [ "$RC" -ne 28 ]; then
  echo "[warn] sse curl rc=${RC} (ok if got lines)"
fi

# --- PH20-05: SSE SSOT Guardrail ---
echo "[5/6] backend legacy redirect (need 308)"
# Check Legacy Path 1: /api/stream/logs
CODE=$(curl4 -o /dev/null -w "%{http_code}" "${SOUL_URL}/api/stream/logs")
if [ "$CODE" -ne 308 ]; then
  echo "[fail] backend /api/stream/logs code=${CODE} (expected 308)"
  exit 1
fi
# Check Legacy Path 2: /api/system/logs/stream
CODE=$(curl4 -o /dev/null -w "%{http_code}" "${SOUL_URL}/api/system/logs/stream")
if [ "$CODE" -ne 308 ]; then
  echo "[fail] backend /api/system/logs/stream code=${CODE} (expected 308)"
  exit 1
fi

echo "[6/6] frontend legacy forwarding (need 200)"
# Check Legacy Path 1: /api/stream/logs -> Should be 200 OK (Forwarding)
CODE=$(curl4 -o /dev/null -w "%{http_code}" "${DASH_URL}/api/stream/logs")
if [ "$CODE" -ne 200 ]; then
  echo "[fail] frontend /api/stream/logs code=${CODE} (expected 200)"
  exit 1
fi

echo "[ok] kingdom smoke passed"