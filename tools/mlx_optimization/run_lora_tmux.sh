#!/usr/bin/env bash
set -euo pipefail

SESSION="lora"
ROOT="/Users/brnestrm/AFO_Kingdom"
WORKDIR="$ROOT/tools/mlx_optimization"
LOG="$ROOT/artifacts/ticket019_lora_train.log"

mkdir -p "$ROOT/artifacts"

tmux new -d -s "$SESSION" -c "$WORKDIR" "
  source .venv/bin/activate
  caffeinate -i python mlx_lora_tuner.py \
    --model mlx-community/Qwen3-VL-2B-Instruct-4bit \
    --data sample_training_data.jsonl \
    --output $ROOT/artifacts/qwen_lora_output \
    --target qwen \
    --epochs 1 \
    > $LOG 2>&1
"

echo "tmux session started: $SESSION"
echo "log: $LOG"
echo "attach: tmux attach -t $SESSION"
