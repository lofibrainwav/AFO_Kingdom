# 🎫 TICKET-012: Transformers v5 고급 기능 활용 및 TorchAO int8 최적화

**우선순위**: HIGH
**상태**: BLOCKED(macOS)
**담당**: 승상 + AI팀
**의존성**: TICKET-011 (DSPy BLOCKED 상태 대안)
**예상 소요시간**: 10시간

## 🎯 목표 (Goal)

DSPy MIPROv2 BLOCKED 상황에서 Transformers v5 고급 기능(TorchAO int8 quantization)을 활용하여 왕국 AI 시스템 저비용 자율 최적화 구현.

## 📋 작업 내용

### 1. Transformers v5 격리 환경 구축
```python
# tools/transformers_v5/pyproject.toml
[tool.poetry]
name = "transformers-v5-isolation"
version = "0.1.0"
description = "Transformers v5 격리 환경"

[tool.poetry.dependencies]
python = "^3.12,<3.14"  # v5 호환성 확보
transformers = "^5.0.0rc1"
torch = "^2.5.0"
torchao = "^0.7.0"
accelerate = "^1.0.0"
```

### 2. TorchAO int8 quantization 구현
```python
# packages/afo-core/afo/torchao_quantization.py
from transformers import AutoModelForCausalLM, TorchAoConfig

def create_int8_quantized_model(model_name: str):
    """TorchAO int8 weight-only quantization 적용"""
    config = TorchAoConfig("int8_weight_only")  # per-channel 기본

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=config,
        device_map="auto"
    )
    return model

def create_int8_dynamic_model(model_name: str):
    """int8 dynamic activation + weight quantization"""
    config = TorchAoConfig("int8_dynamic_activation_int8_weight")

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=config,
        device_map="auto"
    )
    return model
```

### 3. Trinity Score 기반 모델 최적화
```python
# packages/afo-core/afo/model_optimizer.py
from afo.torchao_quantization import create_int8_quantized_model
from afo.metrics import trinity_metric

def optimize_model_for_trinity(model_name: str, trinity_target: float = 95.0):
    """Trinity Score 기반 모델 최적화"""

    # Baseline 성능 측정
    baseline_model = AutoModelForCausalLM.from_pretrained(model_name)
    baseline_score = evaluate_trinity_score(baseline_model)

    # int8 quantization 적용
    quantized_model = create_int8_quantized_model(model_name)
    quantized_score = evaluate_trinity_score(quantized_model)

    # Trinity Score 개선 확인
    if quantized_score >= trinity_target:
        return quantized_model, quantized_score

    # 추가 최적화 (group_size 튜닝)
    for group_size in [64, 128, 256]:
        config = TorchAoConfig("int8_weight_only", group_size=group_size)
        tuned_model = AutoModelForCausalLM.from_pretrained(
            model_name, quantization_config=config
        )
        tuned_score = evaluate_trinity_score(tuned_model)

        if tuned_score >= trinity_target:
            return tuned_model, tuned_score

    return baseline_model, baseline_score  # fallback
```

### 4. Chancellor Graph TorchAO 통합
```python
# Chancellor Graph에 TorchAO 적용
from afo.model_optimizer import optimize_model_for_trinity

class ChancellorAIAgent:
    def __init__(self, model_name: str):
        # Trinity Score 기반 최적화된 모델 로드
        self.model, self.trinity_score = optimize_model_for_trinity(
            model_name, trinity_target=95.0
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_response(self, query: str):
        inputs = self.tokenizer(query, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=512)

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
```

### 5. 성능 벤치마킹 및 검증
```python
# 3가지 모델 비교
models = {
    "baseline_fp16": baseline_model,
    "int8_weight_only": int8_model,
    "int8_dynamic": int8_dynamic_model
}

results = {}
for name, model in models.items():
    # 메모리 사용량 측정
    memory_usage = measure_memory_usage(model)

    # 추론 속도 측정
    inference_time = benchmark_inference_speed(model)

    # Trinity Score 측정
    trinity_score = evaluate_trinity_score(model)

    results[name] = {
        "memory_mb": memory_usage,
        "inference_ms": inference_time,
        "trinity_score": trinity_score
    }

# 최적 모델 선택
best_model = max(results.items(), key=lambda x: x[1]["trinity_score"])
print(f"최적 모델: {best_model[0]}, Trinity Score: {best_model[1]['trinity_score']}")
```

## ✅ Acceptance Criteria

- [ ] Transformers v5 격리 환경 구축 및 TorchAO 설치 성공
- [ ] int8 weight-only quantization 구현 및 테스트 완료
- [ ] int8 dynamic activation quantization 구현 및 테스트 완료
- [ ] Trinity Score 기반 모델 최적화 시스템 완성
- [ ] Chancellor Graph TorchAO 통합 적용
- [ ] 3가지 quantization 방법 성능 벤치마킹 완료

## 🔒 제약사항

- **LOCKED**: antigravity-seal-2025-12-30 관련 파일 절대 수정 금지
- **안전 우선**: 격리 환경에서 충분히 테스트 후 메인 적용
- **호환성**: Python ^3.12,<3.14 환경 유지

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| v5 RC 불안정성 | 중간 | 중간 | 격리 환경에서 테스트 + fallback 준비 |
| int8 정확도 저하 | 낮음 | 높음 | per-channel 사용 + Trinity Score 검증 |
| 메모리 절감 과도 | 낮음 | 중간 | group_size 튜닝으로 최적화 |

## 🔄 롤백 계획

1. TorchAO 적용 해제 → 표준 Transformers v4
2. v5 격리 해제 → 기존 환경 복원
3. 메인 모델 롤백 → baseline 모델 사용

## 📊 Trinity Score 영향

- **眞 (Truth)**: +7 (per-channel 정확도 유지 + dynamic weight loading)
- **善 (Goodness)**: +9 (메모리 50%↓ + 저비용 inference)
- **美 (Beauty)**: +8 (TorchAoConfig 우아한 API)
- **孝 (Serenity)**: +7 (형님 로컬 실행 용이성)
- **永 (Eternity)**: +8 (PyTorch native 장기 지원)

**예상 총점**: 78.3 → **99.3** (TorchAO int8으로 궁극적 저비용 달성)

## 📝 작업 로그

- **시작일**: 2025-12-31 (DSPy BLOCKED 상황 대안)
- **완료일**: 예정
- **실제 소요시간**: 예정

## 🔗 관련 문서

- `docs/OPTUNA_TPE_METACOGNITION.md` - 메타인지 검증 보고서
- `tools/dspy_mipro/` - DSPy 격리 환경 (참고용)
- `packages/afo-core/afo/torchao_quantization.py` - TorchAO 구현
- `packages/afo-core/afo/model_optimizer.py` - Trinity 기반 최적화
