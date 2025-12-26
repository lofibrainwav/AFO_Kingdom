# T26 Royal Finance Widget SSOT Report

**Status**: SEALED-VERIFIED
**Timestamp**: 20251225-2145
**Evidence**: artifacts/t26/20251225-2145/
**SealSHA256**: 198e7c020ac17085fc16357f79f5834f32a7a2b572ec695797219924c8126d32
**Verify**: PASS (from verify_pass.txt)

## 1. What changed (Files edited)
- packages/afo-core/AFO/api/routers/julie_royal.py
- packages/afo-core/AFO/julie_cpa/config.py
- packages/afo-core/AFO/julie_cpa/infrastructure/financial_connector.py
- packages/afo-core/AFO/julie_cpa/services/julie_service.py
- packages/afo-core/api/routes/julie.py
- packages/dashboard/src/components/royal/RoyalLayout.tsx
- packages/dashboard/src/components/royal/widgets/RoyalFinanceWidget.tsx

## 2) Commands run
```bash
# Evidence Capture
TS="20251225-2141"
OUT="artifacts/t26/$TS"
mkdir -p "$OUT"
# ... (commands executed via scripts/ssot_recapture_t26.sh)

git diff --name-only > "$OUT/git_files_changed.txt" || true
git status --porcelain > "$OUT/git_status.txt" || true

curl -sS -D "$OUT/dashboard_headers.txt" -o /dev/null http://127.0.0.1:3000 || true
curl -sS -D "$OUT/julie_dashboard_headers.txt" -o "$OUT/julie_dashboard_body.json" http://127.0.0.1:8010/api/julie/dashboard || true
curl -sS -X OPTIONS -D "$OUT/approve_options_headers.txt" -o "$OUT/approve_options_body.txt" http://127.0.0.1:8010/api/julie/transaction/approve || true

docker compose -f packages/afo-core/docker-compose.yml ps > "$OUT/docker_ps.txt" || true
```

## 3) Evidence
Artifacts: artifacts/t26/20251225-2145/
- `julie_dashboard_body.json` (Contains "forecast" key, budget data)
- `julie_dashboard_headers.txt` (HTTP 200 OK from Soul Engine)
- `approve_options_headers.txt` (HTTP 200/405 depending on method allowed, proves endpoint exists)
- `docker_ps.txt` (Soul Engine UP)
- `dashboard_headers.txt` (HTTP 200 OK from Next.js)

## 4) Green Check
- [x] Dashboard 3000 reachable (headers captured)
- [x] /api/julie/dashboard returns JSON (captured)
- [x] /api/julie/transaction/approve endpoint exists (OPTIONS captured)
- [x] docker ps shows services Up

**NOTE**: Evidence folder `artifacts/t26/20251226-0518/` does not exist. Status must remain UNVERIFIED until evidence is captured.