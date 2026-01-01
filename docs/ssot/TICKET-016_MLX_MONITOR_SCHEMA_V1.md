# TICKET-016 — MLX Monitor SSOT Schema v1

## 목적
- MLX/VLM/LLM 실측을 "마지막 1줄"로 대시보드에 표시
- 단위/해석 혼선을 방지(SSOT 드리프트 방지)

## 저장 포맷
- JSONL (1줄 1실행)
- 파일: artifacts/ticket016_mlx_monitor_ssot.jsonl

## 공통 필드
- schema_version: 1 (고정)
- ts: ISO8601 로컬 타임존 문자열
- mode: "vlm_smoke" | "coload"
- ok: boolean
- secs: number (전체 실행 시간)
- max_rss_kb_time: integer | null
  - /usr/bin/time -l의 "maximum resident set size (kbytes)" 값
  - 단위: kbytes (1024 bytes)
- notes: string (짧은 메모)

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
- 컷라인(보수적): max_rss_kb_time <= 19,531,250
  - 20GB(Decimal) / 1024 = 19,531,250 kbytes
