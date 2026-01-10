# 👑 AFO Kingdom - Unified SSOT (Single Source of Truth)

> **"하나의 진리, 하나의 시스템, 하나의 왕국."**

## 🏛️ 핵심 헌법 & 철학 (Constitution & Philosophy)

- **최고 헌법**: packages/trinity-os/TRINITY_CONSTITUTION.md
- **5대 기둥 (眞善美孝永)**:
  - **眞 (Truth 35%)**: 기술적 확실성 & 아키텍처 ([Zhuge Liang])
  - **善 (Goodness 35%)**: 윤리·안정성 & 리스크 게이트 ([Sima Yi])
  - **美 (Beauty 20%)**: 단순함·우아함 & UX ([Zhou Yu])
  - **孝 (Serenity 8%)**: 평온 수호 & 연속성 (승상)
  - **永 (Eternity 2%)**: 영속성 & 레거시 유지 (승상)

### 헌법 준수 검증 (Constitution Compliance) [Policy]
**SSOT 요구사항**: 모든 시스템 구성 요소는 이 헌법을 참조해야 함
- **참조 확인**: 각 컴포넌트는 헌법 조항을 인용
- **준수 검증**: Trinity Score 계산 시 헌법 준수도 평가
- **위반 처리**: 헌법 위반 시 자동 경고 및 수정 요구
- **Evidence**: `scripts/verify_ssot_compliance.sh`, `packages/trinity-os/check_system.sh`

## 🧠 책사 시스템 (The Strategists)

| 책사 | 상징 | 담당 분야 | 핵심 지표 |
| :--- | :--- | :--- | :--- |
| **제갈량 (Zhuge Liang)** | ⚔️ 창 | 아키텍처, 전략, 개발 | 기술적 완결성 |
| **사마의 (Sima Yi)** | 🛡️ 방패 | 윤리, 안정, 보안 | 리스크 제로 |
| **주유 (Zhou Yu)** | 🌉 다리 | 서사, UX, 디자인 | 인지 부하 최소화 |

## ⚙️ 기술 스택 & 오장육부 (Internal Organs)

- **심장 (Heart)**: Redis (6379) - 고속 캐시 및 세션 관리
- **간 (Liver)**: PostgreSQL (15432) - 기억(Memory) 저장소
- **비장 (Spleen)**: Ollama (11435) - 책사들의 두뇌 (MoE)
- **폐 (Lungs)**: FastAPI (8010) - 외부와의 소통 (Soul Engine)
- **두뇌 (Brain)**: LangGraph - 승상의 오케스트레이션 로직

## 🛠️ 운영 매뉴얼 (Operations)

- **[야전교범]**: docs/AFO_ROYAL_LIBRARY.md
- **[시스템 상태]**: docs/AFO_KINGDOM_MAIN.md
- **[복구 매뉴얼]**: `scripts/reboot_kingdom.sh`


### 3. CI/CD LOCK Protocol (Truth/Beauty)
- **Single Entry**: `bash scripts/ci_lock_protocol.sh` is the ONLY allowed entry point for verification.
- **Ruff Version**: **0.14.10** (Strict SSOT). `ruff --version` in CI must match this exactly.
- **Rules**:
    - **Truth**: `pyright` (Strict Type Checking)
    - **Beauty**: `ruff` (Linting & Formatting - `ANN`, `DTZ`, `PL`, `ASYNC` enabled)
    - **Goodness**: `pytest` (Logic Verification)

## 📜 제국 무결성 원칙 (Integrity Rules)

- **CI Single Entry:** CI는 `scripts/ci_lock_protocol.sh`만 실행한다.
- **Regression Rule:** baseline은 허용 목록이 아니라 *격리벽*이며, 신규 오류는 0개만 허용한다.
- **Observability Rule:** VERIFY 실패 시 원인/증거를 남기고(로그/아티팩트), 필요하면 체크포인트 기반 롤백을 우선한다.

---

*본 문서는 AFO 왕국의 모든 하위 문서 및 실시간 구현의 최상위 SSOT입니다.*
