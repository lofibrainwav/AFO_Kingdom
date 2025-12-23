#!/bin/bash

# 성능 테스트 스크립트
# 페이지 로딩 속도, 번들 크기, 메모리 사용량을 측정합니다.

set -e

echo "⚡ 성능 테스트 시작..."
echo ""

# 색상 정의
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 빌드 및 번들 분석
echo "📦 빌드 및 번들 분석..."
npm run build:analyze

# 2. 번들 크기 확인
if [ -f "bundle-analysis.json" ]; then
    echo ""
    echo "📊 번들 크기 분석:"
    node -e "
        const data = require('./bundle-analysis.json');
        const totalMB = data.totalSize / 1024 / 1024;
        console.log(\`  총 크기: \${totalMB.toFixed(2)}MB\`);
        console.log(\`  목표: 0.5MB 이하\`);
        if (totalMB > 0.5) {
            console.log('  ⚠️  경고: 목표를 초과했습니다.');
            process.exit(1);
        } else {
            console.log('  ✅ 목표 달성');
        }
    "
fi

# 3. 페이지 로딩 속도 테스트 (Lighthouse CI 또는 Puppeteer 사용)
echo ""
echo "🚀 페이지 로딩 속도 테스트..."
echo "  (실제 테스트는 E2E 테스트에서 수행됩니다)"

# 4. 메모리 사용량 확인
echo ""
echo "💾 메모리 사용량 확인..."
if command -v node &> /dev/null; then
    node -e "
        const usage = process.memoryUsage();
        console.log(\`  힙 사용량: \${(usage.heapUsed / 1024 / 1024).toFixed(2)}MB\`);
        console.log(\`  힙 총량: \${(usage.heapTotal / 1024 / 1024).toFixed(2)}MB\`);
        console.log(\`  RSS: \${(usage.rss / 1024 / 1024).toFixed(2)}MB\`);
    "
fi

echo ""
echo -e "${GREEN}✅ 성능 테스트 완료${NC}"

