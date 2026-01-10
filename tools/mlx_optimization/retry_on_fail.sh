#!/bin/bash
set -euo pipefail

cd /Users/brnestrm/AFO_Kingdom/tools/mlx_optimization

MAX_RETRIES=3
RETRY_COUNT=0
SESSION_BASE="lora_retry"

echo "=== LoRA Training with Auto-Retry ==="
echo "Max retries: $MAX_RETRIES"
echo "Time: $(date)"
echo

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "🔄 Attempt $((RETRY_COUNT + 1))/$MAX_RETRIES"

    SESSION_NAME="${SESSION_BASE}_$RETRY_COUNT"

    # Start training in tmux
    tmux new -d -s "$SESSION_NAME" << TMUX_EOF
cd /Users/brnestrm/AFO_Kingdom/tools/mlx_optimization
source .venv/bin/activate

echo "=== LoRA Training Attempt $((RETRY_COUNT + 1)) ==="
echo "Session: $SESSION_NAME"
echo "Time: \$(date)"

# Create log file with attempt number
LOG_FILE="artifacts/lora_attempt_${RETRY_COUNT}_$(date +%Y%m%d_%H%M%S).log"

# Run training with timeout and error handling
timeout 3600 caffeinate -i python mlx_lora_tuner.py \\
  --model mlx-community/Qwen3-VL-2B-Instruct-4bit \\
  --data sample_training_data.jsonl \\
  --output artifacts/qwen_lora_output_attempt_$RETRY_COUNT \\
  --target qwen \\
  --epochs 1 \\
  2>&1 | tee "\$LOG_FILE"

EXIT_CODE=\${PIPESTATUS[0]}

if [ \$EXIT_CODE -eq 0 ]; then
    echo "✅ Training completed successfully!"
    echo "🎉 SUCCESS: \$LOG_FILE" > artifacts/training_success.flag
    exit 0
else
    echo "❌ Training failed with exit code: \$EXIT_CODE"
    echo "📋 Check log: \$LOG_FILE"
    exit \$EXIT_CODE
fi
TMUX_EOF

    echo "⏳ Waiting for training to complete (timeout: 1 hour)..."
    START_TIME=$(date +%s)

    # Wait for session to finish or timeout
    while tmux has-session -t "$SESSION_NAME" 2>/dev/null; do
        sleep 10
        ELAPSED=$(( $(date +%s) - START_TIME ))

        if [ $ELAPSED -gt 3600 ]; then
            echo "⏰ Timeout reached (1 hour), killing session"
            tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true
            break
        fi

        # Progress indicator
        printf "\r⏳ Elapsed: $((ELAPSED / 60))m $((ELAPSED % 60))s"
    done

    echo

    # Check if training succeeded
    if [ -f "artifacts/training_success.flag" ]; then
        echo "🎉 Training succeeded on attempt $((RETRY_COUNT + 1))!"
        SUCCESS_LOG=$(cat artifacts/training_success.flag)
        echo "📋 Success details: $SUCCESS_LOG"

        # SSOT 기록
        python - <<'PY'
import json, pathlib, datetime

ssot = pathlib.Path("artifacts") / "ticket019_retry_ssot.jsonl"

record = {
    "schema_version": 3,
    "ts": datetime.datetime.utcnow().isoformat() + "Z",
    "mode": "lora_retry_success",
    "attempts": '$RETRY_COUNT' + 1,
    "ok": True,
    "output_dir": f"artifacts/qwen_lora_output_attempt_{'$RETRY_COUNT'}",
    "notes": f"LoRA training succeeded on attempt {('$RETRY_COUNT' + 1)}",
}

with ssot.open("a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"SSOT recorded: {ssot}")
PY

        exit 0
    fi

    echo "❌ Attempt $((RETRY_COUNT + 1)) failed"

    # Clean up failed attempt
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true
    rm -f artifacts/training_success.flag

    RETRY_COUNT=$((RETRY_COUNT + 1))

    if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
        echo "⏰ Waiting 30 seconds before retry..."
        sleep 30
    fi
done

echo "💥 All $MAX_RETRIES attempts failed"

# Final SSOT 기록
python - <<'PY'
import json, pathlib, datetime

ssot = pathlib.Path("artifacts") / "ticket019_retry_ssot.jsonl"

record = {
    "schema_version": 3,
    "ts": datetime.datetime.utcnow().isoformat() + "Z",
    "mode": "lora_retry_failed",
    "attempts": 3,
    "ok": False,
    "notes": "All LoRA training attempts failed",
}

with ssot.open("a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Final SSOT recorded: {ssot}")
PY

echo "📋 Check logs in artifacts/ for failure details"
echo "🔍 Run ./tail_logs.sh to see latest attempt logs"
exit 1
