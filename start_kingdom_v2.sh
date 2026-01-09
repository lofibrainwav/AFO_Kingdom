#!/bin/bash

# 🏰 AFO Kingdom "Local First" Startup Script (v2)
# Orchestrates the 4 Pillars: Soul (API), Face (UI), Heart (Redis), Lung (Qdrant)
# Mode: FULLY LOCAL (Docker-Free)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# --- Configuration ---
REDIS_PORT=6379
QDRANT_PORT=6333
BACKEND_PORT=8010
FRONTEND_PORT=3000

# Fix: Ensure Soul Engine talks to Local Qdrant (not Docker 'afo-qdrant')
export QDRANT_HOST=localhost

QDRANT_BINARY="./services/qdrant/qdrant"
QDRANT_LOG="./services/qdrant/qdrant.log"
QDRANT_PID_FILE="./services/qdrant/qdrant.pid"

echo "==================================================="
echo "   🚀 INITIALIZING AFO KINGDOM (LOCAL MODE)        "
echo "==================================================="

# --- Cleanup Trap ---
cleanup() {
    echo ""
    echo "🛑 Shutting down the Kingdom..."
    
    # Kill Qdrant if we started it
    if [ -f "$QDRANT_PID_FILE" ]; then
        QPID=$(cat "$QDRANT_PID_FILE")
        if kill -0 "$QPID" 2>/dev/null; then
            echo "   -> Stopping Qdrant (PID: $QPID)..."
            kill "$QPID"
        fi
        rm "$QDRANT_PID_FILE"
    fi

    # Kill Backend/Frontend (usually handled by Ctrl+C but just in case)
    # Note: simple kill might not be enough if they ignore SIGINT, but usually Ctrl+C propagates.
    
    echo "👋 Kingdom returned to slumber."
}
trap cleanup EXIT

# --- 1. Ignite the Heart (Redis) ---
echo "---------------------------------------------------"
if lsof -i :$REDIS_PORT >/dev/null; then
    echo "✅ Redis (brew)    : ONLINE (:6379)"
else
    brew services start redis >/dev/null || echo "⚠️  Redis start warning"
    sleep 2
    echo "✅ Redis (brew)    : STARTED (:6379)"
fi

# --- 2. Inflate the Lung (Qdrant) ---
if lsof -i :$QDRANT_PORT >/dev/null; then
    echo "✅ Qdrant (local)  : ONLINE (:6333)"
else
    if [ -x "$QDRANT_BINARY" ]; then
        nohup "$QDRANT_BINARY" > "$QDRANT_LOG" 2>&1 &
        echo $! > "$QDRANT_PID_FILE"
        sleep 2
        echo "✅ Qdrant (local)  : STARTED (PID: $(cat $QDRANT_PID_FILE))"
    else
        echo "❌ Qdrant          : MISSING ($QDRANT_BINARY)"
        echo "   -> Run: manual install required"
        exit 1
    fi
fi

# --- 3. Awaken the Soul (Backend) ---
cd "$SCRIPT_DIR/packages/afo-core"
if command -v poetry >/dev/null 2>&1; then
poetry install --without dev >/dev/null || true
fi
# Ensuring we use the correct environment
VENV_PATH=$(poetry env info -p)
export PATH="$VENV_PATH/bin:$PATH"
echo "   -> Using Virtualenv: $VENV_PATH"

poetry run uvicorn api_server:app --reload --port $BACKEND_PORT >/dev/null 2>&1 &
BACKEND_PID=$!
echo "✅ Soul (API)      : ONLINE (:8010, PID: $BACKEND_PID)"

# --- 4. Optional Organs ---
echo "⏸  Postgres (liver) : OPTIONAL (Docker dependent)"
echo "---------------------------------------------------"

# --- 5. Reveal the Face (Frontend) ---
echo "🚀 Launching Dashboard (:3000)..."
cd "$SCRIPT_DIR/packages/dashboard"
if [ ! -d "node_modules" ]; then npm install >/dev/null; fi
npm run dev -- -p $FRONTEND_PORT

wait $BACKEND_PID
