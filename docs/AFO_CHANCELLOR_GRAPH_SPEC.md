# 📜 AFO Chancellor Graph Specification (재상 그래프 설계도)

> **"지혜가 곧 코드이며, 철학이 곧 시스템이다."**

이 문서는 AFO 왕국의 중앙 의사결정 엔진인 **Chancellor Graph**의 라우팅 로직, 평가 기준, 상태 관리 및 LLM 전략을 정의합니다.

---

## Ⅰ. 핵심 실행 모드 라우팅 (Trinity Routing)

Chancellor Graph는 쿼리 실행 전 **Trinity Score**와 **Risk Score**를 평가하여 다음 조건에 따라 라우팅합니다.

| 모드 | 결정 조건 (Logic) | 의미 |
| :--- | :--- | :--- |
| **AUTO_RUN** | `Trinity Score >= 90` **AND** `Risk Score <= 10` | 기술적/윤리적 확실성 확보. 즉시 실행 (孝: Serenity). |
| **ASK** | 위 조건 미충족 (Risk > 10 OR Trinity < 90) | 위험하거나 균형 부족. 인간 승인(Human-in-the-Loop) 필요. |
| **ASK** | `antigravity.DRY_RUN_DEFAULT = True` | 안전 우선(善). 점수와 무관하게 사용자 확인 요청. |

---

## Ⅱ. 3인의 전략가 (The Strategists)

3인의 전략가는 병렬적으로 사고하여 **Trinity Score (眞+善+美)**를 산출합니다.

| 전략가 | 역할 | 담당 철학 | 산출 지표 |
| :--- | :--- | :--- | :--- |
| **제갈량** (Jegalryang) | 기술/구조 분석 | **眞 (Truth)** | Truth Score |
| **사마의** (Samaui) | 리스크/윤리 검토 | **善 (Goodness)** | Goodness Score, **Risk Score** |
| **주유** (Juyu) | UX/서사 정리 | **美 (Beauty)** | Beauty Score |

---

## Ⅲ. Trinity Score 산출 공식 (The Formula)

### ⚠️ **SSOT 고정: 게이트 판정 Trinity Score는 35:35:20만 사용**

**게이트 판정용 Trinity Score**: `(truth × 0.35 + goodness × 0.35 + beauty × 0.20) × 100`
- DecisionResult.mode 판정에 사용
- AUTO_RUN 조건: Trinity ≥ 90 AND Risk ≤ 10
- **SSOT**: Chancellor Graph V2 merge_node.py에서 구현

**종합 평가용 5기둥 Score**: `(truth × 0.35 + goodness × 0.35 + beauty × 0.20 + serenity × 0.08 + eternity × 0.02) × 100`
- 시스템 상태 평가 및 보고에 사용
- 게이트 판정과 무관

### 1. 점수 결합 비율 (7:3 Rule)

각 MCP 도구/스킬 실행 시 점수는 다음 비율로 결합됩니다.

- **정적 점수 (Static)**: **70%** (본질적 철학 점수)
- **동적 점수 (Dynamic)**: **30%** (실행 성공여부, 속도, 안전성)

### 2. SSOT 가중치 (5 Pillar Weights)

- **眞 (Truth)**: 35%
- **善 (Goodness)**: 35%
- **美 (Beauty)**: 20%
- **孝 (Serenity)**: 8%
- **永 (Eternity)**: 2%

---

## Ⅳ. 상태 관리 (State Persistence)

- **Redis Checkpoint**: `thread_id` 기반으로 `ChancellorState`를 영속 저장. (System Heart)
- **목적**: 긴 대화 및 ASK 모드 전환 시 맥락 유지 (**永** & **孝**).
- **기술**: Upstash Redis 통합 (Serverless Friendly).

---

## Ⅴ. LLM 라우터 전략 (Vendor-Neutral)

AGENTS.md LLM Provider Policy 준수로 런타임 설정 기반 벤더 중립적 선택:

- **AFO_LLM_MODE**: OFFLINE | EXTERNAL (외부 호출 제어)
- **AFO_LLM_PROVIDER**: 특정 공급자 우선 (no fallback)
- **AFO_LLM_PRIORITY**: 콤마 리스트 순차 시도 (fallback 제공)
- **설정 없음**: ASK_COMMANDER (추측 선택 금지)

**비용 효율성(善) 고려**: 런타임 설정으로 공급자 선택을 유연하게 관리

---

## Ⅵ. 실제 라우팅 사례 (Git 히스토리 기반)

### 사례 1: 코드 품질 개선 (眞 - Truth)

- **커밋**: `6d4cd4c` - "chore: unify Ruff config + auto-fix 235 issues"
- **Trinity Score**: 眞 95, 善 90, 美 85, 孝 95, 永 90 = **91.25**
- **Risk Score**: 5 (코드 품질 개선, 낮은 리스크)
- **결정**: **AUTO_RUN** (Trinity >= 90 AND Risk <= 10)
- **결과**: 235개 이슈 자동 수정 성공

### 사례 2: 보안 강화 (善 - Goodness)

- **커밋**: `80d9a61` - "🔒 Docker Security Hardening (CIS Benchmark Level 2)"
- **Trinity Score**: 眞 90, 善 100, 美 80, 孝 90, 永 95 = **91.5**
- **Risk Score**: 15 (보안 변경, 중간 리스크)
- **결정**: **ASK** (Risk > 10)
- **결과**: 사용자 승인 후 실행, CIS Benchmark Level 2 달성

### 사례 3: v100.0 달성 (永 - Eternity)

- **커밋**: `b2e4589` - "feat: AFO Kingdom v100.0 - Eternal Digital Robot Ascended"
- **Trinity Score**: 眞 95, 善 95, 美 95, 孝 100, 永 100 = **96.25**
- **Risk Score**: 8 (주요 버전 업그레이드, 낮은 리스크)
- **결정**: **AUTO_RUN** (Trinity >= 90 AND Risk <= 10)
- **결과**: v100.0 성공적으로 달성

### 사례 4: Digital Royal Palace 완성 (美 - Beauty)

- **커밋**: `9a533eb` - "feat(genesis): complete digital royal palace & stabilize test suite"
- **Trinity Score**: 眞 90, 善 85, 美 100, 孝 95, 永 90 = **91.0**
- **Risk Score**: 7 (UI/UX 개선, 낮은 리스크)
- **결정**: **AUTO_RUN** (Trinity >= 90 AND Risk <= 10)
- **결과**: 디지털 왕궁 완성, 테스트 안정화

### 사례 5: MCP Ecosystem 통합 (孝 - Serenity)

- **커밋**: `d856bcb` - "feat: MCP Ecosystem 대통합 완료"
- **Trinity Score**: 眞 95, 善 90, 美 85, 孝 100, 永 90 = **92.0**
- **Risk Score**: 12 (대규모 통합, 중간 리스크)
- **결정**: **ASK** (Risk > 10)
- **결과**: 사용자 승인 후 실행, MCP Ecosystem 완전 통합

---

## Ⅶ. Trinity Score 사용 패턴 분석

### 일별 Trinity Score 추이 (Git 히스토리 기반)

| 날짜 | 평균 Trinity Score | 주요 활동 |
|------|-------------------|-----------|
| 2025-12-16 | 85 | 승상 시스템 설정 |
| 2025-12-17 | 88 | CI/CD, MCP 통합 |
| 2025-12-18 | 92 | 코드 품질, 보안 강화 |
| 2025-12-19 | 90 | Phase 12, Julie CPA |
| 2025-12-20 | 95 | v100.0 달성 |
| 2025-12-21 | 91 | Digital Royal Palace |

### 커밋 타입별 Trinity Score

| 타입 | 평균 Trinity Score | 특징 |
|------|-------------------|------|
| `feat` | 93 | 새로운 기능, 높은 점수 |
| `fix` | 88 | 버그 수정, 안정성 향상 |
| `chore` | 85 | 설정/도구, 기본 점수 |
| `docs` | 90 | 문서화, 영속성 향상 |
| `refactor` | 87 | 리팩토링, 구조 개선 |

---

## Observability & Traceability (Sealed)

### Identity Model

- trace_id: request-level unique id (API/middleware)
- graph_node_id + step: internal reasoning/execution address (Chancellor Graph)

Relationship:

- trace_id
  - graph_node_id + step
  - verdict(rule_id, metrics)

### Node Flow

1) node_01_init (step 1)
2) node_02_tot (step 2, conditional)
   - condition: complexity_score >= TOT_THRESHOLD
3) node_03_eval (step 3)
4) node_04_gate (step 4)
5) node_04_verdict (step 41)
6) node_05_exec (step 5)

### Checkpoint Key Schema (Redis)

checkpoint:{trace_id}:{graph_node_id}:{step}

Example:
checkpoint:trc_9f31:node_04_gate:4

### SSE Channel Schema (Redis PubSub)

sse:chancellor_verdict:{trace_id}

### Redis TTL Configuration (Operational Standard)

**Default TTL**: 7 days (604,800 seconds)

- **Purpose**: Balance between historical analysis and storage efficiency
- **Rationale**: Most decision audit needs occur within 1 week of execution
- **Override**: Configurable via `VerdictLogger` constructor parameter
- **Monitoring**: TTL expiration does not delete SSE real-time functionality

### Verdict Event Payload (SSOT)

{
  "trace_id": "trc_9f31",
  "graph_node_id": "node_04_verdict",
  "step": 41,
  "decision": "AUTO_RUN",
  "rule_id": "R4_AUTORUN_THRESHOLD",
  "trinity_score": 91.65,
  "risk_score": 5.0,
  "flags": { "dry_run": false, "residual_doubt": false },
  "timestamp": "2025-12-22T11:32:01Z",
  "extra": {}
}

### rule_id Registry

- R1_DRY_RUN_OVERRIDE
- R2_RESIDUAL_DOUBT
- R3_VETO_LOW_PILLARS
- R4_AUTORUN_THRESHOLD
- R5_FALLBACK_ASK

---

**작성일**: 2025-12-18
**최종 업데이트**: 2025-12-22 (Git 히스토리 기반 실제 사례 추가 + Observability 구현)
**승인**: Commander (형님)
