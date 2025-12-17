# Contributing to AFO Kingdom

## 세종대왕 정신으로 기여하기

> "백성을 위한 실용, 문화 주권, 기존 확장"

---

## 기여 원칙

### 1. 眞 (Truth) - 진실된 코드

- 타입 힌트 필수 (`mypy --strict` 통과)
- Pydantic 모델로 데이터 검증
- 테스트 커버리지 유지

### 2. 善 (Goodness) - 윤리적 기여

- 라이선스 확인 (MIT/Apache 우선)
- 보안 취약점 즉시 보고
- DRY_RUN 모드 지원

### 3. 美 (Beauty) - 우아한 코드

- Ruff 린팅 통과
- 일관된 네이밍 (snake_case)
- 모듈화된 구조

### 4. 孝 (Serenity) - 평온한 협업

- PR 전 로컬 CI 확인
- 친절한 코드 리뷰
- async/await 패턴 활용

### 5. 永 (Eternity) - 지속 가능

- Docstring 작성
- 주석으로 의도 설명
- 변경 이력 기록

---

## PR 체크리스트

```markdown
- [ ] `ruff check .` 통과
- [ ] `mypy AFO/ --strict` 통과
- [ ] `pytest --cov=AFO` 통과
- [ ] Docstring 작성
- [ ] 라이선스 호환성 확인
```

---

## 커밋 메시지 형식

```
<type>(<scope>): <subject>

feat(api): 眞善美 점수 계산 API 추가
fix(security): Trivy 취약점 패치
docs(readme): 설치 가이드 업데이트
```

---

## 문의

- Issues: GitHub Issue 생성
- 보안: SECURITY.md 참고
