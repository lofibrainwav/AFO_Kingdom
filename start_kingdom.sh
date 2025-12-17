#!/bin/bash

# 🏰 AFO Kingdom One-Click Startup Script
# Starts the Chancellor Backend (Docker) and Trinity Dashboard (Next.js)

set -e # Exit immediately if a command exits with a non-zero status.

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==================================================="
echo "   🚀 INITIALIZING AFO KINGDOM STARTUP SEQUENCE    "
echo "==================================================="

# 1. Start Backend Services
echo ""
echo "🔌 [1/2] Booting Chancellor Backend Services..."
cd "$BASE_DIR/AFO" || { echo "❌ Error: AFO directory not found at $BASE_DIR/AFO"; exit 1; }

# Ensure Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "❌ Error: Docker is not running. Please start Docker Desktop."
  exit 1
fi

echo "   -> Running 'docker-compose up -d'..."
docker-compose up -d

echo "✅ Backend Services Initiated."

# 2. Start Frontend
echo ""
echo "🖥️  [2/2] Launching Trinity Dashboard..."
cd "$BASE_DIR/trinity-dashboard" || { echo "❌ Error: trinity-dashboard directory not found at $BASE_DIR/trinity-dashboard"; exit 1; }

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
