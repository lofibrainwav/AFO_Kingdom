# 🎫 TICKET-002: MIPROv2 최적화 모듈 구현

**우선순위**: HIGH
**상태**: IN_PROGRESS
**담당**: AI팀
**의존성**: TICKET-001
**예상 소요시간**: 4시간

## 🎯 목표 (Goal)

DSPy MIPROv2 최적화 모듈을 구현하여 왕국 AI 시스템의 프롬프트 자동 튜닝을 가능하게 한다.

## 📋 작업 내용

### 1. MIPROv2 모듈 생성
```python
# packages/afo-core/afo/dspy_optimizer.py
import dspy
from dspy.teleprompt import MIPROv2

class AFOMIPROv2Optimizer:
    def __init__(self):
        self.lm = dspy.OpenAI(model="gpt-4o-mini")
        dspy.settings.configure(lm=self.lm)

    def optimize_rag(self, rag_module, trainset, valset):
        optimizer = MIPROv2(metric=self.trinity_metric, auto="heavy")
        return optimizer.compile(rag_module, trainset=trainset, valset=valset)
```

### 2. Trinity Score 메트릭 함수 구현
```python
def trinity_metric(self, example, prediction):
    # 5기둥 기반 정확도 평가
    score = self.calculate_trinity_score(prediction)
    return dspy.Prediction(score=score, feedback=self.generate_feedback())
```

### 3. Bayesian 최적화 파라미터 튜닝
- Expected Improvement (EI) 설정
- 탐색 vs 활용 균형 조정
- num_candidates 최적화

### 4. 통합 테스트
- 기본 RAG 모듈 최적화 테스트
- 성능 향상 수치 측정

## ✅ Acceptance Criteria

- [ ] MIPROv2 모듈 구현 완료
- [ ] Trinity Score 메트릭 통합
- [ ] Bayesian 최적화 동작 확인
- [ ] 기본 테스트 통과
- [ ] 성능 향상 10% 이상 확인

## 🔒 제약사항

- **LOCKED**: antigravity-seal-2025-12-30 관련 파일 절대 수정 금지
- **안전 우선**: 기존 AI 파이프라인 영향 최소화

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| 최적화 실패 | 중간 | 중간 | fallback 기본 프롬프트 유지 |
| API 비용 증가 | 높음 | 중간 | rollout 제한 및 캐싱 적용 |
| 성능 저하 | 낮음 | 높음 | 기존 코드와 격리 구현 |

## 🔄 롤백 계획

1. DSPy 모듈 임포트 제거
2. 기존 AI 파이프라인으로 복원
3. 최적화 코드 삭제

## 📊 Trinity Score 영향

- **眞 (Truth)**: +5 (Bayesian 최적화 정확도 향상)
- **善 (Goodness)**: +2 (효율적 자원 사용)
- **美 (Beauty)**: +3 (우아한 최적화 알고리즘)
- **孝 (Serenity)**: +1 (자동화로 형님 마찰 감소)
- **永 (Eternity)**: +4 (지속적 자율 최적화)

**예상 총점**: 78.3 → 87.3

## 📝 작업 로그

- **시작일**: 2025-12-30 (TICKET-001 완료 후)
- **완료일**: 예정
- **실제 소요시간**: 예정

## 🔗 관련 문서

- `docs/DSPY 123025.md` - MIPROv2 상세 분석
- `packages/afo-core/afo/dspy_optimizer.py` - 구현 파일
