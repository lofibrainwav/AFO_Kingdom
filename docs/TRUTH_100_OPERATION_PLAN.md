# Truth 100% Operation Plan (Zero Defect)

## Mission
Eliminate all 341+ MyPy errors to establish absolute type safety (眞 Integrity).

## Phenomenon Analysis
- **Total Errors**: ~158-341 (Fluctuating based on cache/scan depth)
- **Root Cause**: "Split-Brain" directory structure (`packages/afo-core` vs `AFO/` symlinks).
- **Major Offenders**:
    - `personas.py`: Incompatible imports.
    - `skills_service.py`: Model mismatches.
    - `api_wallet.py`: Returning Any.
    - `llm_router.py`: Import inconsistencies.

## Phase 1: Split-Brain Integration (The "AFO." Protocol)
**Strategy**: Enforce `AFO.` prefix for ALL internal imports.
- This forces MyPy to recognize the canonical path, resolving "Incompatible import" errors.

## Phase 2: Type Safety Hardening
**Strategy**:
1.  **Strict Return Types**: Eliminate `Returning Any`.
2.  **Explicit Casting**: Use `cast(Type, val)` where inference fails.
3.  **TypedDict Completeness**: Ensure all required keys are present.

## Phase 3: Execution Order
1.  `api_wallet.py` (High Risk: Security)
2.  `llm_router.py` (High Risk: Core Logic)
3.  `skills_service.py` (Medium Risk)
4.  Global Verification

## Verification
- Command: `mypy packages/afo-core/AFO --ignore-missing-imports --explicit-package-bases`
- Target: 0 Errors in targeted files.
