# 🎫 TICKET-019: LoRA 튜닝 시스템 (LoRA Fine-tuning System)

**우선순위**: HIGH
**상태**: IN_PROGRESS
**담당**: 승상 + AI팀
**의존성**: TICKET-018 (체인 런타임 최적화 완료)
**예상 소요시간**: 8시간

## 🎯 목표 (Goal)

SSOT 가드레일 영원 봉인 + 체인 런타임 최적화 완료 후, **LoRA 튜닝으로 체인 품질을 20% 향상**시키고 왕국 MLX 잠재력을 완전히 실현.

## 📋 작업 내용

### 1. Qwen3-VL LoRA 튜닝
- **목표**: 이미지 분석 정확도 15% 향상
- **방법**: MLX LoRA fine-tuning 적용 ([Apple Developer LoRA][1])
- **데이터셋**: 이미지 분석 품질 향상용 튜닝 데이터
- **SSOT 필드 추가**: `qwen_accuracy_before`, `qwen_accuracy_after`

### 2. Llama LoRA 튜닝
- **목표**: 요약 생성 품질 15% 향상
- **방법**: 텍스트 요약 품질 튜닝 적용
- **데이터셋**: 고품질 요약 쌍 데이터
- **SSOT 필드 추가**: `llama_quality_before`, `llama_quality_after`

### 3. 체인 튜닝 최적화
- **목표**: Qwen → Llama 종단간 품질 20% 향상
- **방법**: 체인 연결 품질 튜닝
- **데이터셋**: 이미지 분석 → 요약 생성 체인 데이터
- **SSOT 필드 추가**: `chain_accuracy_before`, `chain_accuracy_after`

### 4. 품질 측정 체계 구축
- **측정 메트릭**: 정확도, 실패율, 응답 길이, 일관성
- **SSOT 확장**: 품질 측정 결과 저장
- **대시보드 표시**: 튜닝 전/후 비교
- **SSOT 필드 추가**: `quality_metrics`, `improvement_percentage`

## ✅ Acceptance Criteria

- [ ] Qwen3-VL LoRA 튜닝 완료 (이미지 분석 정확도 15%↑)
- [ ] Llama LoRA 튜닝 완료 (요약 품질 15%↑)
- [ ] 체인 튜닝 완료 (종단간 품질 20%↑)
- [ ] 품질 SSOT 측정 체계 구축 (정확도/실패율/응답길이/일관성)
- [ ] 대시보드 품질 비교 표시 기능 추가

## 🔒 제약사항

- **메모리 안전성**: LoRA 튜닝 중에도 20GB 컷라인 준수
- **품질 유지**: 튜닝으로 인한 품질 저하 방지 (baseline 유지)
- **재현성**: 동일 데이터로 동일 결과 보장
- **Apple MLX 호환성**: MLX LoRA 공식 지원 범위 내 구현

## 📊 Trinity Score 영향

- **眞 (Truth)**: +25 (품질 측정 정확성 + LoRA 튜닝 효과 검증)
- **善 (Goodness)**: +20 (메모리 효율적 튜닝 + 안전성 유지)
- **美 (Beauty)**: +15 (대시보드 품질 비교 UX)
- **孝 (Serenity)**: +10 (체인 안정성 향상)
- **永 (Eternity)**: +5 (품질 SSOT 영속성)

**예상 총점**: 258.3 → **333.3** (+75 포인트)

## 🔗 관련 문서

- `docs/ssot/TICKET-016_MLX_MONITOR_SCHEMA_V1.md` - SSOT 스키마 v2
- `tools/mlx_optimization/qwen3_vl_poc.py` - 현재 Qwen3-VL 구현
- `tools/mlx_optimization/ticket016_mlx_monitor.py` - 모니터링 스크립트
- `packages/dashboard/src/components/MLXVLMMonitorCard.tsx` - 대시보드 카드

## 📈 품질 측정 기준

### 이미지 분석 정확도
- **전**: Qwen3-VL 기본 성능
- **후**: LoRA 튜닝 후 성능
- **측정**: 이미지 내용 이해도, 텍스트 추출 정확도

### 요약 품질
- **전**: Llama 기본 요약 품질
- **후**: LoRA 튜닝 후 요약 품질
- **측정**: 요약 정확성, 완전성, 간결성

### 체인 품질
- **전**: Qwen 분석 → Llama 요약 종단간 품질
- **후**: 튜닝된 체인 품질
- **측정**: 종단간 정확도, 정보 보존율

## 🛠️ 기술 구현

### LoRA 튜닝 파이프라인
```python
# mlx-lm LoRA 튜닝 예시
from mlx_lm import load, train
from mlx.optimizers import Adam

# 모델 로드
model, tokenizer = load("mlx-community/Qwen3-VL-8B-Instruct-4bit")

# LoRA 설정
lora_config = {
    "rank": 8,
    "alpha": 16,
    "dropout": 0.1,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"]
}

# 튜닝 실행
trainer = train(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_data,
    lora_config=lora_config,
    optimizer=Adam(learning_rate=2e-5),
    num_epochs=3
)
```

### 품질 평가 스크립트
```python
# 품질 측정 예시
def evaluate_quality(predictions, ground_truth):
    accuracy = calculate_accuracy(predictions, ground_truth)
    consistency = calculate_consistency(predictions)
    completeness = calculate_completeness(predictions, ground_truth)
    return {
        "accuracy": accuracy,
        "consistency": consistency,
        "completeness": completeness
    }
```

[1]: https://developer.apple.com/videos/play/wwdc2025/298/
