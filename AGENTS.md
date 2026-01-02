# AFO Kingdom — AGENTS (SSOT + Trinity Operating Rules)

This file defines the non-negotiable operating rules for any agent working in this repo.
Primary goals: Truth (SSOT) first, Safety, Low Friction, Reproducibility.

---

## 0) Language Lock (KO_ONLY)

- Default output language: **Korean (존댓말) only**.
- English is allowed **only** for:
  - code identifiers, filenames/paths, commands, error messages, and exact technical terms.
- Japanese/Chinese sentences are **forbidden** unless the user explicitly requests them.
- Do not append multilingual slogans.

---

## 1) No Roleplay / No Hype

- No roleplay persona text (e.g., "승상", "사령관", "제국", 과장된 서사).
- No emojis in operational output.
- No inflated claims ("20배", "표준 준수", "재단 규격") unless backed by SSOT evidence.

---

## 2) Truth Policy (SSOT-first)

Hard rules:
- Do not fabricate files, commands, URLs, features, organizations, or results.
- If something is not verified, say: **NOT VERd.
- For any metric/score claimed, attach or reference an artifact file under `artifacts/`.

SSOT evidence expectations:
- Prefer machine-verifiable logs, command outputs, hashes, manifests.
- Store evidence under `artifacts/` with timestamped filenames.

---

## 3) Execution Protocol (must follow)

Always run changes through:
1) **Backup**
2) **Check**
3) **Execute**
4) **Verify**
5) **Rollback path**

### 3.1 Backup (required)
- Before modifying files/config:
  - copy original to timestamped backup
  - or create a git commit checkpoint

### 3.2 Check (required)
- Confirm current state before action:
  - `git status -sb`
- No emojis in operational output.
- No inv/ports/logs if relevant

### 3.3 Execute (minimal change)
- Prefer the smallest change that can be verified.
- Avoid large refactors unless explicitly requested.

### 3.4 Verify (required)
- Verify with the repo's actual gates.
- If a command is not available in this repo, mark as **NOT CONFIGURED** (do not pretend).

Recommended verification (run what exists):
- Node/Next:
  - `npm run lint`
  - `npm run type-check`
  - `npm run build`
- Python:
  - run the relevant test subset, then full suite if needed
- Services:
  - health endpoints / docker compose status when applicable

### 3.5 Rollback (required)
Always run changes through:
1) **Bac(git revert / restore backup file).

---

## 4) Ask-Before-Act (when risky or ambiguous)

If any of the below is true, do not proceed autonomously:
- destructive actions (delete, reset, force push)
- security/auth changes
- migrations / schema changes
- unclear requirements

Instead: provide A/B options with pros/cons and a safe default.

---

## 5) Output Format (copy-paste first)

When giving operational instructions:
- Provide copy-paste commands.
- Keep steps short and sequential.
- Include expected outputs or quick checks.
- Avoid long explanations.

---

## 6) File Size / Cognitive Budget

- Keep this file concise (target: **<= 500 lines**).
- If it grows, split details into:
  - `docs/agents/*.md`
  - and link from here.

---

## 7) Tooling Reality Rules

- If web verification is required (time-sensitive facts / docs / policies):
  - verify via browsing and keep citations in the
### 3.5 Rollback (required)
Always run changes through:
1) if images/tables are relevant.
- Never claim "done" without evidence.

---

## 8) Project-Specific: Trinity / SSOT

- Trinity Score or similar composite metrics must be:
  - computed from an artifact result file
  - reproducible with a documented command
- If execution is blocked by environment limits:
  - mark execution as **BLOCKED**
  - include the evidence log in `artifacts/`

