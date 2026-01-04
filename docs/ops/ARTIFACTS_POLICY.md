# Artifacts Policy (SSOT)

## Rule
- `artifacts/` is generated output.
- Keep only what is needed for debugging, audits, and SSOT proofs.
- Never commit large transient dumps.

## Keep (commit allowed)
- `artifacts/housekeeping/` (indexes, tree snapshots)
- `artifacts/redteam/**/governance_report.md`
- Small JSONL/MD evidence packs that are explicitly referenced in tickets/docs

## Ignore (do not commit)
- `artifacts/**/tmp/`
- `artifacts/**/logs/` (unless explicitly required)
- Large binaries, model weights, caches, downloads

## Size guard
- Avoid committing any single artifact file over 5MB unless explicitly approved.
