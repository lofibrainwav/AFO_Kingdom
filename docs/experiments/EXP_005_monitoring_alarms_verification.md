# EXP_005 — Monitoring/Alarms Verification (Stage 3)

As-of: 2025-12-27 (PST)
Decision: TBD (Ship / Iterate / Kill)

Hypotheses:
- H1: 8010/8001/3000 장애를 60초 내 감지/기록한다.
- H2: restart_count 증가를 60초 내 감지/기록한다.
- H3: 보안 회귀(unauth 200)를 즉시 감지/기록한다.
- H4: SSE 무음(10초 bytes=0)을 감지/기록한다.

Metrics:
- TTD < 60s
- Evidence completeness 100%

Procedure:
1) Baseline evidence 저장
2) Fault injection(통제) 실행 후 변화/감지 증거 저장
3) Pass/Fail 판정 + 다음 행동 기록

Evidence Paths:
- artifacts/experiments/005/<timestamp>/
