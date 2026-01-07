#!/usr/bin/env bash
set -euo pipefail

# Filial Gate Verify - Phase 1 SSOT Compliance Check
echo "🔒 Running Filial Gate Verify..."

# Basic SSOT compliance check
if [ -f "docs/AFO_ROYAL_LIBRARY.md" ] && [ -f "AGENTS.md" ]; then
  echo "✅ [PASS] Royal Library and Agents manifest present"
else
  echo "❌ [FAIL] Missing core SSOT files"
  exit 1
fi

# Check for Trinity compliance (flexible check)
if grep -q "眞善美" docs/AFO_ROYAL_LIBRARY.md 2>/dev/null || grep -q "Trinity" docs/AFO_ROYAL_LIBRARY.md 2>/dev/null; then
  echo "✅ [PASS] Trinity philosophy compliance verified"
else
  echo "⚠️ [WARN] Trinity philosophy reference not found (non-critical)"
fi

echo "✨ Filial Gate Verify Passed."
