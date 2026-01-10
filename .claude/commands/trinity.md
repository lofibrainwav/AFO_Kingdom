---
description: "Trinity Score 계산 및 행동 결정"
allowed-tools: Read, Bash(git diff:*), Bash(git status:*)
---

# Trinity Score 계산

$ARGUMENTS 작업에 대한 Trinity Score를 계산합니다.

## 5기둥 평가 (0~100 각각)

### 眞 (Truth) - 35%
- [ ] 구현이 정확한가?
- [ ] 기존 패턴을 따르는가?
- [ ] 타입이 안전한가?

### 善 (Goodness) - 35%
- [ ] 테스트가 있는가?
- [ ] CI가 통과하는가?
- [ ] 부작용이 없는가?

### 美 (Beauty) - 20%
- [ ] 코드가 깔끔한가?
- [ ] 린트를 통과하는가?
- [ ] 중복이 없는가?

### 孝 (Serenity) - 8%
- [ ] UX 영향이 적은가?
- [ ] 에러 메시지가 명확한가?
- [ ] 원샷 실행 가능한가?

### 永 (Eternity) - 2%
- [ ] 문서화되었는가?
- [ ] Evidence가 있는가?
- [ ] 롤백 가능한가?

## 계산 공식

```
total = (眞 * 0.35) + (善 * 0.35) + (美 * 0.20) + (孝 * 0.08) + (永 * 0.02)
```

## 행동 결정

| 조건 | 행동 |
|------|------|
| Trinity >= 90 AND Risk <= 10 | AUTO_RUN |
| 그 외 | ASK_COMMANDER |
| Secrets/Auth/Prod 영향 | BLOCK |

## 출력 형식

```
Trinity Score: [점수]/100
- 眞: [점수] (근거)
- 善: [점수] (근거)
- 美: [점수] (근거)
- 孝: [점수] (근거)
- 永: [점수] (근거)

Risk Score: [점수]/100
Decision: [AUTO_RUN | ASK_COMMANDER | BLOCK]
```
