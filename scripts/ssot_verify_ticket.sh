#!/usr/bin/env bash
set -euo pipefail

TICKET="${1:?ticket id required (e.g. T26)}"
TS="${2:?timestamp required (e.g. 20251225-2145)}"
REPORT="${3:?report path required}"
EVDIR="artifacts/$(echo $TICKET | tr '[:upper:]' '[:lower:]')/$TS"
SEAL="$EVDIR/seal.json"

fail() { echo "FAIL: $*"; exit 1; }

test -f "$REPORT" || fail "report missing: $REPORT"
test -d "$EVDIR" || fail "evidence dir missing: $EVDIR"
test -f "$SEAL"  || fail "seal missing: $SEAL"

python - <<PY
import json, hashlib, pathlib, sys

ticket = "$TICKET"
ts = "$TS"
report = pathlib.Path("$REPORT")
evdir = pathlib.Path("$EVDIR")
seal = evdir / "seal.json"

data = json.loads(seal.read_text(encoding="utf-8"))

def req(k):
  if k not in data:
    raise SystemExit(f"FAIL: seal missing key: {k}")

for k in ["ticket","timestamp","report","evidence_dir","files"]:
  req(k)

if data["ticket"] != ticket:
  raise SystemExit(f"FAIL: seal.ticket mismatch {data['ticket']} != {ticket}")
if data["timestamp"] != ts:
  raise SystemExit(f"FAIL: seal.timestamp mismatch {data['timestamp']} != {ts}")

if pathlib.Path(data["report"]).as_posix() != report.as_posix():
  raise SystemExit(f"FAIL: seal.report mismatch {data['report']} != {report.as_posix()}")

if pathlib.Path(data["evidence_dir"]).as_posix() != evdir.as_posix():
  raise SystemExit(f"FAIL: seal.evidence_dir mismatch {data['evidence_dir']} != {evdir.as_posix()}")

files = data["files"]
if not isinstance(files, list) or not files:
  raise SystemExit("FAIL: seal.files must be non-empty list")

missing = []
bad_hash = []
zero = []

for f in files:
  p = evdir / f["path"]
  if not p.exists():
    missing.append(f["path"]); continue
  if p.stat().st_size == 0:
    zero.append(f["path"])
  h = hashlib.sha256(p.read_bytes()).hexdigest()
  if h != f["sha256"]:
    bad_hash.append((f["path"], f["sha256"], h))

if missing:
  raise SystemExit("FAIL: missing files: " + ", ".join(missing))
if zero:
  raise SystemExit("FAIL: zero-byte files: " + ", ".join(zero))
if bad_hash:
  first = bad_hash[0]
  raise SystemExit(f"FAIL: hash mismatch: {first[0]} expected={first[1]} got={first[2]}")

print("PASS: SSOT verified")
PY

echo "PASS: $TICKET is SEALED-VERIFIED (by seal.json + file hashes)"