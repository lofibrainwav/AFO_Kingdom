# RAG Production Rollout — Ops Guide (Shadow → Flag → Gradual)

## 목적
RAG를 응답 파이프라인에 안전하게 투입한다.
- Shadow: 응답 영향 0%, 메트릭만 확대(안정적 버킷팅)

#CH > X-AFO-RAG 헤더 > FLAG ENV > GRADUAL ENV > SH 기본값

## 제어값
### Headers (최우선)
- X-AFO-RAG: 1  (강제 ON)
- X-AFO-RAG: 0  (강제 OFF)
- X-AFO-CLIENT-ID: <stable id> (버킷팅 seed 우선)
- X-Request-ID: <id> (seed 대체)

### ENV
- AFO_RAG_SHADOW_ENABLED=1
- AFO_RAG_FLAG_ENABLED=0|1
- AFO_RAG_ROLLOUT_ENABLED=0|1
- AFO_RAG_ROLLOUT_PERCENT=0..100
- AFO_RAG_TIMEOUT_MS=1000
- AFO_RAG_MAX_CONCURRENCY=8
- AFO_RAG_KILL_SWITCH=0|1

## Health / Metrics
GET /chancellor/rag/shadow/health
- decision_mode: killed|forced_on|forced_off|flag|gradual|shadow_only
- applied: true/false
- rollout_percent, bucket_seed_source
- latency_ms, fallback_reason
- recent entries + aggregates

## Seal (Evidence)
scripts/seal_rag*.json
- health_*.json
- 5pillars_*.json

## 권장 운영 순서
1) Shadow(기본)로 메트릭 안정화 확인
2) Flag(내부 헤더)로 품질/지연 검증
3) Gradual 1% → 5% → 10% … 점진 확대
4) 이상 시 즉시 롤백(KILL_SWITCH=1 또는 percent=0)

## 롤백
- export AFO_RAG_KILL_SWITCH=1
또는
- export AFO_RAG_ROLLOUT_ENABLED=0
- export AFO_RAG_FLAG_ENABLED=0
