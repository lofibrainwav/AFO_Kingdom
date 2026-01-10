# 🏰 [ANTIGRAVITY 명령서] SSOT Restoration Order v1.5 (Council-Sealed)

## 0) Council 합의 요약
* **제갈량(眞)**: `integrity_check.py` Crash Loop 차단 (Advanced Root Finder).
* **사마의(善)**: Playwright SSOT 봉인 (Pin + Install + Browsers).
* **주유(美)**: Dashboard (3000) HTTP 200 증거 확보.
* **승상(孝/永)**: `ssot_verify.sh` Dynamic Task Discovery.

## 1) DRY_RUN (증거 채집: 현상 확정)
```bash
echo "== HEAD =="; git status -sb; git rev-parse --short HEAD
echo "== PORTS ==";
lsof -nP -iTCP:8010 -sTCP:LISTEN || true
lsof -nP -iTCP:3000 -sTCP:LISTEN || true

echo "== HTTP (GET 증거) ==";
curl -sS -o /dev/null -w "8010 /health GET => %{http_code}\n" http://127.0.0.1:8010/health || true
curl -sS -o /dev/null -w "3000 / GET => %{http_code}\n" http://127.0.0.1:3000/ || true

echo "== DASHBOARD TITLE (증거) ==";
curl -sS http://127.0.0.1:3000/ | head -n 80 | sed -n 's/.*<title>\(.*\)<\/title>.*/TITLE => \1/p' || true

echo "== SSOT_VERIFY (trace) =="; bash -x ssot_verify.sh || true

echo "== PLAYWRIGHT DETECT ==";
python3 -c "import importlib.util; print('playwright:', 'OK' if importlib.util.find_spec('playwright') else 'MISSING')" || true
```

## 2) WET-1 (眞) Soul Engine Crash Fix
**Target**: `packages/afo-core/AFO/api/routes/integrity_check.py`
**Action**: Replace `parents[4]` with `_find_workspace_root` (git/marker based).

## 3) WET-2 (善) Playwright SSOT Seal
**Target**: `pyproject.toml` & Environment
**Action**:
```bash
# Pin in pyproject.toml
poetry add --group dev "playwright==1.40.0"

# Install & Browsers
if [ -f poetry.lock ]; then
  poetry run python -m playwright install
else
  pip install "playwright==1.40.0" && python3 -m playwright install
fi
```

## 4) WET-3 (永) ssot_verify.sh Restoration
**Target**: `ssot_verify.sh`
**Action**: Replace hardcoded `TASK_MD_PATH` with dynamic python-based finder.
```bash
LATEST_TASK_MD="$(python3 -c '...glob logic...')"
```

## 5) WET-4 (美) Dashboard Restoration
**Target**: `packages/dashboard`
**Action**: `pnpm install && pnpm dev` targeting Port 3000.

## 6) VERIFY (Final Seal: Exit 0 + Endpoint 증거)
```bash
bash ssot_verify.sh
python3 system_health_check.py

curl -sS -o /dev/null -w "VERIFY 8010 /health GET => %{http_code}\n" http://127.0.0.1:8010/health
curl -sS -o /dev/null -w "VERIFY 3000 / GET => %{http_code}\n" http://127.0.0.1:3000/
```
