# Trinity Score 계산 로직 상세 문서화

## 개요

AFO 왕국의 Trinity Score는 眞善美孝永 5기둥 철학을 기반으로 한 건강도 측정 시스템입니다.
이 문서는 Trinity Score의 계산 로직을 상세히 설명합니다.

## 5기둥 철학 (眞善美孝永)

| 기둥 | 한자 | 영어 | 가중치 | 설명 |
|-----|------|------|--------|------|
| 眞 | Truth | 기술적 확실성 | 35% | 코드 품질, 시스템 안정성 |
| 善 | Goodness | 윤리·안정성 | 35% | 보안, 신뢰성, 사용자 경험 |
| 美 | Beauty | 단순함·우아함 | 20% | 코드 구조, API 설계 |
| 孝 | Serenity | 평온 수호 | 8% | 자동화, 운영 효율성 |
| 永 | Eternity | 영속성 | 2% | 문서화, 유지보수성 |

## 계산 공식

### 1. 기초 점수 계산 (health_service.py)

```python
# 眞 (Truth) - 코어 데이터 계층
truth_score = healthy_redis_and_postgres / total_core_organs

# 善 (Goodness) - 전체 서비스 안정성
goodness_score = healthy_organs / total_organs

# 美 (Beauty) - API 가용성
beauty_score = 1.0 if api_healthy else 0.0

# 孝 (Serenity) - LLM 가용성
filial_score = 1.0 if ollama_healthy else 0.0

# 永 (Eternity) - 영속적 가동
eternity_score = healthy_count / total_organs
```

### 2. Trinity Score 계산 (trinity.py)

```python
trinity_score = (
    0.35 × truth +
    0.35 × goodness +
    0.20 × beauty +
    0.08 × filial_serenity +
    0.02 × eternity
)
```

### 3. 균형 상태 평가

```python
balance_delta = max(values) - min(values)
if balance_delta < 0.3:
    status = "balanced"
elif balance_delta < 0.5:
    status = "warning"
else:
    status = "imbalanced"
```

## 현재 상태 (2025-12-26 기준)

- **Trinity Score**: 1.0 (100%)
- **균형 상태**: balanced
- **각 기둥 점수**:
  - 眞 (Truth): 1.0 - Redis/PostgreSQL 정상
  - 善 (Goodness): 1.0 - 모든 기관 정상
  - 美 (Beauty): 1.0 - API 정상
  - 孝 (Serenity): 1.0 - Ollama 정상
  - 永 (Eternity): 1.0 - 시스템 안정

## 해석 가이드

### 점수 범위
- **0.9-1.0**: Excellent (모든 시스템 정상)
- **0.7-0.9**: Good (부분적 문제)
- **0.5-0.7**: Warning (주의 필요)
- **0.0-0.5**: Critical (즉시 조치 필요)

### 균형 상태
- **balanced**: 모든 기둥이 조화롭게 유지
- **warning**: 일부 기둥에서 불균형 발생
- **imbalanced**: 심각한 불균형 상태

## 구현 파일

- `services/health_service.py`: 기초 건강 상태 측정
- `AFO/domain/metrics/trinity.py`: Trinity Score 계산
- `AFO/observability/rule_constants.py`: 가중치 정의
- `api/routes/comprehensive_health.py`: API 응답 구성

## 모니터링 포인트

- Trinity Score 추이 모니터링
- 각 기둥별 점수 변동 추적
- 균형 상태 변경 감지
- 이상 징후 조기 발견
