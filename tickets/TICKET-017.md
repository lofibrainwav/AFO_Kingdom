# 🎫 TICKET-017: SSOT 체인 피크 모니터링 완성

**우선순위**: HIGH
**상태**: IN_PROGRESS
**담당**: 승상 + AI팀
**의존성**: TICKET-016 (모니터링 체계 구축)
**예상 소요시간**: 4시간

## 🎯 목표 (Goal)

TICKET-016의 SSOT 가드레일을 완벽하게 봉인하기 위해 **체인 실행 피크 측정**을 추가.
deprecated 제거 검증과 함께 진짜 운영 환경 메모리 피크를 SSOT로 확보.

## 📋 작업 내용

### 1. chain_run 모드 추가
```python
# tools/mlx_optimization/ticket016_mlx_monitor.py
# mode=chain_run: Qwen3-VL 이미지 분석 → Llama 요약 생성 체인 실행
# /usr/bin/time -l로 체인 실행 시점 메모리 피크 측정
```

### 2. deprecated 제거 검증
```bash
# vlm_smoke 재실행으로 notes 필드 클린 확인
python tools/mlx_optimization/ticket016_mlx_monitor.py vlm_smoke \
  --model mlx-community/Qwen3-VL-2B-Instruct-4bit \
  --image grok_error.png
```

### 3. 체인 피크 SSOT 데이터 생성
```json
// artifacts/ticket016_mlx_monitor_ssot.jsonl에 추가
{
  "schema_version": 1,
  "mode": "chain_run",
  "max_rss_bytes": 8242880000,  // 체인 피크 (8.2GB 예상)
  "vlm_model": "mlx-community/Qwen3-VL-4B-Instruct-MLX-4bit",
  "llm_model": "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit",
  "image": "grok_error.png",
  "notes": ""  // 클린 상태
}
```

### 4. 스키마 v1.1 업데이트 (선택)
- chain_run 모드 필드 추가
- 체인 실행 메트릭 표준화

## ✅ Acceptance Criteria

- [x] chain_run 모드 구현 (Qwen + Llama 체인 실행)
- [ ] 체인 피크 SSOT 데이터 생성 (실측 값 확보)
- [ ] deprecated 제거 검증 (notes 필드 클린)
- [ ] 대시보드 체인 피크 표시 (선택)

## 🔒 제약사항

- **메모리 안전성**: 체인 피크도 20GB 컷라인 이내 유지
- **시간 제한**: 체인 실행은 30초 이내 완료
- **격리 환경**: tools/mlx_optimization/에서만 실행

## 📊 Trinity Score 영향

- **眞 (Truth)**: +15 (체인 피크 실측 데이터로 정확성 향상)
- **善 (Goodness)**: +5 (deprecated 제거로 안정성 향상)
- **美 (Beauty)**: +0 (UI 변화 최소)
- **孝 (Serenity)**: +3 (더 정확한 건강 모니터링)
- **永 (Eternity)**: +2 (SSOT 스키마 완전 검증)

**예상 총점**: 183.3 → **208.3** (+25 포인트)

## 🔗 관련 문서

- `docs/ssot/TICKET-016_MLX_MONITOR_SCHEMA_V1.md` - 현재 스키마
- `tools/mlx_optimization/ticket016_mlx_monitor.py` - 모니터링 스크립트
- `artifacts/ticket016_mlx_monitor_ssot.jsonl` - SSOT 데이터
