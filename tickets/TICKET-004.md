# 🎫 TICKET-004: Trinity Score 메트릭 통합

**우선순위**: MEDIUM
**상태**: PENDING
**담당**: 품질팀
**의존성**: TICKET-002, TICKET-003
**예상 소요시간**: 2시간

## 🎯 목표 (Goal)

DSPy 최적화 결과에 Trinity Score 메트릭을 통합하여 왕국 철학 기반 평가 체계를 구축한다.

## 📋 작업 내용

### 1. Trinity Score 메트릭 함수 구현
```python
def trinity_metric(example, prediction):
    """5기둥 기반 DSPy 메트릭"""
    truth_score = calculate_truth_score(prediction)
    goodness_score = calculate_goodness_score(prediction)
    beauty_score = calculate_beauty_score(prediction)
    serenity_score = calculate_serenity_score(prediction)
    eternity_score = calculate_eternity_score(prediction)

    weights = {"truth": 0.35, "goodness": 0.35, "beauty": 0.20, "serenity": 0.08, "eternity": 0.02}
    total_score = sum(scores[k] * weights[k] for k in scores)

    feedback = generate_trinity_feedback(scores)
    return dspy.Prediction(score=total_score, feedback=feedback)
```

### 2. 각 기둥별 평가 로직
- **眞**: 사실 정확성 + 타입 안전성
- **善**: 리스크 평가 + 자원 효율성
- **美**: 코드 우아함 + 모듈화
- **孝**: 형님 마찰 최소화
- **永**: 유지보수성 + 확장성

### 3. MIPROv2에 메트릭 적용
```python
optimizer = MIPROv2(metric=trinity_metric, auto="heavy")
optimized_rag = optimizer.compile(rag, trainset=trainset, valset=valset)
```

### 4. 평가 결과 시각화
- Trinity Score 분포 그래프
- 각 기둥별 개선 추이
- 최적화 효과 정량화

## ✅ Acceptance Criteria

- [ ] Trinity Score 메트릭 함수 구현
- [ ] 5기둥별 평가 로직 완성
- [ ] MIPROv2 통합 성공
- [ ] 평가 결과 정확성 검증
- [ ] 시각화 대시보드 구현

## 📊 Trinity Score 영향

- **眞 (Truth)**: +4 (철학 기반 정확 평가)
- **善 (Goodness)**: +3 (포괄적 리스크 평가)
- **美 (Beauty)**: +2 (우아한 평가 체계)
- **孝 (Serenity)**: +2 (형님 중심 평가)
- **永 (Eternity)**: +3 (지속적 품질 관리)

**예상 총점**: 78.3 → 85.3
