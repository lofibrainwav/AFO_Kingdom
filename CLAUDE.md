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
make type-check                  # MyPy type check
make test                        # Unit tests (excludes integration/external)
make test-integration            # Integration tests (needs PostgreSQL, Redis)
make check                       # Lint + test combined

# Run server
cd packages/afo-core && uvicorn api.api_server:app --reload --port 8010
```

### Frontend (Next.js Dashboard)

```bash
cd packages/dashboard
pnpm install                     # Install deps
pnpm dev                         # Dev server (port 3000)
pnpm build                       # Production build
pnpm lint                        # ESLint
pnpm type-check                  # TypeScript check
pnpm lint:fix                    # Auto-fix lint issues
```

### Pre-push Validation

```bash
make pre-push                    # Full validation: lint + type-check + test + scorecard
make ci-local                    # Above + security scan
```

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
- Ruff for linting (target py312, line-length 100)

### TypeScript/React

- Next.js 16 App Router
- React 19 with Server Components
- Tailwind CSS + Glassmorphism design
- SWR for data fetching

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
