# Ticket 4: 정적 생성 강화 + Override 규칙 고정 완료

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7

---

## ✅ 완료된 작업 (A→B 순서)

### A. 정적 생성 강화 (먼저)

#### Commit 1: generateStaticParams() 구현
- ✅ `generateStaticParams()`로 모든 slug를 빌드 타임에 고정
- ✅ slug 검증은 Contract Gate와 동일 규칙 재사용
- ✅ fragment 파일 없으면 `notFound()`로 404
- ✅ metadata/title 자동 생성 추가

### B. Override 규칙 고정 (그 다음)

#### Commit 2: Override 렌더링 레이어 추가
- ✅ SSOT 규칙 구현:
  1. `widgetRegistry[slug]`에 React 컴포넌트가 있으면 **무조건 override**
  2. 없으면 `public/fragments/{fragment_key}.html` 렌더
  3. 둘 다 없으면 404
- ✅ registry에서 React 컴포넌트 체크 로직 추가 (기본 구조)
- ✅ 타입체크 통과

### Commit 3: 안전장치 강화

#### Gate 강화
- ✅ `fragment_key`는 **반드시 존재** (warning → error로 변경)
- ✅ slug 규칙은 기존 그대로 유지
- ✅ 중복 slug는 기존 그대로 유지

---

## 📊 구현 세부사항

### generateStaticParams()
```typescript
export async function generateStaticParams() {
  const payload = generated as unknown as Payload;
  const widgets = payload.widgets || [];
  
  const validSlugs = widgets
    .map((w) => w.id)
    .filter((slug) => isValidSlug(slug));
  
  return validSlugs.map((slug) => ({ slug }));
}
```

### Override 우선순위 규칙 (SSOT)
1. **registry에 React 컴포넌트가 있으면 무조건 override**
2. **없으면 fragment 렌더**
3. **둘 다 없으면 404**

### slug 검증 (Contract Gate와 동일)
- 허용 문자: `a-z`, `0-9`, `-`, `가-힣`
- 연속 하이픈(`--`), 양끝 하이픈(`-foo` / `foo-`) 불가

### fragment_key 검증 (강화)
- **이제는 error로 처리** (표준화 완료되었으므로)
- `fragment_key`가 없으면 validation 실패

---

## 🔧 수정된 파일

1. `packages/dashboard/src/app/docs/[slug]/page.tsx`
   - `generateStaticParams()` 추가
   - `generateMetadata()` 추가
   - Override 규칙 구현

2. `scripts/validate_widgets_json.py`
   - `fragment_key` 검증을 error로 변경
   - Ticket 4 Gate 추가

---

## 📋 다음 단계

### React Override 구현 (선택)
- registry에 React 컴포넌트 저장 기능 추가
- `widgetEntry.component` 활성화

### 성능 최적화 (선택)
- Fragment 파일 캐싱
- 빌드 타임에 fragment를 React 컴포넌트로 변환

---

**상태**: Ticket 4 완료. 정적 생성 강화 + Override 규칙 고정 완료.

