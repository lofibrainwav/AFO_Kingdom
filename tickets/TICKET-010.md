# 🎫 TICKET-010: Optuna TPE + GP+EI 하이브리드 Bayesian 최적화

**우선순위**: HIGH
**상태**: PENDING
**담당**: 승상 + AI팀
**의존성**: TICKET-005, TICKET-009
**예상 소요시간**: 10시간

## 🎯 목표 (Goal)

Optuna TPE(MIPROv2) + 커스텀 GP+EI 하이브리드 전략으로 왕국 AI의 Bayesian 최적화 완성.

## 📋 작업 내용

### 1. TPE + GP+EI 하이브리드 아키텍처 설계
```python
# packages/afo-core/afo/hybrid_bayesian.py
class HybridBayesianOptimizer:
    """TPE + GP+EI 하이브리드 최적화기"""

    def __init__(self, trinity_score=87.3):
        self.tpe_optimizer = MIPROv2(metric=trinity_metric, auto="medium")  # TPE 기반
        self.gp_optimizer = bayesian_optimize  # 커스텀 GP+EI
        self.trinity_score = trinity_score

    def hybrid_optimize(self, program, trainset):
        """2단계 하이브리드 최적화"""
        # Phase 1: MIPROv2(TPE)로 프롬프트 공간 초기 탐색
        tpe_result = self.tpe_optimizer.compile(program, trainset)

        # Phase 2: GP+EI로 파라미터 세부 튜닝
        def objective(params):
            return evaluate_with_params(tpe_result, params)

        optimal_params, score = self.gp_optimizer(objective, bounds)
        return tpe_result.with_params(optimal_params)
```

### 2. Trinity Score 기반 메트릭 통합
```python
# packages/afo-core/afo/trinity_metric_advanced.py
def advanced_trinity_metric(example, prediction, trinity_score=87.3):
    """하이브리드 최적화용 고급 Trinity 메트릭"""

    # 眞: 정확도 기반 (35%)
    truth_score = calculate_structural_accuracy(prediction)

    # 善: 효율성 기반 (35%)
    goodness_score = calculate_resource_efficiency(prediction)

    # 美: 우아함 기반 (20%)
    beauty_score = calculate_aesthetic_quality(prediction)

    # 孝: 안정성 기반 (8%)
    serenity_score = calculate_stability_score(prediction)

    # 永: 지속성 기반 (2%)
    eternity_score = calculate_maintainability(prediction)

    total_score = (truth_score * 0.35 + goodness_score * 0.35 +
                   beauty_score * 0.20 + serenity_score * 0.08 +
                   eternity_score * 0.02)

    return total_score / 100.0
```

### 3. Chancellor Graph 하이브리드 통합
```python
# Chancellor Graph 최적화 적용
from afo.hybrid_bayesian import HybridBayesianOptimizer
from afo.trinity_metric_advanced import advanced_trinity_metric

# Chancellor 프로그램 최적화
chancellor_program = dspy.ChainOfThought("kingdom_query -> decision -> action")

hybrid_optimizer = HybridBayesianOptimizer(trinity_score=95.3)
optimized_chancellor = hybrid_optimizer.hybrid_optimize(
    chancellor_program,
    trainset=kingdom_training_data
)

# Boot-Swap을 통한 안전 배포
boot_swap_deploy(optimized_chancellor, "hybrid_bayesian_v1")
```

### 4. 성능 벤치마킹 및 검증
```python
# 3가지 최적화 방법 비교
methods = {
    "baseline": baseline_chancellor,
    "tpe_only": tpe_optimized_chancellor,
    "gp_only": gp_optimized_chancellor,
    "hybrid": hybrid_optimized_chancellor
}

results = {}
for name, method in methods.items():
    score = evaluate_chancellor_performance(method, test_data)
    results[name] = score
    print(f"{name}: {score:.3f}")

# Trinity Score 기반 증거 봉인
seal_hybrid_results(results, trinity_score=95.3)
```

## ✅ Acceptance Criteria

- [ ] 하이브리드 아키텍처 설계 및 구현 완료
- [ ] 고급 Trinity 메트릭 함수 완성
- [ ] Chancellor Graph 하이브리드 적용 성공
- [ ] 3가지 방법 비교 벤치마크 완료
- [ ] 하이브리드 방법이 최고 성능 달성 (목표: 20%+ 향상)

## 🔒 제약사항

- **LOCKED**: antigravity-seal-2025-12-30 관련 파일 절대 수정 금지
- **안전 우선**: 격리 환경에서 충분히 테스트 후 메인 적용
- **SSOT 유지**: TPE ≠ GP+EI 구분 유지

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| 하이브리드 복잡성 증가 | 중간 | 중간 | 모듈화된 설계로 복잡성 관리 |
| 계산 비용 증가 | 높음 | 중간 | 단계별 최적화 + 캐싱 적용 |
| 메트릭 부정확 | 중간 | 중간 | Trinity Score 전문가 검토 |
| Boot-Swap 실패 | 낮음 | 높음 | 단계별 롤백 계획 수립 |

## 🔄 롤백 계획

1. 하이브리드 적용 해제 → TPE만 사용
2. TPE 적용 해제 → GP+EI만 사용
3. GP+EI 적용 해제 → 기본 Chancellor 복원
4. 성능 메트릭 초기화

## 📊 Trinity Score 영향

- **眞 (Truth)**: +9 (TPE + GP+EI 정확도 상승)
- **善 (Goodness)**: +8 (하이브리드 효율 최적화)
- **美 (Beauty)**: +8 (2단계 최적화의 우아한 조화)
- **孝 (Serenity)**: +7 (완전 자동화로 형님 마찰 최소화)
- **永 (Eternity)**: +9 (지속적 다중 전략 진화)

**예상 총점**: 78.3 → **96.3** (궁극적 자율화 달성)

## 📝 작업 로그

- **시작일**: 2025-12-31 (형님 TPE 메타인지 검증 완료 후)
- **완료일**: 예정
- **실제 소요시간**: 예정

## 🔗 관련 문서

- `docs/OPTUNA_TPE_METACOGNITION.md` - TPE 메타인지 검증 보고서
- `packages/afo-core/afo/hybrid_bayesian.py` - 하이브리드 최적화기
- `packages/afo-core/afo/trinity_metric_advanced.py` - 고급 Trinity 메트릭
- `packages/afo-core/afo/custom_bo_gp.py` - 커스텀 GP+EI 구현
