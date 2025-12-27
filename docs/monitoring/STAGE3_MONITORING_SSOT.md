# STAGE 3 — Monitoring & Alerting SSOT (1 page)

As-of: 2025-12-27 (PST)

Stage 2 Close:
- EXP_001 PASS, EXP_002 PASS, EXP_003 FAIL(SSE silent), EXP_004 PASS(auth guard restored)

Goal:
- 사람이 느끼기 전에 시스템이 먼저 감지/기록/알림한다.

Scope (must monitor):
- HTTP: 8010(/api/health), 8001(/health), 3000(/)
- Security: /api/revalidate/status unauth must NOT be 200 (must be 401/503)
- Containers: restart_count changes
- SSE: endpoints exist but silent (bytes=0 within 10s) => regression signal

Hard Guardrails:
- Stage 3 Ship 조건: "알람이 실제로 울린 증거" 없으면 Ship 금지
- 보안 회귀(unauth 200) 감지 실패는 즉시 VETO

Signals (evidence-first):
- Availability: HTTP 200 유지
- Stability: restart_count 증가 감지
- Security: 보호 엔드포인트 unauth 거부(401/503)
- Stream: SSE 10초 bytes=0이면 silent로 기록

Success Criteria:
- EXP_005에서 최소 3종 신호(HTTP/Restart/Security/SSE) 중 3개 이상을 "강제 테스트"로 검증
- Time-to-detect < 60s
- false positive 0
