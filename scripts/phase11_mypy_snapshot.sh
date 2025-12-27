#!/bin/bash
# Phase 11 MyPy 스냅샷 생성 스크립트
# SSOT 작전문 준수: 증거 번들 필수

set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_DIR="artifacts/mypy/phase11/${TIMESTAMP}"
mkdir -p "$SNAPSHOT_DIR"

echo "📸 Phase 11 MyPy 스냅샷 생성: $TIMESTAMP"
echo "====================================="

# 1. MyPy 전체 결과 저장
echo "🔍 MyPy 전체 분석..."
cd packages/afo-core
mypy AFO/ --config-file ../../pyproject.toml --show-error-codes > "../../$SNAPSHOT_DIR/mypy_full.txt" 2>&1

# 2. 에러 카운트
ERROR_COUNT=$(grep -c "error:" "../../$SNAPSHOT_DIR/mypy_full.txt" || echo "0")
echo "📊 총 에러 수: $ERROR_COUNT"

# 3. 파일별 에러 분포 (TOP 20)
echo "📋 파일별 에러 분포 (TOP 20):" > "../../$SNAPSHOT_DIR/files_summary.txt"
grep "error:" "../../$SNAPSHOT_DIR/mypy_full.txt" | 
    sed 's/:.*$//' | 
    sort | 
    uniq -c | 
    sort -nr | 
    head -20 >> "../../$SNAPSHOT_DIR/files_summary.txt"

# 4. 에러 타입별 분포 (TOP 10)
echo "🔧 에러 타입별 분포 (TOP 10):" > "../../$SNAPSHOT_DIR/error_types.txt"
grep "error:" "../../$SNAPSHOT_DIR/mypy_full.txt" | 
    sed 's/.*\[//' | 
    sed 's/\].*$//' | 
    sort | 
    uniq -c | 
    sort -nr | 
    head -10 >> "../../$SNAPSHOT_DIR/error_types.txt"

# 5. 요약 생성
cat > "../../$SNAPSHOT_DIR/summary.txt" << SUMMARY_EOF
Phase 11 MyPy 스냅샷 - $TIMESTAMP
================================

총 에러 수: $ERROR_COUNT
목표: 236 → 170 (66개 감소 필요)
현재: 236 → $ERROR_COUNT ($(expr 236 - $ERROR_COUNT)개 감소)

TOP FILES (에러 많은 순):
$(head -10 "../../$SNAPSHOT_DIR/files_summary.txt")

TOP ERROR TYPES:
$(head -10 "../../$SNAPSHOT_DIR/error_types.txt")
SUMMARY_EOF

echo "✅ 스냅샷 완료: $SNAPSHOT_DIR"
echo "📄 요약: $SNAPSHOT_DIR/summary.txt"
cd ../..
cat "$SNAPSHOT_DIR/summary.txt"
EOF && chmod +x scripts/phase11_mypy_snapshot.sh