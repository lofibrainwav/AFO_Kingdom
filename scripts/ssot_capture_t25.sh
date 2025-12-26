#!/usr/bin/env bash
set -u

TS="$(date +%Y%m%d-%H%M)"
OUT="artifacts/t25/$TS"
mkdir -p "$OUT"

echo "Running Bandit Scan on packages/afo-core (Timestamp: $TS)..."

# Run Bandit (JSON for parsing, TXT for reading)
# Phase 1 Gate: High Severity Only (-lll)
python3 -m bandit -r packages/afo-core \
  -lll \
  -x ".venv,venv,node_modules,dist,build,.next,__pycache__,site-packages,tests" \
  -f json -o "$OUT/bandit_report.json"

# Capture Exit Code
EXIT_CODE=$?
echo $EXIT_CODE > "$OUT/bandit_exitcode.txt"

# Also generate TXT for quick reading
python3 -m bandit -r packages/afo-core \
  -x ".venv,venv,node_modules,dist,build,.next,__pycache__,site-packages,tests" \
  -f txt -o "$OUT/bandit_report.txt" || true

# Summary
echo "Scan Complete."
echo "Exit Code: $EXIT_CODE"
echo "Evidence Directory: $OUT"
echo "EVIDENCE_DIR=$OUT"