#!/usr/bin/env bash
set -u

TS="$(date +%Y%m%d-%H%M)"
OUT="artifacts/t27/$TS"
mkdir -p "$OUT"

echo "Capturing T27 Evidence (Timestamp: $TS)..."

# 1. Git Changes (What we did)
git diff --name-only > "$OUT/git_files_changed.txt"
git status --porcelain > "$OUT/git_status.txt"

# 2. Source Code Evidence (The Widget & The Endpoint)
cp packages/dashboard/src/components/royal/widgets/KingdomHistoryWidget.tsx "$OUT/KingdomHistoryWidget.tsx"
cp packages/afo-core/api/routes/git_status.py "$OUT/git_status.py"

# 3. Runtime Evidence (The Backend API)
echo "Curling Backend (8010)..."
curl -sS -D "$OUT/api_headers.txt" -o "$OUT/api_body.json" "http://127.0.0.1:8010/api/git/history?limit=5"

# 4. Security Check (Bandit High-Only Verification)
echo "Running Bandit (High Severity)..."
python3 -m bandit -r packages/afo-core -lll -x ".venv,venv,node_modules,dist,build,.next,__pycache__,site-packages,tests" -f json -o "$OUT/bandit_report.json"
echo $? > "$OUT/bandit_exitcode.txt"

echo "Capture Complete. Evidence in $OUT"
echo "EVIDENCE_DIR=$OUT"
