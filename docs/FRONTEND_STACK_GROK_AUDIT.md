# 프론트엔드 스택 그롴 보고서 검증

**날짜**: 2025-12-23  
**방법**: 레포 실제 파일/코드 기반 검증

---

## 검증 기준

- ✅ **Confirmed**: 레포에 실제 존재 (파일/코드/의존성)
- 🟡 **Unconfirmed**: 문서/코드 없음, 도입 제안 가능
- ❌ **False**: 레포와 불일치

---

## 그롴 보고서 항목 검증

### Core Framework

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| Next.js | Next 14+ 고정 | ✅ **Confirmed** | Next.js 16.0.10 (`package.json`) |
| React | React 19 | ✅ **Confirmed** | React 19.2.1 (`package.json`) |

### 스타일링

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| Tailwind CSS | 사용 | ✅ **Confirmed** | `tailwind.config.*`, `globals.css` |
| shadcn/ui | 사용 | ✅ **Confirmed** | `src/components/ui/` (Radix UI 기반) |

### 상태 관리 / 데이터 페칭

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| Zustand | 고정 | ❌ **False** | 레포 검색 결과 없음 |
| React Query + Zustand | 고정 | ❌ **False** | React Query 없음, SWR 사용 중 |

### 인증

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| Clerk | 고정 | ❌ **False** | 레포 검색 결과 없음, 커스텀 Browser Auth 사용 |

### 모니터링 / 분석

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| Sentry | 사용 | ❌ **False** | 레포 검색 결과 없음 |
| Vercel Analytics | 사용 | ❌ **False** | 레포 검색 결과 없음 |

### 차트 / 시각화

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| Recharts | 사용 | ✅ **Confirmed** | `package.json` (recharts: ^3.6.0) |
| Tremor | 사용 | ❌ **False** | 레포 검색 결과 없음 |

### 폼 / 검증

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| Zod | 사용 | ❌ **False** | 레포 검색 결과 없음 |
| React Hook Form | 사용 | ❌ **False** | 레포 검색 결과 없음 |

### i18n

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| next-intl | 사용 | ❌ **False** | 레포 검색 결과 없음 (한국어 고정) |

### 실시간 통신

| 항목 | 그롴 주장 | 실제 상태 | 근거 |
|------|----------|----------|------|
| SSE | 사용 | ✅ **Confirmed** | `src/app/api/mcp/thoughts/sse/route.ts` |

---

## 검증 요약

### ✅ Confirmed (7개)

- Next.js 16.0.10
- React 19.2.1
- Tailwind CSS
- shadcn/ui (Radix UI)
- Recharts
- SSE
- SWR (React Query 대신)

### ❌ False (7개)

- Zustand
- React Query
- Clerk
- Sentry
- Vercel Analytics
- Tremor
- Zod / React Hook Form
- next-intl

### 🟡 Unconfirmed (도입 제안 가능)

- 위 False 항목들은 모두 도입 제안 가능

---

## 결론

그롴 보고서는 **일부 항목이 레포와 불일치**합니다. 특히:

- 상태 관리: Zustand/React Query 주장, 실제는 SWR 사용
- 인증: Clerk 주장, 실제는 커스텀 Browser Auth
- 모니터링: Sentry/Vercel Analytics 주장, 실제는 없음

**권장**: 그롴 보고서는 "의도/방향"으로 분류하고, 실제 스택은 `SSOT_FRONTEND_STACK.md`를 SSOT로 사용.

---

**상태**: 검증 완료. 레포 증거 기반으로 확정.
