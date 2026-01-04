#!/usr/bin/env bash
set -euo pipefail
echo "[git]"
git status -sb
echo
echo "[docs index]"
test -f artifacts/housekeeping/docs_index.md && echo "OK docs_index.md" || (echo "MISSING docs_index.md" && exit 1)
test -f artifacts/housekeeping/docs_index.json && echo "OK docs_index.json" || (echo "MISSING docs_index.json" && exit 1)
echo
echo "[tree snapshot]"
test -f artifacts/housekeeping/tree.txt && echo "OK tree.txt" || (echo "MISSING tree.txt" && exit 1)
echo
echo "[artifacts policy]"
test -f docs/ops/ARTIFACTS_POLICY.md && echo "OK ARTIFACTS_POLICY.md" || (echo "MISSING policy" && exit 1)
