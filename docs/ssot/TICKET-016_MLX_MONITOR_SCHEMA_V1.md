# TICKET-016 — MLX Monitor SSOT Schema v2 (런타임 최적화 확장)

## 목적
- MLX/VLM/LLM 실측을 "마지막 1줄"로 대시보드에 표시
- 단위/해석 혼선을 방지(SSOT 드리프트 방지)

## 저장 포맷
- JSONL (1줄 1실행)
- 파일: artifacts/ticket016_mlx_monitor_ssot.jsonl

## 공통 필드 (v2 확장)
- schema_version: 2 (런타임 최적화 확장)
- ts: ISO8601 로컬 타임존 문자열
- mode: "vlm_smoke" | "coload" | "chain_run"
- ok: boolean
- secs: number (전체 실행 시간)
- max_rss_bytes: integer | null
  - /usr/bin/time -l의 "maximum resident set size" 값
  - 단위: bytes (실측 검증: 213,762,048 bytes = 203 MB)
- cutline_bytes: integer (고정 컷라인)
- status_badge: string (SAFE/OVER_CUTLINE/WARNING)
- health_score: number (0.0-1.0, 건강 점수)
- notes: string (짧은 메모)

## 런타임 최적화 필드 (v2 추가)
- lazy_cache_hit_rate: number (0.0-1.0, 캐시 히트율)
- reload_overhead_ms: integer (모델 재로딩 오버헤드 ms)
- image_pixels: integer (입력 이미지 픽셀 수)
- compression_ratio: number (이미지 압축 비율)
- token_budget: integer (동적 토큰 예산)
- kv_cache_size: integer (KV 캐시 크기 bytes)
- model_fallback: string (메모리 압박 시 폴백 모델)

## 품질 측정 필드 (v3 LoRA 튜닝 추가)
- measured: boolean (실측 데이터 여부)
- measurement_tool: string (측정 도구: time/psutil/manual)
- confidence_level: string (신뢰도: high/medium/low)
- qwen_accuracy_before: number (Qwen3-VL 튜닝 전 정확도)
- qwen_accuracy_after: number (Qwen3-VL 튜닝 후 정확도)
- llama_quality_before: number (Llama 튜닝 전 품질 점수)
- llama_quality_after: number (Llama 튜닝 후 품질 점수)
- chain_accuracy_before: number (체인 튜닝 전 종단간 정확도)
- chain_accuracy_after: number (체인 튜닝 후 종단간 정확도)
- quality_metrics: object (상세 품질 메트릭)
- improvement_percentage: number (개선율 %)

## mode=vlm_smoke 추가 필드
- model_vlm: string
- image: string
- max_tokens: integer
- temperature: number

## mode=coload 추가 필드
- model_vlm: string
- model_llm: string
- rss_bytes_after_vlm: integer (Python resource ru_maxrss)
- rss_bytes_after_llm: integer (Python resource ru_maxrss)

## 정책(권장)
- 컷라인(보수적): max_rss_bytes <= 20,000,000,000
  - 20GB(Decimal) = 20,000,000,000 bytes
  - 안전 마진: 24GB 시스템의 83%
