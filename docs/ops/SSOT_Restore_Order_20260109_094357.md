
# [ORDER] SSOT Restoration Order (AFO Official)

## As-of

* time: 2026-01-09T09:43:57-08:00
* branch: fix/trinity-weights-drift
* sha: f3450831

## Goal

*

## DRY_RUN

```bash
echo "== HEAD =="; git status -sb; git rev-parse --short HEAD
echo "== PORTS =="; lsof -nP -iTCP:8010 -sTCP:LISTEN || true; lsof -nP -iTCP:3000 -sTCP:LISTEN || true
echo "== HTTP =="; curl -sS --max-time 2 -I http://127.0.0.1:8010/health | head -n 5 || true; curl -sS --max-time 2 -I http://127.0.0.1:3000/ | head -n 5 || true
echo "== SSOT_VERIFY (trace) =="; bash -x ssot_verify.sh || true
echo "== PLAYWRIGHT DETECT =="; python3 -c "import importlib.util; print('playwright:', 'OK' if importlib.util.find_spec('playwright') else 'MISSING')" || true
```

## WET (Changes)

* Target:
* Action:

## VERIFY

```bash
bash ssot_verify.sh
python3 system_health_check.py
curl -sS --max-time 2 -I http://127.0.0.1:8010/health | head -n 5
curl -sS --max-time 2 -I http://127.0.0.1:3000/ | head -n 5
./scripts/afo_report_evidence_v1.sh
```
