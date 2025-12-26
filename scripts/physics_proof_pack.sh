#!/usr/bin/env bash
set -euo pipefail

show_ticket () {
  local T="$1"
  local TS="$2"
  local T_LOWER="$(echo "$T" | tr '[:upper:]' '[:lower:]')"
  local EVD="artifacts/${T_LOWER}/$TS"

  echo "=============================="
  echo "TICKET=$T TS=$TS"
  echo "EVIDENCE_DIR=$EVD"

  test -d "$EVD" || { echo "MISSING_DIR"; return 1; }
  test -f "$EVD/seal.json" || { echo "MISSING_SEAL_JSON"; return 1; }
  test -f "$EVD/verify_pass.txt" || { echo "MISSING_VERIFY_PASS"; return 1; }

  echo "-- ls -la --"
  ls -la "$EVD" | sed -n '1,40p'

  echo "-- sha256(seal.json) --"
  shasum -a 256 "$EVD/seal.json" || sha256sum "$EVD/seal.json"

  echo "-- verify_pass.txt (head) --"
  sed -n '1,25p' "$EVD/verify_pass.txt"

  echo "-- PASS? --"
  if rg -n "PASS" "$EVD/verify_pass.txt" >/dev/null; then
    echo "PASS_FOUND=YES"
  else
    echo "PASS_FOUND=NO"
    return 1
  fi
}

show_ticket "T25" "20251225-2210"
show_ticket "T26" "20251225-2145"
show_ticket "T27" "20251225-2225"

echo "ALL_TICKETS_PHYSICS_OK"

show_ticket "T24" "20251225-2251"
