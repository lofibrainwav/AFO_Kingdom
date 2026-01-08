#!/bin/bash
# scripts/ci_lock_protocol.sh
# AFO Kingdom CI/CD LOCK Protocol Enforcement
# 眞善美孝永 - Pyright -> Ruff -> pytest -> SBOM

set -euo pipefail

# 0. Setup
LOG_DIR="artifacts/ci"
mkdir -p "$LOG_DIR"
mkdir -p "artifacts/sbom"

BASE_FILE="$LOG_DIR/pyright_baseline.txt"
REPORT_FILE="$LOG_DIR/pyright_report.txt"
REG_FILE="$LOG_DIR/pyright_regressions.txt"

echo "🔒 [CI/CD LOCK] Starting 4-Gate Verification Protocol..."

# 1. Pyright (眞 - Truth)
echo "⚔️  [Step 1/4] Pyright Static Type Analysis (Truth)..."

# Pyright path discovery
PYRIGHT_BIN="pyright"
if ! command -v pyright &> /dev/null; then
    if [ -f ".venv/bin/pyright" ]; then
        PYRIGHT_BIN=".venv/bin/pyright"
    elif [ -f "venv/bin/pyright" ]; then
        PYRIGHT_BIN="venv/bin/pyright"
    fi
fi

# Run Pyright and capture standardized output (filtering out version warnings and trimming whitespace)
($PYRIGHT_BIN --project packages/afo-core/pyproject.toml 2>&1 | grep -v "pyright version" | grep -v "PYRIGHT_PYTHON_FORCE_VERSION" | grep -v "Please install the new version" | sed 's/[[:space:]]*$//' | grep -v '^$' | LC_ALL=C sort > "$REPORT_FILE") || true

if [ -f "$BASE_FILE" ]; then
    # Standardize baseline for comparison
    LC_ALL=C sort -o "$BASE_FILE" "$BASE_FILE"
    # Find new lines in report that are not in baseline
    comm -13 "$BASE_FILE" "$REPORT_FILE" > "$REG_FILE" || true

    if [ -s "$REG_FILE" ]; then
        echo "⛔️ Pyright regression detected (new warnings):"
        head -n 20 "$REG_FILE"
        echo "...(refer to $REG_FILE for full list)"
        echo "❌ LOCK FAILURE: Truth Pillar compromised by regression."
        exit 1
    fi
    echo "✅ Pyright baseline OK (no regressions detected)."
else
    echo "⚠️  Pyright Baseline not found. Creating from current state..."
    cp "$REPORT_FILE" "$BASE_FILE"
    echo "✅ Baseline created: $BASE_FILE (COMMIT THIS FILE to lock the baseline)"
fi

# 2. Ruff (美 - Beauty)
echo "🌉 [Step 2/4] Ruff Linting & Formatting (Beauty)..."
(cd packages/afo-core && ruff check . 2>&1 | tee "../../$LOG_DIR/ruff_report.txt") || {
    echo "❌ Ruff check failed. Beauty Pillar compromised. Refer to $LOG_DIR/ruff_report.txt"
    exit 1
}
(cd packages/afo-core && ruff format --check . 2>&1 | tee -a "../../$LOG_DIR/ruff_report.txt") || {
    echo "❌ Ruff formatting check failed. Beauty Pillar compromised."
    exit 1
}

# 3. pytest (膽 - Gallbladder/Goodness)
echo "🛡️  [Step 3/4] pytest Unit & Integration Tests (Goodness)..."
# 2026 Optimization: parallel execution with pytest-xdist (-n auto) + exclude slow tests
(cd packages/afo-core && pytest -q --maxfail=1 -n auto --dist worksteal -m "not integration and not external and not slow" --ignore=tests/test_scholars.py 2>&1 | tee "../../$LOG_DIR/pytest_report.txt") || {
    echo "❌ pytest failed. Goodness/Stability Pillar compromised. Refer to $LOG_DIR/pytest_report.txt"
    exit 1
}

# 4. SBOM (永/善 - Eternity/Goodness)
echo "♾️  [Step 4/4] SBOM Generation & Security Seal (Eternity)..."
python3 scripts/generate_sbom.py 2>&1 | tee "$LOG_DIR/sbom_log.txt" || {
    echo "❌ SBOM generation failed. Eternity/Security Pillar compromised."
    exit 1
}

# Standardize SBOM location
mv sbom artifacts/ 2>/dev/null || true

# Standardized Victory Seal Summary
echo ""
echo "===================================================="
echo "🎯 CI/CD LOCK VICTORY SUMMARY"
echo "----------------------------------------------------"
echo "1. Pyright: [PASS] No regressions vs baseline"
echo "2. Ruff:    [PASS] Quality & Format stabilized"
echo "3. pytest:  [PASS] Core organs functional"
echo "4. SBOM:    [PASS] Eternity seal applied"
echo "===================================================="
echo "✨ All 4 gates PASSED. The Kingdom is physically SECURE (SEALED)."
echo "   Artifacts: $LOG_DIR/ and artifacts/sbom/"
echo "===================================================="
exit 0
