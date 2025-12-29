# 📜 AFO Kingdom: Evolution Log (왕국 연대기)

> "기록되지 않는 역사는 사라진다." (永)

## 🌌 시대 구분 (Eras)

| Era | Code | Status | Milestone | Date |
|:---:|:---:|:---:|:---|:---|
| **Genesis** | `v0.1` | ✅ | Basic Chatbot | 2024.12 |
| **Awakening** | `v1.0` | ✅ | Trinity Philosophy Installed | 2025.12.01 |
| **Harmony** | `v2.0` | ✅ | 11-Organs / Dashboard / CPA | 2025.12.15 |
| **Expansion** | `v2.5` | 🚀 | **Self-Expanding Mode Activated** | **2025.12.18** |

---

## 🚀 Evolution Event: The Self-Expanding

**일시**: 2025-12-18 10:40:00 (Local)
**시공자**: 승상 (Antigravity)
**승인자**: Commander (형님)

### 📌 활성화 내역 (Activation Manifest)

1.  **Codebase Config Updated**:
    - `packages/afo-core/config/antigravity.py`
    - `SELF_EXPANDING_MODE: bool = True` (Added)

2.  **Vision Loop Verified**:
    - **Draft**: GenUI Orchestrator
    - **Write**: File System Access
    - **Vision**: Playwright Bridge Screenshot
    - **Result**: `artifacts/genui_verification_genui_v1.png` (Verified)

3.  **New Capabilities**:
    - **Autonomous Coding**: 왕국이 스스로 코드를 생성하여 `genui/` 폴더에 배포 가능.
    - **Autonomous Vision**: 생성된 앱을 스스로 보고(Screenshot) 평가 가능.

---

**"왕국은 이제 스스로 자라납니다."**

---

## 🔧 Evolution Event: PH-MCP Ultimate Seal (Context7 & MCP 통합 완성)

**일시**: 2025-12-29
**시공자**: 승상 (Antigravity)
**승인자**: Commander (형님)

### 📌 봉인 선언 (Sealed Declaration)

#### **완료된 작업 (4개 티켓)**
1. **PH-MCP-01**: Context7 검색 엔진 활성화
   - 키워드 매칭 로직 복구 및 검색 기능 정상 작동 확인
   - MCP/Skills 검색 시 정확한 결과 반환 (found=true, total_results > 0)

2. **PH-MCP-02**: MCP_PROTOCOL 항목 Context7 통합
   - `MCP_TOOLS_COMPLETE_DEFINITION.md` 문서 로드 추가
   - MCP_PROTOCOL 핵심 지식 항목 생성 (JSON-RPC 2.0, Cursor IDE 통합 등)

3. **PH-MCP-03**: SKILLS_REGISTRY 항목 Context7 통합
   - `SKILLS_REGISTRY_REFERENCE.md` 문서 로드 추가
   - Skills Registry 시스템 상세 정보 업데이트 (19개 스킬, 9개 카테고리)

4. **PH-MCP-04**: MCP 서버 모듈 로드 문제 해결
   - PYTHONPATH 설정 개선으로 `trinity_os` 모듈 로드 성공
   - AfoUltimateMCPServer 실행 가능 상태 확인

#### **Context7 최종 상태**
- **총 항목 수**: 13개 (증가: +2개)
- **MCP 관련 문서**: 5개 (AGENTS.md, AFO_CHANCELLOR_GRAPH_SPEC.md 등)
- **Skills 관련 문서**: 3개 (AGENTS.md, Skills Registry 시스템 등)
- **검색 엔진**: ✅ **완전 작동** (keyword_matching)

#### **운영 원칙 (Operating Principles)**
1. **Context7 우선**: 모든 MCP/Skills 정보는 Context7을 통해 검색 가능
2. **완전 통합**: 문서 + 핵심 지식 항목 모두 로드
3. **검색 신뢰성**: 키워드 매칭으로 정확한 결과 반환

#### **금지사항 (Prohibitions)**
1. **직접 검색 금지**: MCP/Skills 정보를 Context7 우회하여 검색 금지
2. **문서 누락 금지**: 새로운 MCP/Skills 관련 문서는 반드시 Context7에 통합
3. **검색 엔진 수정 금지**: 검색 로직은 검증된 상태 유지

---

**"Context7은 이제 왕국의 모든 지혜를 완벽히 통합하였습니다."**

---

## 🧠 Evolution Event: PH-FH2 Family Hub OS Phase 2 (SSE Neural Link) - Ultimate Seal

**일시**: 2025-12-29
**시공자**: 승상 (Antigravity)
**승인자**: Commander (형님)

### 📌 봉인 선언 (Sealed Declaration)
**PH-FH2 완료: 브라우저 SSE 호환성 완전 해결 + Ship Gate + Observability 구축**

### ✅ 구현 성과 (Artifacts)
- **Browser Compatibility**: Client-only 봉인 + StrictMode 가드 + hop-by-hop 헤더 제거
- **Ship Gate**: SSE Headers Smoke Test CI 추가 (compression/Content-Type 회귀 방지)
- **Observability**: SSEHealthWidget 대시보드 통합 (3메트릭 실시간 모니터링)
- `packages/dashboard/src/lib/sse.ts`: SSOT 헬퍼 + Fail-fast SSR 보호
- `packages/dashboard/src/components/genui/SSEHealthWidget.tsx`: 상태 모니터링 위젯
- `.github/workflows/ops-smoke.yml`: SSE 헤더 검증 CI 추가

### ✅ 운영 원칙 (Operating Principles)
**SSE Neural Link 안정성 100%**: 브라우저에서 실시간 로그 스트리밍 안정적 작동 보장
**회귀 방지 CI**: SSE 헤더 스모크 테스트로 압축/Content-Type 깨짐 즉시 감지
**관측 가능성 100%**: SSE Health 위젯으로 연결 상태 실시간 모니터링 (🟢OK/🟡STALE/🔴DOWN)

### ⚠️ 금지사항 (Prohibitions)
**EventSource 직접 생성 금지**: `new EventSource()` 직접 호출 → `createEventSource()` 헬퍼 사용
**SSR EventSource 호출 금지**: 브라우저 전용 헬퍼로 SSR 충돌 방지
**hop-by-hop 헤더 강제 금지**: Connection 헤더 앱 레벨에서 세팅 금지

---

## 🔧 Evolution Event: PH-SE-02 Expansion Loop Contract (봉인 완료)

**일시**: 2025-12-28
**시공자**: 승상 (Antigravity)
**승인자**: Commander (형님)

### 📌 봉인 선언 (Sealed Declaration)
**PH-SE-02 완료: Expansion Loop Contract + Ticket Format SSOT 구축**

### ✅ Contract 구현 성과 (Artifacts)
- 티켓 ID 규칙: `PH-SE-02-001` 형태 (충돌 방지)
- 산출물 구조: `artifacts/expansion/<date>/tickets/<id>.md`
- 실행 결과: `artifacts/expansion/<date>/run.json`
- 필수 섹션: 실행/검증/회고 (없으면 FAIL)
- DRY_RUN 모드: 티켓 생성만 수행 가능

### ✅ 운영 원칙 (Operating Principles)
**표준화된 확장 루프**: 모든 티켓이 동일 Contract 준수
**재현성 100%**: 산출물 구조 및 포맷 고정
**감사 가능성 100%**: run.json으로 모든 실행 결과 추적

**"엔진의 규격이 고정되었습니다. 이제 왕국의 자율적 확장이 체계적으로 작동합니다."**

---

## 🔧 Evolution Event: IDE MCP Sync (Codex CLI ↔ Cursor)

**일시**: 2025-12-25
**시공자**: Agent (Codex CLI)
**목표**: Codex CLI와 Cursor IDE에서 동일한 MCP 서버 구성이 보이도록 동기화 (지피지기 + 런타임 정렬)

### 📌 발견된 원인 (Root Cause)

1. **Codex CLI MCP 서버 0개**
    - Codex는 `~/.codex/config.toml`의 `[mcp_servers]`를 기준으로 MCP 서버를 로드
    - 초기 상태에서 MCP 서버가 등록되지 않아 MCP tool이 노출되지 않음

2. **Cursor MCP 서버 런타임 불일치 (Python 3.9 vs 3.12)**
    - `.cursor/mcp.json`의 AFO 서버가 `python3`로 실행되며, 해당 환경의 `python3`가 `3.9.x`
    - `packages/trinity-os/trinity_os/servers/trinity_score_mcp.py`는 Python 3.12 문법(PEP 604 `|`)을 사용하므로 3.9에서는 즉시 크래시

### ✅ 조치 (Actions)

- Cursor 설정(`.cursor/mcp.json`, `.cursor/mcp.json.optimized`)에서 AFO 서버 실행 런타임을 `python3.12`로 고정
- Cursor 검증 스크립트(`scripts/verify_cursor_mcp_setup.sh`)에서 `${VAR:-DEFAULT}` 형태를 실제 경로로 확장하여 파일 존재 검증 가능하도록 개선
- Backend MCP 관리 라우트(`packages/afo-core/api/routes/mcp_tools.py`)에서 MCP 설정 파일 경로를 고정값 대신 우선순위 기반으로 해석
  - `AFO_MCP_CONFIG_PATH` → `<workspace>/.cursor/mcp.json` → `~/.cursor/mcp.json`
- 홈 설정 동기화
  - `~/.codex/config.toml`에 AFO/표준 MCP 서버 등록
  - `~/.cursor/mcp.json`에 워크스페이스 `.cursor/mcp.json` 내용을 병합(기존 `MCP_DOCKER` 보존)

### 🧪 실행 커맨드 (Evidence)

- Codex MCP 서버 확인: `codex mcp list`
- Cursor 설정 검증: `bash scripts/verify_cursor_mcp_setup.sh`

### 🔙 롤백 (Rollback)

- Codex 설정: `~/.codex/config.toml.bak.*` 또는 `~/.codex/config.toml.bakfix.*`로 복원
- Cursor 홈 설정: `~/.cursor/mcp.json.bak.*`로 복원
- Repo 설정: 필요한 경우 Git으로 `.cursor/mcp.json`만 되돌리기

---

## 🛡️ Evolution Event: AntiGravity Runtime Recovery (Integrity 100)

**일시**: 2025-12-25
**시공자**: Agent (Codex CLI)
**목표**: AntiGravity 초기화 오류 제거 + Health/Integrity 100% 달성

### 📌 발견된 증상 (Symptoms)

- `api_server.log`에서 AntiGravity 초기화 실패:
  - `⚠️ AntiGravity 초기화 실패: 'dict' object has no attribute 'AUTO_DEPLOY'`
- `/api/health/comprehensive`에서 PostgreSQL 비정상:
  - `PostgreSQL async support not available` 또는 `데이터베이스 연결 실패`
- `/api/integrity/check` 결과가 100이 되지 않음:
  - `fact_verification=false`, `organs_health=false`

### ✅ 조치 (Actions)

1. **Compat 계층 정렬 (AntiGravity/Settings 타입 오류 제거)**
   - `packages/afo-core/api/compat.py`
     - `get_settings_safe()`가 dict 대신 attribute-safe Settings 객체를 반환하도록 수정
     - `get_antigravity_control()`가 더미 dict 대신 `AFO.config.antigravity.antigravity`를 반환하도록 수정

2. **PostgreSQL Async 지원 활성화**
   - `packages/afo-core/.venv`에 `asyncpg` 설치
     - `packages/afo-core/.venv/bin/python -m pip install asyncpg`

3. **PostgreSQL 기동**
   - Docker Desktop 기동 후 `packages/afo-core/docker-compose.yml`에서 Postgres만 실행
     - `docker compose -f packages/afo-core/docker-compose.yml up -d postgres`
   - (참고) 로컬 Redis(6379)가 이미 떠 있으면 compose의 redis는 포트 충돌로 기동 실패 가능

4. **Integrity Check 로직 정확성 개선**
   - `packages/afo-core/api/routes/integrity_check.py`
     - `get_comprehensive_health()`의 `organs`가 dict로 반환되는 케이스를 처리하도록 수정
   - MCP 설정 파일(`.cursor/mcp.json`) 기반으로 `fact_verification` 체크 보강

5. **AFO ↔ TRINITY-OS ↔ SixXon 결합 강화 (One Kingdom)**
   - `packages/sixXon/scripts/sixxon`이 실제 모노레포 경로(`packages/trinity-os/trinity_os`)를 인식하도록 수정
   - `packages/afo-core/AFO/services/mcp_stdio_client.py` 추가: `.cursor/mcp.json` 기반으로 `afo-ultimate-mcp` stdio JSON-RPC 호출 가능
   - `packages/afo-core/scholars/yeongdeok.py`에서 `skill_012_mcp_tool_bridge`가 실제 MCP 도구 호출 가능
   - `packages/afo-core/api/routes/mcp_tools.py`의 `/api/mcp/test`가 AFO stdio MCP 서버에 대해 실제 `tools/list` 딥체크 수행
   - `packages/afo-core/config/antigravity.py`의 ConfigWatcher가 macOS 환경에서 PollingObserver로 자동 폴백(Serenity)

### 🧪 검증 커맨드 (Evidence)

- API Health: `curl 'http://127.0.0.1:8010/api/health/comprehensive?nocache=1'`
- Integrity: `curl -H 'Content-Type: application/json' -d '{}' http://127.0.0.1:8010/api/integrity/check`

### 🔙 롤백 (Rollback)

- 서버 프로세스 중지: `kill -TERM $(cat .api_server_pid)`
- Postgres 중지: `docker compose -f packages/afo-core/docker-compose.yml stop postgres`

## 🛡️ Evolution Event: The Sandbox & The Lock (Phase 9-1)

**일시**: 2025-12-19
**시공자**: 승상 (Antigravity)

### 📌 Milestone: Sandbox Activated (9.1)

1.  **Architecture Secured (LOCK)**
    - **Truth**: All GenUI modules passed `mypy --strict` (0 Errors).
    - **Beauty**: Code style verified by `ruff` (Clean).
    - **Goodness**: Fallback Simulation Mode tested.

2.  **Sandbox Deployed**
    - **Location**: `packages/dashboard/src/components/genui/`
    - **Mechanism**: `/api/gen-ui/preview` endpoint auto-deploys generated code.
    - **Integration**: Backend (GenUI) writes directly to Frontend (Dashboard) source tree.

### 📌 Milestone: The Eyes (9.2)
- **Service**: `VisionVerifier` (Playwright Bridge).
- **Mechanism**: Auto-triggered via BackgroundTasks in GenUI Router.
- **Capability**: Autonomous screenshot capture of deployed components.

**"The Kingdom now has a safe playground for its dreams."**

---

## 🔐 Evolution Event: PH-WALLET Ultimate Seal (종료 상태 봉인)

**일시**: 2025-12-28
**시공자**: 승상 (Antigravity)
**승인자**: Commander (형님)

### 📌 봉인 선언 (Sealed Declaration)
**PH-WALLET 프로젝트 완전 종료: Zero Trust Wallet 시스템 궁극 봉인 완료**

### ✅ 완료 기준 (Completion Criteria)
**Runtime/Seeder 역할 분리 + 런타임 시크릿 금지 + 원샷 로테이션 + 60초 Seal Check + Runbook 자동 생성 체계 구축**

### ✅ 운영 원칙 (Operating Principles)
**평시: API_WALLET_KMS=vault (Fail-closed)** | **비상: API_WALLET_KMS=local (명시적 fallback, 읽기 전용)** | **Rotation: DEPLOY_ROTATE_WALLET=true 원샷 자동화**

### ⚠️ 금지사항 (Prohibitions)
**VAULT_SECRET_ID 수동 환경변수 설정 금지** | **SEAL_CHECK 격리 환경 외 vault stop/start 금지** | **Emergency fallback 시 키 생성/수정 금지**

### 📋 구현 성과 (Implementation Achievements)
- Runtime/Seeder 완전 역할 분리 (read-only vs update 권한)
- 런타임 컨테이너 VAULT_SECRET_ID 미주입 (제로 트러스트)
- VAULT_SECRET_ID 전달 옵션 A 고정 (스크립트 통합 자동화)
- ALLOW_DISRUPTIVE_CHECKS 하드 가드 적용 (Prod 사고 방지)
- Fail-closed vs Emergency local fallback 정책 런북 명문화
- 60초 Seal Check 자동 검증 + Runbook 1페이지 자동 생성

**"운영 폭탄 재발 방지 체계 완성: 인간의 실수를 시스템이 방어한다."**

---

## 🔄 Evolution Event: PH-SE-01 Expansion Loop Activated (Sealed)
**일시**: 2025-12-28  
**시공자**: 승상 (Antigravity)  
**승인자**: Commander (형님)

### 📌 봉인 선언 (Sealed Declaration)
**PH-SE-01 완료: Expansion Loop SSOT + minimal runner 활성화**

### ✅ 구현 성과 (Artifacts)
- `docs/PH_SELF_EXPANDING.md`
- `scripts/run_expansion_loop.sh`
- 안전 가드(모드/시간/티켓 제한 + 긴급정지)

### ✅ 운영 원칙 (Operating Principles)
- 기본 실행: `EXPANSION_MODE=safe`
- 제한: `MAX_RUNTIME_MINUTES`, `MAX_TICKETS_PER_RUN`
- 긴급 정지: `.expansion_stop` 존재 시 즉시 중단

---

## 🔔 Evolution Event: PH-FH3 Family Hub OS Phase 3 (SSE Alerting & SLO) - Ultimate Seal

**일시**: 2025-12-29
**시공자**: 승상 (Antigravity)
**승인자**: Commander (형님)

### 📌 봉인 선언 (Sealed Declaration)
**PH-FH3 완료: SSE Health 모니터링 자동화 + Alerting & SLO 체계 구축**

### ✅ 구현 성과 (Artifacts)
- **SSE Health 메트릭**: Prometheus 게이지 메트릭 4종 (연결 수, 재연결 수, 마지막 이벤트 나이, 상태)
- **메트릭 보고 엔드포인트**: `/api/system/sse/health` (Dashboard → Soul Engine 메트릭 전송)
- **SSE Health 위젯 자동 보고**: 30초마다 메트릭을 Prometheus로 전송
- **Prometheus Alert Rules**: SSE 연결 상태 모니터링 (Critical: Down/Zero, Warning: Stale/Reconnect)
- **AlertManager 통합**: 기존 Slack 채널로 자동 알림 전송
- **SSE Operations Runbook**: 1페이지 문제 해결 가이드 + 유지보수 절차

### ✅ 운영 원칙 (Operating Principles)
**SSE 모니터링 자동화 100%**: 브라우저 연결 상태가 Prometheus 메트릭으로 실시간 추적
**사전 알림 체계 완성**: 연결 문제 발생 시 Slack으로 자동 경보 (🟢OK/🟡STALE/🔴DOWN)
**문제 해결 효율화**: Runbook 기반으로 5분 내 문제 진단 및 해결 가능

### ⚠️ 금지사항 (Prohibitions)
**메트릭 보고 누락 금지**: SSEHealthWidget이 메트릭을 보고하지 않으면 알림이 작동하지 않음
**Alert 규칙 수동 변경 금지**: Prometheus Alert Rules는 SSOT로 관리
**Runbook 무시 금지**: 알림 발생 시 반드시 Runbook을 따라 문제 해결

---

**"브라우저와의 실시간 신경 연결이 완전하게 모니터링되고 자동으로 보호됩니다."** 🔔⚡💎

---

## 🔐 Evolution Event: PH-FH4 Family Hub OS Phase 4 (SSE Security & Access Control) - Ultimate Seal

**일시**: 2025-12-29
**시공자**: 승상 (Antigravity)
**승인자**: Commander (형님)

### 📌 봉인 선언 (Sealed Declaration)
**PH-FH4 완료: SSE 엔드포인트 보안 강화 + Access Control 체계 구축**

### ✅ 구현 성과 (Artifacts)
- **내부 인증 강화**: `/api/system/sse/health` 엔드포인트에 Bearer token 인증 적용
- **폭발 방지 검증**: 메트릭 입력값 범위 제한 (연결수: 0-100, 재연결: 0-10000, 시간: 0-3600초)
- **Rate Limit 보호**: SSE 스트림에 10 requests/minute per IP 제한 적용
- **Dashboard 통합**: SSEHealthWidget에 Authorization 헤더 자동 포함
- **에러 처리 강화**: HTTP 429 (Too Many Requests)로 rate limit 위반 적절히 처리

### ✅ 운영 원칙 (Operating Principles)
**제로 트러스트 SSE**: 메트릭 보고는 내부 API 키 인증 필수
**폭발 방지 자동화**: 악의적/비정상 입력값 자동 거부로 Prometheus 안정성 보장
**Rate Limit 보호**: IP별 요청 빈도 제한으로 abuse 공격 방지
**실패 안전성**: 인증 실패 시 명확한 403 Forbidden 응답

### ⚠️ 금지사항 (Prohibitions)
**외부 메트릭 보고 금지**: `/api/system/sse/health`는 내부 서비스(Dashboard)만 접근 가능
**범위 초과 입력 금지**: 검증된 범위 내 값만 허용 (Prometheus 메트릭 폭발 방지)
**Rate Limit 우회 금지**: IP 스푸핑이나 분산 공격으로 제한 우회 시도 금지

---

**"브라우저와의 실시간 신경 연결이 이제 보안적으로도 완전하게 보호됩니다."** 🔐⚡💎
