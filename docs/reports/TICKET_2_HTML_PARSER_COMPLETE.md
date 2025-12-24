# 티켓 2: HTML 파서 → generated JSON → Registry 자동등록 완료

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7 + MCP 도구/스킬/학자 활용

---

## ✅ 완료된 작업

### Phase 2-0: normalize 실행
- ✅ `scripts/normalize_legacy_widgets.mjs` 실행
- ✅ HTML 섹션에 data-widget-id 자동 주입

### Phase 2-1: 파서 스크립트 생성
- ✅ `packages/dashboard/scripts/generate_widgets_from_html.mjs` 생성
- ✅ HTML에서 data-widget-id와 id를 읽어서 JSON 생성
- ✅ 정규식 기반 파싱 (cheerio 없이 순수 Node.js)

### Phase 2-2: Registry 자동 등록
- ✅ `packages/dashboard/src/widgets/registry.ts`에 generated widgets 자동 등록 추가
- ✅ 중복/불량 무시로 부팅 안전성 보장
- ✅ try-catch로 generated 파일 없을 때도 안전

### Phase 2-3: /docs 페이지 Registry 기반 렌더
- ✅ `packages/dashboard/src/app/docs/page.tsx` 수정
- ✅ `listWidgets()`로 generated 위젯 목록 표시
- ✅ Legacy HTML 링크 포함

### Phase 2-4: /docs/[slug] 페이지 생성
- ✅ `packages/dashboard/src/app/docs/[slug]/page.tsx` 생성
- ✅ Legacy HTML로 점프하는 안전한 방식
- ✅ 티켓 3에서 HTML 추출 예정

### Phase 2-5: package.json 자동 생성 연결
- ✅ `gen:widgets` 스크립트 추가
- ✅ `predev`, `prebuild` 훅 설정

### Phase 2-6: 실행/검증
- ✅ normalize 실행 완료
- ✅ gen:widgets 실행 완료
- ✅ 빌드 검증 완료

---

## 📊 생성된 파일

1. `packages/dashboard/scripts/generate_widgets_from_html.mjs` - HTML 파서
2. `packages/dashboard/src/generated/widgets.generated.json` - Generated 위젯 목록
3. `packages/dashboard/src/app/docs/[slug]/page.tsx` - 동적 라우트 페이지

---

## 🔧 수정된 파일

1. `packages/dashboard/src/widgets/registry.ts` - Generated widgets 자동 등록
2. `packages/dashboard/src/app/docs/page.tsx` - Registry 기반 렌더
3. `packages/dashboard/package.json` - gen:widgets 스크립트 추가

---

## 🎯 다음 단계 (티켓 3)

티켓 3: HTML 추출 및 React 렌더
- 각 위젯의 HTML 조각(innerHTML) 저장
- 빌드 타임에 섹션별 HTML fragment 파일 생성
- `/docs/[slug]`에서 fragment 렌더
- React 위젯이 있으면 override(교체)

---

**상태**: 티켓 2 완료. HTML 파서 → generated JSON → Registry 자동등록 완료.

