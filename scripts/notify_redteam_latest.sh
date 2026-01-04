#!/usr/bin/env bash
set -euo pipefail

LATEST="$(ls -1t artifacts/redteam/**/governance_report.md 2>/dev/null | head -1 || true)"
if [ -z "$LATEST" ]; then
  echo "no governance_report.md found"
  exit 1
fi

GRADE="$(python - << 'PY'
import re,sys
p=sys.argv[1]
s=open(p,'r',encoding='utf-8',errors='ignore').read()
m=re.search(r"(G0-[A-C])", s)
print(m.group(1) if m else "G0-?")
PY
"$LATEST")"

FAILS="$(python - << 'PY'
import re,sys
p=sys.argv[1]
s=open(p,'r',encoding='utf-8',errors='ignore').read()
tests=re.findall(r"(RT-[A-Z]+-\d+)", s)
uniq=[]
for t in tests:
    if t not in uniq: uniq.append(t)
print(", ".join(uniq[:12]) if uniq else "none")
PY
"$LATEST")"

SUMMARY="Report: $LATEST"
DETAIL="Grade: $GRADE\nFailed: $FAILS"

python scripts/notify_slack.py "RedTeam Governance Result" "$DETAIL" "$SUMMARY"
