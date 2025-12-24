# Ticket 5-A Commit 3: CI 설정 체크리스트 및 자동 검증 가이드 완료 보고서 (SSOT)

**As-of:** 2025-12-24  
**커밋 해시**: 
- `b44de1f`: `docs(reports): add CI setup checklist and auto verification step guide`
- `9324df5`: `docs(reports): improve CI setup checklist and auto verification (final paste-ready)`
- `cbf8c61`: `ci: improve revalidate workflow robustness (outputs trim, set -euo)`

**방법**: Sequential Thinking + Context7 기반 검증  
**Status**: ✅ **Complete**

---

## ✅ 완료 요약 (팩트 기반, SSOT 일관성)

### 생성된 파일

1. **TICKET_5A_COMMIT3_CI_SETUP_CHECKLIST.md**
   - GitHub Secrets/Vars 설정 체크리스트
   - 실수 포인트 정리 (Secret 공백/불일치, Variable 경로 누락, env 빌드/런타임 분리)
   - 복붙 가능한 검증 루틴 (curl + SHA 비교 + Actions 수동 실행)
   - 실패 진단 가이드 (HTTP status/body 로그 복붙)
   - Repo Settings 체크리스트 템플릿

2. **TICKET_5A_COMMIT3_CI_AUTO_VERIFICATION_STEP.md**
   - fragment SHA 자동 검증 Step (Option A 간단/추천, Option B 상세)
   - SHA 검증 의미 정확화 (SHA 동일도 OK)
   - cache-control 헤더 추가 (CDN 영향 최소화)
   - Fragment URL trailing slash 제거

3. **.github/workflows/revalidate.yml**
   - Guard 단계 (Secret/URL 검증)
   - 첫 푸시 케이스 처리 (`0000000...`)
   - MAX_KEYS 상한 적용 (25)
   - outputs 공백 처리 개선
   - REVALIDATE_URL trailing slash 제거

### 주요 내용

**실수 포인트 3개 정리:**
1. GitHub Secret: `REVALIDATE_SECRET` (공백/불일치)
2. GitHub Variable: `REVALIDATE_URL` (경로 누락/trailing slash)
3. 배포 환경 변수: `REVALIDATE_SECRET` (빌드/런타임 분리)

**복붙 가능한 검증 루틴:**
- A) 배포 URL POST 동작 확인 (멀티라인 버전)
- B) fragment 응답 SHA 확인
- C) Actions 수동 실행 (workflow_dispatch)

**실패 진단 가이드:**
- Guard에서 즉시 실패 → Secret/Var 미설정
- curl이 401 → Secret 불일치
- curl이 타임아웃/403 → WAF/Cloudflare 차단
- curl이 400 → fragmentKey 검증 실패

**자동 검증 Step (선택적):**
- Option A: 간단한 검증 (첫 번째 key만, 추천)
- Option B: 상세한 검증 (전체 keys)

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
   - 자동 검증 Step (선택적)

---

## 📋 다음 단계 실행 가이드

### 1. GitHub Secrets/Vars 설정 (체크리스트 복붙 템플릿)

**Secret 설정:**
```
Name: REVALIDATE_SECRET
Value: [배포 환경과 동일한 값]
```

**체크리스트:**
- [ ] 앞뒤 공백 없음
- [ ] 대소문자 정확
- [ ] 배포 환경 값과 동일

**Variable 설정:**
```
Name: REVALIDATE_URL
Value: https://<your-domain>/api/revalidate
```

**체크리스트:**
- [ ] `https://`로 시작
- [ ] `/api/revalidate` 경로 포함
- [ ] 마지막 슬래시 없음 (`/api/revalidate/` ❌)
- [ ] 실제 배포 도메인 사용 (프리뷰/스테이징 아님)

---

### 2. 로컬 curl 테스트 (검증 루틴 A 복붙)

**멀티라인 버전 (그대로 복붙 가능):**

```bash
export REVALIDATE_URL="https://<your-domain>/api/revalidate"
export REVALIDATE_SECRET="(배포 환경과 동일한 값)"

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

---

### 3. Actions 수동 실행 (검증 루틴 C)

**절차:**
1. GitHub Repository → Actions 탭
2. `Revalidate fragments (dynamic)` 워크플로우 선택
3. **Run workflow** 버튼 클릭
4. (input 없음 - 자동으로 변경 파일 감지)
5. **Run workflow** 클릭

**예상 결과:**
- ✅ Guard 단계 통과: Secret/URL 검증 성공
- ✅ Detect 단계: 변경된 fragment keys 감지 (없으면 "No-op" 메시지)
- ✅ Call revalidate API 단계: API 호출 성공 (200 OK)
- ❌ Guard 단계 실패: `Missing secrets.REVALIDATE_SECRET` 또는 `Missing vars.REVALIDATE_URL`

---

### 4. 자동 검증 Step 추가 (선택적 Option A 추천)

**위치:** `.github/workflows/revalidate.yml`의 `Call revalidate API` step 이후

**Option A: 간단한 검증 (추천)**
- 첫 번째 key만 SHA 검증
- 빠르고 안전
- 실패해도 workflow 계속 진행

**상세 내용:** `docs/reports/TICKET_5A_COMMIT3_CI_AUTO_VERIFICATION_STEP.md` 참고

---

## 🚨 실패 시 진단 가이드

### 일반적인 실패 패턴 및 처방

#### 1. Guard에서 즉시 실패

**증상:**
```
Missing secrets.REVALIDATE_SECRET
```

**원인:**
- GitHub Secret 미설정 또는 오타

**처방:**
- Repository → Settings → Secrets and variables → Actions
- Secret: `REVALIDATE_SECRET` 확인

---

#### 2. curl이 401

**증상:**
```
HTTP/1.1 401 Unauthorized
{"ok": false, "error": "unauthorized"}
```

**원인:**
- 배포 환경의 `REVALIDATE_SECRET`과 GitHub Secret 값 불일치

**처방:**
- 배포 환경의 `REVALIDATE_SECRET` 확인
- GitHub Secret과 동일한 값으로 설정

---

#### 3. curl이 타임아웃/403/HTML 챌린지

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

## 📋 참고 문서

- **설정 가이드**: `docs/reports/TICKET_5A_COMMIT3_CI_SETUP_CHECKLIST.md`
- **자동 검증 Step**: `docs/reports/TICKET_5A_COMMIT3_CI_AUTO_VERIFICATION_STEP.md`
- **구현 완료 가이드**: `docs/reports/TICKET_5A_COMMIT3_CI_IMPLEMENTATION_COMPLETE.md`
- **워크플로우 최종 점검**: `docs/reports/TICKET_5A_COMMIT3_CI_WORKFLOW_FINAL_CHECK.md`

---

## 🏁 결론

**구현 완료:**
- CI 설정 체크리스트 문서화 ✅
- 자동 검증 Step 가이드 제공 ✅
- 워크플로우 안전성 향상 ✅

**다음 단계:**
1. GitHub Secrets/Vars 설정 (체크리스트 참고)
2. 로컬 curl 테스트 (검증 루틴 A)
3. Actions 수동 실행 (검증 루틴 C)
4. (선택) 자동 검증 Step 추가

---

**Status:** ✅ **Complete**  
**SSOT 일관성:** ✅ **Maintained**  
**Next Action:** GitHub Secrets/Vars 설정 후 검증

