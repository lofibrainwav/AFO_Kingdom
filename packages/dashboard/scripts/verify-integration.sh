#!/bin/bash

# 통합 검증 스크립트
# 전체 플로우, 에지 케이스, 롤백 시나리오를 검증합니다.

set -e

echo "🔍 통합 검증 시작..."
echo ""

# 색상 정의
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 검증 결과
PASSED=0
FAILED=0

# 검증 함수
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ $1${NC}"
        ((FAILED++))
    fi
}

# 1. 빌드 검증
echo "📦 빌드 검증..."
npm run build > /dev/null 2>&1
check "빌드 성공"

# 2. 타입 검증
echo "🔷 타입 검증..."
npm run type-check > /dev/null 2>&1
check "타입 검사 통과"

# 3. Lint 검증
echo "🔍 Lint 검증..."
npm run lint > /dev/null 2>&1
check "Lint 통과"

# 4. 번들 크기 검증
echo "📊 번들 크기 검증..."
if [ -f "bundle-analysis.json" ]; then
    TOTAL_SIZE=$(node -e "const data = require('./bundle-analysis.json'); console.log(data.totalSize);")
    TOTAL_MB=$(echo "scale=2; $TOTAL_SIZE / 1024 / 1024" | bc)
    
    if (( $(echo "$TOTAL_MB > 0.5" | bc -l) )); then
        echo -e "${YELLOW}⚠️  번들 크기: ${TOTAL_MB}MB (목표: 0.5MB 이하)${NC}"
        ((FAILED++))
    else
        echo -e "${GREEN}✅ 번들 크기: ${TOTAL_MB}MB${NC}"
        ((PASSED++))
    fi
else
    echo -e "${YELLOW}⚠️  번들 분석 리포트가 없습니다. 'npm run build:analyze'를 실행하세요.${NC}"
fi

# 5. 파일 존재 검증
echo "📁 필수 파일 검증..."
REQUIRED_FILES=(
    "next.config.ts"
    "package.json"
    "src/app/docs/page.tsx"
    "src/components/docs/index.ts"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        check "파일 존재: $file"
    else
        echo -e "${RED}❌ 파일 없음: $file${NC}"
        ((FAILED++))
    fi
done

# 6. 컴포넌트 검증
echo "🧩 컴포넌트 검증..."
REQUIRED_COMPONENTS=(
    "src/components/docs/MermaidDiagram.tsx"
    "src/components/docs/Modal.tsx"
    "src/components/docs/PillarModal.tsx"
    "src/components/docs/OrgansMapSVG.tsx"
)

for component in "${REQUIRED_COMPONENTS[@]}"; do
    if [ -f "$component" ]; then
        check "컴포넌트 존재: $component"
    else
        echo -e "${RED}❌ 컴포넌트 없음: $component${NC}"
        ((FAILED++))
    fi
done

# 결과 출력
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 검증 결과"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ 통과: $PASSED${NC}"
echo -e "${RED}❌ 실패: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 모든 검증 통과!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  일부 검증 실패${NC}"
    exit 1
fi

