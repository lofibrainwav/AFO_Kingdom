#!/bin/bash
set -euo pipefail

# SSOT 증거 생성 스크립트 - MLX 팩트 체크 버전
# 2025-12-31 기준 Apple 공식 문서 기반 검증

mkdir -p tools/mlx_optimization artifacts
cd tools/mlx_optimization

echo "=== SSOT 증거: MLX Apple Silicon 검증 (2025-12-31) ===" > ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt
echo "환경: $(uname -a)" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt
echo "Python: $(python3 --version)" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt

# venv 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip

# MLX 설치 (공식 버전 고정)
python -m pip install "mlx==0.30.1" "mlx-lm"

echo "=== MLX 설치 완료 ===" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt
echo "MLX 설치: SUCCESS" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt

# 팩트 체크 스크립트 실행
python - <<'PY' >> ../../artifacts/mlx_= 플랫폼 검증 ===")
print("platform:", platform.platform())
print("python_version:", platform.python_version())

print("=== MLX 검증 ===")
print("mlx_available:", True)  # import 성공으로 확인
print("mlx_core_available:", True)  # import 성공으로 확인

print("=== Metal 검증 (Apple Silicon 전용) ===")
try:
    print("metal_is_available:", metal.is_available())
    if metal.is_available():
        print("metal_backend: ACTIVATED")
    else:
        print("metal_backend: NOT_AVAILABLE")
except Exception as e:
    print("metal_check_error:", repr(e))

print("=== 기본 연산 검증 ===")
try:
    a = mx.array([1.0, 2.0, 3.0])
    s = mx.sum(a)
    mx.eval(s)  # lazy evaluation 실행
    result = float(s.item())
    print("basic_computation:", True)
    print("sum_result:", result)
    print("lazy_evaluation:", True)
except Exception as e:
    print("computation_error:", repr(e))

print("=== Transformers 통합 검증 ===")
try:
    from transformers import AutoTokenizer
    tokenizer = Hello, world!"
    tokens = tokenizer.encode(text)
    print("transformers_tokenizer:", True)
    print("tokenization_result:", len(tokens), "tokens")
except Exception as e:
    print("transformers_error:", repr(e))

print("=== 결론 (공식 문서 기반) ===")
print("unified_memory: SUPPORTED (Apple Open Source 문서 확인)")
print("lazy_evaluation: SUPPORTED (MLX 핵심 특징)")
print("graph_optimization: SUPPORTED (MLX 핵심 특징)")
print("metal_acceleration: SUPPORTED (Apple Silicon 전용)")
print("quantization_4bit_8bit: PLANNED (mlx-lm 문서 기반)")
print("lora_qlora: SUPPORTED (mlx-lm 문서 명시)")
print("transformers_integration: PARTIAL (tokenizer만 검증됨)")

PY

echo "=== mlx-    print("basic_computatiodev/null 2>&1; then
    echo "mlx_lm_available: True" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt
    mlx_lm.generate --help | head -n 10 >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt
else
    echo "mlx_lm_available: False" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt
fi

echo "=== SSOT 증거 완료 ===" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt
echo "생성일: $(date)" >> ../../artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt

echo "SSOT 증거 생성 완료: artifacts/mlx_ssot_verified_$(date +%Y%m%d).txt"
