#!/usr/bin/env bash
set -euo pipefail

# AFO Kingdom Hardening Gate
# Disallows specific patterns in critical files

echo "🛡️  Running Hardening Gate..."

EXIT_CODE=0

# 1. Check for Hardcoded Sentry DSN Placeholder
SENTRY_PLACEHOLDER="https://your_sentry_dsn.ingest.sentry.io/1234567"
TARGET_FILE="packages/afo-core/AFO/api_server.py"

if grep -Fq "${SENTRY_PLACEHOLDER}" "${TARGET_FILE}"; then
  echo "❌ [FAIL] Hardcoded Sentry DSN placeholder found in ${TARGET_FILE}"
  EXIT_CODE=1
else
  echo "✅ [PASS] Sentry DSN placeholder check"
fi

# 2. Check for host.docker.internal in Organs Truth (Should rely on env/defaults or explicit sanitization)
# We want to ensure we aren't hardcoding this specific docker-internal DNS in the python logic layer
TRUTH_FILE="packages/afo-core/AFO/health/organs_truth.py"
HOST_INTERNAL="host.docker.internal"

if grep -Fq "${HOST_INTERNAL}" "${TRUTH_FILE}"; then
  echo "❌ [FAIL] ${HOST_INTERNAL} found in ${TRUTH_FILE}. Use env vars or sanitization."
  EXIT_CODE=1
else
  echo "✅ [PASS] Organs Truth hostname check"
fi

if [ $EXIT_CODE -eq 0 ]; then
  echo "✨ All Hardening Gates Passed."
else
  echo "🚫 Hardening Gate Failed."
fi

exit $EXIT_CODE
