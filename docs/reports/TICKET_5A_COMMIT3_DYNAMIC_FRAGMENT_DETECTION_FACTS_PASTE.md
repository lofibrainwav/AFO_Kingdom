# Ticket 5A Commit 3 — Dynamic Fragment Detection Example (FACTS/PASTE)

**As-of**: 2025-12-24  
**Status**: 예시 (제안)  
**SSOT 원칙 준수**: 팩트 기반, 복붙 가능한 최종본

---

## FACTS (검증됨)

* "변경된 파일 목록 → fragmentKey 리스트 생성 → API 호출"은 GitHub Actions에서 흔히 쓰는 패턴이고, **Guard(Secret/URL) + 상한(MAX_KEYS)** 같은 안전장치가 핵심이다. *(왕국 구현 방향과도 일치)*
* `revalidate`는 "캐시 무효화"라서 **내용이 안 바뀌면 SHA가 동일해도 정상**이다(이미 형님이 문서에 반영한 규칙).

---

## PASTE (최종 붙여넣기 버전)

> 아래는 "변경된 fragments/**/*.html"에서 key를 뽑아 **최대 25개만** 호출하는 step 예시.  
> **jq 없이**(러너 환경 편차 방지) python으로 JSON 만들어서 안정성 올림.

```yaml
- name: Detect fragment keys
  id: detect
  shell: bash
  run: |
    set -euo pipefail

    BASE="${{ github.event.before }}"
    HEAD="${{ github.sha }}"

    # 첫 푸시(0000...) 방어
    if [[ "$BASE" == "0000000000000000000000000000000000000000" ]]; then
      BASE="$(git rev-parse "${HEAD}~1" || true)"
    fi

    if [[ -z "${BASE:-}" ]]; then
      echo "keys=" >> "$GITHUB_OUTPUT"
      echo "count=0" >> "$GITHUB_OUTPUT"
      exit 0
    fi

    files="$(git diff --name-only "$BASE" "$HEAD" -- 'fragments/**/*.html' || true)"
    if [[ -z "${files// }" ]]; then
      echo "keys=" >> "$GITHUB_OUTPUT"
      echo "count=0" >> "$GITHUB_OUTPUT"
      exit 0
    fi

    MAX_KEYS=25
    count=0
    keys=()

    while IFS= read -r f; do
      [[ -z "${f// }" ]] && continue

      # fragments/home-hero.html -> home-hero
      b="$(basename "$f")"
      key="${b%.html}"

      # 형님이 쓰는 동일 정규식 정책
      if [[ ! "$key" =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]; then
        echo "skip invalid key: $key" >&2
        continue
      fi

      keys+=("$key")
      count=$((count+1))
      if [[ "$count" -ge "$MAX_KEYS" ]]; then
        break
      fi
    done <<< "$files"

    if [[ "$count" -eq 0 ]]; then
      echo "keys=" >> "$GITHUB_OUTPUT"
      echo "count=0" >> "$GITHUB_OUTPUT"
      exit 0
    fi

    joined="$(IFS=,; echo "${keys[*]}")"
    echo "keys=$joined" >> "$GITHUB_OUTPUT"
    echo "count=$count" >> "$GITHUB_OUTPUT"

- name: Revalidate changed fragments
  if: steps.detect.outputs.count != '0'
  shell: bash
  env:
    REVALIDATE_SECRET: ${{ secrets.REVALIDATE_SECRET }}
    REVALIDATE_URL: ${{ vars.REVALIDATE_URL }}
  run: |
    set -euo pipefail

    [[ -n "${REVALIDATE_SECRET:-}" ]] || { echo "missing REVALIDATE_SECRET" >&2; exit 1; }
    [[ -n "${REVALIDATE_URL:-}" ]] || { echo "missing REVALIDATE_URL" >&2; exit 1; }

    # trailing slash 제거
    REVALIDATE_URL="${REVALIDATE_URL%/}"

    IFS=',' read -r -a KEYS <<< "${{ steps.detect.outputs.keys }}"

    for key in "${KEYS[@]}"; do
      KEY="$key" python3 -c "import json,os; print(json.dumps({'fragmentKey': os.environ['KEY']}))" > payload.json

      curl -fsS -X POST "$REVALIDATE_URL" \
        -H "x-revalidate-secret: $REVALIDATE_SECRET" \
        -H "content-type: application/json" \
        --data-binary @payload.json \
        1>/dev/null

      echo "revalidated: $key"
    done
```

---

**참고 자료**:
- GitHub Actions: [Contexts and expression syntax](https://docs.github.com/en/actions/learn-github-actions/contexts)
- GitHub Actions: [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

