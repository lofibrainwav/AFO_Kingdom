# STAGE 4 — Deployment & Expansion SSOT (1 page)

As-of: 2025-12-27 (PST)

Stage 3 Close:
- EXP_005 PASS: SSE/HTTP/Security 3종 알람 검증 완료

Goal:
- 로컬 성공을 "재현 가능한 배포"로 고정한다.
- 실패해도 5분 안에 롤백 가능한 상태를 만든다.

Scope:
- Build/Run 재현성 (Docker/Compose 또는 표준 런커맨드)
- 환경변수/시크릿 운영 규칙 고정
- 클린 스타트 스모크 테스트 증거화
- 롤백 실험(강제 실패 → 복구) 증거화

Hard Guardrails:
- Backup → Check → Execute → Verify
- Rollback 경로 없는 변경 금지
- 시크릿은 로그/아티팩트/깃에 남기지 않는다
- "HTTP 200 OK만"으로 배포 성공 판정 금지 (보안 401도 함께 확인)

Success Criteria:
- EXP_006 PASS: (8010/8001/3000) HTTP 200 + (revalidate unauth) 401/503 + 컨테이너 restart_count 안정
- EXP_007 PASS: 실패 유발 후 롤백 성공(동일 체크 통과) 증거 확보

---

## Decision Record — EXP_007 Rollback Drill (As-of: 2025-12-27T13:12:05-08:00)

- Verdict: PASS
- Baseline (guard OK): unauth=401 / wrong=401 / auth=200
- Fault (secret missing, deterministic fail): unauth=503 / wrong=503 / auth=503
- Rollback (guard OK restored): unauth=401 / wrong=401 / auth=200
- Time-to-Rollback (TTR): 45s (target ≤ 300s) ✅
- Evidence: artifacts/experiments/007/<timestamp>/
- Meaning: "배포 실패 → 5분 내 복구"가 증거로 재현 가능하게 고정됨.

---

## Resolution — EXP_006 Reproducibility Issue

- Problem: Environment variable not passed during clean restart
- Solution: Implement env_file in docker-compose.yml for consistent secret injection
- Implementation: Created .env.afo with proper permissions and gitignore
- Next Action: Add env_file directive to docker-compose.yml service configuration
- Expected Outcome: EXP_006 will PASS on retry with consistent secret delivery
