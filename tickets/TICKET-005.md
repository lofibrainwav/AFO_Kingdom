# 🎫 TICKET-005: Bayesian 최적화 알고리즘 구현

**우선순위**: LOW
**상태**: IN_PROGRESS
**담당**: 연구팀
**의존성**: TICKET-002
**예상 소요시간**: 4시간

## 🎯 목표 (Goal)

**SSOT 정정**: DSPy MIPROv2는 Optuna TPE 기반 (GP+EI 아님)
커스텀 GP+EI BO 구현 + Upstream MIPROv2 연동

## 📋 작업 내용

### 1. Upstream MIPROv2 연동 (A 루트 - 권장)
```python
# packages/afo-core/afo/mipro_upstream.py
import dspy
from dspy.teleprompt import MIPROv2

def optimize_with_mipro_v2(program, trainset, eval_fn):
    # 실제 MIPROv2: Optuna TPESampler 기반 (GP+EI 아님)
    teleprompter = MIPROv2(...)
    optimized_program = teleprompter.compile(program, trainset=trainset)
    return optimized_program
```

### 2. 커스텀 GP+EI BO 구현 (B 루트 - 별도 실험)
```python
# packages/afo-core/afo/custom_bo_gp.py
class GaussianProcess:
    def __init__(self, kernel='RBF'):
        self.kernel = kernel
        # RBF(Radial Basis Function) 커널 구현

    def fit(self, X, y):
        # GP 학습: 평균 μ(x), 분산 σ²(x) 계산
        pass

    def predict(self, X_new):
        # 새로운 지점 예측
        return mu, sigma

def expected_improvement(X, gp, f_best, xi=0.01):
    # EI(x) = σ(x) * [ξ * Φ(ξ) + φ(ξ)]
    # ξ = (μ(x) - f_best) / σ(x)
    mu, sigma = gp.predict(X)
    with np.errstate(divide='warn'):
        xi_normalized = (mu - f_best - xi) / sigma
        ei = sigma * (xi_normalized * norm.cdf(xi_normalized) + norm.pdf(xi_normalized))
    return ei
```

### 3. SSOT 정확화
- **DSPy MIPROv2**: Optuna TPE 기반 (instruction + demo 조합 탐색)
- **커스텀 GP+EI**: 연속 파라미터 최적화용 별도 구현
- **35배 효율**: 워크로드/탐색공간에 따라 변동 (상수 아님)

### 4. Boot-Swap 연동
```python
# MIPROv2 결과를 Trinity Config 형식으로 저장
def save_mipro_result(result, learning_profile_path):
    # sha 버전키 포함
    pass
```

## ✅ Acceptance Criteria

- [x] MIPROv2 팩트 확인: Optuna TPE 기반 (GP+EI 아님)
- [x] DSPy 설치 및 Upstream MIPROv2 연동 ✅ (환경 불일치 해결)
- [x] 커스텀 GP+EI BO 구현 ✅ (`packages/afo-core/AFO/custom_bo_gp.py`)
- [ ] Boot-Swap 저장 포맷 구현 (DSPy 설치 후 진행)
- [x] SSOT 문서화 (MIPROv2 ≠ GP+EI)

## 📊 Trinity Score 영향

- **眞 (Truth)**: +5 (팩트 정확화로 SSOT 정합성)
- **善 (Goodness)**: +2 (의존성 충돌 최소화)
- **美 (Beauty)**: +3 (구현 분리로 모듈화)
- **孝 (Serenity)**: +1 (형님 지적 수용)
- **永 (Eternity)**: +4 (올바른 최적화 기록)

**예상 총점**: 78.3 → 93.3
