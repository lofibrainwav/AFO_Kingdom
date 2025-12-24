# 티켓 1: Widget Registry 기초 구조 생성 - 최종 상태

**날짜**: 2025-12-23  
**상태**: ✅ 완료

---

## ✅ 완료된 작업

### 1. 폴더 및 파일 생성
- ✅ `packages/dashboard/src/widgets/` 폴더 생성
- ✅ `packages/dashboard/src/widgets/types.ts` 생성
- ✅ `packages/dashboard/src/widgets/registry.ts` 생성

### 2. Bootstrap 위젯 등록
- ✅ `legacy-kingdom-dashboard` 위젯 등록
- ✅ `docs-hub` 위젯 등록

### 3. 기존 에러 수정
- ✅ `next.config.ts`: Turbopack 설정 수정 (`turbopack: {}` 추가)
- ✅ `route.ts`: Next.js 15+ params Promise 처리
- ✅ `tsconfig.json`: Playwright 제외

---

## 🔧 생성된 파일 구조

```
packages/dashboard/src/widgets/
├── types.ts      # 위젯 메타 타입 정의
└── registry.ts   # 위젯 등록/조회 시스템
```

---

## 📊 Registry 함수

- `registerWidget(meta: WidgetMeta)`: 위젯 등록
- `getWidget(id: string)`: 위젯 조회
- `listWidgets()`: 모든 위젯 목록 (정렬됨)
- `listEnabledWidgets()`: 활성화된 위젯 목록

---

## 🎯 다음 단계 (티켓 2)

HTML 파서 업그레이드:
- HTML의 `data-widget-id` / `id`를 읽어서
- `generated/widgets.json` 생성
- registry에 "자동 등록(Generated)" 추가

---

**상태**: 티켓 1 완료. Widget Registry 기초 구조 생성 완료.

