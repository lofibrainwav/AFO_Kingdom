# AFO GenUI & Vision Capabilities (Operation Gwanggaeto)
**Date**: 2025-12-21
**Classification**: SYSTEM_CAPABILITY

## 1. GenUI Orchestrator (The Creator)
- **Role**: Generates React/Next.js components on demand.
- **Engine**: Uses `LLMRouter` (Ultra Tier) for "Royal Architect" level code.
- **Stack**: Next.js 16, Tailwind v4, Shadcn UI, Lucide Icons.
- **Workflow**: Vibe Prompt -> LLM Generation -> Critic Review -> File System.

## 2. Vision Verifier (The Eyes)
- **Role**: Physically verifies generated UIs using Playwright.
- **Capabilities**:
    - `verify_url(url, name)`: Screenshots and checks console errors.
    - **Self-Healing**: Detects Hydration errors and 404s.
- **Integration**: Called automatically after GenUI creation.

## 3. Julie Tax Engine (The Truth)
- **Backend**: `JulieService.py` (Python) handles all tax logic.
- **Frontend**: `JulieTaxWidget.tsx` (React) connects via `POST /api/julie/calculate-tax`.
- **Logic**: 2025 Federal/CA Rules, Surtax, QBI, 401k/HSA Advice.
- **Beauty**: Implements "Jade Bell" sound and Glassmorphism.

## 4. Usage
To generate a new component:
```python
orchestrator = GenUIOrchestrator()
result = await orchestrator.generate_component("Create a floating crypto ticker")
```

To verify it:
```python
verifier = VisionVerifier()
result = await verifier.verify_url("http://localhost:3000/genui/ticker", "crypto_ticker")
```
