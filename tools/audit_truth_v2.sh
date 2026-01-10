#!/bin/bash
cd /Users/brnestrm/AFO_Kingdom
set -u

echo "=== A) WHAT FILES CHANGED? ==="
git status -sb

echo
echo "=== B) LOCATE build_organs_final / docs probe / hardcoded scores ==="
# Fallback to grep if rg is missing
if command -v rg &> /dev/null; then
    rg -n "def build_organs_final|SSOT Canon Found|SSOT Missing|score=100|score=90|localhost\", 3000|from config\.settings|from config\.health_check_config" -S packages tools AFO || true
else
    grep -rnE "def build_organs_final|SSOT Canon Found|SSOT Missing|score=100|score=90|localhost\", 3000|from config\.settings|from config\.health_check_config" packages tools AFO || true
fi

echo
echo "=== C) SHOW THE EXACT FILE + HEAD SNIPPET (top 80 lines) ==="
python3 - << 'PY'
import subprocess, shlex, os
# Find file defining build_organs_final using grep to be safe
cmd="grep -l -R \"def build_organs_final\" packages tools AFO 2>/dev/null"
p=subprocess.run(cmd, shell=True, capture_output=True, text=True)
paths=[x.strip() for x in p.stdout.splitlines() if x.strip()]
print("FOUND:", paths)
for path in paths[:3]:
    if not os.path.exists(path): continue
    print("\n---", path, "---")
    # Read file directly
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
            # User asked for top 120 lines
            print("".join(lines[:120]))
    except Exception as e:
        print(f"Error reading {path}: {e}")
PY

echo
echo "=== D) PYTHON COMPILE CHECK (catch import path break) ==="
python3 -m compileall packages/afo-core -q || true

echo
echo "=== E) CI SINGLE ENTRY (SSOT) ==="
if [ -f scripts/ci_lock_protocol.sh ]; then
    bash scripts/ci_lock_protocol.sh || true
else
    echo "scripts/ci_lock_protocol.sh not found."
fi

echo
echo "=== F) LIVE PAYLOAD CHECK ==="
curl -sS http://127.0.0.1:8010/api/health/comprehensive | python3 -m json.tool | head -220 || echo "Curl failed (API likely down or waiting)"
