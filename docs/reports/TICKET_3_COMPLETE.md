# Ticket 3: HTML Fragment 추출 및 렌더 완료

**날짜**: 2025-12-23  
**방법**: 3개 커밋으로 안전하게 진행

---

## ✅ 완료된 작업 (3 커밋)

### Commit 1: Node generator가 fragment_key만 생성
- ✅ `generate_widgets_from_html.mjs`에서 각 위젯에 `fragment_key` 추가
- ✅ `fragment_key = id` (slug와 1:1 매칭)
- ✅ 검증 통과 (fragment_key 표준화)

### Commit 2: HTML fragment 파일 생성 (빌드 타임)
- ✅ `generate_fragments.mjs` 스크립트 생성
- ✅ HTML에서 위젯별 innerHTML 추출
- ✅ 저장 경로: `packages/dashboard/public/fragments/{fragment_key}.html`
- ✅ 섹션 찾는 기준:
  1. `data-widget-id="{id}"` (1순위, 가장 안전)
  2. `id="{html_section_id}"` (2순위, fallback)

### Commit 3: /docs/[slug] 라우트에서 fragment 렌더 + 404 + override
- ✅ slug 검증 (허용 문자: a-z, 0-9, -, 가-힣)
- ✅ fragment 파일 읽기 (fallback: fragment_key ?? html_section_id ?? sourceId)
- ✅ 파일 없으면 404
- ✅ `dangerouslySetInnerHTML`로 렌더
- ✅ React override 준비 (주석 처리)

---

## 📊 생성된 파일

1. `packages/dashboard/scripts/generate_fragments.mjs` - Fragment 생성 스크립트
2. `packages/dashboard/public/fragments/{fragment_key}.html` - Fragment 파일들 (35개)
3. `packages/dashboard/src/app/docs/[slug]/page.tsx` - Fragment 렌더 라우트

---

## 🔧 수정된 파일

1. `packages/dashboard/scripts/generate_widgets_from_html.mjs` - fragment_key 추가
2. `packages/dashboard/package.json` - gen:fragments 스크립트 추가
3. `packages/dashboard/src/app/docs/[slug]/page.tsx` - Fragment 렌더 로직

---

## 🎯 구현 세부사항

### Fragment 저장 경로
- **경로**: `packages/dashboard/public/fragments/{fragment_key}.html`
- **이유**: Next.js에서 정적 파일로 읽기 쉬움, 안정적

### 섹션 찾는 기준
1. **1순위**: `data-widget-id="{id}"` (가장 안전)
2. **2순위**: `id="{html_section_id}"` (fallback)

### Slug 검증
- 허용 문자: `a-z`, `0-9`, `-`, `가-힣`
- 연속 하이픈(`--`), 양끝 하이픈(`-foo` / `foo-`) 불가

### Fragment 포인터 (fallback)
- 읽을 때: `fragment_key ?? html_section_id ?? sourceId`
- 생성(Node): 무조건 `fragment_key`만 사용

---

## 📋 다음 단계

### React Override 구현 (선택)
- React 컴포넌트가 있으면 fragment 대신 컴포넌트 렌더
- 예: `getReactOverride(w.id)` 함수 구현

### 성능 최적화 (선택)
- Fragment 파일 캐싱
- 빌드 타임에 fragment를 React 컴포넌트로 변환

---

**상태**: Ticket 3 완료. HTML Fragment 추출 및 렌더 완료.

