#!/bin/bash
# AFO 왕국 Phase 11 - MyPy 레거시 정화 스냅샷 스크립트
# SSOT 작전문 준수: 증거 번들 생성

set -euo pipefail

# 타임스탬프 생성
TS=$(date +"%Y%m%d_%H%M%S")
SNAPSHOT_DIR="artifacts/mypy/phase11/${TS}"

echo "🏰 Phase 11 MyPy 스냅샷 생성"
echo "============================"
echo "타임스탬프: ${TS}"
echo "저장 위치: ${SNAPSHOT_DIR}"
echo ""

# 디렉토리 생성
mkdir -p "${SNAPSHOT_DIR}" || {
    echo "❌ 디렉토리 생성 실패: ${SNAPSHOT_DIR}"
    exit 1
}

# MyPy 실행 및 결과 저장
echo "🔍 MyPy 실행 중..."
cd packages/afo-core

# 전체 MyPy 결과
mypy AFO/ --config-file ../../pyproject.toml --show-error-codes > "${SNAPSHOT_DIR}/mypy_full.txt" 2>&1 || true

# 에러 카운트
ERROR_COUNT=$(grep -c "error:" "${SNAPSHOT_DIR}/mypy_full.txt" || echo "0")

# TOP FILES 분석 (에러가 가장 많은 파일들)
echo "📊 TOP FILES 분석..."
grep "error:" "${SNAPSHOT_DIR}/mypy_full.txt" | \
    sed 's/:.*$//' | \
    sort | \
    uniq -c | \
    sort -nr | \
    head -20 > "${SNAPSHOT_DIR}/top_files.txt"

# 각 파일별 에러 상세
while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]*([0-9]+)[[:space:]]+(.*)$ ]]; then
        count="${BASH_REMATCH[1]}"
        file="${BASH_REMATCH[2]}"

        echo "📁 ${file} (${count} errors):" >> "${SNAPSHOT_DIR}/files_detail.txt"
        grep "^${file}:" "${SNAPSHOT_DIR}/mypy_full.txt" | head -10 >> "${SNAPSHOT_DIR}/files_detail.txt"
        echo "" >> "${SNAPSHOT_DIR}/files_detail.txt"
    fi
done < "${SNAPSHOT_DIR}/top_files.txt"

# 요약 생성
cat > "${SNAPSHOT_DIR}/summary.txt" << EOF
# Phase 11 MyPy 스냅샷 요약
# 타임스탬프: ${TS}
# 총 에러 수: ${ERROR_COUNT}

## TOP 10 FILES (에러 많은 순)
$(head -10 "${SNAPSHOT_DIR}/top_files.txt")

## 다음 타겟 추천
$(head -3 "${SNAPSHOT_DIR}/top_files.txt" | sed 's/^[[:space:]]*[0-9]*[[:space:]]*//')

## 게이트 상태
- MyPy: ${ERROR_COUNT} errors
- pytest: $(cd packages/afo-core && python -m pytest tests/ --tb=no -q 2>/dev/null | grep -E "(passed|failed|errors)" | tail -1 || echo "실행 실패")
- Health: $(curl -fsS -m 2 http://127.0.0.1:8010/api/health/comprehensive >/dev/null 2>&1 && echo "✅" || echo "❌")
EOF

echo "✅ 스냅샷 완료: ${SNAPSHOT_DIR}"
echo ""
echo "📋 TOP 5 FILES:"
head -5 "${SNAPSHOT_DIR}/top_files.txt"
echo ""
echo "📈 총 에러: ${ERROR_COUNT} (목표: 170)"
echo ""
echo "📁 증거 번들 위치: ${SNAPSHOT_DIR}"
