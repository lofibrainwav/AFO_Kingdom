# Ticket 5-A Commit 2: Live Edit SSOT 봉인 완료

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 2 (Live Edit 최소 구현)  
**Status:** 🟢 **SSOT Sealed - Implementation Complete**

---

## ✅ SSOT 일관성 보장 (형님 지적사항 반영)

### 1. `slug === fragment_key` 가정 제거

**문제점:**
- ❌ `const draftUrl = `/fragments/draft/${slug}.html`;` (slug 직접 사용)
- ❌ SSOT는 "slug ↔ fragment_key 1:1"이지 "항상 동일 문자열"이라고 런타임에서 가정하면 깨질 여지

**해결:**
- ✅ `fragmentKeyFromSlug(slug)` 변환 함수 사용
- ✅ `const draftUrl = `/fragments/draft/${fragmentKey}.html`;` (fragmentKey 사용)

### 2. Live 라우트 slug 검증 SSOT 분리 제거

**문제점:**
- ❌ `useParams()`로 받고 바로 fetch하면, slug 규칙 위반이 런타임에서 애매하게 처리될 수 있음
- ❌ SSOT는 "검증 → notFound()"로 딱 끊었는데 Live 라우트가 Client Page라서 분리됨

**해결:**
- ✅ `/docs/[slug]/live/page.tsx`는 **서버 컴포넌트**로 두고
- ✅ 클라이언트 컴포넌트(Poller)에 `slug`/`fragmentKey`만 넘겨
- ✅ 서버 컴포넌트에서 slug 검증 후 Poller에 전달

---

## 📋 최종 구현 구조

### 1. 서버 컴포넌트: `packages/dashboard/src/app/docs/[slug]/live/page.tsx`

**역할:**
- SSOT slug 검증 (기존 page.tsx와 동일 규칙)
- `fragmentKeyFromSlug(slug)` 변환 함수 사용
- 클라이언트 컴포넌트(Poller)에 `fragmentKey` 전달
- SSOT 경로와 완전 분리 유지

**핵심 코드:**
```typescript
// SSOT slug 검증 (기존 page.tsx와 동일)
if (!isValidSlug(slug)) {
  notFound();
}

// fragmentKey 변환 (SSOT 일관성)
const fragmentKey = fragmentKeyFromSlug(slug);

// Poller에 전달
<LiveEditPoller fragmentKey={fragmentKey} />
```

### 2. 클라이언트 컴포넌트: `packages/dashboard/src/components/live/LiveEditPoller.tsx`

**역할:**
- `fragmentKey`를 받아서 polling
- `/fragments/draft/{fragmentKey}.html` fetch
- Draft 우선, 없으면 Publish fallback
- 실시간 업데이트 (2초 간격)

**핵심 코드:**
```typescript
// fragmentKey 사용 (slug 직접 사용 금지)
const draftUrl = `/fragments/draft/${fragmentKey}.html`;
const publishUrl = `/fragments/${fragmentKey}.html`;
```

---

## ✅ 검증 결과

### TypeScript 타입 체크
```bash
pnpm -C packages/dashboard type-check
```
**결과**: ✅ 통과 (에러 없음)

---

## 🔒 SSOT 일관성 보장 체크리스트

### ✅ 유지된 것 (절대 건드리지 않음)

1. **SSOT 규칙**
   * slug 검증 (Contract Gate와 동일) ✅
   * fragment_key 필수 (빌드 타임 검증) ✅
   * 렌더링 우선순위 (React → Fragment → 404) ✅

2. **Gate 검증**
   * 빌드 타임 검증 유지 ✅
   * Contract Gate 유지 ✅
   * fragment_key 검증 유지 ✅

3. **기존 Fragment**
   * `public/fragments/{fragment_key}.html` 유지 ✅
   * fragment overwrite 없음 ✅

### ✅ 확장된 것 (읽기 경로만)

1. **Live Edit**
   * 전용 라우트 `/docs/[slug]/live` 분리 ✅
   * 서버 컴포넌트에서 slug 검증 (SSOT 일관성) ✅
   * `fragmentKeyFromSlug(slug)` 변환 함수 사용 ✅
   * 클라이언트 컴포넌트(Poller)에서 polling (fetch) ✅
   * fragment overwrite 없이 테스트 ✅

---

## 🏁 결론

Commit 2 (Live Edit)는 **SSOT 일관성을 완벽히 보장**하는 안전한 구현입니다.

**SSOT 일관성:**
* slug 검증 (기존 page.tsx와 동일 규칙) ✅
* `fragmentKeyFromSlug(slug)` 변환 함수 사용 ✅
* 서버 컴포넌트에서 검증 후 Poller에 전달 ✅

**안전 범위:**
* SSOT 규칙 유지 ✅
* Gate 영향 없음 ✅
* 기존 fragment 유지 ✅
* SSOT 경로와 완전 분리 ✅

---

**Status:** 🟢 **SSOT Sealed - Implementation Complete**  
**Next Action:** Commit 3 (Edge Revalidate 설계) 또는 검증 후 진행

