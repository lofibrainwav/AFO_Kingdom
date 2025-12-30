# PH-OPS-01 — Daily Roll Call (SSOT)

Single entry:
- `bash scripts/ops/daily_roll_call.sh`

Optional full gate:
- `RUN_CI_LOCK=1 bash scripts/ops/daily_roll_call.sh`

Env overrides (if ports differ):
- `AFO_BASE_URL` (default `http://127.0.0.1:8010`)
- `WALLET_URL`   (default `http://127.0.0.1:8011`)
- `GRAFANA_URL`  (default `http://127.0.0.1:3000`)
