#!/usr/bin/env bash
set -euo pipefail

: "${AFO_OBSIDIAN_VAULT:?Set AFO_OBSIDIAN_VAULT}"

export AFO_QDRANT_URL="${AFO_QDRANT_URL:-http://localhost:6333}"
export AFO_OBSIDIAN_COLLECTION="${AFO_OBSIDIAN_COLLECTION:-obsidian_vault}"
export AFO_OBSIDIAN_STATE="${AFO_OBSIDIAN_STATE:-data/dspy/obsidian_qdrant_state.json}"

# 1) Incremental Index (qdrant down이면 자동 스킵)
poetry run python scripts/obsidian_refresh_incremental.py || true

# 2) Global Summary (항상 생성)
poetry run python scripts/obsidian_build_global_summary.py
