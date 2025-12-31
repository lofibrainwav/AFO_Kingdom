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

FPID=0
trap 'pushd packages/afo-core >/dev/null; docker-compose down >/dev/null 2>&1; popd >/dev/null; [[ $FPID -ne 0 ]] && kill $FPID 2>/dev/null || true' EXIT INT TERM

info "Starting backend..."
pushd packages/afo-core >/dev/null
docker-compose up --build -d
popd >/dev/null

info "Starting frontend..."
pushd packages/dashboard >/dev/null
[[ ! -d node_modules ]] && npm install
npm run dev &
FPID=$!
info "Kingdom ready → http://localhost:3000 (Ctrl+C to stop)"
popd >/dev/null

wait $FPID
