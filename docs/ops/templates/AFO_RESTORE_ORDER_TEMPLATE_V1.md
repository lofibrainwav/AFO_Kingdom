# [ORDER] <TITLE> (AFO Official)

## As-of
- time:
- branch:
- sha:

## Goal
-

## DRY_RUN
```bash
```

## WET (Changes)

* Target:
* Action:

## VERIFY

```bash
bash ssot_verify.sh
python3 system_health_check.py
curl -sS -I http://127.0.0.1:8010/health | head -n 5
curl -sS -I http://127.0.0.1:3000/ | head -n 5
./scripts/afo_report_evidence_v1.sh
```

