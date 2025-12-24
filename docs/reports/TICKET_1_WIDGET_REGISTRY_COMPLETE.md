# 티켓 1: Widget Registry 기초 구조 생성 완료

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7

---

## ✅ 완료된 작업

### 1. 폴더 생성
- ✅ `packages/dashboard/src/widgets/` 폴더 생성

### 2. 파일 생성
- ✅ `packages/dashboard/src/widgets/types.ts` 생성
  - WidgetCategory 타입
  - WidgetVisibility 타입
  - WidgetMeta 타입
  - WidgetRegistryEntry 타입

- ✅ `packages/dashboard/src/widgets/registry.ts` 생성
  - registerWidget 함수
  - getWidget 함수
  - listWidgets 함수
  - listEnabledWidgets 함수
  - Bootstrap 위젯 2개 등록 (legacy-kingdom-dashboard, docs-hub)

### 3. 타입 체크 및 빌드 검증
- ✅ 타입 체크 실행
- ✅ 빌드 검증 실행

---

## 🔧 생성된 파일 구조

```
packages/dashboard/src/widgets/
├── types.ts      # 위젯 메타 타입 정의
└── registry.ts   # 위젯 등록/조회 시스템
```

---

## 📊 Bootstrap 위젯

### 1. legacy-kingdom-dashboard
- ID: `legacy-kingdom-dashboard`
- 카테고리: `legacy`
- 가시성: `internal`
- 라우트: `/legacy/kingdom_dashboard.html`

### 2. docs-hub
- ID: `docs-hub`
- 카테고리: `panel`
- 가시성: `public`
- 라우트: `/docs`

---

## 🎯 다음 단계 (티켓 2 준비)

HTML 파서 업그레이드:
- HTML의 `data-widget-id` / `id`를 읽어서
- `generated/widgets.json` 생성
- registry에 "자동 등록(Generated)" 추가

---

**상태**: 티켓 1 완료. Widget Registry 기초 구조 생성 완료.

