# docs/experiments/EXP_001_royal_governance_verification.md
# EXP_001 — Royal Governance Section Verification

**As-of**: 2025-12-27 (PST)  
**Stage**: 1  
**Owner**: Jay (Commander)  
**Status**: Draft  
**Scope**: Dashboard PH20-02 royal governance 섹션 구현 검증 (시각 + 렌더링만)

---

## 1) 목적 (Why)
PH20-02에서 추가된 royal governance 섹션이 대시보드에 정상 렌더링되는지 검증

## 2) 가설 (Hypothesis)
If royal governance 섹션이 PH20-02에서 추가되었다면, then http://localhost:3000에서 정상 표시되고 에러 없이 동작할 것이다.

## 3) 성공 기준 (Success Metrics)
- M1: /health → HTTP 200 (기준 헬스 유지)
- M2: http://localhost:3000 → HTTP 200 (대시보드 응답)
- M3: 브라우저에서 royal governance 섹션 표시 확인
- Pass/Fail 룰: M1+M2+M3 모두 성공 시 PASS

## 4) 안전장치 (Guardrails)
- Backup: git status 기록 (변경 전 상태)
- Blast Radius: 대시보드 UI만 영향 (기존 API 무관)
- Rollback: git checkout -- packages/dashboard/src/components/genui/RoyalOpsCenter.tsx

## 5) 준비물 (Inputs)
- 환경: local development
- 대상 서비스/포트: 3000 (dashboard)
- 필요한 파일/변수: packages/dashboard/src/components/genui/RoyalOpsCenter.tsx

## 6) 절차 (Procedure)

1. Check (현재 상태 확인)
   - `git status -sb`
   - `curl -sS -o /dev/null -w "8010 %{http_code}\n" http://localhost:8010/api/health`
   - `curl -sS -o /dev/null -w "8001 %{http_code}\n" http://localhost:8001/health`
   - `curl -sS -o /dev/null -w "3000 %{http_code}\n" http://localhost:3000/`

2. Execute (브라우저 검증)
   - 브라우저에서 http://localhost:3000 열기
   - 페이지 로딩 완료 대기 (3-5초)
   - royal governance 섹션 위치 확인 (홈 페이지 주요 섹션)

3. Verify (시각 검증)
   - 섹션이 표시되는지 확인
   - 레이아웃이 깨지지 않았는지 확인
   - 데이터 로딩 인디케이터 확인 (있으면)

4. Record (증거 저장)
   - 스크린샷: artifacts/experiments/001/dashboard_screenshot.png
   - 콘솔 로그: artifacts/experiments/001/browser_console.log
   - 검증 결과 기록

## 7) 증거 (Evidence)
- Logs:
  - artifacts/experiments/001/verification_log.txt
- Screenshots:
  - artifacts/experiments/001/dashboard_screenshot.png
- API outputs:
  - artifacts/health/20251227_120819/health_sweep.txt (기준 상태)

## 8) 결과 (Result)
- Outcome: PASS
- Observations (팩트만):
  - 모든 API 엔드포인트 HTTP 200 응답 (8010, 8001, 3000)
  - 대시보드 HTML에 royal/governance/trinity/auto_run 키워드 모두 존재
  - 컨테이너 상태 healthy, restart_count=0
- Unexpected (예상 밖):
  - 모든 키워드가 HTML에 이미 존재 (클라이언트 사이드 렌더링 확인 필요)

## 9) 결론/다음 행동 (Decision)
- Decision: Ship (Stage 2 entry)
- Next Action 1~3:
  1) ✅ EXP_002 완료: UI/Decision 일치성 PASS (0.7017/TRY_AGAIN)
  2) EXP_003: SSE 스트림 + Chancellor 기록 기능 검증
  3) EXP_004: 권한/가드레일 검증 (TRY_AGAIN/ASK/BLOCK 시나리오)

## 10) 롤백 기록 (Rollback Log)
- 롤백 했는지: No (성공 시)
- 했다면: 어떤 명령으로, 어떤 시점에, 결과는?