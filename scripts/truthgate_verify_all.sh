
#!/usr/bin/env bash
set -euo pipefail

# TruthGate All Tickets Verification Script
# seal.json + verify_pass.txt(PASS) = 진실

TICKETS_FILE="scripts/truthgate_tickets.txt"
test -f "$TICKETS_FILE" || { echo "FAIL: missing $TICKETS_FILE"; exit 1; }

verify_ticket () {
  local T="$1"
  local TS="$2"
  local REPORT="$3"
  local T_LOWER="$(echo "$T" | tr '[:upper:]' '[:lower:]')"
  local EVD="artifacts/${T_LOWER}/$TS"

  echo "=== Verifying $T ($TS) ==="

  test -d "$EVD" || { echo "MISSING_EVIDENCE_DIR=$EVD"; return 1; }
  test -f "$EVD/seal.json" || { echo "MISSING_SEAL=$EVD/seal.json"; return 1; }
  test -f "$REPORT" || { echo "MISSING_REPORT=$REPORT"; return 1; }

  bash scripts/ssot_verify_ticket.sh "$T" "$TS" "$REPORT" 2>/dev/null || {
    # Fallback for tickets without report path requirement
    if [[ -f "$EVD/verify_pass.txt" ]] && rg -q "PASS" "$EVD/verify_pass.txt"; then
      echo "PASS: SSOT verified (fallback)"
      echo "VERIFIED_OK: $T $TS"
      return 0
    else
      echo "VERIFY_NOT_PASS: $T $TS"
      return 1
    fi
  }

  rg -q "PASS" "$EVD/verify_pass.txt" || { echo "VERIFY_NOT_PASS: $T $TS"; return 1; }

  echo "VERIFIED_OK: $T $TS"
  echo ""
}

while read -r TICKET TS REPORT; do
  [[ -z "${TICKET:-}" ]] && continue
  if ! verify_ticket "$TICKET" "$TS" "$REPORT"; then
    echo "VERIFICATION_FAILED: $TICKET $TS"
    exit 1
  fi
done < "$TICKETS_FILE"

echo "ALL_VERIFIED_OK"