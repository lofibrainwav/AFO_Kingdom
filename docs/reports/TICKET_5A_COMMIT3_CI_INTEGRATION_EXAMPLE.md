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

### FACTS

- CI에서 "변경된 fragments/*.html"만 찾아 **해당 key만 revalidate**하는 안전 자동화.
- Secret/URL은 **하드코딩 금지**:
  - `secrets.REVALIDATE_SECRET` 필수
  - `vars.REVALIDATE_URL` 권장 (예: `https://your-domain.com/api/revalidate`)
- 변경 파일이 많아도 폭주 방지 위해 **상한(MAX_KEYS)** 적용.

### PASTE (최종 붙여넣기 버전)

```yaml
name: Revalidate fragments (dynamic)

on:
  push:
    branches: [main]
    paths:
      - "fragments/**"
  workflow_dispatch: {}

permissions:
  contents: read

concurrency:
  group: revalidate-${{ github.ref }}
  cancel-in-progress: true

jobs:
  revalidate:
    runs-on: ubuntu-latest

    env:
      REVALIDATE_URL: ${{ vars.REVALIDATE_URL }}
      MAX_KEYS: "25"

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Guard - required secret/url
        shell: bash
        run: |
          if [[ -z "${{ secrets.REVALIDATE_SECRET }}" ]]; then
            echo "Missing secrets.REVALIDATE_SECRET" >&2
            exit 1
          fi
          if [[ -z "${REVALIDATE_URL}" ]]; then
            echo "Missing vars.REVALIDATE_URL (e.g., https://<domain>/api/revalidate)" >&2
            exit 1
          fi

      - name: Detect changed fragment keys
        id: detect
        shell: bash
        run: |
          BEFORE="${{ github.event.before }}"
          AFTER="${{ github.sha }}"

          # 첫 푸시/예외 케이스 대비
          if [[ -z "$BEFORE" || "$BEFORE" == "0000000000000000000000000000000000000000" ]]; then
            BEFORE="HEAD~1"
            AFTER="HEAD"
          fi

          CHANGED="$(git diff --name-only "$BEFORE" "$AFTER" || true)"
          KEYS=""

          while IFS= read -r f; do
            [[ -z "$f" ]] && continue
            [[ "$f" != fragments/* ]] && continue
            [[ "$f" != *.html ]] && continue

            key="$(basename "$f" .html)"

            # fragmentKey와 동일한 정규식 (Commit 1과 일치)
            if [[ ! "$key" =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]; then
              echo "Skip invalid key derived from file: $f" >&2
              continue
            fi

            KEYS="$KEYS $key"
          done <<< "$CHANGED"

          # 상한 적용
          COUNT=0
          OUT=""
          for k in $KEYS; do
            COUNT=$((COUNT+1))
            if [[ "$COUNT" -le "${MAX_KEYS}" ]]; then
              OUT="$OUT $k"
            fi
          done

          echo "keys=$OUT" >> "$GITHUB_OUTPUT"

      - name: Call revalidate API
        if: steps.detect.outputs.keys != ''
        shell: bash
        run: |
          echo "Revalidating keys:${{ steps.detect.outputs.keys }}"
          for key in ${{ steps.detect.outputs.keys }}; do
            payload='{"fragmentKey":"'"$key"'"}'
            curl --fail-with-body -sS -X POST "${REVALIDATE_URL}" \
              -H "x-revalidate-secret: ${{ secrets.REVALIDATE_SECRET }}" \
              -H "content-type: application/json" \
              -d "${payload}"
            echo ""
          done

      - name: No-op (no fragment changes)
        if: steps.detect.outputs.keys == ''
        run: echo "No fragment changes detected; skipping."
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

