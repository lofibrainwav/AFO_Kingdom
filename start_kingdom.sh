#!/bin/bash

# 🏰 AFO Kingdom One-Click Startup Script
# Starts the Chancellor Backend (Python/FastAPI) and Trinity Dashboard (Next.js)

set -e # Exit immediately if a command exits with a non-zero status.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "==================================================="
echo "   🚀 INITIALIZING AFO KINGDOM STARTUP SEQUENCE    "
echo "==================================================="

# 1. Start Backend Services (Python/FastAPI)
echo ""
echo "🔌 [1/2] Booting Chancellor Backend Services..."
cd "$SCRIPT_DIR/packages/afo-core" || { echo "❌ Error: afo-core directory not found at $SCRIPT_DIR/packages/afo-core"; exit 1; }

# Check if Python environment is available
if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
  echo "❌ Error: Python is not available. Please install Python 3.12+."
  exit 1
fi

echo "   -> Installing Python dependencies..."
if command -v poetry >/dev/null 2>&1; then
  poetry install --no-dev || echo "⚠️ Poetry install failed, trying alternative..."
fi

echo "   -> Starting FastAPI server..."
echo "   -> Backend will be available at: http://localhost:8010"
uvicorn api_server:app --reload --port 8010 &
BACKEND_PID=$!

echo "✅ Backend Services Initiated (PID: $BACKEND_PID)."

# 2. Start Frontend
echo ""
echo "🖥️  [2/2] Launching Trinity Dashboard..."
cd "$SCRIPT_DIR/packages/dashboard" || { echo "❌ Error: dashboard directory not found at $SCRIPT_DIR/packages/dashboard"; exit 1; }

# Check for node_modules
if [ ! -d "node_modules" ]; then
    echo "   -> 📦 First run detected. Installing dependencies..."
    npm install
fi

echo "   -> Starting Next.js Development Server..."
echo "   -> Dashboard will be available at: http://localhost:3000"
echo "==================================================="
echo "🟢 SYSTEM ONLINE. Press Ctrl+C to stop the dashboard."
echo "==================================================="

# Run npm run dev
npm run dev
