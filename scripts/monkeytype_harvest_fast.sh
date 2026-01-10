#!/bin/bash
set -euo pipefail

# Fast Harvest for Pre-commit (runs on critical paths only)
# Goal: < 5 seconds execution

echo "🐵 [MonkeyType] Fast Harvest (Pre-commit) running..."

# 1. Clean previous partial DB (optional, but good for fresh preview)
rm -f monkeytype_fast.sqlite3 || true

# 2. Run selected fast tests
# Targeting Trinity & Health core for rapid feedback
export MONKEYTYPE_TRACEBACKS=0 # Disable heavy tracebacks for speed
export MONKEYTYPE_MAX_TRACEBACKS=0

python3 -m pytest -v --tb=no \
  --monkeytype-output=monkeytype_fast.sqlite3 \
  packages/afo-core/tests/test_trinity_engine.py \
  packages/afo-core/tests/test_trinity_unified.py \
  packages/afo-core/tests/test_goodness_serenity.py \
  > /dev/null 2>&1 || echo "⚠️  MonkeyType Fast Harvest had test failures (ignoring for pre-commit)"

# 3. Generate Preview (Silent unless changes found)
# We just check if we CAN generate a stub for a known target, effectively testing the pipeline.
# For pre-commit, we might just want to *collect* data or show a small stat.
# Let's show a quick stat.
if [ -f monkeytype_fast.sqlite3 ]; then
    SIZE=$(ls -lh monkeytype_fast.sqlite3 | awk '{print $5}')
    echo "✅ [MonkeyType] Harvested types into monkeytype_fast.sqlite3 ($SIZE)"
else
    echo "⚠️  [MonkeyType] No database generated."
fi
