#!/bin/bash

# AICPA Core Startup Script
echo ">> Starting AICPA Core on Port 3005..."

# Optimization: Auto-kill port 3005 if in use
PID=$(lsof -ti :3005)
if [ ! -z "$PID" ]; then
  echo ">> Port 3005 is busy. Stopping existing process ($PID)..."
  kill -9 $PID
  sleep 1
fi
echo ">> Checking API Key..."

if grep -q "PLACEHOLDER" .env; then
    echo "⚠️  WARNING: GEMINI_API_KEY is not set in .env!"
    echo "   Please add your Gemini API Key to .env before using AI features."
fi

# Install dependencies if node_modules is missing
if [ ! -d "node_modules" ]; then
    echo ">> Installing dependencies..."
    npm install
fi

# Start Vite
echo ">> Launching Vite Server..."
npm run dev
