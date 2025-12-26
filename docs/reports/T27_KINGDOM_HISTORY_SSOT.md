# T27 Kingdom History Widget SSOT Report

**Status**: SEALED-VERIFIED
**Timestamp**: 20251225-2225
**Evidence**: artifacts/t27/20251225-2225/
**SealSHA256**: 7b07af160bcd41a28b848cc02056e4d13e57b3d0564d20761044149f856a936f
**Verify**: PASS (from verify_pass.txt)

## 1. What changed (Files edited)
## 1. What changed (Files edited)

### Backend
- `packages/afo-core/api/routes/git_status.py`: Added `/api/git/history` endpoint.
- `packages/afo-core/docker-compose.yml`: Mounted `/workspace` for `.git` access.
- `packages/afo-core/Dockerfile`: Added `git` to system dependencies.

### Frontend
- `packages/dashboard/src/components/royal/widgets/KingdomHistoryWidget.tsx`: New Widget.
- `packages/dashboard/src/components/royal/RoyalLayout.tsx`: Integrated Widget.

## 2. Commands run

```bash
# Evidence Capture
TS="20251225-2225"
OUT="artifacts/t27/$TS"
mkdir -p "$OUT"
git diff --name-only > "$OUT/git_files_changed.txt"
curl -sS "http://127.0.0.1:8010/api/git/history?limit=5" > "$OUT/api_body.json"
python3 -m bandit -r packages/afo-core -lll -f json -o "$OUT/bandit_report.json"
```

## 3. Evidence

All evidence files are stored in: `artifacts/t27/20251225-2225/`

- `api_body.json`: Git History API Response (5 commits returned)
- `bandit_report.json`: Security scan results (High Severity = 0)
- `bandit_exitcode.txt`: Exit code 0
- `seal.json`: Physical seal with file hashes
- `verify_pass.txt`: Verification output (PASS)

## 4. Green Check

- [x] **Backend API**: `/api/git/history` returns structured JSON data.
- [x] **Security**: Bandit exit code 0 (No High Severity issues).
- [x] **Dependencies**: `git` installed in Docker container.
- [x] **Volume Mount**: `/workspace` mount provides `.git` access.
- [x] **Frontend Widget**: `KingdomHistoryWidget.tsx` created and integrated.
- [x] **Physical Verification**: `seal.json` + `verify_pass.txt` (PASS) present.

**Status**: SEALED-VERIFIED (TruthGate Passed).
