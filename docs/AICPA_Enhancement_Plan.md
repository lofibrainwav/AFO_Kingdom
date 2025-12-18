# AICPA_Julie Enhancement Plan

## Goal
Transform the "AI Studio" frontend into the true **Julie CPA AutoMate** interface.
**Missing Parts**:
1.  **CPA Dashboard**: Visualization of the financial data provided by `JulieEngine` (Backend).
2.  **Backend Integration**: Connect frontend to `http://localhost:8011/api/julie/status` instead of just mock data.
3.  **Persona Alignment**: Update UI to reflect "LA Korean-American" context (Currency $, English/Korean mix).

## Analysis (Truth)
- **Current Frontend**: Focuses on "Prompt Engineering" (R.C.A.T.E framework).
- **Current Backend**: Provides "Financial Status" (Risk alerts, Spending, Tax advice).
- **Gap**: The frontend has no view to show "Risk Alerts" or "Spending".

## Proposed Changes

### 1. New Component: `CPADashboard.tsx` (Beauty)
- **Features**:
    - **Financial Health Card**: Monthly Spending vs Budget (Visual Bar).
    - **Risk Alerts**: Display alerts from `/api/julie/status`.
    - **Julie's Advice**: "3-Line Summary" from the engine.
    - **Transactions**: List of simulated transactions (LA Context).

### 2. Service Update: `julieService.ts` (Goodness)
- [NEW] Create `services/julieService.ts` to fetch from `/api/julie/status`.
- Replaces direct Gemini calls for *financial* data (keeping Gemini for *prompt* generation for now).

### 3. App Integration
- Add **"CPA Mode"** or **"Dashboard"** tab to `App.tsx`.
- Modify `GlobalClock` or Header to show "Julie CPA" branding more clearly.

## Verification
- Run `npm run dev`.
- Verify "CPA Dashboard" loads data from `localhost:8011`.
- Verify "LA/US" context in the UI.
