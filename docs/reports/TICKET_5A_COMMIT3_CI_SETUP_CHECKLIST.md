# Ticket 5-A Commit 3: CI 설정 체크리스트 (복붙 템플릿)

**As-of:** 2025-12-23  
**Scope:** GitHub Secrets/Vars 설정 및 배포 환경 변수 설정  
**Status:** 📋 **Setup Checklist**

---

## ⚠️ 마지막 3개 "필수" 설정, 실수 포인트

### 1) GitHub Secret: `REVALIDATE_SECRET`

**설정 위치:**
- Repository → Settings → Secrets and variables → Actions
- New repository secret
- Name: `REVALIDATE_SECRET`
- Value: (배포 환경과 **완전히 동일**해야 함)

**자주 하는 실수:**
- ❌ 앞뒤 공백 포함해서 저장
- ❌ 로컬 `.env.local` 값이랑 GitHub Secret 값이 다른데 "같다고 생각"함
- ❌ 대소문자 구분 안 함

**검증 방법:**
```bash
# 로컬에서 배포 환경 값 확인
echo "$REVALIDATE_SECRET"

# GitHub Secret과 비교 (수동)
# Repository → Settings → Secrets and variables → Actions
# REVALIDATE_SECRET 값 확인
```

**✅ 올바른 예시:**
```
Value: your-secret-key-here-12345
(앞뒤 공백 없음, 대소문자 정확)
```

---

### 2) GitHub Variable: `REVALIDATE_URL`

**설정 위치:**
- Repository → Settings → Secrets and variables → Actions
- Variables 탭
- New repository variable
- Name: `REVALIDATE_URL`
- Value: `https://<your-domain>/api/revalidate` (완전한 URL)

**자주 하는 실수:**
- ❌ `https://<domain>`까지만 넣고 끝냄 (경로 누락)
- ❌ `http://`로 넣어서 리다이렉트/차단
- ❌ 프리뷰/스테이징 도메인 넣어놓고 prod로 착각
- ❌ 마지막 슬래시 포함 (`/api/revalidate/` ❌)

**✅ 올바른 예시:**
```
Value: https://afo.kingdom/api/revalidate
(https://, 경로 포함, 마지막 슬래시 없음)
```

**❌ 잘못된 예시:**
```
https://afo.kingdom                    # 경로 누락
http://afo.kingdom/api/revalidate      # http (리다이렉트/차단 가능)
https://afo.kingdom/api/revalidate/    # 마지막 슬래시 (불필요)
```

---

### 3) 배포 환경 변수: `REVALIDATE_SECRET`

**설정 위치:**
- Vercel: Project Settings → Environment Variables
- Cloudflare Pages: Settings → Environment Variables
- Railway: Variables 탭
- Docker: `.env` 파일 또는 `docker-compose.yml`
- 기타: 배포 플랫폼의 환경 변수 설정

**자주 하는 실수:**
- ❌ "빌드 시 env"에만 넣고 런타임엔 없음
- ❌ 스테이징에만 넣고 프로덕션엔 없음
- ❌ GitHub Secret과 값이 다름

**✅ 올바른 설정:**
```
Environment: Production (또는 All Environments)
Name: REVALIDATE_SECRET
Value: (GitHub Secret과 동일한 값)
```

**검증 방법:**
```bash
# 배포 환경에서 확인 (실제 배포 환경에 따라 다름)
# 예: Vercel CLI
vercel env ls

# 예: Docker
docker exec <container> env | grep REVALIDATE_SECRET
```

---

## 📋 "1분 컷" 최종 검증 루틴 (복붙 그대로)

### A) 배포 URL POST 동작 확인

**멀티라인 버전 (그대로 복붙 가능):**

```bash
export REVALIDATE_URL="https://<your-domain>/api/revalidate"
export REVALIDATE_SECRET="(배포 환경과 동일한 값)"

curl -i -X POST "$REVALIDATE_URL" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

> **주의:** 위의 커맨드는 **멀티라인**으로 작성되어 있어 그대로 복붙하면 정상 실행됩니다. 한 줄로 붙이면 bash에서 실행 실패할 수 있습니다.

**예상 결과:**
- ✅ 200 OK: `{"ok": true, "revalidated": ["/fragments/home-hero.html"]}`
- ❌ 401 Unauthorized: Secret 불일치
- ❌ 400 Bad Request: fragmentKey 검증 실패
- ❌ Timeout/403: WAF/Cloudflare 차단

---

### B) fragment 응답이 실제로 바뀌는지 SHA 확인

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

---

### C) Actions 수동 실행

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

## 🚨 실패하면, "응답 1줄"만 보면 바로 진단됨

### 진단 가이드

**로컬 curl 실패 시:**
```
# HTTP status 라인 + 응답 body만 복붙
HTTP/1.1 401 Unauthorized
{"ok": false, "error": "unauthorized"}
```

**Actions 실패 시:**
```
# 실패한 step의 마지막 30줄 로그만 복붙
Missing secrets.REVALIDATE_SECRET
```

---

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

#### 4. curl이 400 Bad Request

**증상:**
```
HTTP/1.1 400 Bad Request
{"ok": false, "error": "invalid_fragmentKey"}
```

**원인:**
- fragmentKey 검증 실패 (정규식 불일치)

**처방:**
- fragmentKey가 `/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/` 패턴인지 확인

---

#### 5. REVALIDATE_URL 오류

**증상:**
```
Missing vars.REVALIDATE_URL
```

**원인:**
- GitHub Variable 미설정 또는 오타

**처방:**
- Repository → Settings → Secrets and variables → Actions
- Variables 탭에서 `REVALIDATE_URL` 확인
- 값이 `https://<domain>/api/revalidate` 형식인지 확인

---

## 📋 Repo Settings 체크리스트 (복붙 템플릿)

### GitHub Repository 설정

**위치:** Repository → Settings → Secrets and variables → Actions

#### Secret 설정

```
Name: REVALIDATE_SECRET
Value: [배포 환경과 동일한 값]
```

**체크리스트:**
- [ ] 앞뒤 공백 없음
- [ ] 대소문자 정확
- [ ] 배포 환경 값과 동일

> **주의:** 위의 템플릿은 줄바꿈이 포함되어 있어 복붙 시 실수를 줄일 수 있습니다.

#### Variable 설정

```
Name: REVALIDATE_URL
Value: https://<your-domain>/api/revalidate
```

**체크리스트:**
- [ ] `https://`로 시작
- [ ] `/api/revalidate` 경로 포함
- [ ] 마지막 슬래시 없음 (`/api/revalidate/` ❌)
- [ ] 실제 배포 도메인 사용 (프리뷰/스테이징 아님)

> **주의:** 위의 템플릿은 줄바꿈이 포함되어 있어 복붙 시 실수를 줄일 수 있습니다. 마지막 슬래시(`/`)는 포함하지 마세요.

---

### 배포 환경 설정

**위치:** (배포 플랫폼에 따라 다름)

#### 환경 변수 설정

```
Name: REVALIDATE_SECRET
Value: [GitHub Secret과 동일한 값]
Environment: Production (또는 All Environments)
```

**체크리스트:**
- [ ] GitHub Secret과 값 동일
- [ ] Production 환경에 설정됨
- [ ] 런타임 환경 변수로 설정됨 (빌드 시 env 아님)

---

## 🏁 결론

**설정 완료 후:**
1. 로컬 curl 테스트 (A)
2. Fragment SHA 확인 (B)
3. Actions 수동 실행 (C)

**실패 시:**
- HTTP status + 응답 body 또는 Actions 로그 마지막 30줄 제공
- 위의 진단 가이드 참고

---

**Status:** 📋 **Setup Checklist**  
**Next Action:** 위의 체크리스트에 따라 설정 후 검증

