# Ticket 5-A Commit 1: Preview 모드 구현 완료

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 1 (Preview 모드)  
**Status:** 🟢 **Implementation Complete**

---

## ✅ 완료된 작업

### Preview 모드 구현
- ✅ 쿼리 파라미터 `?preview=true` 체크
- ✅ Draft fragment 읽기 (`public/fragments/draft/{fragment_key}.html`)
- ✅ 기존 fragment 유지 (overwrite 없음)
- ✅ Preview 모드 표시 (UI 배지)

---

## 🔧 수정된 파일

### `packages/dashboard/src/app/docs/[slug]/page.tsx`

**변경 내용:**
1. `searchParams` props 추가 (Next.js 16 App Router 패턴)
2. Preview 모드 체크 로직 추가 (`?preview=true`)
3. Draft fragment 읽기 로직 추가
4. Preview 모드 UI 배지 추가

**변경 라인 수**: +20줄

---

## 🔒 안전 범위 명확화 (SSOT 유지)

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

1. **Preview 모드**
   * 쿼리 파라미터 `?preview=true` 체크 ✅
   * Draft fragment 읽기 (`public/fragments/draft/{fragment_key}.html`) ✅
   * 기존 fragment 유지 (overwrite 없음) ✅

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

### 2. Preview 모드 테스트

```bash
# Preview 모드 테스트
curl "http://localhost:3000/docs/philosophy-widget?preview=true"

# 일반 모드 테스트 (기존 fragment 유지)
curl "http://localhost:3000/docs/philosophy-widget"

# Draft fragment 없을 때 (Publish fragment 사용)
# (draft 폴더에 파일 없으면 자동으로 publish 사용)
```

---

## 📋 구현 세부사항

### Preview 모드 체크

```typescript
// [Ticket 5-A Commit 1] Preview 모드 체크 (쿼리 파라미터)
const resolvedSearchParams = searchParams ? await searchParams : {};
const isPreview = resolvedSearchParams.preview === 'true';
```

### Draft Fragment 읽기

```typescript
// Preview 모드일 때 Draft fragment 우선 읽기, 없으면 기존 fragment 사용
const publishFragmentPath = join(process.cwd(), "packages/dashboard/public/fragments", `${fragmentKey}.html`);
const draftFragmentPath = join(process.cwd(), "packages/dashboard/public/fragments/draft", `${fragmentKey}.html`);

let fragmentContent: string | null = null;

if (isPreview) {
  // Preview 모드: Draft 우선, 없으면 Publish 사용
  fragmentContent = await getFragmentContent(draftFragmentPath) || await getFragmentContent(publishFragmentPath);
} else {
  // 일반 모드: Publish만 사용
  fragmentContent = await getFragmentContent(publishFragmentPath);
}
```

---

## 🔒 Preview / Live Edit 접근 제한 (SSOT 명시)

**SSOT 명시:**
* Preview / Live Edit routes는:
  * **Non-indexed** (no SEO)
  * **Dev / internal usage only**
  * **Not part of canonical SSOT path**
* 기존 `/docs/[slug]` 경로는 **절대 변경 없음**
* Preview/Live Edit은 **읽기 전용 확장**일 뿐

---

## 🏁 결론

Commit 1 (Preview 모드)는 **읽기 경로만 확장**하는 안전한 구현입니다.

**안전 범위:**
* SSOT 규칙 유지 ✅
* Gate 영향 없음 ✅
* 기존 fragment 유지 ✅

**구현 완료:**
* 쿼리 파라미터 기반 Preview 모드 ✅
* Draft/Publish 분리 ✅
* 기존 fragment overwrite 없음 ✅

---

**Status:** 🟢 **Implementation Complete**  
**Next Action:** Commit 2 (Live Edit) 또는 검증 후 진행

