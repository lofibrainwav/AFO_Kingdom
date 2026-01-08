#!/bin/bash
# AFO 왕국 보안 정리 검증 스크립트
# 실행 시각 기반 실시간 검증 제공

echo "=== 🔒 AFO 왕국 보안 정리 검증 스크립트 ==="
echo "실행 시각: $(date '+%Y-%m-%d %H:%M:%S')"
echo "실행자: $(whoami)"
echo "작업 디렉토리: $(pwd)"
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 검증 함수
check_result() {
    local label="$1"
    local command="$2"
    local expected="$3"
    local actual

    echo -n "🔍 $label: "
    actual=$(eval "$command" 2>/dev/null)

    if [ "$actual" = "$expected" ]; then
        echo -e "${GREEN}✅ PASS${NC} ($actual)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (실제: $actual, 기대: $expected)"
        return 1
    fi
}

echo "📊 검증 항목 실행 중..."
echo ""

# 1. 민감 파일 검증
check_result "민감 캐시 파일 수" "find . -path '*/.mypy_cache*' -name '*secrets*' -type f | wc -l | tr -d ' '" "0"

# 2. .gitignore 규칙 검증
check_result ".gitignore .mypy_cache 규칙 수" "grep -c '\.mypy_cache' .gitignore" "2"

# 3. 로그 파일 존재 검증
log_count=$(ls artifacts/logs/ | grep -E "(security-scan|cline-background)" | wc -l)
check_result "보안 관련 로그 파일 수" "echo $log_count" "2"

# 4. 압축 파일 무결성 검증
if gzip -t artifacts/logs/cline-background-codebase-analysis-2026-01-08.log.gz 2>/dev/null; then
    echo -e "🗜️  압축 파일 무결성: ${GREEN}✅ PASS${NC}"
else
    echo -e "🗜️  압축 파일 무결성: ${RED}❌ FAIL${NC}"
fi

# 5. Evolution Log 기록 검증
if grep -q "PH-SEC-CLEANUP" docs/AFO_EVOLUTION_LOG.md; then
    echo -e "📜 Evolution Log 기록: ${GREEN}✅ PASS${NC}"
else
    echo -e "📜 Evolution Log 기록: ${RED}❌ FAIL${NC}"
fi

# 6. Git 커밋 상태 검증
if git log --oneline -1 | grep -q "보안 취약점 DRY_RUN 정리"; then
    echo -e "🔗 Git 커밋 기록: ${GREEN}✅ PASS${NC}"
else
    echo -e "🔗 Git 커밋 기록: ${RED}❌ FAIL${NC}"
fi

echo ""
echo "=== 📈 상세 상태 보고 ==="

echo "📁 로그 파일 상세:"
ls -lh artifacts/logs/ | grep -E "(security|cline-background)" || echo "로그 파일을 찾을 수 없음"

echo ""
echo "🛡️ .gitignore 규칙 상세:"
grep -n "\.mypy_cache" .gitignore || echo ".mypy_cache 규칙을 찾을 수 없음"

echo ""
echo "✅ 검증 스크립트 실행 완료"
echo "문제가 발견되면 즉시 보고 바랍니다."