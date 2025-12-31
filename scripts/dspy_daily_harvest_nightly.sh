#!/usr/bin/env bash
set -euo pipefail

# Default LM if not set
export AFO_DSPY_LM="${AFO_DSPY_LM:-openai/gpt-4o-mini}"
export AFO_BASE_URL="${AFO_BASE_URL:-http://localhost:8010}"
export AFO_RAG_PATH="${AFO_RAG_PATH:-/api/query}"
export AFO_CONTEXT7_PATH="${AFO_CONTEXT7_PATH:-/api/context7/search}"
export AFO_GRAPHRAG_INDEX="${AFO_GRAPHRAG_INDEX:-data/dspy/graphrag_index.json}"

# Run with poetry
poetry run python scripts/dspy_daily_graphrag_harvest.py --commit "$@"
