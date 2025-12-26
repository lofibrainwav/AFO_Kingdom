#!/usr/bin/env bash
set -euo pipefail

TICKET="${1:?usage: $0 T22 docs/reports/T22_XXX_SSOT.md 'keyword_regex' [TS]}"
REPORT="${2:?report path required}"
KW="${3:?keyword regex required}"
TS="${4:-$(date +%Y%m%d-%H%M)}"

tx="$(echo "$TICKET" | tr '[:upper:]' '[:lower:]')"
OUT="artifacts/${tx}/${TS}"
mkdir -p "$OUT"

echo "$TICKET" > "$OUT/ticket.txt"
echo "$TS" > "$OUT/timestamp.txt"
git rev-parse --abbrev-ref HEAD > "$OUT/git_branch.txt" || true
git status --porcelain > "$OUT/git_status.txt" || true
git diff --cached --name-only > "$OUT/git_staged_files.txt" || true
git diff --name-only > "$OUT/git_files_changed.txt" || true

# Codebase keyword research (evidence)
rg -n "$KW" packages -S > "$OUT/rg_codebase_${tx}.txt" || true

# Dashboard reachability (evidence)
curl -sS -D "$OUT/dashboard_headers.txt" -o /dev/null http://127.0.0.1:3000 || true

# FastAPI OpenAPI discovery (evidence)
curl -sS -D "$OUT/openapi_headers.txt" -o "$OUT/openapi.json" http://127.0.0.1:8010/openapi.json || true

python3 - <<'PY'
import json, re, pathlib
out = pathlib.Path("'$OUT'")
kw = re.compile(r"'$KW'", re.I)

paths_txt = out/"api_paths_matching.txt"
calls_txt = out/"api_calls_plan.txt"

openapi = out/"openapi.json"
matched = []

def safe_name(s: str) -> str:
  return re.sub(r"[^a-zA-Z0-9._-]+","_",s).strip("_")[:120]

if openapi.exists():
  try:
    spec = json.loads(openapi.read_text(encoding="utf-8"))
    paths = spec.get("paths", {})
    for path, methods in paths.items():
      if kw.search(path) or any(kw.search(k) for k in methods.keys()):
        for m in methods.keys():
          matched.append((m.upper(), path))
  except Exception:
    pass

paths_txt.write_text("\n".join([f"{m} {p}" for m,p in matched]) + ("\n" if matched else ""), encoding="utf-8")

# Build safe call plan: GET preferred, otherwise OPTIONS only
plan = []
for m,p in matched:
  if m == "GET":
    plan.append(("GET", p))
  else:
    plan.append(("OPTIONS", p))

calls_txt.write_text("\n".join([f"{m} {p}" for m,p in plan]) + ("\n" if plan else ""), encoding="utf-8")
PY

# Execute call plan (evidence)
if [[ -s "$OUT/api_calls_plan.txt" ]]; then
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    METHOD="${line%% *}"
    PATH="${line#* }"
    SAFE="$(python3 - <<PY
import re
s=r"$METHOD $PATH"
print(re.sub(r"[^a-zA-Z0-9._-]+","_",s).strip("_")[:120])
PY
)"
    curl -sS --max-time 10 -X "$METHOD" \
      -D "$OUT/api_${SAFE}_headers.txt" \
      -o "$OUT/api_${SAFE}_body.txt" \
      "http://127.0.0.1:8010${PATH}" || true
  done < "$OUT/api_calls_plan.txt"
fi

# --- GREEN CHECK (auto) ---
python3 - <<'PY'
import json, pathlib, re

out = pathlib.Path("'$OUT'")

def http_code(headers_path: pathlib.Path) -> int:
  if not headers_path.exists():
    return 0
  txt = headers_path.read_text(encoding="utf-8", errors="ignore")
  m = re.search(r"HTTP/\\S+\\s+(\\d+)", txt)
  return int(m.group(1)) if m else 0

dashboard_ok = http_code(out/"dashboard_headers.txt") in (200,301,302,307,308)
openapi_ok = http_code(out/"openapi_headers.txt") == 200 and (out/"openapi.json").exists() and (out/"openapi.json").stat().st_size > 0

paths = (out/"api_paths_matching.txt").read_text(encoding="utf-8", errors="ignore").strip().splitlines() if (out/"api_paths_matching.txt").exists() else []
has_matching_paths = len(paths) > 0

# Any GET call returning 200 with non-empty body
api_ok = False
for p in out.glob("api_*_headers.txt"):
  code = http_code(p)
  if code == 200:
    body = out/(p.name.replace("_headers.txt","_body.txt"))
    if body.exists() and body.stat().st_size > 0:
      api_ok = True
      break

green = {
  "dashboard_reachable": dashboard_ok,
  "openapi_available": openapi_ok,
  "matching_api_paths_found": has_matching_paths,
  "at_least_one_api_200_with_body": api_ok,
}
green["pass"] = all(green.values())

(out/"green_check.json").write_text(json.dumps(green, indent=2), encoding="utf-8")

if green["pass"]:
  (out/"green_pass.txt").write_text("PASS: GREEN CHECK\n", encoding="utf-8")
else:
  (out/"green_pass.txt").write_text("FAIL: GREEN CHECK\n", encoding="utf-8")
PY

# --- SEAL (include evidence files + staged code files) ---
python3 - <<'PY'
import hashlib, json, os, time
from pathlib import Path

ticket = "'$TICKET'"
ts = "'$TS'"
out = Path("'$OUT'")
repo = Path(".")

def sha256_file(p: Path) -> str:
  h = hashlib.sha256()
  with p.open("rb") as f:
    for chunk in iter(lambda: f.read(1024*1024), b""):
      h.update(chunk)
  return h.hexdigest()

# evidence files (exclude seal/verify recursion)
evidence_files = []
for p in sorted(out.rglob("*")):
  if p.is_file():
    if p.name in ("seal.json","verify_pass.txt"):
      continue
    rel = p.as_posix()
    evidence_files.append(rel)

# staged code files
try:
  staged = os.popen("git diff --cached --name-only --diff-filter=ACMRT").read().strip().splitlines()
except Exception:
  staged = []
staged = [s for s in staged if s and not s.startswith("artifacts/")]

files = []
seen = set()

def add_file(relpath: str):
  rp = Path(relpath)
  if not rp.exists() or rp.is_dir():
    return
  if relpath in seen:
    return
  seen.add(relpath)
  files.append({
    "path": relpath,
    "bytes": rp.stat().st_size,
    "sha256": sha256_file(rp),
  })

for rel in evidence_files:
  add_file(rel)

for rel in staged:
  add_file(rel)

seal = {
  "ticket": ticket,
  "timestamp": ts,
  "report": "'$REPORT'",
  "evidence_dir": out.as_posix(),
  "created_at_utc": int(time.time()),
  "files": files,
}

(out/"seal.json").write_text(json.dumps(seal, indent=2), encoding="utf-8")
PY

# --- VERIFY ---
python3 - <<'PY'
import hashlib, json, sys
from pathlib import Path

def sha256_file(p: Path) -> str:
  h = hashlib.sha256()
  with p.open("rb") as f:
    for chunk in iter(lambda: f.read(1024*1024), b""):
      h.update(chunk)
  return h.hexdigest()

out = Path("'$OUT'")
seal = json.loads((out/"seal.json").read_text(encoding="utf-8"))
bad = []
for f in seal.get("files", []):
  p = Path(f["path"])
  if not p.exists():
    bad.append(f"missing:{f['path']}")
    continue
  h = sha256_file(p)
  if h != f["sha256"]:
    bad.append(f"sha_mismatch:{f['path']}")

if bad:
  (out/"verify_pass.txt").write_text("FAIL: SSOT verify\n" + "\n".join(bad) + "\n", encoding="utf-8")
  sys.exit(1)

(out/"verify_pass.txt").write_text(
  "PASS: SSOT verified\n"
  f"PASS: {seal.get('ticket')} evidence sealed (by seal.json + file hashes)\n",
  encoding="utf-8"
)
PY

# --- REPORT header auto-update (Status depends on green_pass) ---
mkdir -p "$(dirname "$REPORT")"
if [[ ! -f "$REPORT" ]]; then
  cat > "$REPORT" <<EOF
# ${TICKET} SSOT Report
**Status**: UNVERIFIED
**Timestamp**: ${TS}
**Evidence**: ${OUT}/
**SealSHA256**: TBD
**Verify**: TBD

## 1) What changed (Files edited)
- TBD

## 2) Commands run
- TBD

## 3) Evidence
- TBD

## 4) Green Check
- [ ] TBD
EOF
fi

SEAL_SHA="$(python3 - <<PY
import hashlib
from pathlib import Path
p=Path("$OUT/seal.json")
h=hashlib.sha256(p.read_bytes()).hexdigest()
print(h)
PY
)"

GREEN_LINE="$(head -n 1 "$OUT/green_pass.txt" 2>/dev/null || true)"
if [[ "$GREEN_LINE" == "PASS: GREEN CHECK" ]]; then
  STATUS="SEALED-VERIFIED"
else
  STATUS="UNVERIFIED"
fi

python3 - <<PY
import re
from pathlib import Path
rp=Path("$REPORT")
txt=rp.read_text(encoding="utf-8", errors="ignore")

def rep(key, val):
  nonlocal_txt[0] = re.sub(rf"^\\*\\*{re.escape(key)}\\*\\*:\\s*.*$", f"**{key}**: {val}", nonlocal_txt[0], flags=re.M)

nonlocal_txt=[txt]
rep("Status", "$STATUS")
rep("Timestamp", "$TS")
rep("Evidence", "$OUT/")
rep("SealSHA256", "$SEAL_SHA")
rep("Verify", "PASS (from verify_pass.txt)")
rp.write_text(nonlocal_txt[0], encoding="utf-8")
PY

echo "TICKET=$TICKET"
echo "TS=$TS"
echo "EVIDENCE_DIR=$OUT"
echo "REPORT=$REPORT"
echo "SEAL_SHA256=$SEAL_SHA"
cat "$OUT/green_pass.txt"
