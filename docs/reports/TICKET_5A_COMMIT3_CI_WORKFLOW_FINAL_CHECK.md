# Ticket 5-A Commit 3: CI Workflow 최종 점검 (Stage-0)

**As-of:** 2025-12-23  
**Scope:** `.github/workflows/revalidate.yml` 최종 점검  
**Status:** 🔍 **Final Check Complete**

---

## ✅ Stage-0 판정: "CI까지 빌드/실행 가능 상태"

### 현재 상태 (팩트)

1. **로컬/레포 상태**
   - ✅ `pnpm-lock.yaml` 존재
   - ✅ `pnpm install (frozen-lockfile)` 통과 가능
   - ✅ `pnpm build` 통과 가능
   - → **워크스페이스 자체는 건강함**

2. **CI 워크플로**
   - ✅ `.github/workflows/revalidate.yml` 추가됨
   - ✅ Guard 단계 (Secret/URL 검증)
   - ✅ 첫 푸시 케이스 처리 (`0000000...`)
   - ✅ MAX_KEYS 상한 적용 (25)
   - ✅ 폭주/누락 방지 장치 포함

3. **남은 작업**
   - ⚠️ GitHub Actions 설정 (Secret + Variable)
   - ⚠️ 배포 환경 변수 (`REVALIDATE_SECRET`)
   - ⚠️ 외부 접근 가능 확인

---

## 🔍 잠재적 문제점 점검 (YAML/셸 포인트)

### 1. outputs 공백 처리

**현재 코드:**
```bash
echo "keys=$OUT" >> "$GITHUB_OUTPUT"
```

**잠재적 문제:**
- `$OUT`이 공백으로 시작하면 GitHub Actions outputs에 공백이 포함됨
- 예: `keys= home-hero` (공백 포함)

**개선 방안:**
```bash
# 방법 1: 선행 공백 제거
OUT="${OUT# }"
echo "keys=$OUT" >> "$GITHUB_OUTPUT"

# 방법 2: 공백 정규화 (xargs)
OUT="$(echo $OUT | xargs)"
echo "keys=$OUT" >> "$GITHUB_OUTPUT"

# 방법 3: 빈 값 체크 추가
if [[ -n "$OUT" ]]; then
  OUT="${OUT# }"  # 선행 공백 제거
  echo "keys=$OUT" >> "$GITHUB_OUTPUT"
fi
```

**권장:** 방법 1 (선행 공백 제거) - 가장 단순하고 안전

---

### 2. quote 처리 (payload 생성)

**현재 코드:**
```bash
payload='{"fragmentKey":"'"$key"'"}'
curl --fail-with-body -sS -X POST "${REVALIDATE_URL}" \
  -H "x-revalidate-secret: ${{ secrets.REVALIDATE_SECRET }}" \
  -H "content-type: application/json" \
  -d "${payload}"
```

**점검 결과:**
- ✅ 이미 안전함
- `'"$key"'` 패턴은 quote 이스케이프가 올바르게 처리됨
- `$key`는 정규식으로 검증되므로 특수문자 없음

**결론:** 수정 불필요

---

### 3. 첫 푸시 케이스 처리

**현재 코드:**
```bash
if [[ -z "$BEFORE" || "$BEFORE" == "0000000000000000000000000000000000000000" ]]; then
  BEFORE="HEAD~1"
  AFTER="HEAD"
fi
```

**점검 결과:**
- ✅ 이미 처리되어 있음
- 첫 푸시 시 `HEAD~1`로 fallback

**결론:** 수정 불필요

---

### 4. MAX_KEYS 로직

**현재 코드:**
```bash
COUNT=0
OUT=""
for k in $KEYS; do
  COUNT=$((COUNT+1))
  if [[ "$COUNT" -le "${MAX_KEYS}" ]]; then
    OUT="$OUT $k"
  fi
done
```

**점검 결과:**
- ✅ 로직 정상
- COUNT 증가 후 비교하는 방식은 안전함

**잠재적 개선:**
- `$KEYS`가 빈 값이면 루프가 실행되지 않음 (정상)
- `$OUT`이 공백으로 시작할 수 있음 (위의 outputs 공백 처리로 해결)

**결론:** outputs 공백 처리만 개선하면 됨

---

### 5. set -euo pipefail

**현재 코드:**
- Guard 단계: `set -euo pipefail` 없음
- Detect 단계: `set -euo pipefail` 없음
- Call revalidate API 단계: `set -euo pipefail` 없음

**점검 결과:**
- ⚠️ `set -euo pipefail`이 없으면 에러가 무시될 수 있음
- 하지만 `curl --fail-with-body`로 에러 감지는 가능

**권장:**
- Guard 단계에 `set -euo pipefail` 추가 (필수)
- Detect 단계는 선택적 (빈 값 처리 필요)
- Call revalidate API 단계는 선택적 (curl 실패 시 계속 진행 가능)

---

## 🔧 최종 패치 (diff)

### 패치 1: outputs 공백 처리 개선

```diff
--- a/.github/workflows/revalidate.yml
+++ b/.github/workflows/revalidate.yml
@@ -111,7 +111,8 @@ jobs:
           # 상한 적용
           COUNT=0
           OUT=""
           for k in $KEYS; do
             COUNT=$((COUNT+1))
             if [[ "$COUNT" -le "${MAX_KEYS}" ]]; then
               OUT="$OUT $k"
             fi
           done
 
-          echo "keys=$OUT" >> "$GITHUB_OUTPUT"
+          # 선행 공백 제거 후 outputs에 추가
+          if [[ -n "$OUT" ]]; then
+            OUT="${OUT# }"
+            echo "keys=$OUT" >> "$GITHUB_OUTPUT"
+          else
+            echo "keys=" >> "$GITHUB_OUTPUT"
+          fi
```

### 패치 2: Guard 단계에 set -euo pipefail 추가

```diff
--- a/.github/workflows/revalidate.yml
+++ b/.github/workflows/revalidate.yml
@@ -67,6 +67,7 @@ jobs:
       - name: Guard - required secret/url
         shell: bash
         run: |
+          set -euo pipefail
           if [[ -z "${{ secrets.REVALIDATE_SECRET }}" ]]; then
             echo "Missing secrets.REVALIDATE_SECRET" >&2
             exit 1
```

---

## ✅ 최단 루트로 검증 (복붙용)

### A) 배포 URL이 살아있는지 (로컬에서 30초 컷)

```bash
export REVALIDATE_URL="https://<your-domain>/api/revalidate"
export REVALIDATE_SECRET="(배포와 동일한 값)"

curl -i -X POST "$REVALIDATE_URL" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

**예상 결과:**
- ✅ 200 OK: `{"ok": true, "revalidated": ["/fragments/home-hero.html"]}`
- ❌ 401 Unauthorized: Secret 불일치
- ❌ 400 Bad Request: fragmentKey 검증 실패
- ❌ Timeout/403: WAF/Cloudflare 차단

### B) revalidate 전/후로 fragment가 바뀌는지 SHA로 확인

```bash
# 1. 현재 fragment 내용 확인
curl -fsS "https://<your-domain>/fragments/home-hero.html" | shasum -a 256

# 2. Fragment 파일 수정 후 revalidate 호출
# (GitHub Actions에서 자동 또는 수동 실행)

# 3. 변경 후 fragment 내용 확인
curl -fsS "https://<your-domain>/fragments/home-hero.html" | shasum -a 256
```

**예상 결과:**
- SHA 해시가 변경됨 (revalidate 성공)
- 또는 동일 (revalidate 실패 또는 내용 미변경)

### C) GitHub Actions에서 수동 실행 (workflow_dispatch)

**절차:**
1. GitHub Repository → Actions 탭
2. `Revalidate fragments (dynamic)` 워크플로우 선택
3. Run workflow 버튼 클릭
4. (input 없음 - 자동으로 변경 파일 감지)
5. Run workflow 클릭

**예상 결과:**
- ✅ Guard 단계 통과: Secret/URL 검증 성공
- ✅ Detect 단계: 변경된 fragment keys 감지 (없으면 "No-op" 메시지)
- ✅ Call revalidate API 단계: API 호출 성공 (200 OK)
- ❌ Guard 단계 실패: `Missing secrets.REVALIDATE_SECRET` 또는 `Missing vars.REVALIDATE_URL`

---

## 🚨 가장 흔한 실패 패턴 (바로 처방)

### 1. Guard에서 즉시 실패

**증상:**
```
Missing secrets.REVALIDATE_SECRET
```

**원인:**
- `REVALIDATE_SECRET` 또는 `REVALIDATE_URL` 미설정/오타

**처방:**
- Repository → Settings → Secrets and variables → Actions
- Secret: `REVALIDATE_SECRET` 확인
- Variable: `REVALIDATE_URL` 확인

---

### 2. curl이 401

**증상:**
```
{"ok": false, "error": "unauthorized"}
```

**원인:**
- 배포 환경의 `REVALIDATE_SECRET`과 GitHub Secret 값 불일치

**처방:**
- 배포 환경의 `REVALIDATE_SECRET` 확인
- GitHub Secret과 동일한 값으로 설정

---

### 3. curl이 타임아웃/403/HTML 챌린지

**증상:**
```
curl: (28) Operation timed out
curl: (403) Forbidden
<html>... Cloudflare challenge ...</html>
```

**원인:**
- WAF/Cloudflare가 `/api/revalidate`를 봇챌린지로 차단

**처방:**
- Cloudflare/WAF 설정에서 `/api/revalidate` 경로 예외 추가
- 또는 헤더 시크릿으로 보안 유지 (현재 방식 유지)

---

## 📋 최종 권장 사항

### 필수 패치

1. **outputs 공백 처리 개선** (위의 패치 1)
2. **Guard 단계에 set -euo pipefail 추가** (위의 패치 2)

### 선택적 개선

1. Detect 단계에 `set -euo pipefail` 추가 (선택적)
2. Call revalidate API 단계에 `set -euo pipefail` 추가 (선택적)

---

## 🏁 결론

**현재 상태:**
- ✅ 워크스페이스 건강함
- ✅ CI 워크플로 기본 구조 완성
- ⚠️ outputs 공백 처리 개선 필요
- ⚠️ Guard 단계에 set -euo pipefail 추가 권장

**다음 단계:**
1. 위의 패치 1, 2 적용
2. GitHub Secrets/Vars 설정
3. 수동 실행 테스트 (workflow_dispatch)
4. 자동 트리거 테스트 (fragment 파일 수정 후 push)

---

**Status:** 🔍 **Final Check Complete**  
**Next Action:** 패치 적용 후 GitHub Secrets/Vars 설정

