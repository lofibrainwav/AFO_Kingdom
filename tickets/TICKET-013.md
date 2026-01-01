# 🎫 TICKET-013: vLLM TorchAO 고속 서빙 시스템 구축

**우선순위**: HIGH
**상태**: PENDING
**담당**: 승상 + AI팀
**의존성**: TICKET-012 (TorchAO int8 최적화 완료 후)
**예상 소요시간**: 8시간

## 🎯 목표 (Goal)

TorchAO int8 최적화된 모델을 vLLM으로 고속 서빙하여 왕국 AI 시스템의 초고속 저비용 추론 구현.

## 📋 작업 내용

### 1. vLLM 격리 환경 구축
```python
# tools/vllm_torchao/pyproject.toml
[tool.poetry]
name = "vllm-torchao-serving"
version = "0.1.0"
description = "vLLM TorchAO 고속 서빙 격리 환경"

[tool.poetry.dependencies]
python = "^3.12,<3.14"
vllm = "^0.10.0"
torch = "^2.5.0"
torchao = "^0.7.0"
transformers = "^5.0.0rc1"
accelerate = "^1.0.0"
```

### 2. TorchAO 모델 vLLM 서빙 구현
```python
# packages/afo-core/afo/vllm_torchao_serving.py
from vllm import EngineArgs, LLMEngine, SamplingParams
from transformers import TorchAoConfig
import torch

class VLLMTorchAOServing:
    def __init__(self, model_name: str, quantization: str = "torchao"):
        """TorchAO 모델을 vLLM으로 서빙"""

        # TorchAO int8 설정
        torchao_config = TorchAoConfig("int8_weight_only")

        # vLLM 엔진 설정
        self.engine_args = EngineArgs(
            model=model_name,
            quantization=quantization,  # "torchao"
            dtype="auto",
            max_model_len=4096,
            gpu_memory_utilization=0.8,
            tensor_parallel_size=torch.cuda.device_count() if torch.cuda.is_available() else 1
        )

        self.engine = LLMEngine.from_engine_args(self.engine_args)
        self.tokenizer = self.engine.get_tokenizer()

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7):
        """고속 추론 실행"""

        sampling_params = SamplingParams(
            temperature=temperature,
            max_tokens=max_tokens,
            stop=["\n\n", "###"]
        )

        # 비동기 추론
        request_id = f"request_{hash(prompt)}"
        self.engine.add_request(request_id, prompt, sampling_params)

        # 결과 수집
        results = []
        while self.engine.has_unfinished_requests():
            step_outputs = self.engine.step()
            for output in step_outputs:
                if output.finished:
                    results.append(output)

        return self.tokenizer.decode(results[0].outputs[0].text) if results else ""
```

### 3. Trinity Score 기반 모델 선택 및 서빙
```python
# packages/afo-core/afo/trinity_model_selector.py
from afo.vllm_torchao_serving import VLLMTorchAOServing
from afo.metrics import trinity_metric

class TrinityModelSelector:
    def __init__(self):
        self.models = {}  # model_name -> VLLMTorchAOServing instance
        self.trinity_scores = {}  # model_name -> trinity_score

    def register_model(self, model_name: str, trinity_score: float):
        """모델 등록 및 서빙 준비"""
        if trinity_score >= 95.0:  # 고품질 모델만 등록
            serving = VLLMTorchAOServing(model_name)
            self.models[model_name] = serving
            self.trinity_scores[model_name] = trinity_score

    def select_best_model(self, query_complexity: str = "medium"):
        """쿼리 복잡도에 따른 최적 모델 선택"""

        if query_complexity == "low":
            # 간단한 쿼리는 가벼운 모델
            return max(self.trinity_scores.items(),
                      key=lambda x: x[1] if x[0].endswith("7B") else 0)

        elif query_complexity == "high":
            # 복잡한 쿼리는 강력한 모델
            return max(self.trinity_scores.items(),
                      key=lambda x: x[1] if x[0].endswith("70B") else 0)

        else:
            # 중간 복잡도는 Trinity Score 기반 선택
            return max(self.trinity_scores.items(), key=lambda x: x[1])

    def generate_response(self, query: str, complexity: str = "medium"):
        """최적 모델로 응답 생성"""
        best_model_name, _ = self.select_best_model(complexity)
        serving = self.models[best_model_name]

        response = serving.generate(query)
        return response, best_model_name
```

### 4. Chancellor Graph vLLM 통합
```python
# Chancellor Graph에 vLLM 서빙 통합
from afo.trinity_model_selector import TrinityModelSelector

class ChancellorVLLMAgent:
    def __init__(self):
        self.model_selector = TrinityModelSelector()

        # TorchAO 최적화된 모델들 등록
        torchao_models = [
            ("microsoft/DialoGPT-medium", 92.3),
            ("meta-llama/Llama-2-7b-chat-hf", 96.7),
            ("meta-llama/Llama-2-13b-chat-hf", 98.1),
        ]

        for model_name, score in torchao_models:
            self.model_selector.register_model(model_name, score)

    def query_kingdom(self, question: str, context_complexity: str = "medium"):
        """왕국 지식 쿼리 처리"""

        # 컨텍스트 기반 복잡도 분석
        complexity = self.analyze_complexity(question)

        # 최적 모델 선택 및 추론
        response, model_used = self.model_selector.generate_response(
            question, complexity
        )

        return {
            "response": response,
            "model_used": model_used,
            "trinity_score": self.model_selector.trinity_scores[model_used],
            "inference_time": "measured_time"  # 실제 측정 값
        }

    def analyze_complexity(self, question: str):
        """질문 복잡도 분석"""
        if len(question.split()) < 10:
            return "low"
        elif len(question.split()) > 50 or any(word in question.lower()
              for word in ["analyze", "compare", "explain", "design"]):
            return "high"
        else:
            return "medium"
```

### 5. 성능 모니터링 및 최적화
```python
# packages/afo-core/afo/vllm_performance_monitor.py
import time
import psutil
from afo.vllm_torchao_serving import VLLMTorchAOServing

class VLLMPerformanceMonitor:
    def __init__(self, serving: VLLMTorchAOServing):
        self.serving = serving
        self.metrics = {
            "throughput": [],
            "latency": [],
            "memory_usage": [],
            "gpu_utilization": []
        }

    def benchmark_model(self, test_queries: list, batch_size: int = 1):
        """모델 성능 벤치마킹"""

        for query in test_queries:
            start_time = time.time()

            # 추론 실행
            response = self.serving.generate(query)

            end_time = time.time()

            # 메트릭 수집
            latency = end_time - start_time
            memory_mb = psutil.virtual_memory().used / 1024 / 1024
            gpu_memory = torch.cuda.memory_allocated() / 1024 / 1024 if torch.cuda.is_available() else 0

            self.metrics["latency"].append(latency)
            self.metrics["memory_usage"].append(memory_mb)
            self.metrics["gpu_memory"].append(gpu_memory)

        # 평균 메트릭 계산
        avg_latency = sum(self.metrics["latency"]) / len(self.metrics["latency"])
        avg_memory = sum(self.metrics["memory_usage"]) / len(self.metrics["memory_usage"])
        avg_gpu_memory = sum(self.metrics["gpu_memory"]) / len(self.metrics["gpu_memory"])

        throughput = len(test_queries) / sum(self.metrics["latency"])

        return {
            "throughput_qps": throughput,
            "avg_latency_ms": avg_latency * 1000,
            "avg_memory_mb": avg_memory,
            "avg_gpu_memory_mb": avg_gpu_memory
        }
```

## ✅ Acceptance Criteria

- [ ] vLLM 격리 환경 구축 및 TorchAO 통합 성공
- [ ] TorchAO int8 모델 vLLM 서빙 구현 완료
- [ ] Trinity Score 기반 모델 선택 시스템 완성
- [ ] Chancellor Graph vLLM 통합 적용
- [ ] 성능 벤치마킹 및 최적화 완료 (throughput 1.5x↑ 목표)
- [ ] 고속 서빙 API 엔드포인트 구축

## 🔒 제약사항

- **LOCKED**: antigravity-seal-2025-12-30 관련 파일 절대 수정 금지
- **안전 우선**: 격리 환경에서 충분히 테스트 후 메인 적용
- **GPU 메모리**: 최대 80% 활용, OOM 방지

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| vLLM TorchAO 통합 복잡성 | 중간 | 중간 | 단계별 테스트 + 공식 문서 준수 |
| GPU 메모리 부족 | 높음 | 높음 | 메모리 모니터링 + fallback 모델 |
| Throughput 목표 미달 | 낮음 | 중간 | 벤치마킹 기반 튜닝 |

## 🔄 롤백 계획

1. vLLM 서빙 중단 → 표준 Transformers 추론
2. TorchAO 모델 해제 → FP16 모델 사용
3. 고속 서빙 API 제거 → 기본 API 복원

## 📊 Trinity Score 영향

- **眞 (Truth)**: +9 (native 정확 로드 + PagedAttention)
- **善 (Goodness)**: +9 (throughput 1.5~2x↑ + 메모리 50~70%↓)
- **美 (Beauty)**: +9 (TorchAO backend + vLLM API 우아함)
- **孝 (Serenity)**: +8 (형님 고속 서빙 용이성)
- **永 (Eternity)**: +9 (PyTorch native + vLLM 장기 지원)

**예상 총점**: 78.3 → **100.0** (고속 저비용 궁극 달성)

## 📝 작업 로그

- **시작일**: 2025-12-31 (TorchAO 최적화 완료 후)
- **완료일**: 예정
- **실제 소요시간**: 예정

## 🔗 관련 문서

- `tools/transformers_v5/` - TorchAO 격리 환경
- `packages/afo-core/afo/vllm_torchao_serving.py` - vLLM 서빙 구현
- `packages/afo-core/afo/trinity_model_selector.py` - Trinity 기반 선택
- `packages/afo-core/afo/vllm_performance_monitor.py` - 성능 모니터링
