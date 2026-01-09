#!/bin/bash
cd /Users/brnestrm/AFO_Kingdom
set -u

echo "=== A) CHANGED FILES + HEAD ==="
git status -sb
git log -n 8 --oneline

echo
echo "=== B) NO HARDCODED SCORE / SECURITY / DOCS PATH HACKS? ==="
# Fallback to grep if rg is missing
if command -v rg &> /dev/null; then
    rg -n 'score\s*=\s*(100|90)|Security Scans Verified|trivy-results\.json|AFO_FINAL_SSOT\.md|TICKETS\.md|localhost:8010|127\.0\.0\.1:8010' -S packages/afo-core AFO tools || true
else
    grep -rnE 'score\s*=\s*(100|90)|Security Scans Verified|trivy-results\.json|AFO_FINAL_SSOT\.md|TICKETS\.md|localhost:8010|127\.0\.0\.1:8010' packages/afo-core AFO tools || true
fi

echo
echo "=== C) SHOW THE ACTUAL IMPLEMENTATION (first 260 lines around probes) ==="
python3 - << 'PY'
import subprocess, shlex, os
patterns = [
  "TICKETS.md", "trivy-results.json", "AFO_FINAL_SSOT.md",
  "localhost:8010", "127.0.0.1:8010",
  "def build_organs", "OrganReport", "口_Docs", "免疫_Trinity_Gate", "腦_Soul_Engine"
]
# Use grep instead of rg for safety in this python block since users env might vary
cmd_parts = []
for p in patterns:
    cmd_parts.append(f"-e {shlex.quote(p)}")
pattern_string = " ".join(cmd_parts)

# Constructing a grep command that searches recursively
cmd = f"grep -l -R {pattern_string} packages/afo-core AFO tools 2>/dev/null"

# Attempt to run check
try:
    p = subprocess.run("grep -l -R -E 'TICKETS.md|trivy-results.json|AFO_FINAL_SSOT.md|localhost:8010|127.0.0.1:8010' packages/afo-core 2>/dev/null", shell=True, capture_output=True, text=True)
    paths = [x.strip() for x in p.stdout.splitlines() if x.strip()]
except:
    paths = []

print("FILES FOUND:", paths)

for path in paths[:4]:
  if not os.path.exists(path): continue
  print("\n---", path, "---")
  try:
    with open(path, 'r') as f:
        lines = f.readlines()
        print("".join(lines[:260]))
  except Exception as e:
    print(f"Error reading {path}: {e}")
PY

echo
echo "=== D) CI SINGLE ENTRY (SSOT) ==="
if [ -f scripts/ci_lock_protocol.sh ]; then
    bash scripts/ci_lock_protocol.sh || true
else
    echo "scripts/ci_lock_protocol.sh not found."
fi

echo
echo "=== E) LIVE PAYLOAD (REAL NUMBERS) ==="
if pgrep -f "api_server.py" > /dev/null; then
    curl -sS http://127.0.0.1:8010/api/health/comprehensive | python3 -m json.tool | head -260 || echo "Curl failed"
else
    echo "API Server not running"
fi

echo
echo "=== F) CHECK THE 3 CLAIMS DIRECTLY ==="
python3 - << 'PY'
import json, subprocess
try:
    raw = subprocess.check_output("curl -sS http://127.0.0.1:8010/api/health/comprehensive", shell=True)
    d = json.loads(raw)
    b = d.get("trinity_breakdown") or d.get("breakdown") or {}
    org = d.get("organs") or {}
    print("trinity_score:", d.get("trinity_score"), "health%:", d.get("health_percentage"))
    print("breakdown.truth:", b.get("truth"))
    print("breakdown.goodness:", b.get("goodness"))
    print("breakdown.eternity:", b.get("eternity"))
    print("iccls_gap:", b.get("iccls_gap"), "sentiment:", b.get("sentiment"))
    print("organs keys:", list(org.keys())[:12])
except Exception as e:
    print(f"Check failed: {e}")
PY
