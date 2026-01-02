#!/bin/bash
set -euo pipefail

echo "🏰 Checking Royal Lock Gates..."

# 1. Git Cleanliness
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Git dirty. Commit changes first."
    exit 1
fi

# 2. Branch & Sync
branch="$(git rev-parse --abbrev-ref HEAD)"
local_sha="$(git rev-parse HEAD)"
# Fetch to ensure we have latest remote info
git fetch origin "$branch" >/dev/null 2>&1 || true
remote_sha="$(git ls-remote origin "refs/heads/$branch" | awk '{print $1}')"

echo "Branch: $branch"
echo "Local : $local_sha"
echo "Remote: $remote_sha"

if [ "$local_sha" != "$remote_sha" ]; then
    echo "❌ Local/Remote mismatch. Push or pull required."
    exit 1
fi

# 3. Dependency Sync
echo "🔧 Syncing dependencies..."
uv sync --frozen >/dev/null

# 4. Namespace Purity
echo "🐍 Checking Namespace..."
env -u PYTHONPATH uv run python -c "import importlib.util as u; assert u.find_spec('AFO') is not None; assert u.find_spec('afo') is None"

# 5. Linting (Ruff)
echo "🧹 Running Ruff..."
uv run ruff check packages/afo-core --force-exclude
uv run ruff format packages/afo-core --check --force-exclude

# 6. Type Checking (Pyright)
echo "🔍 Running Pyright..."
uv run pyright

# 7. Testing
echo "🧪 Running Pytest..."
uv run pytest -q

echo "✅ ROYAL LOCK PROOF PACK: ALL GREEN"
