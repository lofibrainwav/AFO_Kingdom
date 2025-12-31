#!/usr/bin/env bash
set -euo pipefail

: "${AFO_OBSIDIAN_VAULT:?Set AFO_OBSIDIAN_VAULT}"

export AFO_QDRANT_URL="${AFO_QDRANT_URL:-http://localhost:6333}"
export AFO_OBSIDIAN_COLLECTION="${AFO_OBSIDIAN_COLLECTION:-obsidian_vault}"

poetry run python scripts/obsidian_build_qdrant_index.py
poetry run python scripts/obsidian_build_global_summary.py
