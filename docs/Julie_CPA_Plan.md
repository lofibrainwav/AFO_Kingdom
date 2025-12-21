# Julie CPA AutoMate Implementation Plan (Phase 8)

## Goal
Integrate the existing **Julie CPA Frontend** (`AICPA/aicpa-core`) with the **AntiGravity Backend** (`afo-soul-engine`).
Shift from "Client-Side AI" to "Server-Side AI" to ensure **Goodness (Security)** and **Serenity (Zero Config)**.

## Current State Analysis (Truth)
- **Frontend**: React/Vite app on port `3005`.
- **AI Logic**: `geminiService.ts` calls Google Gemini API directly (Client-side).
- **Backend Link**: `trinityService.ts` attempts to call `localhost:8010` (Correct Port).
- **Security Risk**: API keys required in local `.env`, distinct from Vault.

## Proposed Architecture (Target)

### 1. Secure Link (Truth & Serenity)
- **Frontend**: Update `trinityService.ts` to target `http://localhost:8010` (Soul Engine Port).
- **Backend**: Create `api/routes/julie.py` to handle CPA requests.

### 2. Vault Integration (Goodness)
- **Problem**: Client-side keys are unsafe and create "Configuration Friction".
- **Solution**:
    1. Backend `JulieRouter` uses `VaultManager` to retrieve `GEMINI_API_KEY`.
    2. Frontend sends prompt to Backend -> Backend calls Gemini -> Returns result.
    3. User needs **Zero Configuration** in the frontend folder.

### 3. Implementation Steps

#### Phase 8-1: Bridge Repair
- [ ] [MODIFY] `AICPA/aicpa-core/services/trinityService.ts`: Fix port to `8010`.
- [ ] [NEW] `packages/afo-core/api/routes/julie.py`: Create basic health/status endpoint.
- [ ] [MODIFY] `packages/afo-core/api_server.py`: Register `julie_router`.

#### Phase 8-2: Brain Transplant (Server-Side AI)
- [ ] [MODIFY] `packages/afo-core/api/routes/julie.py`: Add `/api/julie/generate` endpoint.
    - Uses `vault_manager` for keys.
    - Uses `google-generative-ai` (Python SDK).
- [ ] [MODIFY] `AICPA/aicpa-core/services/geminiService.ts`: Replace direct calls with `fetch('/api/julie/generate')`.

## Verification Plan
- **Manual**: Run `npm run dev`, verify "Trinity Link" indicator is active.
- **Functional**: Send a prompt in the "Prompt Generator" tab and verify response without a local `.env` key.
