#!/bin/bash
set -euo pipefail

# Surgical removal of any process/container hijacking port 8010
echo "⚔️  Exorcising Port 8010 hijackers..."

# Stop and remove ANY container holding 8010
DOCKER_8010=$(docker ps --all --filter "publish=8010" -q)
if [ ! -z "$DOCKER_8010" ]; then
    echo "Found hijacker containers: $DOCKER_8010. Removing..."
    docker stop $DOCKER_8010 || true
    docker rm $DOCKER_8010 || true
else
    echo "No hijacker containers found pinning 8010."
fi

# Clean rebuild of soul-engine with a fresh fingerprint
echo "🏗️  Rebuilding Soul Engine with a fresh fingerprint (No-Cache)..."
cd "$(dirname "$0")/../packages/afo-core"
# Generate a fresh fingerprint
FINGERPRINT=$(date +%Y%m%d_%H%M%S)
echo "Generated Fingerprint: $FINGERPRINT"

# Force rebuild to ensure no 'Ghost Code' remains
BUILD_VERSION=$FINGERPRINT docker compose build --no-cache soul-engine
BUILD_VERSION=$FINGERPRINT docker compose up -d soul-engine

echo "✅ Exorcism complete. Wait 8s for truth verification..."
sleep 8
"$(dirname "$0")/verify_fingerprint.sh"
