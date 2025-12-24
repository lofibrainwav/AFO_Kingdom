# Ticket 5-A Commit 3: Edge Revalidate 설계 (SSOT 봉인)

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 3 (Edge Revalidate 설계)  
**Status:** 🟡 **Design Phase - SSOT Sealed**

---

## 🎯 목표

**"언제/어떻게 invalidate(갱신 트리거)할지"**를 문서로 확정하고, **코드는 최소(또는 0)**로 간다.

**핵심 원칙:**
- Gate 영향 0
- SSOT 경로 0 변경
- 읽기 확장만
- fragment overwrite 금지 유지

---

## ✅ SEALED 5 LINES (Requirements)

1. **Revalidate 대상은 Fragment 우선, Page는 선택적이다.** (SSOT = Fragment)
2. **Trigger는 3단계:** Local Dev → CI → Editor UI(확장).
3. **인증은 `x-revalidate-secret` 헤더 필수**이며, Query Parameter는 금지한다.
4. **부작용 금지:** SSOT Gate/Contract/빌드타임 검증 변경 없음, fragment overwrite 금지 유지.
5. **성공 조건:** revalidate 호출 후 **다음 요청부터** 최신 캐시 보장 (Fragment 경로 기준).

## Scope

- ✅ Read 경로만 확장
- ✅ SSOT 경로 0 변경
- ✅ Gate 영향 없음

## API (Commit 1)

- **Route:** `POST /api/revalidate`
- **Runtime:** Edge
- **Auth Header:** `x-revalidate-secret: <value>` (서버의 `process.env.REVALIDATE_SECRET`와 일치해야 함)
- **Body(JSON):**
  - `{ "fragmentKey": "..." }`
- **Effect:**
  - `revalidatePath("/fragments/{fragmentKey}.html")`

## Revalidate Targets

- **Fragment:** `/fragments/{fragmentKey}.html` (Commit 1)
- **Page(선택):** `/docs/[slug]` (Commit 2 확장)

## Commit Plan

- **Commit 1:** API Route 생성(최소 구현) — Fragment만 revalidate  
  - `packages/dashboard/src/app/api/revalidate/route.ts`
- **Commit 2:** Page Revalidate 확장(선택) — Fragment + Page 동시 revalidate  
  - `packages/dashboard/src/app/api/revalidate/route.ts` (modify)
- **Commit 3:** CI 통합(자동화) — Fragment 생성 후 자동 revalidate  
  - `.github/workflows/revalidate.yml` (new)

## Security Notes

- Query Parameter 금지(Secret 노출 방지)
- 헤더만 사용

---

## 🔒 SSOT 체크리스트

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

1. **Edge Revalidate**
   - On-demand revalidation API
   - 언제 invalidate (트리거)
   - 어디까지 실시간

---

## 📋 설계 5줄 (SSOT 봉인)

### 1. Revalidate 대상은 무엇?

**우선순위:**
1. **Publish fragment** (`/fragments/{fragmentKey}.html`) - **필수**
2. **Docs page** (`/docs/[slug]`) - **선택적** (나중에 확장)

**이유:**
- Fragment가 SSOT의 핵심
- Page는 Fragment를 렌더하므로 Fragment만 revalidate해도 충분
- 나중에 Page도 revalidate 필요하면 확장 가능

**범위 정의:**
- **단일 fragment**: `?fragmentKey=philosophy-widget`
- **전체 docs**: `?path=/docs` (모든 `/docs/[slug]` 페이지)
- **특정 slug**: `?slug=philosophy-widget` (해당 `/docs/[slug]` 페이지)

---

### 2. 트리거는 누가 쏘나?

**3단계 트리거 전략:**

#### Phase 1: 로컬 dev (개발용)
```bash
# 수동 테스트
curl -X POST http://localhost:3000/api/revalidate \
  -H "X-Revalidate-Secret: ${REVALIDATE_SECRET}" \
  -H "Content-Type: application/json" \
  -d '{"fragmentKey": "philosophy-widget"}'
```

#### Phase 2: CI (자동화)
```yaml
# .github/workflows/revalidate.yml
- name: Revalidate after fragment generation
  run: |
    curl -X POST ${{ secrets.REVALIDATE_URL }} \
      -H "X-Revalidate-Secret: ${{ secrets.REVALIDATE_SECRET }}" \
      -H "Content-Type: application/json" \
      -d '{"path": "/docs"}'
```

#### Phase 3: 에디터 UI (확장 가능)
- 나중에 에디터에서 "Publish" 버튼 클릭 시 자동 호출
- 현재는 설계만 (구현은 나중에)

---

### 3. 인증 방식

**SSOT: `REVALIDATE_SECRET` 헤더 필수**

**구현:**
```typescript
// packages/dashboard/src/app/api/revalidate/route.ts
const secret = request.headers.get("X-Revalidate-Secret");
const expectedSecret = process.env.REVALIDATE_SECRET;

if (!secret || secret !== expectedSecret) {
  return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
}
```

**금지:**
- ❌ 쿼리 파라미터 (`?secret=...`) - URL에 노출 위험
- ❌ 쿠키 - CSRF 위험
- ✅ 헤더만 사용 (보안)

**환경변수:**
- `.env.local`: `REVALIDATE_SECRET=dev-secret-key`
- `.env.production`: `REVALIDATE_SECRET=prod-secret-key` (배포 시 설정)

---

### 4. 부작용 금지

**절대 금지:**
- ❌ SSOT Gate/Contract 건드리지 않는다
- ❌ fragment overwrite 금지 유지
- ❌ 빌드 타임 검증 변경 금지
- ❌ slug 검증 규칙 변경 금지

**허용:**
- ✅ 읽기 경로만 확장 (캐시 invalidation)
- ✅ On-demand revalidation API
- ✅ Fragment/Page 캐시 갱신

---

### 5. 성공 조건

**"이 API 한 번 호출하면, 다음 요청부터 최신"을 보장할 범위 정의**

**성공 조건:**
1. **Fragment revalidate**
   - API 호출 후 `/fragments/{fragmentKey}.html` 요청 시 최신 내용 반환
   - 검증: `curl /fragments/{fragmentKey}.html` → 최신 내용 확인

2. **Page revalidate (선택적)**
   - API 호출 후 `/docs/[slug]` 요청 시 최신 fragment 렌더
   - 검증: `curl /docs/{slug}` → 최신 fragment 확인

**실패 조건:**
- API 호출 후에도 이전 캐시 반환 → 실패
- 인증 실패 → 401 반환
- 잘못된 fragmentKey → 404 반환

---

## 📋 나중에 구현할 때의 파일 경로/커밋 쪼개기

### Commit 1: API Route 생성 (최소 구현)

**파일 경로:**
- `packages/dashboard/src/app/api/revalidate/route.ts`

**구현 내용:**
- `REVALIDATE_SECRET` 헤더 검증
- `fragmentKey` 파라미터 받기
- `revalidatePath()` 호출 (Fragment만)
- 성공/실패 응답

**Gate 영향:** 없음 (읽기 경로만 확장)

---

### Commit 2: Page Revalidate 확장 (선택적)

**파일 경로:**
- `packages/dashboard/src/app/api/revalidate/route.ts` (수정)

**구현 내용:**
- `path` 파라미터 추가 (`/docs` 또는 `/docs/[slug]`)
- `revalidatePath()` 호출 (Page도)
- Fragment + Page 동시 revalidate

**Gate 영향:** 없음 (읽기 경로만 확장)

---

### Commit 3: CI 통합 (자동화)

**파일 경로:**
- `.github/workflows/revalidate.yml` (신규)

**구현 내용:**
- Fragment 생성 후 자동 revalidate
- `REVALIDATE_SECRET` 시크릿 사용
- 성공/실패 알림

**Gate 영향:** 없음 (CI 워크플로우만 추가)

---

## ✅ 검증 체크리스트 (재현 가능)

### 1. Gate 영향 없음 보증

```bash
# Contract Gate 검증 (변경 없음)
python3 scripts/validate_widgets_json.py
# 예상: ✅ 통과

# TypeScript 타입 체크
pnpm -C packages/dashboard type-check
# 예상: ✅ 통과

# Next.js 빌드 (정적 생성 유지)
pnpm -C packages/dashboard build
# 예상: ✅ 통과
```

### 2. Revalidate API 테스트

```bash
# 1. Fragment revalidate 테스트
curl -X POST http://localhost:3000/api/revalidate \
  -H "X-Revalidate-Secret: ${REVALIDATE_SECRET}" \
  -H "Content-Type: application/json" \
  -d '{"fragmentKey": "philosophy-widget"}'

# 2. 성공 조건 확인
curl http://localhost:3000/fragments/philosophy-widget.html
# 예상: 최신 fragment 내용 반환

# 3. 인증 실패 테스트
curl -X POST http://localhost:3000/api/revalidate \
  -H "Content-Type: application/json" \
  -d '{"fragmentKey": "philosophy-widget"}'
# 예상: 401 Unauthorized
```

---

## 🔒 안전 범위 명확화

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

1. **Edge Revalidate**
   - On-demand revalidation API
   - Fragment revalidate (필수)
   - Page revalidate (선택적)
   - CI 통합 (자동화)

---

## 🏁 결론

Commit 3 (Edge Revalidate 설계)는 **"언제/어떻게 invalidate할지"**를 문서로 확정하는 단계입니다.

**설계 봉인 (위 "SEALED 5 LINES" 참조):**
- Revalidate 대상: Fragment 우선, Page 선택적
- 트리거: 로컬 dev → CI → 에디터 UI (3단계)
- 인증: `x-revalidate-secret` 헤더 필수
- 부작용 금지: SSOT Gate/Contract 건드리지 않음
- 성공 조건: 다음 요청부터 최신 캐시 보장

**안전 범위:**
- Gate 영향 없음
- SSOT 경로 0 변경
- 읽기 경로만 확장
- fragment overwrite 금지 유지

**구현 계획:**
- Commit 1: API Route 생성 (최소 구현)
- Commit 2: Page Revalidate 확장 (선택적)
- Commit 3: CI 통합 (자동화)

---

**Status:** 🟡 **Design Phase - SSOT Sealed**  
**Next Action:** 구현 필요 시 Commit 1부터 시작 (커밋 메시지 및 테스트 curl은 아래 문서 참조)

