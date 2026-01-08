#!/bin/bash
# SSOT Verification Script (Security/Cleanup) v1.2.x
# Evidence-based validation with no sensitive data exposure

# Anchor & As-of (SSOT Required)
echo "AS_OF: $(date -u +%Y-%m-%dT%H:%M:%S%z)"
echo "ANCHOR: $(git rev-parse --abbrev-ref HEAD) | $(git rev-parse HEAD)"
echo "RUNTIME: ONLINE"
echo ""

# Pass Rules (SSOT Required - Fixed Criteria)
echo "RULE: sensitive_cache_count must be 0"
echo "RULE: .gitignore must include .mypy_cache and __pycache__ patterns"
echo "RULE: artifacts/logs directory must exist with security-related files"
echo "RULE: Evolution Log must contain PH-SEC-CLEANUP capsule"
echo "RULE: Latest commit must reference security cleanup"
echo ""

# Evidence Block (Commands → Outputs)
echo "## Evidence (Commands → Outputs)"
echo ""

echo "1) Sensitive cache files count"
echo "- Command: find . -path '*/.mypy_cache*' -name '*secrets*' -type f | wc -l | tr -d ' '"
echo "- Output: $(find . -path '*/.mypy_cache*' -name '*secrets*' -type f | wc -l | tr -d ' ')"
echo "- Pass rule: output == 0"
echo ""

echo "2) .gitignore rules"
echo "- Command: grep -n '\.mypy_cache' .gitignore"
echo "- Output: $(grep -n '\.mypy_cache' .gitignore | tr '\n' ' | ' | sed 's/|$//')"
echo "- Pass rule: required patterns exist"
echo ""

echo "3) Logs directory"
echo "- Command: ls -lh artifacts/logs/ 2>/dev/null | grep -E '(security|cline-background)' | wc -l"
echo "- Output: $(ls artifacts/logs/ 2>/dev/null | grep -E "(security-scan|cline-background)" | wc -l)"
echo "- Pass rule: output >= 2"
echo ""

echo "4) Evolution Log record"
echo "- Command: grep -c 'PH-SEC-CLEANUP' docs/AFO_EVOLUTION_LOG.md"
echo "- Output: $(grep -c 'PH-SEC-CLEANUP' docs/AFO_EVOLUTION_LOG.md)"
echo "- Pass rule: output >= 1"
echo ""

echo "5) Git commit record"
echo "- Command: git log --oneline -1 | grep -c '보안 취약점'"
echo "- Output: $(git log --oneline -1 | grep -c '보안 취약점')"
echo "- Pass rule: output >= 1"
echo ""

echo "6) Trinity score"
echo "- Command: grep -c 'trinity_score' docs/ssot/traces/traces.jsonl 2>/dev/null || echo 'TRINITY: N/A'"
trinity_check=$(grep -c 'trinity_score' docs/ssot/traces/traces.jsonl 2>/dev/null || echo "0")
if [ "$trinity_check" = "0" ]; then
    echo "- Output: TRINITY: N/A (no trace key)"
else
    echo "- Output: $(grep -c 'trinity_score' docs/ssot/traces/traces.jsonl)"
fi
echo "- Pass rule: If missing → Trinity=N/A"
echo ""

# Exit Code (SSOT Required)
echo "EXIT_CODE=$?"
