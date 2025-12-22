# AFO Royal Architect's Blueprint 🏛️
**Status**: SSOT for Royal Dashboard Components
**Philosophy**: "Map is Territory" (Docs -> Code)

## 1. Julie Royal Tax Widget (Goodness/善)
**Vibe**: "Predictable Prosperity" (LA 2025 Edition)
**Source**: Julie-Perplexity Report (12/21/25)
**Data Source**: `JulieEngine` (Simulated with 2025 IRS/FTB Rules)

### 5 Pillars Spec
- **Truth (眞)**: 
    - **Federal**: 2025 Brackets (10-37%), Standard Deductions (Single $15,750 / MFJ $31,500).
    - **CA State**: 9 Brackets (1-12.3%) + 1% Mental Health Surtax (> $1M).
    - **QBI**: 20% Deduction for Schedule C/K-1 (Phase-out ~$394k MFJ).
- **Goodness (善)**: 
    - Risk Gauge: **Emerald** (< 20% Eff. Rate), **Red** (> 30% Eff. Rate).
    - Logic: "Conservative Estimation" (Overestimate tax slightly to be safe).
- **Beauty (美)**: Glassmorphism Card. Slider for "Income Sensitivity".
- **Serenity (孝)**: Real-time "What-If" (e.g., 401k contribution impact).
- **Eternity (永)**: Versioned Tax Tables (v2025.1).

### Logic Spec (TRD)
1.  **Inputs**: Income (W2/1099), Filing Status (Single/MFJ).
2.  **Calc**: Gross -> AGI (minus 401k) -> Taxable (minus Standard/QBI) -> Brackets -> Total Tax.
### 3. Julie's Optimization Strategy (Template Engine)
**Logic (Standardized Procedures)**:
*   **401k/SEP**: If income > $0, suggest max contribution ($23,500). Calculate tax saving based on *Marginal Rate*.
*   **HSA**: If Filing Status = Single, suggest $4,300; else $8,550. Calculate tax saving.
*   **QBI**: If Business Income exists (Simulated at 30%), show "Auto-Saving" from 20% deduction.

**UI Component**:
*   **Advice Cards**: Stacked, clickable cards.
*   **Visuals**: Emerald theme, "Save $X" badges.
*   **Interaction**: Hover effects, clear "Action" vs "Impact" text.
4.  **Output**: Effective Rate, Marginal Rate, "Safe to Spend".

### UI Schema (Proposed)
- **Type**: `Molecule` (Card)
- **Components**:
    - `Card` (shadcn)
    - `Slider` (shadcn) for "Income Adjustment"
    - `Progress` (shadcn) for "Tax Bracket Position"
    - `Table` (shadcn) for "Breakdown"

### User Story
"As the Commander, I want to see how much of my Treasury is 'Real Money' vs 'Tax Liability', so I can spend with peace of mind."
