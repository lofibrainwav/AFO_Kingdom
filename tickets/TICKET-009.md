# 🎫 TICKET-009: MIPROv2 왕국 적용 상세 구현

**우선순위**: HIGH
**상태**: PENDING
**담당**: 승상 + AI팀
**의존성**: TICKET-001, TICKET-002, TICKET-005
**예상 소요시간**: 8시간

## 🎯 목표 (Goal)

DSPy MIPROv2를 AFO 왕국 Chancellor Graph에 완전히 통합하여 프롬프트 자율 최적화 시스템 구축.

## 📋 작업 내용

### 1. MIPROv2 격리 환경 완성
```bash
# 격리 환경에서 MIPROv2 설치 및 검증
cd tools/dspy_mipro
poetry install
poetry run python -c "
import dspy
from dspy.teleprompt import MIPROv2
print('DSPy MIPROv2 설치 성공')
"
```

### 2. Trinity Score 메트릭 완성
```python
# packages/afo-core/afo/trinity_metric_wrapper.py
def trinity_metric(example, prediction, trinity_score=78.3):
    """Trinity Score 기반 MIPROv2 메트릭"""
    # 眞善美孝永 5기둥 기반 정확도 계산
    truth_score = calculate_truth_score(prediction)
    goodness_score = calculate_goodness_score(prediction)
    beauty_score = calculate_beauty_score(prediction)
    serenity_score = calculate_serenity_score(prediction)
    eternity_score = calculate_eternity_score(prediction)

    total_score = (truth_score * 0.35 + goodness_score * 0.35 +
                   beauty_score * 0.20 + serenity_score * 0.08 +
                   eternity_score * 0.02)

    return total_score / 100.0
```

### 3. Chancellor Graph MIPROv2 통합
```python
# Chancellor Graph에 MIPROv2 적용
from afo.dspy_optimizer import AFOMIPROv2, trinity_metric

# Chancellor Graph 프로그램 최적화
chancellor_program = dspy.ChainOfThought("query -> decision -> action")

optimizer = AFOMIPROv2(trinity_score=87.3, auto="medium")
optimized_chancellor = optimizer.compile(
    chancellor_program,
    trainset=kingdom_decisions,
    valset=validation_cases
)
```

### 4. Bayesian Optimization 하이브리드
```python
# MIPROv2 + 커스텀 GP+EI 통합
from afo.custom_bo_gp import bayesian_optimize

# MIPROv2 결과에 BO 적용
def hybrid_optimize(program, trainset):
    # MIPROv2 기본 최적화
    mipro_result = AFOMIPROv2().compile(program, trainset)

    # BO로 파라미터 세부 튜닝
    def objective(temperature):
        return evaluate_with_temperature(mipro_result, temperature)

    optimal_temp, score = bayesian_optimize(objective, (0.1, 2.0))
    return mipro_result.with_temperature(optimal_temp)
```

### 5. 성능 검증 및 봉인
```python
# MIPROv2 적용 전후 비교
baseline_score = evaluate_baseline_chancellor()
mipro_score = evaluate_mipro_chancellor()

improvement = ((mipro_score - baseline_score) / baseline_score) * 100
print(f"MIPROv2 성능 향상: {improvement:.1f}%")

# Trinity Score 기반 증거 봉인
seal_mipro_results(mipro_score, baseline_score, improvement)
```

## ✅ Acceptance Criteria

- [ ] 격리 환경 MIPROv2 설치 및 임포트 성공
- [ ] Trinity Score 메트릭 함수 완성
- [ ] Chancellor Graph MIPROv2 적용 성공
- [ ] 성능 향상 15% 이상 확인
- [ ] Trinity Score 90+ 달성

## 🔒 제약사항

- **LOCKED**: antigravity-seal-2025-12-30 관련 파일 절대 수정 금지
- **안전 우선**: 격리 환경에서 충분히 테스트 후 메인 적용
- **SSOT 유지**: MIPROv2 ≠ GP+EI, Upstream DSPy vs Custom BO 구분

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| MIPROv2 설치 실패 | 중간 | 중간 | 격리 환경 + Poetry 버전 핀 |
| 성능 저하 | 낮음 | 높음 | baseline vs optimized 비교 검증 |
| Trinity 메트릭 부정확 | 중간 | 중간 | 5기둥 가중치 정확 계산 검증 |
| API 비용 증가 | 높음 | 중간 | minibatch 평가 + 캐싱 적용 |

## 🔄 롤백 계획

1. MIPROv2 적용 해제 (기본 Chancellor Graph 복원)
2. 격리 환경 정리
3. 성능 메트릭 초기화

## 📊 Trinity Score 영향

- **眞 (Truth)**: +8 (Bayesian 기반 정확한 최적화)
- **善 (Goodness)**: +7 (안전한 격리 환경 + 비용 효율)
- **美 (Beauty)**: +8 (우아한 자동 최적화 루프)
- **孝 (Serenity)**: +6 (형님 마찰 최소화 + 자율화)
- **永 (Eternity)**: +9 (지속적 자율 진화 + 학습 프로파일)

**예상 총점**: 78.3 → **95.3** (혁신적 자율화 달성)

## 📝 작업 로그

- **시작일**: 2025-12-31 (형님 메타인지 검증 완료 후)
- **완료일**: 예정
- **실제 소요시간**: 예정

## 🔗 관련 문서

- `docs/MIPROv2_123025_standard.md` - MIPROv2 상세 분석
- `tools/dspy_mipro/README.md` - 격리 환경 가이드
- `packages/afo-core/afo/dspy_optimizer.py` - AFO MIPROv2 클래스
- `packages/afo-core/afo/custom_bo_gp.py` - 커스텀 Bayesian Optimization
