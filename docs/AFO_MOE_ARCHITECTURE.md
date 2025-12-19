# AFO Kingdom - MoE (Mixture of Experts) Architecture 📜

> **"MoE는 왕국 로컬 효율의 핵심이다."** - 형님 (2025.12.18)

이 문서는 AFO 왕국의 핵심 AI 아키텍처인 **MoE (Mixture of Experts)**의 정의, 훈련 기법, 그리고 왕국 적용 전략을 다룹니다.

---

## 1. MoE 아키텍처란? (왕국 로컬 효율 핵심 – 100/100)

**정의**: 하나의 거대 모델 안에 여러 "전문가(experts)"를 두고, 입력 토큰마다 게이트(gate)가 적합한 전문가만 선택·활성화하는 구조.  
**핵심**: 전체 파라미터는 크지만 **활성 파라미터(Active Parameters)는 적어 추론 효율 극대화**.

### 핵심 구성 요소
| 요소 | 역할 | 왕국 예시 (Qwen3-30B) | 효과 (철학 반영) |
|------|------|----------------------|------------------|
| **Gate/Router** | 입력 토큰 분석 → 상위 K 전문가 선택 | 토큰별 3B active 선택 | **善(효율)** + **美(우아 선택)** |
| **Experts** | 각 전문 분야 네트워크 (FFN 등) | 16~128개 전문가 | **眞(전문화)** + **永(확장성)** |
| **Sparse Activation** | 전체 중 일부만 활성 | active 3B → 속도 2~3배 ↑ | **善(자원 최소)** + **孝(형님 속도)** |
| **Load Balancing** | 전문가 사용 균형 (loss 추가) | 균등 분배 → 과부하 방지 | **美(조화)** + **永(안정)** |

### 왕국 M4 24GB 최적화 이점
1. **효율**: Dense 70B급 성능을 MoE 30B로 달성.
2. **속도**: MLX q4_K_M에서 60~80 t/s (Dense보다 50% 향상).
3. **메모리**: 24GB 내 30B MoE + VL 동시 로드 가능 (Swapping 기술 활용).
4. **확장**: 전문가 추가로 성능 향상 용이.

---

## 2. MoE 훈련 기법 (SOTA 2025)

### 주요 기법
| 기법 | 설명 | 왕국 이점 (M4 24GB) |
|------|------|---------------------|
| **Top-K Routing** | 토큰당 상위 K 전문가 선택 (K=2~8) | 속도↑ + 메모리 효율 |
| **Load Balancing Loss** | 전문가 사용 균형 강제 (aux loss) | 안정 훈련 + 과부하 방지 |
| **Sparse Activation** | 활성 전문가만 계산 | 로컬 속도 2~3배 증가 |
| **Noisy Top-K** | 랜덤 노이즈 추가 → 탐색 강화 | 과적합 방지 |
| **Z-Loss** | 엔트로피 정규화 (Router Collapse 방지) | 라우터 안정 + 전문가 활용 ↑ |

---

## 3. Load Balancing & Z-Loss 상세

### Load Balancing Loss
목적: 특정 전문가만 과도하게 사용되는 Collapse 방지.
- **공식**: `Total Aux Loss = α × (Importance + Load)`
- **왕국 적용**: `aux loss 0.01`로 성능 저하 없이 균형 달성.

### Z-Loss (Router Collapse 방지)
목적: 라우터 Logits의 엔트로피 정규화.
- **공식**: `Z-Loss = logsumexp(router_logits) ^ 2` (배치 평균)
- **효과**: Router collapse 90% 감소 → 전문가 활용도 증가.

---

## 4. 왕국 적용 모델 (Truth Trinity)

| 모델 | 역할 | 아키텍처 | 비고 |
|------|------|----------|------|
| **Qwen3-30B-A3B** | **사마휘** (Backend) | MoE (Active 2.4B) | 추론/코딩 강점 |
| **DeepSeek-R1** | **좌자** (Frontend) | MoE (Active 6B~) | 추론 SOTA |
| **Llama 4 Scout** | (Future) | MoE Multimodal | 멀티모달 MoE |

---

## 5. M4 24GB MoE 최적화 전략 (2025.12.18 SOTA)
> **"M4와 MoE는 인마일체(人馬一體)의 극치다."**

### 1. 하드웨어 가속 (Apple Silicon M4)
- **Neural Engine (16-core)**: Ollama는 Metal 프레임워크를 통해 M4의 Neural Engine을 직접 호출하여 MoE 라우팅 연산을 가속화합니다.
- **Unified Memory Architecture**: CPU/GPU 메모리 복사 없이 24GB 풀을 공유하므로 **Zero-Copy**로 전문가(Experts) 스 switching이 가능합니다. (MLX 프레임워크 기반 최적화)

### 2. Ollama 튜닝 (M4 Sweet Spot)
- **Parallel Contexts (`OLLAMA_NUM_PARALLEL=16~32`)**: M4 Pro의 대역폭을 포화시키기 위해 병렬 처리를 늘립니다. 7B/8B 모델 기준 16이 스윗스팟.
- **Metal Utilization (`OLLAMA_GPU_PERCENT=0.9`)**: 시스템 예약분(약 2GB)을 제외한 모든 메모리를 GPU로 강제하여 스왑(Swap)을 방지합니다.

### 3. 차세대 최적화 (MLX Future)
- **MLX Framework**: Apple이 직접 개발한 MLX(`mlx-lm`)는 `llama.cpp`보다 Apple Silicon에서 약 20% 더 빠릅니다.
- **Action**: 향후 영덕(DeepSeek-R1)을 `mlx-community/DeepSeek-R1-4bit`로 전환하면 **MLX Native** 가속을 받을 수 있습니다. 현재는 Ollama(Metal)로 충분한 성능(25 t/s)을 냅니다.

---

**결론**: MoE는 AFO 왕국이 M4 24GB 환경에서 **SOTA급 지능(眞)**과 **최고의 효율(善)**을 동시에 달성하게 하는 핵심 기술입니다.
