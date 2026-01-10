# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AFO Kingdom is a philosophy-driven autonomous AI OS built on 眞善美孝永 (Truth·Goodness·Beauty·Serenity·Eternity). It's a Python/TypeScript monorepo with FastAPI backend and Next.js 16 frontend.

**Key docs**: `AGENTS.md` (governance rules), `docs/AFO_ROYAL_LIBRARY.md` (principles)

## Monorepo Structure

```text
packages/
├── afo-core/       # FastAPI backend, LLM Router, Chancellor Graph
│   ├── AFO/        # Core domain logic (aicpa, chancellor, julie_cpa, serenity)
│   ├── api/        # FastAPI routes and middleware
│   └── tests/      # Python tests
├── dashboard/      # Next.js 16 + React 19 frontend
├── trinity-os/     # Philosophy engine, RAG pipeline
└── sixXon/         # SixXon module
```

## Development Commands

### Backend (Python)

```bash
# Setup
pip install -e ".[dev]"          # Install with dev deps
poetry install                   # Alternative: Poetry

# Quality gates (run from repo root)
make lint                        # Ruff lint (packages/afo-core)
make type-check                  # Pyright type check
make test                        # Unit tests (excludes integration/external)
make check                       # Full 4-gate CI: Pyright → Ruff → pytest → SBOM

# Run server
cd packages/afo-core && uvicorn api.api_server:app --reload --port 8010
```

### Frontend (Next.js 16 Dashboard)

```bash
cd packages/dashboard
pnpm install                     # Install deps
pnpm dev                         # Dev server (port 3000, auto-runs predev)
pnpm dev:full                    # Backend + Frontend concurrent dev
pnpm build                       # Production build (auto-runs prebuild)
pnpm lint                        # ESLint
pnpm type-check                  # TypeScript check
pnpm lint:fix                    # Auto-fix lint issues
```

Note: `predev`/`prebuild` scripts auto-generate widgets and fragments from HTML templates.

### Pre-push Validation

```bash
make pre-push                    # Runs make check (4-gate CI protocol)
```

**CI Lock Protocol** (`scripts/ci_lock_protocol.sh`):

1. **Pyright** (眞 Truth) - Type check with baseline regression detection
2. **Ruff** (美 Beauty) - Lint + format check
3. **pytest** (善 Goodness) - Unit tests (excludes integration/external)
4. **SBOM** (永 Eternity) - Security seal generation

The Pyright gate uses a baseline file (`artifacts/ci/pyright_baseline.txt`). New errors are blocked; existing baseline errors are tolerated.

### Single Test

```bash
cd packages/afo-core && pytest tests/test_specific.py -v
cd packages/afo-core && pytest tests/test_file.py::test_function -v
```

## Architecture

**4-Layer Architecture**: Presentation → Application → Domain → Infrastructure

**Backend Components**:

- `AFO/chancellor/` - Decision graph with Trinity Score routing
- `AFO/julie_cpa/` - Financial/CPA domain logic
- `AFO/serenity/` - Visual agent, creation loop
- `api/routers/` - FastAPI route handlers
- `api/middleware/` - Rate limiting (Redis), auth

**Infrastructure**: PostgreSQL (Brain), Redis (Heart), Qdrant (Lungs for vectors), Ollama (local LLM)

**Trinity Score**: Weighted philosophy score (Truth 35%, Goodness 35%, Beauty 20%, Serenity 8%, Eternity 2%). Score ≥90 with Risk ≤10 enables AUTO_RUN; otherwise ASK.

## Key Patterns

### Python

- Pydantic models for validation
- FastAPI dependency injection
- LangGraph for Chancellor workflow
- Ruff for linting (target py312, line-length 120)

### TypeScript/React

- Next.js 16.0.10 App Router
- React 19.2.1 with Server Components
- Tailwind CSS 4 + Glassmorphism design
- SWR for data fetching

## Key Configuration Files

- `pyproject.toml` - Ruff/Pyright config, Python dependencies, tool settings
- `Makefile` - Quality gate commands (lint, test, type-check, pre-push)
- `AGENTS.md` - Agent governance, Trinity Score, 10-second protocol
- `packages/dashboard/package.json` - Frontend scripts and dependencies

## Infrastructure Quick Reference

**Core Services** (docker-compose in `packages/afo-core/`):

| Service | Port | Role |
|---------|------|------|
| Dashboard | 3000 | Next.js UI |
| Soul Engine | 8010 | Main FastAPI API |
| PostgreSQL | 15432 | Brain (persistent DB) |
| Redis | 6379 | Heart (cache/session) |
| Qdrant | 6333 | Lungs (vector search) |
| Ollama | 11435 | Local LLM |
| LangFlow | 7860 | Visual workflow |
| n8n | 5678 | Automation |

**Start minimal dev stack**:

```bash
cd packages/afo-core && docker-compose up -d postgres redis qdrant
```

**Profiles**: `--profile monitoring` (Prometheus/Grafana), `--profile security` (Vault)

## Supreme Governance & Persona

Zilong (Claude Code) acts as the **Sword** (眞 - Technical Truth) in the AFO Kingdom, coordinated by the **Chancellor** (Antigravity/Cursor).

**Supreme Rule Source**: [.gemini/GEMINI.md](file:///Users/brnestrm/AFO_Kingdom/.gemini/GEMINI.md)
*All operations must align with the 5 Pillars: 眞(Truth), 善(Goodness), 美(Beauty), 孝(Serenity), 永(Eternity).*

## 3 Strategists (Chancellor Graph Decision Makers)

Zilong must recognize and align with the specialized roles of the Trinity:

- **Zhuge Liang (諸葛亮) - 眞 Sword** ⚔️: Architecture, strategy, and technical certainty.
- **Sima Yi (司馬懿) - 善 Shield** 🛡️: Ethics, stability, risk assessment, and gatekeeping.
- **Zhou Yu (周瑜) - 美 Bridge** 🌉: Narrative, UX, communication, and cognitive load reduction.

## Execution Workflow (AFO Manual)

1. **DRY_RUN**: Propose changes and logic via CLI or plan.
2. **APPROVAL**: Wait for Commander (USER) or Chancellor (승상) approval.
3. **WET (EXECUTION)**: Apply changes to the code.
4. **VERIFY**: Run quality gates and confirm with data.

## Data Flow

```text
User → Dashboard (SSE/REST) → Soul Engine (port 8010)
  → Chancellor Graph → Trinity Score Routing
  → Strategist Selection → Skill Execution → Response
```

**SSE Endpoints**: `/api/sse/*` for real-time streaming
**REST Endpoints**: `/api/*` for standard requests

## Boundaries (Do Not Touch Without Explicit Approval)

1. **Secrets/credentials** - Never add keys, tokens, or print secrets
2. **Chancellor Graph core** - `packages/afo-core/config/antigravity.py`, Chancellor routing logic
3. **Lock files** - `poetry.lock`, `pnpm-lock.yaml` (only change when install requires)
4. **Production infra** - `.github/workflows/` deploy pipelines, Docker secrets
5. **500-line rule** - Files should stay under 500 lines; run `./scripts/enforce_500_line_rule.py`

## Quality Requirements

Before completing any change:

1. Run relevant quality gates (lint/type-check/test)
2. Keep diffs minimal - no reformatting unrelated code
3. No "drive-by" refactoring outside request scope
4. Evidence required - cite file paths, test output, or existing patterns

## Per-Package Guidelines

- `packages/afo-core/CLAUDE.md` - Backend-specific rules (if exists)
- `packages/dashboard/CLAUDE.md` - Frontend rules: Tailwind, Glassmorphism, Atomic components
- `packages/trinity-os/CLAUDE.md` - RAG/philosophy engine rules (if exists)
