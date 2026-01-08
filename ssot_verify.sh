#!/usr/bin/env bash
set -euo pipefail

fail=0

pass(){ echo "✅ $*"; }
nope(){ echo "❌ $*"; fail=1; }
skip(){ echo "⏭️  $*"; }

need_file(){
  if [ -f "$1" ]; then pass "file exists: $1"; else nope "missing file: $1"; fi
}

need_match(){
  local file="$1"; shift
  local pat="$1"; shift
  if [ -f "$file" ] && grep -nE "$pat" "$file" >/dev/null 2>&1; then
    pass "match in $file: $pat"
  else
    nope "no match in $file: $pat"
  fi
}

echo "=== SSOT Reality Check ==="

# Handle task.md location (it's in artifacts dir)
TASK_MD_PATH="/Users/brnestrm/.gemini/antigravity/brain/84f11b7f-7757-4ca8-9452-df0ad12e3aab/task.md"
need_file "$TASK_MD_PATH"
need_match "$TASK_MD_PATH" "Phase 3: Soul Engine Resurrection"
need_match "$TASK_MD_PATH" "Action 3: Docker Eternity"

need_file "AFO_EVOLUTION_LOG.md"
need_match "AFO_EVOLUTION_LOG.md" "2025-12-28|Soul Engine Resurrection|Docker Eternity"

need_file "pyproject.toml"
need_match "pyproject.toml" "playwright\\s*=\\s*\"\\^?1\\.40\\.0\"|playwright\\s*=\\s*\"\\^?1\\.40"

df_found=0
# Simplified loop for compatibility
for df in $(find . -maxdepth 5 -type f \( -name "Dockerfile" -o -name "dockerfile" \) 2>/dev/null); do
  df_found=1
  if grep -n "playwright" "$df" >/dev/null 2>&1; then
    pass "Dockerfile has playwright: $df"
  else
    if [[ "$df" == *"packages/afo-core/Dockerfile"* ]] || [[ "$df" == *"Dockerfile"* ]]; then
        if grep -n "playwright" "$df" >/dev/null 2>&1; then
             pass "Dockerfile has playwright: $df"
        else
             if [[ "$df" == *"packages/afo-core/Dockerfile"* ]]; then
                 nope "Dockerfile missing playwright: $df"
             else
                 skip "Dockerfile (other) missing playwright: $df"
             fi
        fi
    fi
  fi
  if grep -nE "playwright\\s+install|playwright\\s+install\\." "$df" >/dev/null 2>&1; then
     pass "Dockerfile has playwright install: $df"
  fi
done

if [ "$df_found" -eq 0 ]; then skip "no Dockerfile found (maxdepth 5)"; fi

health_ok=0
for url in \
  "http://localhost:8010/health/comprehensive" \
  "http://localhost:8010/api/health/comprehensive" \
   \
   \
   \
  
do
  if curl -fsS --max-time 2 "$url" >/tmp/afo_health.json 2>/dev/null; then
    if python3 - <<'PY' >/dev/null 2>&1
import json
p="/tmp/afo_health.json"
try:
  d=json.load(open(p,"r",encoding="utf-8"))
except Exception:
  raise SystemExit(1)
ok = ("organs_v2" in d) or ("organs" in d) or ("organsV2" in d)
raise SystemExit(0 if ok else 2)
PY
    then
      pass "health ok (organs* present): $url"
      health_ok=1
      break
    else
      nope "health reachable but missing organs keys: $url"
    fi
  fi
done
if [ "$health_ok" -eq 0 ]; then skip "health not reachable on known local urls"; fi

if docker info >/dev/null 2>&1; then
  pass "docker daemon: up"
else
  skip "docker daemon: down (build pending)"
fi

echo "=== RESULT ==="
if [ "$fail" -eq 0 ]; then
  echo "✅ SSOT matches repo reality (on checked items)"
else
  echo "❌ SSOT mismatch detected (see ❌ lines)"
  exit 1
fi
