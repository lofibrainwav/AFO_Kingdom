# AFO_AGENT_COMMAND_CONTRACT_V1 (SSOT)
Applies to: Antigravity / Cursor / Cline (IDE agents)

## Goal
Commands must be executable, evidence-backed, and SSOT-safe.

## Required Structure (copy/paste contract)
[TASK_ID] <short title>
GOAL: <1 sentence>
SCOPE:
- Files:
- Services/Ports:
MODE: DRY_RUN -> WET -> VERIFY

DRY_RUN (evidence collection):
- Provide exact commands (copy/paste)
- Must include: git context, ports, HTTP, ssot_verify trace, playwright detect

WET (changes):
- Provide patch plan (file path + minimal edit)
- If code change: show full replacement block or unified diff

VERIFY (seal):
- Must include:
  - bash ssot_verify.sh (or evidence of missing)
  - python3 system_health_check.py (if available)
  - curl GET checks: 8010/health and 3000/
  - Evidence block (E1~E6) produced by scripts/afo_report_evidence_v1.sh

## Output Requirements
- Always end with:
  1) "Command Pack" (copy/paste)
  2) Evidence block (E1~E6)
  3) Rollback (how to revert last change)
