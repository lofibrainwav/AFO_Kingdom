#!/bin/bash
# AFO Kingdom - Korean SSOT Enforcer
# 眞·善·美·孝·永

TARGET_FILES=(
  "scripts/dspy_mipro_training_gate.py"
  "scripts/dspy_promote_graphrag_gold.py"
  "scripts/dspy_daily_graphrag_harvest.py"
)

HEADER="# Language: ko-KR (AFO SSOT)"

for file in "${TARGET_FILES[@]}"; do
  if [ -f "$file" ]; then
    if ! grep -q "$HEADER" "$file"; then
      echo "🇰🇷 Applying Korean SSOT Header to $file..."
      # Insert header after imports or shebang (simplified: prepend to file, but safely)
      # For python scripts, we can put it as a comment at the top
      temp_file=$(mktemp)
      echo "$HEADER" > "$temp_file"
      cat "$file" >> "$temp_file"
      mv "$temp_file" "$file"
      chmod +x "$file"
    else
      echo "✅ $file already has SSOT Header."
    fi
  else
    echo "⚠️ $file not found!"
  fi
done

echo "📜 Korean SSOT Enforcement Complete."
