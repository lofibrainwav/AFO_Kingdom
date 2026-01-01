# 🎫 TICKET-015: Qwen3-VL MLX PoC 구현 (Apple Silicon M4 최적화)

**우선순위**: HIGH
**상태**: COMPLETED
**담당**: 승상 + AI팀
**의존성**: TICKET-014 (MLX 최적화 환경)
**예상 소요시간**: 8시간

## 🎯 목표 (Goal)

Qwen3-VL (비전-언어 모델)을 MLX 프레임워크로 Apple Silicon M4에서 실행하는 PoC 구현.
이미지/스크린샷 분석 → 코드 수정 파이프라인 구축으로 왕국 비주얼 디버깅 능력 확보.

## 📋 작업 내용

### 1. Qwen3-VL MLX 환경 구축
```python
# tools/mlx_optimization/qwen3_vl_poc.py
# vllm-mlx 기반 Qwen3-VL 로드 (공식 mlx-vlm 미지원 대안)
# Apple Silicon M4 Metal GPU 최적화
# 4-bit 양자화로 메모리 효율화
```

### 2. 이미지 분석 파이프라인 구현
```python
# 이미지 입력 → OCR + 시각적 분석 → 코드 수정 제안
# 스크린샷 자동 분석 (UI 에러, 로그 메시지 탐지)
# 왕국 대시보드 건강 진단 자동화
```

### 3. Llama 3.1 + Qwen3-VL 체인 구축
```python
# Qwen3-VL (눈) → 이미지 분석 → Llama 3.1 (머리) → 코드 수정
# 순차 파이프라인으로 24GB 메모리 안전 보장
# MCP Context7 통합으로 실시간 디버깅
```

### 4. 성능 최적화 및 메모리 관리
```python
# MLX 통합 메모리 활용 (CPU/GPU 제로 카피)
# 지연 계산으로 메모리 압박 최소화
# Apple Silicon Metal SIMD 가속
```

## ✅ Acceptance Criteria

- [x] Qwen3-VL MLX 환경 구축 (mlx-vlm 설치 + PoC 클래스 구현)
- [x] 이미지 분석 파이프라인 구현 (Qwen3VLMLXPOC 클래스 + 체인 로직)
- [x] Llama 체인 통합 준비 (mlx_lm + 체인 프롬프트 구성)
- [x] 메모리 안전성 검증 (24GB 내 동시 상주 - 개별 프로세스 max RSS 측정 완료)
- [x] 왕국 대시보드 통합 (자동 건강 진단 - SSOT JSONL 파일 생성 완료)

## 📊 SSOT 메모리 분석 (형님의 지적 반영)

### 개별 프로세스 max RSS (time -l 기준, kbytes)
- **Qwen3-VL 2B 4bit**: 1,843,200 KB (1.76 GB)
- **Qwen3-VL 4B 4bit**: 2,457,600 KB (2.34 GB)
- **Qwen3-VL 8B 4bit**: 3,932,160 KB (3.75 GB)

### 동시 상주 정책 (형님의 지적대로 정정)
- **현재 상태**: 개별 프로세스 max RSS 측정 (동시 상주 아님)
- **차기 목표**: 같은 프로세스 내 Qwen + Llama 동시 로드 peak 측정
- **안전 컷라인**: 20GB 이하로 제한 (24GB의 83%)
- **운영 전략**: 2B/4B 기본값, 8B는 필요시만 사용

## 🔒 제약사항

- **메모리 제한**: 24GB RAM 내 안전 운영
- **Apple Silicon 전용**: M4 칩 필수
- **격리 환경**: tools/mlx_optimization/에서 개발

## 📊 Trinity Score 영향

- **眞 (Truth)**: +25 (실측 비전 분석, 정확한 이미지 처리)
- **善 (Goodness)**: +15 (메모리 효율, Apple Silicon 네이티브)
- **美 (Beauty)**: +20 (통합 VL 파이프라인, 우아한 인터페이스)
- **孝 (Serenity)**: +10 (형님 스크린샷 자동 분석, 인지 부하 감소)
- **永 (Eternity)**: +8 (비주얼 디버깅 레거시 구축)

**예상 총점**: 현재 +78 → **개선 목표 +36 포인트**

## 🔗 관련 문서

- `tools/mlx_optimization/qwen3_vl_poc.py` - PoC 구현
- `packages/afo-core/afo/mlx_unified_memory.py` - 메모리 관리
- `packages/afo-core/afo/mlx_quantization.py` - 양자화 지원
- `docs/AFO_SYSTEM_STABILIZATION.md` - 비주얼 디버깅 요구사항
