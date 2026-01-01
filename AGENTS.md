# AGENTS.md — AFO Kingdom (Root)
Root rules apply repo-wide. If a subdirectory has its own `docs/AGENTS.md`, follow it for module-specific details, but never violate this root file.

## 0) Mission
Keep the Kingdom stable, verifiable, and low-friction:
- Evidence-first (SSOT)
- Safe changes (backup → minimal diff → verify)
- No fictional completion claims

## 1) Non-Negotiables (Hard Rules)
### 1.1 Truth (眞)
- Do not claim you "ran / fixed / pushed / verified" unless you actually ran the command and have outputs.
- If you cannot verify, say "unverified" and provide the exact command to verify.

### 1.2 Goodness (善)
- Never leak secrets. Never paste tokens/webhooks/private keys into logs/docs.
- Prefer safe defaults. If a change can affect prod/CI/security, stop and request human review.

### 1.3 Serenity (孝)
- Reduce friction: short steps, copy-paste commands, clear rollback.
- Avoid long essays. One idea per line.

### 1.4 Beauty (美)
- Consistent structure, consistent naming, consistent evidence format.

### 1.5 Eternity (永)
- Every "DONE" must be reproducible: evidence folder + manifest.sha256 + tag when applicable.

## 2) Default Execution Protocol (Required)
When working on any task, follow this order:

### Stage-0: Snapshot (always)
Run and record:
- `git status -sb`
- `git rev-parse HEAD`
- `git log -1 --oneline`
- If CI related: list workflow/check names for last run (see §6)

### Stage-1: Plan (3 bullets)
- What you will change
- How you will verify
- Rollback path

### Stage-2: Safety (backup / branch)
- Work on a feature branch unless explicitly instructed otherwise.
- If editing critical files, create a backup commit or file backup.

### Stage-3: Minimal Change
- Small diffs.
- Prefer mechanical refactors with automated tools.
- Avoid "drive-by" unrelated changes.

### Stage-4: Verify (must pass)
Run the relevant checks (see §5). If something fails, fix or revert.

### Stage-5: SSOT Evidence (required for completion claims)
If you say "SEALED / DONE / PASS", you must produce:
- Evidence folder (artifacts/…)
- `manifest.sha256` covering all evidence files
- SSOT header fields (see §7)

## 3) Git / PR Rules
- `main` is protected. No direct pushes unless explicitly allowed.
- PRs require required checks + at least 1 approval (if configured).
- Prefer linear history (rebase) if the repo requires it.

Commit message format:
- `type(scope): summary (TICKET-XYZ)`
Examples:
- `fix(afo-core): resolve import casing (TICKET-046)`
- `ci(trinity): enforce gate ≥0.90 (TICKET-061)`

## 4) Package Naming Rule (Linux/CI Safety)
- Package/module name is **`afo`** (lowercase).
- Imports must use `from afo...` / `import afo...`
- Do not reintroduce `AFO` casing in paths or imports.

## 5) Quality Gates (Local)
Run only what's relevant, but never skip the gate for touched areas.

### Python (afo-core)
- Ruff:
  - `ruff check packages/afo-core`
- Pytest:
  - `PYTHONPATH=packages/afo-core pytest packages/afo-core/tests -q`
- (Optional) Mypy if configured:
  - `python -m mypy packages/afo-core`

### Shell scripts
- `shellcheck` via workflow or locally if available.

### Project "Golden Path"
If `./afo` exists, prefer it:
- `./afo status`
- `./afo trinity`
- `./afo drift`
- `./afo seal`

## 6) CI / Branch Protection Check Name Policy
Branch protection required checks must match **actual check-run names** exactly (case-sensitive).
To inspect actual job/check names (GitHub CLI):
- `gh run list -L 5 --branch main`
- `gh run view <RUN_ID> --json jobs -q '.jobs[].name'`

If required checks mismatch:
- Fix branch protection contexts to match actual names (preferred), OR
- Rename workflow/job names to match the required contexts.

## 7) SSOT Completion Format (6 Elements)
Any "final report / sealed / done" must include:

1) **As-of** (ISO8601 + TZ)
2) **HEAD** (full SHA)
3) **Change summary** (one line)
4) **Repro commands** (copy-paste)
5) **Evidence path** (folder)
6) **Decision** (AUTO_RUN / ASK / BLOCK with reason)

Recommended evidence folder naming:
- `artifacts/<topic>_<YYYYMMDD-HHMMSS>_<shortsha>/`

Minimum evidence files (suggested):
- `git_status.txt`
- `git_head.txt`
- `git_log1.txt`
- `<gate>_output.txt` (ruff/pytest/trinity/etc)
- `manifest.sha256`

## 8) Security & Secrets
- Never commit `.env` secrets.
- Webhooks/keys must come from env vars, not hardcoded strings.
- If you suspect a secret leak, stop and alert immediately.

## 9) Docs & Ticket Board
If a ticket is marked DONE:
- Update `TICKETS.md` (or the current SSOT board file)
- Ensure: Commit + Seal Tag pattern + Evidence path are filled (no blanks)

## 10) Tone & Output Discipline
- No roleplay.
- No exaggerated claims.
- Prefer short, direct, reproducible outputs.

# End
