#!/bin/bash
# AFO Kingdom - SSOT ScoreCard Autogen v1
# [眞善美孝永] Antigravity Chancellor Script

AS_OF=$(date +"%Y-%m-%d (%Z)")
BRANCH=$(git branch --show-current)
SHA=$(git rev-parse --short HEAD)

# Runtime Status Detection
if lsof -i :8010 > /dev/null; then
    RUNTIME="ONLINE | Port 8010 Active"
else
    RUNTIME="OFFLINE | Docker Daemon / Soul Engine 미기동"
fi

# Trinity Score (Current Target / Simulation)
# Note: Final Runtime score will be aggregated from trunk traces.jsonl
TRINITY="95.5% [Target (Simulation)]"

# Debt Status Collection
# Ruff: Frozen baseline established at 2026-01-08
RUFF_DEBT=2285

# Pyright: Count from actual baseline file if exists
PYRIGHT_FILE="packages/afo-core/AFO/pyright_baseline.txt"
if [ -f "$PYRIGHT_FILE" ]; then
    PYRIGHT_DEBT=$(grep -c "error:" "$PYRIGHT_FILE")
else
    PYRIGHT_DEBT="N/A"
fi

cat <<EOF
## 🧾 SSOT ScoreCard (Current Pillar Status)
> [!NOTE]
> **As-of**: $AS_OF
> **Repo Anchor**: Branch \`$BRANCH\` | SHA \`$SHA\`
> **Runtime Status**: **$RUNTIME**
> **Trinity Score**: **$TRINITY**
> **Debt Status**: Ruff: Frozen=$RUFF_DEBT | Pyright(strict): Baseline=$PYRIGHT_DEBT
EOF
