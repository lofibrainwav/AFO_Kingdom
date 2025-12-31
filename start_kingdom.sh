#!/bin/bash
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
error() { echo -e "${RED}ERROR: $1${NC}" >&2; exit 1; }
info()  { echo -e "${GREEN}$1${NC}"; }

[[ -d packages/afo-core ]]   || error "Missing packages/afo-core"
[[ -d packages/dashboard ]]  || error "Missing packages/dashboard"

command -v docker >/dev/null         || error "Docker missing"
command -v docker-compose >/dev/null || error "docker-compose missing"
command -v node >/dev/null           || error "Node.js missing"
command -v npm >/dev/null            || error "npm missing"
command -v python3 >/dev/null        || error "python3 missing"

info "Executing Clinical Cleaning (美)..."
python3 scripts/md_clinical_clean.py task.md walkthrough.md implementation_plan.md FUTURE_STRATEGY.md || true

FPID=0
trap 'pushd packages/afo-core >/dev/null; docker-compose down >/dev/null 2>&1; popd >/dev/null; [[ $FPID -ne 0 ]] && kill $FPID 2>/dev/null || true' EXIT INT TERM

info "Starting backend..."
pushd packages/afo-core >/dev/null
docker-compose up --build -d
popd >/dev/null

info "Waiting for Soul Engine (8010) to initialize..."
MAX_RETRIES=30
COUNT=0
while ! curl -s http://localhost:8010/api/health >/dev/null; do
    sleep 1
    COUNT=$((COUNT+1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        error "Soul Engine failed to start within ${MAX_RETRIES}s"
    fi
    echo -n "."
done
echo ""
info "Soul Engine is LIVE."

info "Starting frontend..."
pushd packages/dashboard >/dev/null
[[ ! -d node_modules ]] && npm install
npm run dev &
FPID=$!
info "Kingdom ready → http://localhost:3000 (Ctrl+C to stop)"
popd >/dev/null

wait $FPID
