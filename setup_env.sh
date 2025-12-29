#!/bin/bash
# AFO Kingdom Environment Setup (Operation Flat Earth)
# Usage: source setup_env.sh

# 1. Root Definition
export WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export AFO_CORE="$WORKSPACE_ROOT/packages/afo-core"
export TRINITY_OS="$WORKSPACE_ROOT/packages/trinity-os"
export DASHBOARD="$WORKSPACE_ROOT/packages/dashboard"

# 2. Python Path Standardization
# Includes both core and OS packages for seamless imports
export PYTHONPATH="$AFO_CORE:$TRINITY_OS:$PYTHONPATH"

# 3. Virtual Environment Activation
if [ -d "$AFO_CORE/.venv" ]; then
    source "$AFO_CORE/.venv/bin/activate"
    echo "✅ Activated virtual environment: $AFO_CORE/.venv"
else
    echo "⚠️  Virtual environment not found at $AFO_CORE/.venv"
fi

# 4. Aliases for Convenience
alias afo-chk="python3 $WORKSPACE_ROOT/scripts/verify_all_skills_trinity_score.py"
alias afo-run="python3 -m AFO.api_server"
alias afo-mcp="python3 -m AFO.mcp.afo_skills_mcp"
alias afo-smoke="python3 $WORKSPACE_ROOT/scripts/mcp_smoke_test_afo_skills.py"

echo "🌍 [Operation Flat Earth] Environment Standardized."
echo "   WORKSPACE_ROOT: $WORKSPACE_ROOT"
echo "   PYTHONPATH: $(echo $PYTHONPATH | cut -d':' -f1-2)..."
echo "   Ready to serve, Commander."
