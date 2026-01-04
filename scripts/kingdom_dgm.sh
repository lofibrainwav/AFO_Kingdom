#!/usr/bin/env bash
set -euo pipefail

if [ "${BASH_SOURCE[0]}" != "$0" ]; then
  echo "❌ Do not source this script."
  return 1 2>/dev/null || exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p artifacts/dgm_runs

ts="$(date -u +"%Y%m%dT%H%M%SZ")"
boot="artifacts/dgm_runs/dgm_boot_${ts}.jsonl"

openai_set="$([ -n "${OPENAI_API_KEY:-}" ] && echo 1 || echo 0)"
anthropic_set="$([ -n "${ANTHROPIC_API_KEY:-}" ] && echo 1 || echo 0)"

python - <<PY > "$boot"
import json, os, datetime
print(json.dumps({
  "ts": datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
  "ollama_base_url": os.getenv("OLLAMA_BASE_URL"),
  "openai_key_set": bool(os.getenv("OPENAI_API_KEY")),
  "anthropic_key_set": bool(os.getenv("ANTHROPIC_API_KEY")),
  "afo_dgm_run": os.getenv("AFO_DGM_RUN","0"),
}))
PY

if [[ "${AFO_DGM_RUN:-0}" != "1" ]]; then
  echo "✅ DGM wiring OK. (Set AFO_DGM_RUN=1 to execute.)"
  tail -n 1 "$boot"
  exit 0
fi

command -v docker >/dev/null 2>&1 || { echo "❌ docker not found"; exit 1; }
[[ "$openai_set" == "1" && "$anthropic_set" == "1" ]] || { echo "❌ Missing OPENAI_API_KEY or ANTHROPIC_API_KEY"; exit 1; }

python tools/dgm/upstream/DGM_outer.py
