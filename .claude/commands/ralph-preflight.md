---
description: "랄프 루프 사전 점검 - 30초 안전 체크리스트"
allowed-tools: Bash(git:*), Bash(make:*), Read
---

# Ralph Loop Preflight Check

랄프 루프 실행 전 필수 안전 점검입니다.

## 30초 안전 체크리스트 실행

다음 명령을 순서대로 실행하여 안전 상태를 확인합니다:

```bash
echo "=== Ralph Preflight Check ==="
echo ""

# 1. Git 상태 확인
echo "1. Git Status:"
git status --short
echo ""

# 2. 현재 브랜치 확인
echo "2. Current Branch:"
git branch --show-current
echo ""

# 3. 미커밋 변경 확인
DIRTY=$(git status --porcelain | wc -l | tr -d ' ')
if [ "$DIRTY" -gt 0 ]; then
  echo "   WARNING: $DIRTY uncommitted changes detected!"
  echo "   → Commit or stash before Ralph Loop"
else
  echo "   OK: Working directory clean"
fi
echo ""

# 4. Pyright 기준선 확인
echo "3. Pyright Baseline:"
if [ -f "artifacts/ci/pyright_baseline.txt" ]; then
  head -1 artifacts/ci/pyright_baseline.txt
else
  echo "   WARNING: No baseline file found"
fi
echo ""

# 5. 최근 테스트 상태
echo "4. Last Test Status:"
if [ -f "artifacts/ci/pytest_report.txt" ]; then
  tail -3 artifacts/ci/pytest_report.txt
else
  echo "   No recent test report"
fi
echo ""

echo "=== Preflight Complete ==="
```

## 체크리스트 결과 해석

| 항목 | 상태 | 조치 |
|------|------|------|
| Git Clean | 필수 | 더러우면 `git stash` 또는 커밋 |
| 격리 브랜치 | 권장 | `git checkout -b fix/ralph-...` |
| Pyright 기준선 | 필수 | 442 이하 확인 |
| 테스트 상태 | 참고 | 현재 실패 테스트 파악 |

## 브랜치 생성 (선택)

격리 브랜치가 필요하면:

```bash
git checkout -b fix/ralph-$(date +%Y%m%d_%H%M%S)
git commit --allow-empty -m "RALPH_CHECKPOINT: 시작점"
```

## 다음 단계

- **ALL OK** → `/ralph [작업내용]` 실행
- **WARNING** → 문제 해결 후 다시 점검
- **FAIL** → Ralph Loop 사용 불가
