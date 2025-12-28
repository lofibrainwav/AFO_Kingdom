#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="$ROOT_DIR/artifacts/ph19_security/$TS"
mkdir -p "$OUT_DIR"

PIPAUDIT_RC=0
GITLEAKS_RC=0
BANDIT_RC=0

{
  echo "timestamp=$TS"
  echo "pwd=$ROOT_DIR"
  echo "python=$(python3 --version 2>&1 || true)"
  echo "git=$(git --version 2>&1 || true)"
  echo "gitleaks=$(command -v gitleaks >/dev/null 2>&1 && gitleaks version 2>&1 || echo 'MISSING')"
  echo "bandit=$(python3 -c 'import bandit; print(bandit.__version__)' 2>/dev/null || echo 'MISSING')"
  echo "pip_audit=$(python3 -c 'import pip_audit; print(pip_audit.__version__)' 2>/dev/null || echo 'MISSING')"
} > "$OUT_DIR/tool_versions.txt"

echo "[PH19] output: $OUT_DIR"

run_cmd() {
  local name="$1"; shift
  set +e
  "$@" >"$OUT_DIR/${name}.stdout.txt" 2>"$OUT_DIR/${name}.stderr.txt"
  local rc=$?
  set -e
  echo "$rc" > "$OUT_DIR/${name}.rc.txt"
  return 0
}

echo "[1/3] pip-audit (deps vulnerabilities)"
if python3 -c "import pip_audit" >/dev/null 2>&1; then
  set +e
  TMP_PIPAUDIT="$(mktemp)"
  python3 -m pip_audit --format=json --progress-spinner=off . \
    1>"$TMP_PIPAUDIT" \
    2>"$OUT_DIR/pip_audit.stderr.txt"
  PIPAUDIT_RC=$?

  # Atomic Write & Validation (Enhanced)
  if [ $PIPAUDIT_RC -eq 0 ]; then
    if python3 -c "import json,sys; json.load(open(sys.argv[1],'r',encoding='utf-8'))" "$TMP_PIPAUDIT" >/dev/null 2>&1; then
      # Extra validation: check for shell script contamination
      if grep -q 'EOF && echo\|heredoc\|#!/.*bash\|#!/.*sh' "$TMP_PIPAUDIT" 2>/dev/null; then
        echo "Pip-audit output contaminated (shell script detected)" > "$OUT_DIR/pip_audit.stderr.txt"
        PIPAUDIT_RC=98
        echo "$PIPAUDIT_RC" > "$OUT_DIR/pip_audit.rc.txt"
        rm -f "$TMP_PIPAUDIT"
      else
        mv "$TMP_PIPAUDIT" "$OUT_DIR/pip_audit.json"
        echo "$PIPAUDIT_RC" > "$OUT_DIR/pip_audit.rc.txt"
      fi
    else
      echo "Pip-audit output corrupted (invalid JSON)" > "$OUT_DIR/pip_audit.stderr.txt"
      PIPAUDIT_RC=99
      echo "$PIPAUDIT_RC" > "$OUT_DIR/pip_audit.rc.txt"
      rm -f "$TMP_PIPAUDIT"
    fi
  else
    echo "$PIPAUDIT_RC" > "$OUT_DIR/pip_audit.rc.txt"
    rm -f "$TMP_PIPAUDIT"
  fi

  set -e
else
  PIPAUDIT_RC=127
  echo "$PIPAUDIT_RC" > "$OUT_DIR/pip_audit.rc.txt"
  echo "pip-audit MISSING. Install: python3 -m pip install -U pip-audit" > "$OUT_DIR/pip_audit.stderr.txt"
fi

echo "[2/3] gitleaks (git history secrets)"
if command -v gitleaks >/dev/null 2>&1; then
  set +e
  gitleaks detect \
    --no-banner \
    --no-color \
    --log-level error \
    --report-format json \
    --report-path "$OUT_DIR/gitleaks.json" \
    --config "$ROOT_DIR/gitleaks.toml" \
    --redact \
    .
  GITLEAKS_RC=$?
  set -e
  echo "$GITLEAKS_RC" > "$OUT_DIR/gitleaks.rc.txt"
else
  GITLEAKS_RC=127
  echo "$GITLEAKS_RC" > "$OUT_DIR/gitleaks.rc.txt"
  echo "gitleaks MISSING. Install (macOS): brew install gitleaks" > "$OUT_DIR/gitleaks.stderr.txt"
fi

echo "[3/3] bandit (static security)"
if python3 -c "import bandit" >/dev/null 2>&1; then
  set +e
  TMP_BANDIT="$(mktemp)"
  python3 -m bandit \
    -c pyproject.toml \
    -r . \
    --severity-level medium \
    --confidence-level medium \
    -f json \
    -o "$TMP_BANDIT"
  BANDIT_RC=$?
  
  # Atomic Write & Validation (Enhanced)
  if [ $BANDIT_RC -eq 0 ]; then
    if python3 -c "import json,sys; json.load(open(sys.argv[1],'r',encoding='utf-8'))" "$TMP_BANDIT" >/dev/null 2>&1; then
      # Extra validation: check for shell script contamination
      if grep -q 'EOF && echo\|heredoc\|#!/.*bash\|#!/.*sh' "$TMP_BANDIT" 2>/dev/null; then
        echo "Bandit output contaminated (shell script detected)" > "$OUT_DIR/bandit.stderr.txt"
        BANDIT_RC=98
        echo "$BANDIT_RC" > "$OUT_DIR/bandit.rc.txt"
        rm -f "$TMP_BANDIT"
      else
        mv "$TMP_BANDIT" "$OUT_DIR/bandit.json"
        echo "$BANDIT_RC" > "$OUT_DIR/bandit.rc.txt"
      fi
    else
      echo "Bandit output corrupted (invalid JSON)" > "$OUT_DIR/bandit.stderr.txt"
      BANDIT_RC=99
      echo "$OUT_DIR/bandit.rc.txt"
      rm -f "$TMP_BANDIT"
    fi
  else
    echo "$BANDIT_RC" > "$OUT_DIR/bandit.rc.txt"
    rm -f "$TMP_BANDIT"
  fi
  rm -f "$TMP_BANDIT"
  set -e
else
  BANDIT_RC=127
  echo "$BANDIT_RC" > "$OUT_DIR/bandit.rc.txt"
  echo "bandit MISSING. Install: python3 -m pip install -U 'bandit[toml]'" > "$OUT_DIR/bandit.stderr.txt"
fi

python3 - <<'PY'
import json
from pathlib import Path

# We know script wrote OUT_DIR; infer from argv? We'll locate latest via rc files:
root = Path.cwd() / "artifacts" / "ph19_security"
latest = sorted([p for p in root.glob("*") if p.is_dir()])[-1]
def safe_json_count(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        # common patterns
        if "results" in data and isinstance(data["results"], list):
            return len(data["results"])
        if "findings" in data and isinstance(data["findings"], list):
            return len(data["findings"])
        # pip-audit format
        if "dependencies" in data and isinstance(data["dependencies"], list):
            vulns = 0
            for dep in data["dependencies"]:
                if "vulns" in dep:
                    vulns += len(dep["vulns"])
            return vulns
    return None

pip_cnt = safe_json_count(latest / "pip_audit.json")
git_cnt = safe_json_count(latest / "gitleaks.json")
ban_cnt = safe_json_count(latest / "bandit.json")

summary = []
summary.append(f"# PH19 Security Sweep Summary ({latest.name})")
summary.append("")
summary.append(f"- pip-audit: vulnerabilities={pip_cnt if pip_cnt is not None else 'n/a'} rc={(latest/'pip_audit.rc.txt').read_text().strip()}")
summary.append(f"- gitleaks: findings={git_cnt if git_cnt is not None else 'n/a'} rc={(latest/'gitleaks.rc.txt').read_text().strip()}")
summary.append(f"- bandit: findings={ban_cnt if ban_cnt is not None else 'n/a'} rc={(latest/'bandit.rc.txt').read_text().strip()}")
summary.append("")
summary.append("## Gate rule")
summary.append("- PASS = all rc == 0")
summary.append("- FAIL = any rc != 0 (including missing tools)")
(latest / "summary.md").write_text("\n".join(summary), encoding="utf-8")
PY

echo ""
echo "== SUMMARY =="
cat "$OUT_DIR/summary.md"
echo ""

if [[ "$PIPAUDIT_RC" -ne 0 || "$GITLEAKS_RC" -ne 0 || "$BANDIT_RC" -ne 0 ]]; then
  echo "[PH19] FAIL (rc: pip-audit=$PIPAUDIT_RC, gitleaks=$GITLEAKS_RC, bandit=$BANDIT_RC)"
  exit 1
fi

echo "[PH19] PASS (all clear)"
