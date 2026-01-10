#!/bin/bash
set -euo pipefail

cd /Users/brnestrm/AFO_Kingdom

echo "=== A) WHAT FILES CHANGED? ==="
git status -sb || echo "Git status failed"

echo
echo "=== B) LOCATE build_organs_final / docs probe / hardcoded scores ==="
# Using grep instead of rg if rg is not in path, but attempting rg first
if command -v rg &> /dev/null; then
    rg -n "def build_organs_final|SSOT Canon Found|SSOT Missing|score=100|score=90|localhost\", 3000|from config\.settings|from config\.health_check_config" -S packages tools AFO || true
else
    grep -rnE "def build_organs_final|SSOT Canon Found|SSOT Missing|score=100|score=90|localhost\", 3000|from config\.settings|from config\.health_check_config" packages tools AFO || true
fi

echo
echo "=== C) SHOW THE EXACT FILE + HEAD SNIPPET (top 80 lines) ==="
python3 - << 'PY'
import subprocess, shlex, os
# Find file defining build_organs_final
cmd="grep -l \"def build_organs_final\" -R packages tools AFO 2>/dev/null"
p=subprocess.run(cmd, shell=True, capture_output=True, text=True)
paths=[x.strip() for x in p.stdout.splitlines() if x.strip()]
print("FOUND:", paths)
for path in paths[:3]:
    if not os.path.exists(path): continue
    print("\n---", path, "---")
    # Python compatible sed alternative or just read file
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
            print("".join(lines[:120]))
    except Exception as e:
        print(f"Error reading {path}: {e}")
PY

echo
echo "=== D) PYTHON COMPILE CHECK (catch import path break) ==="
python3 -m compileall packages/afo-core -q || echo "Compile check noticed errors, continuing..."

echo
echo "=== E) CI SINGLE ENTRY (SSOT) ==="
if [ -f scripts/ci_lock_protocol.sh ]; then
    bash scripts/ci_lock_protocol.sh || echo "CI Lock Protocol failed"
else
    echo "scripts/ci_lock_protocol.sh not found, skipping."
fi

echo
echo "=== F) LIVE PAYLOAD CHECK ==="
# Check if API is running, if not, skip curl
if pgrep -f "api_server.py" > /dev/null; then
    curl -sS http://127.0.0.1:8010/api/health/comprehensive | python3 -m json.tool | head -220 || echo "Curl failed"
else
    echo "API Server not running, skipping live payload check."
fi
