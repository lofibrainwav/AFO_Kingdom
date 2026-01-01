# 🎫 TICKET-001: DSPy 환경 설정 및 의존성 추가

**우선순위**: HIGH
**상태**: IN_PROGRESS
**담당**: 개발팀
**의존성**: 없음
**예상 소요시간**: 2시간

## 🎯 목표 (Goal)

DSPy 3.x 프레임워크를 AFO 왕국 Poetry 환경에 안전하게 추가하고 기본 설정을 완료한다.

## 📋 작업 내용

### 1. Poetry 의존성 추가
```bash
poetry add dspy-ai==3.0.0
```

### 2. pyproject.toml 검증
- Python 버전 호환성 확인 (3.12+)
- 의존성 충돌 검사
- Poetry lock 파일 업데이트

### 3. 기본 임포트 테스트
```python
import dspy
print(f"DSPy 버전: {dspy.__version__}")
```

### 4. 환경 설정
- OpenAI API 키 설정 (선택)
- 기본 LM 설정 (GPT-4o-mini 권장)

## ✅ Acceptance Criteria

- [ ] `poetry add dspy-ai==3.0.0` 성공
- [ ] `poetry install` 완료 (충돌 없음)
- [ ] `import dspy` 성공
- [ ] 기본 설정 완료
- [ ] Trinity Score 영향 없음

## 🔒 제약사항

- **LOCKED**: antigravity-seal-2025-12-30 관련 파일 절대 수정 금지
- **안전 우선**: 기존 기능에 영향 없도록 추가만 수행

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| 의존성 충돌 | 중간 | 높음 | Poetry resolver 확인 후 추가 |
| API 키 누출 | 낮음 | 높음 | 환경변수만 사용 |
| 성능 저하 | 낮음 | 중간 | 기존 코드 영향 최소화 |

## 🔄 롤백 계획

1. `poetry remove dspy-ai`
2. `poetry install`
3. `git checkout HEAD~1` (필요시)

## 📊 Trinity Score 영향

- **眞 (Truth)**: +2 (새로운 프레임워크 정확도 향상)
- **善 (Goodness)**: +1 (안전한 의존성 관리)
- **美 (Beauty)**: +1 (코드 구조 개선)
- **孝 (Serenity)**: 0 (형님 마찰 없음)
- **永 (Eternity)**: +1 (지속적 최적화 기반 구축)

**예상 총점**: 78.3 → 80.3

## 📝 작업 로그

- **시작일**: 2025-12-30
- **완료일**: 예정
- **실제 소요시간**: 예정

## 🔗 관련 문서

- `docs/DSPY 123025.md` - MIPROv2 상세 분석
- `pyproject.toml` - 의존성 설정
- `poetry.lock` - 잠금 파일
