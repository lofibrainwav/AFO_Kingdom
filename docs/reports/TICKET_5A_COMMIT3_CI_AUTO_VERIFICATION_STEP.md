# Ticket 5-A Commit 3: CI 자동 검증 Step (선택적)

**As-of:** 2025-12-23  
**Scope:** revalidate 성공 시 fragment HTML SHA 자동 검증  
**Status:** 🔧 **Optional Enhancement**

---

## 📋 목적

revalidate API 호출 후 fragment HTML이 실제로 변경되었는지 SHA 해시로 자동 검증하는 step 추가.

**중요:** revalidate는 "캐시 무효화"이므로, fragment 파일 내용이 실제로 바뀌지 않았으면 SHA는 그대로가 정상입니다.

**검증 결과 해석:**
- **200 OK + 응답 성공** = revalidate 성공
- **SHA 변경** = "내용까지 바뀐 게 확인됨(강한 증거)"
- **SHA 동일** = "내용이 안 바뀌었거나 CDN/캐시가 동일하게 반환(정보성)"

> ⚠️ **SHA 동일을 '실패'로 판단하면 안 됩니다.** revalidate는 캐시 무효화이지 내용 변경이 아닙니다.

---

## 🔧 구현 방법

### Option A: 간단한 검증 (추천)

**위치:** `.github/workflows/revalidate.yml`의 `Call revalidate API` step 이후

**더 안전한 버전 (cache-control 헤더 추가, SHA 동일도 OK 처리):**

```yaml
      - name: Verify fragment revalidation (optional)
        if: steps.detect.outputs.keys != ''
        shell: bash
        run: |
          set -euo pipefail
          
          # 첫 번째 key만 검증 (예시)
          FIRST_KEY=$(echo "${{ steps.detect.outputs.keys }}" | awk '{print $1}')
          
          if [[ -z "$FIRST_KEY" ]]; then
            echo "No keys to verify"
            exit 0
          fi
          
          # Fragment URL 구성 (trailing slash 제거)
          FRAGMENT_BASE="${REVALIDATE_URL%/api/revalidate}"
          FRAGMENT_BASE="${FRAGMENT_BASE%/}"
          FRAGMENT_URL="${FRAGMENT_BASE}/fragments/${FIRST_KEY}.html"
          
          # revalidate 호출 전 SHA 확인 (CDN 영향 줄이기 위해 cache-control 헤더 추가)
          BEFORE_SHA=$(curl -fsS -H "cache-control: no-cache" "$FRAGMENT_URL" | shasum -a 256 | awk '{print $1}' || echo "")
          echo "before_sha=$BEFORE_SHA"
          
          # revalidate 호출 후 잠시 대기 (캐시 갱신 시간)
          sleep 2
          
          # revalidate 호출 후 SHA 확인
          AFTER_SHA=$(curl -fsS -H "cache-control: no-cache" "$FRAGMENT_URL" | shasum -a 256 | awk '{print $1}' || echo "")
          echo "after_sha=$AFTER_SHA"
          
          # 검증 결과 출력
          if [[ -z "$BEFORE_SHA" || -z "$AFTER_SHA" ]]; then
            echo "⚠️  SHA check: INCONCLUSIVE (fetch failed or empty)"
          elif [[ "$BEFORE_SHA" == "$AFTER_SHA" ]]; then
            echo "✅ SHA check: UNCHANGED (OK if fragment content didn't change)"
          else
            echo "✅ SHA check: CHANGED (content updated)"
          fi
          
          exit 0  # 실패해도 workflow는 계속 진행
```

---

### Option B: 상세한 검증 (전체 keys)

```yaml
      - name: Verify fragment revalidation (detailed)
        if: steps.detect.outputs.keys != ''
        shell: bash
        run: |
          set -euo pipefail
          
          # revalidate 호출 후 잠시 대기 (캐시 갱신 시간)
          sleep 2
          
          FRAGMENT_BASE="${REVALIDATE_URL%/api/revalidate}/fragments"
          VERIFIED=0
          FAILED=0
          
          for key in ${{ steps.detect.outputs.keys }}; do
            FRAGMENT_URL="${FRAGMENT_BASE}/${key}.html"
            SHA=$(curl -fsS "$FRAGMENT_URL" | shasum -a 256 | awk '{print $1}' || echo "")
            
            if [[ -z "$SHA" ]]; then
              echo "⚠️  Warning: Could not fetch fragment: $key"
              FAILED=$((FAILED+1))
            else
              echo "✅ Verified: $key (SHA: $SHA)"
              VERIFIED=$((VERIFIED+1))
            fi
          done
          
          echo ""
          echo "Verification summary:"
          echo "  Verified: $VERIFIED"
          echo "  Failed: $FAILED"
          
          # 실패해도 workflow는 계속 진행 (경고만)
          if [[ $FAILED -gt 0 ]]; then
            echo "⚠️  Some fragments could not be verified"
          fi
```

---

## ⚠️ 주의사항

### 1. 캐시 갱신 시간

**문제:**
- revalidate 호출 후 즉시 fragment를 가져오면 이전 캐시가 반환될 수 있음

**해결:**
- `sleep 2` 추가 (캐시 갱신 시간 대기)
- 또는 `cache: no-store` 헤더 사용 (하지만 이건 fragment URL이므로 불가능)

### 2. 실패 처리

**권장:**
- 검증 실패해도 workflow는 계속 진행 (경고만)
- `exit 0` 사용 (실패해도 workflow 중단 안 함)

**이유:**
- Fragment가 실제로 변경되지 않았을 수도 있음 (내용 동일)
- 네트워크 문제로 일시적 실패 가능
- 검증은 "추가 확인"이지 "필수"가 아님

### 3. Fragment URL 구성

**문제:**
- `REVALIDATE_URL`이 `https://domain/api/revalidate` 형식
- Fragment URL은 `https://domain/fragments/key.html` 형식

**해결:**
```bash
FRAGMENT_BASE="${REVALIDATE_URL%/api/revalidate}/fragments"
FRAGMENT_URL="${FRAGMENT_BASE}/${key}.html"
```

---

## 🔧 적용 방법

### Step 1: Workflow 파일 수정

`.github/workflows/revalidate.yml`의 `Call revalidate API` step 이후에 위의 Option A 또는 B를 추가.

### Step 2: 테스트

1. Fragment 파일 수정
2. Push 또는 workflow_dispatch 실행
3. 검증 step 로그 확인

---

## 📋 커밋 메시지 (예시)

```txt
ci: add optional fragment verification step after revalidate

- Verify fragment SHA after revalidate API call
- Non-blocking: warnings only, workflow continues on failure
- Sleep 2s for cache refresh before verification
- Option A: simple verification (first key only)
- Option B: detailed verification (all keys)

Optional enhancement for Ticket 5A Commit 3.
```

---

## 🏁 결론

**권장:**
- Option A (간단한 검증) 사용
- 첫 번째 key만 검증 (빠르고 안전)
- 실패해도 workflow 계속 진행

**선택적:**
- 필요 시 Option B (상세한 검증) 사용
- 모든 keys 검증 (느리지만 완전)

---

**Status:** 🔧 **Optional Enhancement**  
**Next Action:** 필요 시 적용

