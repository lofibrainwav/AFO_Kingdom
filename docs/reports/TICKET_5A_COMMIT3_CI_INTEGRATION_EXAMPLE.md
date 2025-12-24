# Ticket 5-A Commit 3: CI 통합 (예시/설계 단계)

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 3 (CI 통합)  
**Status:** 🟡 **Example/Design Phase (Not Implemented)**

---

## 📋 팩트 (현재 상태)

- **Commit 3**: CI 통합 (설계/예시 단계 🟡)
- **목적**: 변경된 fragment에 대해 CI에서 revalidate API 호출 자동화
- **상태**: 워크플로우 YAML 예시 준비 (적용 전)

---

## 📝 예시 YAML (붙여넣기용) — 안전/확실 버전

**파일**: `.github/workflows/revalidate.yml` (예시/미구현)

> **사전 준비 (필수)**
> - GitHub **Secrets**: `REVALIDATE_SECRET`
> - GitHub **Variables** (또는 Secrets): `REVALIDATE_URL`
>   예: `https://afo.kingdom/api/revalidate` (실서버 엔드포인트)

```yaml
name: Revalidate changed fragments

on:
  push:
    branches: [main]
    paths:
      - "packages/dashboard/public/fragments/**"
      - "packages/dashboard/src/app/docs/**"
      - "docs/**"

jobs:
  revalidate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Detect changed fragment keys
        id: detect
        shell: bash
        run: |
          set -euo pipefail

          BEFORE="${{ github.event.before }}"
          AFTER="${{ github.sha }}"

          # diff가 실패하면(예: 첫 커밋/얕은 히스토리) fallback
          CHANGED="$(git diff --name-only "$BEFORE" "$AFTER" 2>/dev/null || git diff --name-only HEAD~1 HEAD || true)"
          echo "Changed files:"
          echo "$CHANGED"

          # fragments/*.html 에서 key 추출
          KEYS=""
          while IFS= read -r f; do
            [[ "$f" =~ ^packages/dashboard/public/fragments/.*\.html$ ]] || continue
            key="$(basename "$f" .html)"

            # API와 동일한 정규식으로 1차 검증 (공백 없음)
            if [[ "$key" =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]; then
              KEYS="$KEYS $key"
            fi
          done <<< "$CHANGED"

          # 중복 제거 + 최대 20개 제한(폭주 방지)
          KEYS="$(echo "$KEYS" | tr ' ' '\n' | awk 'NF' | sort -u | head -n 20 | tr '\n' ' ')"

          echo "fragment_keys=$KEYS" >> "$GITHUB_OUTPUT"
          echo "Detected fragment keys: $KEYS"

      - name: Trigger revalidate API (per fragment)
        if: steps.detect.outputs.fragment_keys != ''
        env:
          REVALIDATE_URL: ${{ vars.REVALIDATE_URL }}
          REVALIDATE_SECRET: ${{ secrets.REVALIDATE_SECRET }}
        shell: bash
        run: |
          set -euo pipefail

          if [[ -z "${REVALIDATE_URL:-}" ]]; then
            echo "Missing vars.REVALIDATE_URL"
            exit 1
          fi

          for key in ${{ steps.detect.outputs.fragment_keys }}; do
            echo "Revalidating: $key"
            curl -fS -X POST "$REVALIDATE_URL" \
              -H "content-type: application/json" \
              -H "x-revalidate-secret: $REVALIDATE_SECRET" \
              -d "{\"fragmentKey\":\"$key\"}"
          done
```

---

## 📋 커밋 메시지 (예시)

```txt
ci: revalidate changed fragments on push to main
```

---

## 🔒 SSOT 일관성 보장

### ✅ 유지할 것 (절대 건드리지 않음)

1. **SSOT 규칙**
   - slug 검증 (Contract Gate와 동일)
   - fragment_key 필수 (빌드 타임 검증)
   - 렌더링 우선순위 (React → Fragment → 404)

2. **Gate 검증**
   - 빌드 타임 검증 유지
   - Contract Gate 유지
   - fragment_key 검증 유지

3. **기존 Fragment**
   - `public/fragments/{fragment_key}.html` 유지
   - fragment overwrite 없음

### ✅ 확장 가능한 것 (읽기 경로만)

1. **CI 통합**
   - 변경된 fragmentKey 자동 감지
   - revalidate API 자동 호출

---

## ⚠️ 주의사항

- **정규식 오타 금지**: `/^[A-Za-z0-9].../` (공백 없음)
- **Content-Type 필수**: curl 예시에 `-H "content-type: application/json"` 포함
- **상태 명확화**: Commit 3는 **예시/설계 단계** (미구현)
- **pnpm filter 대신**: `working-directory: packages/dashboard` 사용 (안전)

---

**Status:** 🟡 **Example/Design Phase (Not Implemented)**  
**Next Action:** 필요 시 구현 시작

