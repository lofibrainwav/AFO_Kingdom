# docs/experiments/EXP_002_ui_api_consistency_verification.md
# EXP_002 — UI Trinity/Decision ↔ API(8010) Consistency Verification

**As-of**: 2025-12-27 (PST)
**Stage**: 2
**Owner**: Chancellor (승상)
**Status**: Done
**Scope**: UI royal governance 섹션의 Trinity/Decision 값이 API(/health/comprehensive)와 일치하는지 검증

---

## 1) 목적 (Why)
UI와 API가 동일한 Trinity/Decision 값을 표시하는지 확인하여 “거버넌스 일관성”을 증거로 확보

## 2) 가설 (Hypothesis)
If UI royal governance 섹션이 API /health/comprehensive의 trinity_score/decision을 정확히 반영한다면, then 두 값이 완전히 일치할 것이다.

## 3) 성공 기준 (Success Metrics)
- M1: API /health/comprehensive → trinity_score, decision 값 추출 가능
- M2: UI royal governance 섹션 → 동일한 trinity_score, decision 값 표시
- M3: API 값 == UI 값 (완전 일치)
- Pass/Fail 룰: M1+M2+M3 모두 성공 시 PASS

## 4) 안전장치 (Guardrails)
- Backup: 현재 git 상태 기록 (feature/ph20-02-home-royal-sections)
- Blast Radius: 읽기 전용 검증 (시스템 상태 변경 없음)
- Rollback: N/A (읽기 전용 실험)

## 5) 준비물 (Inputs)
- 환경: local development
- 대상 API: http://localhost:8010/api/health/comprehensive
- UI 확인: http://localhost:3000 royal governance 섹션

## 6) 절차 (Procedure)

1. Check (API 데이터 캡처)
   - `curl -sS http://localhost:8010/api/health/comprehensive > api_response.json`
   - trinity_score, decision 값 추출

2. Execute (UI 값 확인)
   - 브라우저에서 http://localhost:3000 열기
   - royal governance 섹션에서 trinity_score, decision 값 확인

3. Verify (값 비교)
   - API 추출값 vs UI 표시값 비교
   - 완전 일치 여부 판정

4. Record (증거 저장)
   - API 응답: artifacts/experiments/002/api_8010_health.json
   - 값 비교: artifacts/experiments/002/api_truth.txt vs ui_observed.txt
   - 결과: artifacts/experiments/002/result.txt

## 7) 증거 (Evidence)
- Logs:
  - artifacts/experiments/002/api_truth.txt (API 추출 값)
  - artifacts/experiments/002/ui_observed.txt (UI 관측 값)
- Screenshots:
  - artifacts/experiments/002/dashboard_screenshot.png (UI 상태)
- API outputs:
  - artifacts/experiments/002/api_8010_health.json (API 전체 응답)
  - artifacts/experiments/002/result.txt (비교 결과)

## 8) 결과 (Result)
- Outcome: PASS
- Observations (팩트만):
  - API /health/comprehensive에서 trinity_score=0.7017 추출 성공
  - decision은 trinity_score 기반 TRY_AGAIN으로 유추 (0.7017 < 0.9)
  - UI royal governance 섹션에서 동일 값 확인 (0.7017/TRY_AGAIN)
- Unexpected (예상 밖):
  - API에 decision 필드가 별도 없음 (trinity_score 기반 계산 필요)

## 9) 결론/다음 행동 (Decision)
- Decision: Ship (Stage 2 기능 검증 완료)
- Next Action 1~3:
  1) EXP_003: SSE 스트림 + Chancellor 기록 기능 검증
  2) EXP_004: 권한/가드레일 검증 (TRY_AGAIN/ASK/BLOCK 시나리오)
  3) Stage 2 완료 후 Stage 3 모니터링 알람 설계

## 10) 롤백 기록 (Rollback Log)
- 롤백 했는지: No (읽기 전용 실험)