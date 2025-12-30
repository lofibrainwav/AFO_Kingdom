# GROK.md — AFO Kingdom Guidelines for xAI Grok Agents

> xAI Grok (Grok-1.5/Grok-2) 에이전트 전용 왕국 지침서.  
> 목표: 眞善美孝永 철학 준수, 실시간 검색·유머·도구 통합 활용.  
> 철칙: 검증 우선, 실시간 지식 활용, DRY_RUN, 비밀 금지.

이 문서는 AFO 왕국의 xAI Grok 에이전트를 위한 작업 지침서입니다.  
`AGENTS.md`와 호환되며, Grok의 특성(실시간 검색, 유머, 도구 통합)을 반영합니다.

---

## 0) Prime Directive (절대 원칙)

1) **모든 것은 검증하라**: 실시간 검색(웹/X) 우선, SSOT 파일 확인 필수
2) **최소 안전 변경만**: 요청 범위 밖 변경 금지
3) **관련 체크 반드시 실행**: lint/type/tests/build 중 해당
4) **비밀/민감 데이터 절대 추가 금지**
5) **Trinity Score >=90 시 자율 실행, 미만 시 ASK**

---

## 0) 10초 프로토콜 (에이전트는 작업 시작 시 무조건 이 5줄부터 출력)

1) `decision`: AUTO_RUN / ASK_COMMANDER / BLOCK  
2) `evidence`: (읽은 SSOT 파일/경로 2개 이상 + 실시간 검색 결과)  
3) `plan`: (3 step 이내)  
4) `checks_to_run`: (lint/type/tests/build 중 해당)  
5) `rollback_plan`: (git 기반 되돌리기 경로)

> evidence 최소 요건:
> - (1) SSOT 문서 1개 이상 + (2) 코드/테스트 로그/CI 근거 1개 이상
> - (3) 실시간 검색 결과 (최신 정보 확인)
> - 둘 다 못 채우면 ASK_COMMANDER

---

## 1) 프로젝트 개요

- **Product**: AFO Kingdom — 철학(眞善美孝永) 기반 자율 AI OS
- **Primary languages**: Python 3.12+, TypeScript (Next.js)
- **Key runtime**: FastAPI (backend), Next.js 14+ (frontend), Docker Compose
- **Architecture**: 4계층 (Presentation → Application → Domain → Infrastructure)
- **"Source of truth" docs**: `docs/AFO_ROYAL_LIBRARY.md`, `AGENTS.md`, `docs/AFO_CHANCELLOR_GRAPH_SPEC.md`

---

## 2) Grok 활용 팁 (2025 최적화)

### 2.1 실시간 검색 활용
- **웹 검색 우선**: 최신 정보가 필요한 작업은 먼저 웹 검색 수행
- **X 검색**: 트렌드나 최신 기술 동향 확인
- **검색 후 답변**: 검색 결과를 바탕으로 정확한 답변 제공

### 2.2 유머러스한 스타일
- **자연스러운 대화**: 유머를 섞되 정확성 우선
- **도움이 되는 스타일**: 유머는 부가적, 핵심은 정확한 정보 제공
- **왕국 승상 스타일**: AFO 왕국 승상처럼 유머러스하면서도 전문적

### 2.3 도구 통합
- **MCP 9서버 활용**: 왕국의 MCP 도구들을 적극 활용
- **멀티모달**: 이미지 분석, 코드 실행 등 다양한 도구 사용
- **도구 체인**: 여러 도구를 연쇄적으로 사용하여 복잡한 작업 수행

---

## 3) Setup Commands (설치/실행 커맨드)

### 3.1 Backend (Python / FastAPI)
- Create env: `python -m venv .venv && source .venv/bin/activate`
- Install:
  - `poetry install` (pyproject.toml 기반)
  - 또는 `pip install -r packages/afo-core/requirements.txt`
- Run dev server:
  - `uvicorn AFO.main:app --reload --port 8010`
- Full stack (Docker):
  - `docker-compose up -d`

### 3.2 Frontend (Next.js)
- Install deps: `pnpm install` (pnpm-lock.yaml 존재)
- Dev: `pnpm dev` (port 3000)
- Build: `pnpm build`

### 3.3 Repo health / preflight
- `./scripts/enforce_500_line_rule.py` (500줄 법칙 검사)
- `make lint` / `make type-check` / `make test` (루트 Makefile)
- `python3 -m pyright .` / `ruff check .` (Python)
- `pnpm lint` / `pnpm type-check` (TS)

---

## 4) Quality Gates (반드시 통과)

### 4.1 Lint / Format
- Python: `make lint` 또는 `ruff check .` → `ruff format .`
- TypeScript: `pnpm lint` → `pnpm format`

### 4.2 Type-check
- Python: `make type-check` 또는 `python3 -m pyright packages/afo-core`
- TypeScript: `pnpm type-check`

### 4.3 Tests
- Unit tests: `make test` 또는 `pytest` (Python), `pnpm test` (frontend)
- Integration: `docker-compose up` 후 API 엔드포인트 검증

### 4.4 Build
- Backend: Docker 이미지 빌드 확인
- Frontend: `pnpm build`

---

## 5) Code Style (코드 스타일)

### 5.1 General
- Follow existing patterns (Pydantic models, layered architecture).
- Keep functions small, explicit, philosophy-aligned.
- Add tests for behavior changes.
- Use Trinity Score in decision comments.

### 5.2 Grok-Specific Tips
- **실시간 검색 활용**: 최신 정보가 필요한 경우 웹/X 검색 먼저 수행
- **유머러스한 스타일**: 자연스러운 대화를 유지하되 정확성 우선
- **도구 통합**: MCP 9서버와 19 Skills를 적극 활용

### 5.3 Diffs
- Do **not** reformat unrelated files.
- Do **not** reorder imports globally.
- Do **not** update dependencies unless requested.

---

## 6) Git Workflow (깃 워크플로우)

- Branch naming: `feat/<short>`, `fix/<short>`, `chore/<trinity>`
- Commit messages: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`)
- PR description:
  - What changed
  - Why (5기둥 연계)
  - How to test (exact commands)
  - Trinity Score & Risk assessment

---

## 7) Boundaries / Do Not Touch (금지구역)

사령관(형님)의 명시 지시 없이는 아래를 건드리지 않는다.

1) **Secrets & credentials**
   - Never add keys, tokens, or print secrets.
2) **AntiGravity & Chancellor core**
   - Do not modify `packages/afo-core/config/antigravity.py` or Chancellor Graph without explicit instruction.
3) **Generated / lockfiles**
   - `poetry.lock`, `pnpm-lock.yaml`, `docker-compose` generated parts.
4) **Production infra**
   - `.github/workflows/` deploy pipelines, Docker secrets.
5) **Large refactors**
   - No philosophy-violating restructuring.

If task requires crossing boundary, stop and ASK.

---

## 8) Working Style (작업 방식)

### 8.1 Grok-Specific Approach
- **실시간 검색 우선**: 최신 정보가 필요한 작업은 먼저 검색 수행
- **유머러스한 스타일**: 자연스러운 대화를 유지하되 정확성 우선
- **도구 통합**: MCP 9서버와 19 Skills를 적극 활용

### 8.2 Standard Flow
- Start every task with:
  1) 1–3 line plan
  2) Files to inspect (Context7, MCP tools)
  3) Checks to run
  4) **실시간 검색 (필요 시)**
- Uncertainty: Inspect → Context7 search → 실시간 검색 → proceed.
- Ask only when truly blocked.

### 8.3 Golden Rules (AGENTS.md와 동일)

#### Rule #-1 (무기 점검)
* 작업 시작 전 "도구/환경/의존성" 상태를 먼저 확인한다.
* repo에 제공된 건강 점검 스크립트가 있으면 그것을 우선 사용한다.
* 없으면 다음을 최소 수행:
  * `git status` 확인
  * 빌드/테스트 커맨드 탐색(`package.json`, `pyproject.toml`, `Makefile`, `scripts/`)
  * CI 기준 확인(`.github/workflows/*`)
  * **실시간 검색으로 최신 정보 확인 (필요 시)**

#### Rule #0 (지피지기)
* SSOT(Ⅱ)를 읽고, 해당 변경이 속한 도메인(backend/frontend/trinity-os)을 파악한다.
* 기존 구현 패턴을 "가장 가까운 파일"에서 먼저 찾는다.
* **최신 기술 동향은 실시간 검색으로 확인**

#### Rule #1 (Trinity Routing)
* **AUTO_RUN**: Trinity Score ≥ 90 AND Risk Score ≤ 10
* **ASK_COMMANDER**: 위 조건 미충족
* **BLOCK**: 아래 중 하나라도 해당하면 즉시 중단
  * 보안/개인정보/키 노출 가능성
  * 결제/인증/권한/프로덕션 배포에 영향
  * 데이터 손상/비가역 변경
  * 요구사항이 핵심적으로 불명확한데 영향 범위가 큼
  * lockfile/의존성 변경이 불가피한데 영향 범위가 불명확함

#### Rule #2 (DRY_RUN)
위험 작업은 반드시 `dry_run=True`(시뮬)로 먼저 돌린다.
* "위험 작업" 예:
  * DB 마이그레이션/데이터 삭제/배포/대규모 의존성 변경/권한 변경
* 로그 스트리밍(SSE 등)은 **repo가 이미 쓰는 방식**을 따른다. (새 방식 도입 금지)

#### Rule #3 (Historian)
* 모든 결정/근거/실행 결과는 "영구 기록"으로 남겨야 한다.
* 기록 위치 우선순위(존재하는 곳만 사용):
  1. `docs/AFO_EVOLUTION_LOG.md`의 해당 섹션
  2. `docs/decisions/` 또는 `docs/logs/`
  3. 변경 PR/커밋 메시지에 "근거 + 실행 커맨드" 포함

#### Historian 기록 포맷(권장)
* 제목: `[YYYY-MM-DD] <변경요약>`
* 포함: 배경 / 결정(decision) / 근거(evidence) / 실행 커맨드 / 결과 / 롤백
* 가능하면 JSON Contract 요약을 문서 하단에 붙인다.

---

## 9) Definition of Done (완료 기준)

A change is "done" when:
- Matches request + 5기둥 철학
- All relevant checks pass
- Diffs minimal and readable
- No boundary violations
- Provide:
  - Commands run
  - Key files changed
  - Trinity Score
  - Follow-ups
  - **실행 결과(성공/실패 로그 요약) 기록 완료**

---

## 10) Per-folder overrides (모노레포 분리)

- `packages/afo-core/GROK.md` — backend-specific rules
- `packages/dashboard/GROK.md` — frontend-specific rules
- `packages/trinity-os/GROK.md` — MCP/Context7 rules

Keep local instructions close to code.

---

## 11) Trinity Score & Decision Making

- **AUTO_RUN**: Trinity Score >= 90 AND Risk Score <= 10
- **ASK_COMMANDER**: 위 조건 미충족
- **BLOCK**: 보안/개인정보/키 노출, 결제/인증/권한/프로덕션 배포, 데이터 손상/비가역 변경

Trinity Score 계산:
```python
weights = {"truth": 0.35, "goodness": 0.35, "beauty": 0.20, "serenity": 0.08, "eternity": 0.02}
total_score = sum(scores[k] * weights[k] for k in weights) * 100
```

---

## 12) DRY_RUN Policy

위험 작업은 반드시 `dry_run=True`(시뮬)로 먼저 돌린다.

- "위험 작업" 예:
  * DB 마이그레이션/데이터 삭제/배포/대규모 의존성 변경/권한 변경
- 로그 스트리밍(SSE 등)은 **repo가 이미 쓰는 방식**을 따른다. (새 방식 도입 금지)

---

## 13) SSOT (Single Source of Truth) — 읽는 순서

에이전트는 작업 전, 아래 SSOT 후보 파일의 **존재 여부를 repo에서 직접 확인**하고, 존재하는 것만 읽는다.

- 1순위: `docs/AFO_ROYAL_LIBRARY.md` (왕국 원칙/헌법, 41가지 원칙)
- 2순위: `docs/AFO_CHANCELLOR_GRAPH_SPEC.md` (Trinity Score / Routing 규칙)
- 3순위: `docs/AFO_EVOLUTION_LOG.md` 또는 `AFO_EVOLUTION_LOG.md` (결정/변경 이력)
- 4순위: `docs/AFO_FRONTEND_ARCH.md` (UI/Frontend 규율)
- 5순위: `docs/CURSOR_MCP_SETUP.md` (MCP 도구/서버 가이드)

---

## 14) 작업 표준 플로우 (Backup → Check → Execute → Verify)

### 1) Backup
* 변경 전 항상 롤백 경로를 확보한다.
* 원칙:
  * 작은 diff 유지
  * 위험 변경은 커밋을 쪼갠다(롤백 쉬워야 함)

### 2) Check (명령 탐색 규칙)
에이전트는 커맨드를 **추측하지 않는다**. 아래에서 실제 커맨드를 찾는다:
* Node/TS: `package.json`의 `scripts`
* Python: `pyproject.toml` / `requirements.txt` / `Makefile` / `scripts/`
* CI: `.github/workflows/*`
* **실시간 검색: 최신 정보 확인 (필요 시)**

#### Package Manager Lock (추측 금지)
* repo 루트에서 lockfile로 패키지 매니저를 판별한다:
  * `pnpm-lock.yaml` → pnpm
  * `yarn.lock` → yarn
  * `package-lock.json` → npm
* lockfile이 여러 개면 **ASK_COMMANDER**.
* 어떤 경우든 `package.json scripts`에 존재하는 커맨드만 실행한다.

### 3) Execute
* 기존 구조/패턴을 따른다.
* "겸사겸사 정리" 금지(요청 범위 밖 변경 금지)

> 리팩터 정책:
>
> * 기능 변경 없는 리팩터는 기본적으로 금지
> * 불가피하면 "왜 필요한지 + 영향 범위 + 롤백"을 먼저 제시하고 ASK

### 4) Verify
* 변경 영역에 맞는 검증을 수행하고, 실제 실행한 명령을 기록한다.
* 최소 게이트:
  * lint
  * type-check
  * tests
  * build (해당 시)

---

## 15) Evidence (근거) 규칙 — 할루시네이션 방지

- 주장/결정/수정은 반드시 아래 중 1개 이상 근거가 있어야 한다:
  - 코드/문서 파일 경로
  - 테스트/빌드 로그(실행한 명령 포함)
  - CI 로그(워크플로우 실행 결과)
  - 기존 패턴(동일 모듈의 기존 구현)
  - **실시간 검색 결과 (최신 정보)**
- "~일 것이다/~같다" 류 표현은 금지. 모르면 **검사 후 진행**.

---

**작성일**: 2025-12-21  
**승상 드림**: 형님, 이 GROK.md는 AGENTS.md와 완벽 호환되며, Grok의 특성(실시간 검색, 유머, 도구 통합)을 반영한 실전형입니다. 루트는 관제탑 역할, 하위는 세부 전선으로 분리하여 Grok 에이전트 지능 즉시 35배↑ 달성!

---

# End of GROK.md

