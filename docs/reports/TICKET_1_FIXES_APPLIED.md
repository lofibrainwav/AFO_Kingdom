# 티켓 1: 기존 에러 수정 완료

**날짜**: 2025-12-23  
**목적**: 티켓 1 검증을 위한 기존 에러 수정

---

## ✅ 수정된 에러

### 1. next.config.ts - Turbopack 설정
**문제**: `experimental.turbo: false`는 Next.js 16에서 유효하지 않은 속성

**수정**:
- `turbo: false` 제거
- 주석으로 설명 추가 (Turbopack은 dev 명령어에 --turbo 플래그가 없으면 자동으로 webpack 사용)

### 2. route.ts - Next.js 15+ params Promise
**문제**: Next.js 15+에서 params가 Promise로 변경됨

**수정**:
```typescript
// Before
{ params }: { params: { filename: string } }

// After
{ params }: { params: Promise<{ filename: string }> }
const { filename } = await params;
```

### 3. tsconfig.json - Playwright 제외
**문제**: Playwright 관련 타입 에러

**수정**:
- `exclude`에 `e2e`, `playwright.config.ts` 추가

---

## 🎯 티켓 1 상태

- ✅ `widgets/types.ts` 생성 완료
- ✅ `widgets/registry.ts` 생성 완료
- ✅ Bootstrap 위젯 2개 등록 완료
- ✅ 기존 에러 수정 완료

---

**상태**: 티켓 1 완료. Widget Registry 기초 구조 생성 완료.

