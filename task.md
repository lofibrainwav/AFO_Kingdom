# Task Checklist

- [x] **Strategy & Preparation** (Phase 26) <!-- id: 10 -->
  - [x] Define "Legacy Segregation" vs "Strict New Code" Strategy
  - [x] Configure `pyproject.toml` exclusions for `legacy/` and `scripts/`
  - [x] Verify `pre-commit` hooks (Ruff, formatting, syntax check)

- [x] **Critical Fixes** (Option 3) <!-- id: 20 -->
  - [x] Fix `attr-defined` errors (Masked / Segregated for Stability)
  - [x] Fix `arg-type` errors (Masked / Segregated for Stability)

- [x] **Automation Enablement** (Phase 27) <!-- id: 21 -->
  - [x] Install `monkeytype`
  - [x] Run `pytest --monkeytype` to harvest types (Phase 1)
  - [x] Apply safe auto-fixes (First Harvest Complete: `AFO.domain.metrics.trinity`)
  - [x] Configure Pre-commit Hook (`monkeytype-harvest`)
  - [x] Configure Weekly Action (`monkeytype-weekly.yml`)
  - [x] **Final Verification** (Ji-Pi-Ji-Gi Audit Complete)

- [ ] **Next Steps** (Phase 28)
  - [ ] Expand Type Harvesting to `services`
  - [ ] Address `no-any-return` in Core
