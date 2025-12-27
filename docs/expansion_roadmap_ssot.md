# AFO Expansion Roadmap SSOT (Stage 1~4)

**As-of**: 2025-12-27 (PST)  
**Owner**: Jay (Commander) / Chancellor (Assistant)  
**Decision Mode**: AUTO_RUN if Trinity≥0.90 & Risk≤0.10, else ASK  
**Core Rule**: Backup → Check → Execute → Verify

---

## North Star (1줄)
"형님의 가시성(孝)을 항상 지키면서, 진실(眞)·안전(善)·미학(美)·영속(永)을 단계적으로 확장한다."

## Hard Guardrails (절대 금지)
- **추측 금지**: 로그/명령/파일로 확인 전 단정 금지
- **범위 폭발 금지**: 한 Stage 안에서 신규 축(아키텍처 대수술) 추가 금지
- **실험 증거 없는 merge 금지**: 실험 문서 + 증거 경로 없으면 완료 인정 불가
- **롤백 없는 변경 금지**: 실패 시 되돌리는 명령(또는 태그) 반드시 포함

---

## Stage Map (1페이지 요약)

### Stage 1 — "가시성/거버넌스 검증"
**Goal**: "눈에 보이는 건강 + 핵심 정책이 실제로 작동"  
**Deliverables**
- SSOT 1p + EXP 문서 1개(최소)  
- Health Sweep 증거(텍스트) + 대시보드 시각 검증 스크린/로그
**Success**
- 핵심 서비스 health 200 / restart_count=0 / 주요 페이지 동작
- 거버넌스(Trinity/Decision) 표시가 UI/API에서 일치

### Stage 2 — "Royal Governance 기능 실험 확장"
**Goal**: 실제 기능(정책/판단/기록)이 **실사용 루프**로 들어감  
**Deliverables**
- EXP 2~3개: (예) Chancellor/Decision 기록, SSE 스트림, 권한/가드레일  
- 실패/경고 케이스 재현 + 기대 동작(TRY_AGAIN/ASK 포함) 검증
**Success**
- "정상/경고/부분 실패" 케이스에서 시스템이 **안전하게** 동작
- 재현 가능한 시나리오(입력→출력→증거) 확보

### Stage 3 — "모니터링/알람 실배치"
**Goal**: 장애를 "나중에 발견"이 아니라 "바로 감지"  
**Deliverables**
- 알람 3종 이상(최소): RestartCount, Health HTTP, Error Keyword
- 알람 트리거 테스트(의도적 실패) + 복구 절차 문서
**Success**
- 알람이 실제로 울리고, 대응 Runbook으로 5분 내 정상화 가능

### Stage 4 — "정화(Tidying) + 점진 이관(Strangler Fig)"
**Goal**: 레거시/부채를 **안전하게** 줄이면서 확장성 확보  
**Deliverables**
- Tidying 리스트(주간) + Strangler Facade/Compat 계획(월간)
- 변경 전/후 품질지표(테스트/타입/린트) 증거
**Success**
- 변경은 작게, 효과는 누적(리그레션 0, 경고 감소 추세 유지)

---

## Decision Record (이번 사이클)
- **Current**: Stage 2 진행 중 (EXP_002 완료, EXP_003/004 준비)
- **Next Action (1줄)**: EXP_003 SSE 스트림 + Chancellor 기록 검증 실행
- **Evidence Paths**:
  - docs/experiments/EXP_001_royal_governance_verification.md
  - docs/experiments/EXP_002_ui_api_consistency_verification.md (추가 예정)
  - artifacts/health/20251227_120819/health_sweep.txt
  - artifacts/experiments/001/...
  - artifacts/experiments/002/...
- **Rollback**: git checkout -- packages/dashboard/src/components/genui/RoyalOpsCenter.tsx
- 2025-12-27: EXP_001 Decision=Ship Evidence=artifacts/experiments/001/
- 2025-12-27: EXP_002 Decision=Ship Evidence=artifacts/experiments/002/ (API/UI 일치성 PASS)
## Decision Record
- [2025-12-27 (PST)] Stage 2 CLOSE: EXP_001 PASS, EXP_002 PASS, EXP_003 FAIL(SSE silent), EXP_004 PASS(auth guard restored). Stage 3 OPEN: Monitoring/Alarms (EXP_005).
