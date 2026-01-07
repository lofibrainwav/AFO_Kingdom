---
description: "DRY_RUN 모드 - 병자궤도야 (모의전)"
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git status:*)
---

# DRY_RUN 모드 (병자궤도야)

손자병법 제3선 "병자궤도야" - 위험한 작업은 반드시 모의전으로 결과를 미리 봅니다.

## $ARGUMENTS

이 작업을 DRY_RUN 모드로 분석합니다.

## DRY_RUN 체크리스트

1. **영향 범위 분석**:
   - 변경될 파일 목록
   - 의존하는 모듈/함수
   - 테스트 커버리지

2. **Risk 평가**:
   - Auth/Payment/Secrets 관련? (+60)
   - DB/데이터 변경? (+40)
   - 의존성 변경? (+30)
   - 테스트 없는 핵심 로직? (+25)

3. **예상 결과**:
   - 성공 시 상태
   - 실패 시 롤백 방법
   - 부작용 가능성

4. **필요한 검증**:
   - [ ] Pyright 통과
   - [ ] Ruff 통과
   - [ ] pytest 통과
   - [ ] 수동 테스트

## DRY_RUN 결과 형식

```yaml
dry_run_result:
  task: "$ARGUMENTS"
  mode: "DRY_RUN"

  impact_analysis:
    files_to_change: [목록]
    dependencies: [목록]
    test_coverage: [%]

  risk_assessment:
    score: [0-100]
    factors:
      - [요인1]: +[점수]
      - [요인2]: +[점수]

  expected_outcome:
    success: "[설명]"
    failure: "[롤백 방법]"
    side_effects: "[부작용]"

  verification_needed:
    - [게이트1]
    - [게이트2]

  recommendation: [PROCEED | CAUTION | ABORT]
```

## 다음 단계

- **PROCEED**: WET(실행) 모드로 전환 가능
- **CAUTION**: 추가 검토 후 진행
- **ABORT**: 작업 중단, 재설계 필요
