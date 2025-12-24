# REVALIDATE_URL 설정 가이드 (FACTS/PASTE)

**As-of**: 2025-12-24  
**Status**: 설정 가이드 (SSOT 준수)  
**SSOT 원칙 준수**: 팩트 기반, 복붙 가능한 최종본

---

## ⚠️ 중요: 배포 전/후 구분

**현재 상황**:

- 도메인: `brnestrm.com`
- Vercel이 있지만 **프론트엔드가 아직 배포되지 않음**
- fragments는 아직 서빙되는 환경이 없음

**REVALIDATE_URL 설정 시점**:

- ✅ **지금 (로컬 개발)**: `http://localhost:3000/api/revalidate` (테스트용)
- ✅ **나중 (Vercel 배포 후)**: `https://brnestrm.com/api/revalidate` 또는 Vercel 도메인

**가이드 사용법**:

- 로컬 개발 중이라면 → "로컬 개발 환경" 섹션 참고
- Vercel 배포 후라면 → "프로덕션 환경" 섹션 참고

---

## FACTS (검증됨)

- **Next.js App Router에서 `revalidatePath()`는 Route Handlers (`app/api` 디렉토리)에서 호출 가능하며, Edge Runtime과 Node.js Runtime 모두 지원한다.** ([Next.js 공식 문서][1])
- **GitHub Actions Secrets는 `secrets.REVALIDATE_SECRET` 형식으로 접근하며, Variables는 `vars.REVALIDATE_URL` 형식으로 접근한다.** ([GitHub Actions 공식 문서][2])
- **`curl`의 `-H` 옵션은 HTTP 헤더를 설정하며, `-d` 옵션은 POST 요청의 body를 설정한다.** ([curl 공식 문서][3])
- **fragments는 `packages/dashboard/public/fragments/` 경로에 저장되며, Next.js에서 정적 파일로 서빙된다.** (코드베이스 확인: `packages/dashboard/src/app/docs/[slug]/page.tsx`)
- **revalidate API는 `packages/dashboard/src/app/api/revalidate/route.ts`에 구현되어 있으며, Edge Runtime을 사용한다.** (코드베이스 확인)

---

## REVALIDATE_URL 선택 규칙 (이거 하나면 끝)

**REVALIDATE_URL = "fragments를 서빙하는 같은 도메인" + `/api/revalidate`**

- 만약 fragment가 여기서 열린다:
  - `https://[형님의 실제 도메인]/fragments/home-hero.html`
  - 예: `https://afo.example.com/fragments/home-hero.html`
- 그럼 revalidate는 무조건 여기여야 함:
  - `https://[형님의 실제 도메인]/api/revalidate`
  - 예: `https://afo.example.com/api/revalidate`

✅ 즉, **prod/staging 구분은 "지금 실제로 fragments가 뜨는 도메인이 어디냐"**로 자동 결정됨.

---

## GitHub Actions 설정 (Secrets/Vars) — 체크리스트

GitHub Repo → **Settings → Secrets and variables → Actions**

### 1) Secret: `REVALIDATE_SECRET`

- 값: **배포 환경(dashboard runtime)에 설정된 REVALIDATE_SECRET와 완전히 동일**
- 체크:
  - [ ] 앞뒤 공백 없음
  - [ ] 대소문자 정확
  - [ ] prod/staging 중 "선택한 도메인 X"의 환경변수 값과 동일

### 2) Variable: `REVALIDATE_URL`

- 값: `https://[형님의 실제 도메인]/api/revalidate`
  - 예: `https://afo.example.com/api/revalidate`
- 체크:
  - [ ] `https://`로 시작
  - [ ] 경로가 **반드시** `/api/revalidate`
  - [ ] 마지막 `/` 없음 (지금 워크플로가 제거도 하지만, 저장도 깔끔하게)
  - [ ] 도메인은 **fragments가 실제로 뜨는 도메인**

---

## 배포 환경 변수 설정 (필수)

배포된 **dashboard(Next) 런타임 환경**에:

- `REVALIDATE_SECRET=<위 Secret과 동일한 값>`

> "빌드 시 env에만 있음 / 런타임엔 없음" 이 케이스가 제일 많이 터짐.

---

## 1분 컷 검증 루틴 (복붙용, 로컬에서)

아래에서 `[형님의 실제 도메인]`만 바꿔서 그대로 실행.

**예시**: 형님의 도메인이 `afo.example.com`이라면 `DOMAIN="https://afo.example.com"`로 설정

### A) fragments 도메인이 맞는지 확인

```bash
export DOMAIN="https://[형님의 실제 도메인]"
# 예: export DOMAIN="https://afo.example.com"

curl -I "$DOMAIN/fragments/home-hero.html"
```

- 기대: `200` (또는 CDN이면 `200/304` 등 "성공" 계열)
- 실패면: **X가 잘못됐거나**, fragments 경로가 그 환경에 없음

### B) REVALIDATE_URL POST 동작 확인

```bash
export REVALIDATE_URL="https://[형님의 실제 도메인]/api/revalidate"
# 예: export REVALIDATE_URL="https://afo.example.com/api/revalidate"
export REVALIDATE_SECRET="(배포 환경과 동일한 값)"

curl -i -X POST "$REVALIDATE_URL" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

**해석**

- `200` + `{ ok: true ... }` → ✅ 성공
- `401` → Secret 불일치/누락
- `403/timeout` → WAF/Cloudflare/네트워크 차단 가능성
- `400` → fragmentKey 검증 실패(키 포맷/길이)
- `308/301` → URL에 `/` 붙었거나 리다이렉트 발생(지금은 trailing slash 제거 패치가 있지만, 저장값도 깔끔히)

---

## GitHub Actions에서 수동 실행 (workflow_dispatch)

Actions → **Revalidate fragments (dynamic)** → **Run workflow**

- Guard에서 바로 죽으면: Secret/Var 미설정
- curl step에서 죽으면: URL 접근 불가 / Secret 불일치 / 배포환경 미설정

---

## "prod vs staging"을 스스로 확정하는 초간단 판별

- **형님이 브라우저에서 늘 보는 정식 도메인**(예: `https://afo.example.com`, `https://dashboard.example.com`)에서 fragments가 뜨면 → 그게 prod
- 프리뷰/스테이징 도메인(예: `https://afo-staging.example.com` 또는 `https://<hash>.vercel.app`)에서만 뜨면 → 그게 staging/preview

**형님이 실제로 사용하는 도메인을 알려주시면, prod/staging 구분과 REVALIDATE_URL을 바로 설정해드리겠습니다.**

---

## 로컬 개발 환경 (지금)

**현재 상황**: 프론트엔드가 아직 배포되지 않았으므로, 로컬 개발 환경에서 테스트합니다.

### 로컬 REVALIDATE_URL 설정

```bash
# 로컬 개발 서버 실행
cd packages/dashboard
pnpm dev
# → http://localhost:3000 에서 서빙됨
```

**로컬 테스트용 REVALIDATE_URL**:

- `http://localhost:3000/api/revalidate`

**로컬 테스트 (복붙용)**:

```bash
# 1. 로컬 fragments 접근 확인
curl -I "http://localhost:3000/fragments/home-hero.html" | head -1

# 2. 로컬 REVALIDATE_URL POST 테스트
export REVALIDATE_SECRET="(로컬 .env.local에 설정한 값)"
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

**기대 결과**:

- 1번: `HTTP/1.1 200 OK` (로컬 서버가 실행 중이어야 함)
- 2번: `200` + `{ ok: true ... }` (로컬 .env.local에 REVALIDATE_SECRET 설정 필요)

---

## 프로덕션 환경 (Vercel 배포 후)

**Vercel 배포 후**: `brnestrm.com` 또는 Vercel 도메인에서 fragments가 서빙됩니다.

### 프로덕션 REVALIDATE_URL 설정

**도메인**: `brnestrm.com` (또는 Vercel이 제공하는 도메인)

**프로덕션 REVALIDATE_URL**:

- `https://brnestrm.com/api/revalidate` (커스텀 도메인 사용 시)
- 또는 `https://[프로젝트명].vercel.app/api/revalidate` (Vercel 기본 도메인 사용 시)

### 프로덕션 팩트체크 (3줄)

**형님의 도메인이 `brnestrm.com`이라면**:

```bash
# 1. fragments 접근 가능 여부 확인
curl -I "https://brnestrm.com/fragments/home-hero.html" | head -1

# 2. REVALIDATE_URL 형식 검증
echo "REVALIDATE_URL=https://brnestrm.com/api/revalidate" | grep -E '^REVALIDATE_URL=https://[^/]+/api/revalidate$'

# 3. 경로 일관성 확인 (fragments와 revalidate가 같은 도메인인지)
echo "✅ fragments: https://brnestrm.com/fragments/*.html" && echo "✅ revalidate: https://brnestrm.com/api/revalidate"
```

**기대 결과**:

- 1번: `HTTP/2 200` 또는 `HTTP/1.1 200 OK` (배포 후)
- 2번: `REVALIDATE_URL=https://brnestrm.com/api/revalidate` (매칭됨)
- 3번: 두 경로 모두 같은 도메인 사용

**⚠️ 주의**: Vercel 배포가 완료된 후에만 위 테스트가 성공합니다.

---

## 로컬 배선 완료 상태 확인 (FACTS)

**형님이 준 상태로 확정 가능한 것**:

- `localhost:3000`에서 fragments가 **200 OK**
- `POST /api/revalidate`가 **200 OK** + `{"ok":true,"revalidated":[...]}`
- 즉, **revalidate 라우트/키 검증/응답 포맷/fragmentKey→경로 매핑**까지 로컬에서 정상

✅ **로컬 배선은 이미 "끝난 상태(=기능이 돈다)"**

---

## 다음 단계: 배포된 도메인 X에서 똑같이 200 OK 만들기

**목표**: Vercel + brnestrm.com에서 로컬과 동일하게 동작하도록 설정

**REVALIDATE_URL = `https://X/api/revalidate`** (X는 fragments를 실제로 서빙하는 도메인)

### A안 (prod): `X = brnestrm.com`

**조건**:
- Vercel Project에 커스텀 도메인 연결 완료 후
- Vercel Env(Production)에 `REVALIDATE_SECRET` 세팅

**GitHub Actions 설정**:
- Secret: `REVALIDATE_SECRET` (Vercel과 **완전 동일**)
- Variable: `REVALIDATE_URL=https://brnestrm.com/api/revalidate` (마지막 `/` 없이)

### B안 (staging/preview 먼저): `X = <project>.vercel.app`

**조건**:
- 먼저 vercel.app 도메인으로 검증 성공 → 그 다음 brnestrm.com으로 옮기면 마찰이 제일 적음

**GitHub Actions 설정**:
- Secret: `REVALIDATE_SECRET` (Vercel과 **완전 동일**)
- Variable: `REVALIDATE_URL=https://<project>.vercel.app/api/revalidate` (마지막 `/` 없이)

**형님 성향(마찰 최소) 기준이면 B안(vercel.app) 1번 성공 → A안(prod)** 이 제일 깔끔함.

---

## 배포 후 "30초 컷" 검증 (로컬 터미널, 복붙용)

`X`만 바꿔서 그대로 실행:

```bash
export X="brnestrm.com"   # 또는 <project>.vercel.app
export DOMAIN="https://${X}"
export REVALIDATE_URL="${DOMAIN}/api/revalidate"
export REVALIDATE_SECRET="(Vercel Production과 동일한 값)"

echo "=== 1) fragments 200 OK? ==="
curl -I "${DOMAIN}/fragments/philosophy-widget.html" | head -n 5

echo ""
echo "=== 2) revalidate 200 OK? ==="
curl -i -X POST "${REVALIDATE_URL}" \
  -H "x-revalidate-secret: ${REVALIDATE_SECRET}" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"philosophy-widget"}'
```

### 결과가 이렇게 나오면 끝

- (1)에서 `HTTP/... 200`
- (2)에서 `HTTP/... 200` + `{"ok":true,...}`

---

## 실패 패턴 4개만 보면 됨

### 1. `401` → Secret 불일치

**원인**: 공백/대소문자 포함. Vercel 값 = GitHub Secret = 로컬 export 값 **셋이 동일**해야 함.

**해결**:
- Vercel Production Environment Variables 확인
- GitHub Secrets 확인 (앞뒤 공백 없음, 대소문자 정확)
- 로컬 export 값 확인

### 2. `308/301` → URL 끝 `/` 문제나 리다이렉트

**원인**: URL 끝에 `/` 붙었거나 리다이렉트 발생

**해결**:
- REVALIDATE_URL에서 마지막 `/` 제거 (지금 워크플로우에서 `%/` 제거 넣어둔 건 정답)
- 로컬 테스트도 마지막 `/` 없이

### 3. `403/timeout` → Cloudflare/WAF가 POST 막음

**원인**: Cloudflare/WAF가 POST 요청을 차단

**해결**:
- `/api/revalidate`만 예외 룰 필요할 수 있음
- Cloudflare Dashboard에서 Firewall Rules 확인

### 4. `404` → 배포 결과에 `/api/revalidate` 라우트가 안 올라감

**원인**: 빌드/라우팅 확인 필요

**해결**:
- Vercel Build Log 확인
- `packages/dashboard/src/app/api/revalidate/route.ts` 파일 존재 확인
- Next.js 빌드 성공 여부 확인

---

**참고 자료**:

- [Next.js: revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)
- [GitHub Actions: Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [curl: Manual](https://curl.se/docs/manual.html)

[1]: https://nextjs.org/docs/app/api-reference/functions/revalidatePath "Functions: revalidatePath | Next.js"
[2]: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions "Using secrets in GitHub Actions"
[3]: https://curl.se/docs/manual.html "curl Manual"
