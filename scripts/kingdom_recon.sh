#!/usr/bin/env bash
set -u
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="$ROOT/artifacts/recon/$TS"
mkdir -p "$OUT"
ln -sfn "$OUT" "$ROOT/artifacts/recon/latest"

cap() {
  local name="$1"; shift
  bash -lc "$*" >"$OUT/${name}.log" 2>&1
  echo $? >"$OUT/${name}.code"
}

echo "$TS" > "$OUT/_ts.txt"

cap git_status "cd '$ROOT' && git status -sb"
cap git_head "cd '$ROOT' && git rev-parse HEAD && echo && git tag --points-at HEAD || true"
cap git_recent "cd '$ROOT' && git log -10 --oneline --decorate"
cap git_diffstat "cd '$ROOT' && git diff --stat || true"

cap ports_listen "for p in 8010 3000 15432 6379 3001 3002; do echo '== :'\$p' =='; lsof -nP -iTCP:\$p -sTCP:LISTEN || true; echo; done"
cap proc_grep "ps aux | egrep -i 'uvicorn|api_server|afo|next|node|pnpm|docker|redis|postgres|qdrant|grafana|webui|ollama' | head -n 200 || true"

cap docker_ps "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' || true"
cap docker_compose_ps "docker compose ps 2>/dev/null || docker-compose ps 2>/dev/null || true"
cap docker_compose_logs "docker compose logs --tail 200 2>/dev/null || docker-compose logs --tail 200 2>/dev/null || true"

cap curl_8010_health "curl -sfL -m 3 http://localhost:8010/health || true"
cap curl_8010_metrics "curl -sfL -m 3 http://localhost:8010/metrics || true"
cap curl_3000 "curl -si -m 3 http://localhost:3000/ | head -n 30 || true"

cap find_state_md "cd '$ROOT' && (git ls-files | egrep -n 'AFO_STATE_OF_KINGDOM.md$' || true); echo; find . -maxdepth 6 -name 'AFO_STATE_OF_KINGDOM.md' -print || true"
cap find_trinity_score "cd '$ROOT' && (git ls-files | egrep -n 'trinity_score\\.json$' || true); echo; find . -maxdepth 6 -name 'trinity_score.json' -print || true"
cap find_evo_log "cd '$ROOT' && (git ls-files | egrep -n 'AFO_EVOLUTION_LOG\\.md$' || true); echo; find . -maxdepth 6 -name 'AFO_EVOLUTION_LOG.md' -print || true"

cap find_known_logs "cd '$ROOT' && find . -maxdepth 7 -type f \\( -name 'api_server.log' -o -name 'server.log' -o -name 'dashboard_reboot.log' -o -name 'dashboard_final.log' \\) -print || true"

for f in api_server.log server.log dashboard_reboot.log dashboard_final.log; do
  cap "tail_${f}" "cd '$ROOT' && P=\$(find . -maxdepth 7 -type f -name '$f' | head -n 1); if [ -n \"\$P\" ]; then echo \"== \$P ==\"; tail -n 200 \"\$P\"; else echo 'NOT_FOUND'; fi"
done

echo "$OUT"
