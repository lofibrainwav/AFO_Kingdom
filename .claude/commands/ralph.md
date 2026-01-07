---
description: "안전 랄프 루프 - 자율 버그 수정 (칠종칠금)"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Ralph Wiggum Loop (안전 버전)

삼국지 제갈량 "칠종칠금" - 반복을 통해 버그를 완전히 제압합니다.

## $ARGUMENTS

위 작업을 안전 랄프 루프 모드로 수행합니다.

---

## 1. 사전 안전 점검 (30초 체크리스트)

실행 전 반드시 확인:

```bash
# 1. Git 상태 확인 (깨끗해야 함)
git status

# 2. 새 브랜치 생성 (격리)
git checkout -b fix/ralph-$(date +%Y%m%d_%H%M%S)

# 3. 체크포인트 커밋 (롤백 지점)
git commit --allow-empty -m "RALPH_CHECKPOINT: 시작점"

# 4. 현재 상태 기록
make check 2>&1 | tee /tmp/ralph_baseline.log
```

---

## 2. 안전장치 6대 확인

| # | 안전장치 | 확인 |
|---|---------|------|
| 1 | 격리 브랜치 | `git branch --show-current` |
| 2 | 체크포인트 커밋 | `git log --oneline -1` |
| 3 | 반복 횟수 제한 | MAX_ITERATIONS=8 (기본값) |
| 4 | 완료 문구 | `<promise>TASK_COMPLETE</promise>` |
| 5 | 종료 조건 | `/check GREEN` 또는 테스트 PASS |
| 6 | Pyright 기준선 | TOTAL_DIAGNOSTICS <= 442 |

---

## 3. 작업 프로토콜

### Phase 1: 문제 분석 (첫 번째 반복)
1. 실패 로그/테스트 재현
2. Root Cause 식별
3. 수정 계획 수립

### Phase 2: 수정 반복 (2-N 반복)
1. 코드 수정
2. `make check` 실행
3. 결과 확인:
   - **PASS** → Phase 3으로
   - **FAIL** → 다시 수정

### Phase 3: 검증 및 종료
1. 전체 테스트 통과 확인
2. Pyright 기준선 확인 (442 이하)
3. `<promise>TASK_COMPLETE</promise>` 출력

---

## 4. 금지 구역 (Ralph Loop 사용 금지)

다음 파일/작업은 Ralph Loop 대상에서 **제외**:

- `config/antigravity.py` - Chancellor 핵심
- `AFO/api_wallet.py` - 지갑/보안
- `AFO/api/auth/` - 인증 관련
- 아키텍처 결정이 필요한 작업
- 모호한 요구사항

---

## 5. 탈출 조건 (Escape Hatches)

다음 상황 발생 시 **즉시 중단**:

```
IF 반복 >= MAX_ITERATIONS (8):
  → 중단, 수동 검토 요청
  → 출력: <promise>BLOCKED: MAX_ITERATIONS</promise>

IF Pyright 기준선 초과 (>442):
  → 롤백: git checkout .
  → 다른 접근 방식 시도
  → 출력: <promise>BLOCKED: PYRIGHT_REGRESSION</promise>

IF 동일 에러 3회 연속:
  → 중단, Root Cause 재분석 필요
  → 출력: <promise>BLOCKED: REPEATED_FAILURE</promise>
```

---

## 6. 결과 보고 형식

작업 완료 시:

```yaml
ralph_result:
  task: "$ARGUMENTS"
  iterations: [실제 반복 횟수]
  status: [COMPLETE | BLOCKED]

  changes:
    files_modified: [파일 목록]
    lines_changed: [+N / -M]

  verification:
    pyright: [PASS/FAIL] (errors: N)
    ruff: [PASS/FAIL]
    pytest: [PASS/FAIL] (passed: N, failed: M)

  rollback_command: "git reset --hard RALPH_CHECKPOINT"
```

---

## 7. 종료 Promise

성공 시:
```
<promise>TASK_COMPLETE</promise>
```

실패/차단 시:
```
<promise>BLOCKED: [사유]</promise>
```

---

## 참고: 롤백 방법

문제 발생 시 즉시 롤백:

```bash
# 체크포인트로 롤백
git reset --hard $(git log --oneline | grep "RALPH_CHECKPOINT" | head -1 | cut -d' ' -f1)

# 또는 브랜치 삭제 후 main으로
git checkout main
git branch -D fix/ralph-*
```
