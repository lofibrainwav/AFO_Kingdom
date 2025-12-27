# EXP_007 — Deploy Rollback Test (Stage 4)

Purpose:
- 배포 실패 시 5분 내 롤백 가능한지 증거로 확인한다.
- “재현 가능한 실패 → 복구” 메커니즘을 검증한다.

Hypotheses:
- H1: 강제 실패 유발 후 5분 내 롤백 성공
- H2: 롤백 후 동일 EXP_006 체크 통과
- H3: 롤백 과정에서 데이터 손실 없음

Metrics:
- Time-to-rollback < 300s
- Post-rollback EXP_006 equivalent check
- No data loss

Evidence Directory:
- artifacts/experiments/007/<timestamp>/
