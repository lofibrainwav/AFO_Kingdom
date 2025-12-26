#!/usr/bin/env bash
set -euo pipefail

TICKET="${1:?TICKET required (e.g. T28)}"
TITLE="${2:-TITLE}"
TS="$(date +%Y%m%d-%H%M)"
tx="$(echo "$TICKET" | tr '[:upper:]' '[:lower:]')"
EVD="artifacts/${tx}/${TS}"
RPT="docs/reports/${TICKET}_${TITLE}_SSOT.md"

mkdir -p "$EVD" "docs/reports"

cat > "$RPT" <<EOF
# ${TICKET} ${TITLE} SSOT Report
**Status**: UNVERIFIED
**Timestamp**: ${TS}
**Evidence**: ${EVD}/
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

echo "REPORT=$RPT"
echo "EVIDENCE_DIR=$EVD"
ls -la "$EVD" >/dev/null
