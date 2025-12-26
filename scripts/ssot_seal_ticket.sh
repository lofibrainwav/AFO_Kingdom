#!/usr/bin/env bash
set -euo pipefail

TICKET="${1:?ticket id (e.g. T26)}"
TS="${2:?timestamp (e.g. 20251225-2145)}"
REPORT="${3:?report path}"
TICKET_LOWER=$(echo "$TICKET" | tr '[:upper:]' '[:lower:]')
EVDIR="artifacts/$TICKET_LOWER/$TS"
SEAL="$EVDIR/seal.json"

test -f "$REPORT" || (echo "FAIL: report missing $REPORT" && exit 1)
test -d "$EVDIR" || (echo "FAIL: evidence dir missing $EVDIR" && exit 2)

python3 - <<PY
import hashlib, json, os, pathlib, time

ticket="$TICKET"
ts="$TS"
report=pathlib.Path("$REPORT").as_posix()
evdir=pathlib.Path("$EVDIR")

files=[]
for p in sorted(evdir.rglob("*")):
  if p.is_file() and p.name != "seal.json":
    rel=p.relative_to(evdir).as_posix()
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    files.append({"path": rel, "bytes": p.stat().st_size, "sha256": h})

data={
  "ticket": ticket,
  "timestamp": ts,
  "report": report,
  "evidence_dir": evdir.as_posix(),
  "created_at_utc": int(time.time()),
  "files": files,
}
(evdir/"seal.json").write_text(json.dumps(data, indent=2, ensure_ascii=False)+ "\n", encoding="utf-8")
print("WROTE:", (evdir/"seal.json").as_posix(), "files=", len(files))
PY
