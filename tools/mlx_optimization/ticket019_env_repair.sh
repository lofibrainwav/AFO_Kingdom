#!/bin/bash
set -euo pipefail

cd /Users/brnestrm/AFO_Kingdom/tools/mlx_optimization
mkdir -p artifacts

{
  echo "=== TICKET-019 MLX ENV REPAIR ==="
  date
  pwd
  python3 -V || true
  echo "git_sha=$(cd /Users/brnestrm/AFO_Kingdom && git rev-parse --short HEAD 2>/dev/null || true)"
  echo

  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate

  python -m pip install -U pip setuptools wheel

  export PIP_DEFAULT_TIMEOUT=600
  python -m pip install -U --prefer-binary --retries 20 --timeout 600 --progress-bar off mlx mlx-lm mlx-vlm

  python - <<'PY'
import mlx, mlx_lm, mlx_vlm
print("mlx", getattr(mlx,"__version__",None))
print("mlx_lm", getattr(mlx_lm,"__version__",None))
print("mlx_vlm", getattr(mlx_vlm,"__version__",None))
PY

  python -m mlx_vlm.generate -h | head -n 80

} 2>&1 | tee artifacts/ticket019_env_repair.log
