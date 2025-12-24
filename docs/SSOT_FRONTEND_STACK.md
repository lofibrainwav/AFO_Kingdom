# SSOT: AFO Kingdom 프론트엔드 스택 (증거 기반)

**작성일**: 2025-12-23  
**근거**: 레포 실제 파일/코드 기반  
**목적**: Widget Registry + HTML 자동파싱(/docs) 리팩터링과 연결

---

## ✅ 현재 확정 스택 (증거 기반)

### Core Framework
| 항목 | 버전/사용 여부 | 근거 파일 |
|------|---------------|----------|
| **Next.js** | 16.0.10 | `packages/dashboard/package.json` |
| **React** | 19.2.1 | `packages/dashboard/package.json` |
| **React DOM** | 19.2.1 | `packages/dashboard/package.json` |
| **TypeScript** | 5.9.3 | `packages/dashboard/package.json` |

### 스타일링
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **Tailwind CSS** | ✅ 사용 | `packages/dashboard/tailwind.config.*`, `globals.css` |
| **shadcn/ui** | ✅ 사용 (Radix UI 기반) | `packages/dashboard/src/components/ui/` (avatar, badge, button, card, input, skeleton) |
| **Radix UI** | ✅ 사용 | `@radix-ui/react-avatar`, `@radix-ui/react-slot` (package.json) |

### 상태 관리 / 데이터 페칭
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **Zustand** | ❌ 없음 | 레포 검색 결과 없음 |
| **React Query (TanStack Query)** | ❌ 없음 | 레포 검색 결과 없음 |
| **SWR** | ✅ 사용 | `packages/dashboard/package.json` (swr: ^2.3.8) |
| **Custom Hooks** | ✅ 사용 | `packages/dashboard/src/hooks/` (useApi, useNotifications, useSpatialAudio, useVoiceReaction) |

### 인증
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **Clerk** | ❌ 없음 | 레포 검색 결과 없음 |
| **Browser Auth** | ✅ 사용 (커스텀) | `packages/dashboard/src/components/wallet/BrowserAuthModal.tsx` |

### 모니터링 / 분석
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **Sentry** | ❌ 없음 | 레포 검색 결과 없음 |
| **Vercel Analytics** | ❌ 없음 | 레포 검색 결과 없음 |

### 차트 / 시각화
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **Recharts** | ✅ 사용 | `packages/dashboard/package.json` (recharts: ^3.6.0) |
| **Tremor** | ❌ 없음 | 레포 검색 결과 없음 |
| **Mermaid** | ✅ 사용 | `packages/dashboard/package.json` (mermaid: ^10.9.1) |

### 폼 / 검증
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **Zod** | ❌ 없음 | 레포 검색 결과 없음 |
| **React Hook Form** | ❌ 없음 | 레포 검색 결과 없음 |

### i18n
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **next-intl** | ❌ 없음 | 레포 검색 결과 없음 |

### 실시간 통신
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **SSE (Server-Sent Events)** | ✅ 사용 | `packages/dashboard/src/app/api/mcp/thoughts/sse/route.ts` |
| **EventSource** | ✅ 사용 (클라이언트) | SSE 라우트 존재 |

### 기타 라이브러리
| 항목 | 사용 여부 | 근거 파일 |
|------|----------|----------|
| **Framer Motion** | ✅ 사용 | `packages/dashboard/package.json` (framer-motion: ^12.23.26) |
| **GSAP** | ✅ 사용 | `packages/dashboard/package.json` (gsap: ^3.14.2) |
| **Lucide React** | ✅ 사용 | `packages/dashboard/package.json` (lucide-react: ^0.561.0) |
| **use-sound** | ✅ 사용 | `packages/dashboard/package.json` (use-sound: ^5.0.0) |

---

## 🟡 의도/방향 (도입 후보)

### Unconfirmed 항목 (그롴 보고서에서 언급되었을 수 있으나 레포에 없음)

1. **Zustand** - 상태 관리 라이브러리
   - 현재: Custom hooks 사용
   - 도입 제안: 복잡한 전역 상태가 필요할 때

2. **React Query (TanStack Query)** - 서버 상태 관리
   - 현재: SWR 사용
   - 도입 제안: 더 강력한 캐싱/동기화가 필요할 때

3. **Clerk** - 인증 서비스
   - 현재: 커스텀 Browser Auth 사용
   - 도입 제안: 엔터프라이즈급 인증이 필요할 때

4. **Sentry / Vercel Analytics** - 모니터링/분석
   - 현재: 없음
   - 도입 제안: 프로덕션 모니터링이 필요할 때

5. **Zod / React Hook Form** - 폼 검증
   - 현재: 없음
   - 도입 제안: 복잡한 폼이 필요할 때

6. **next-intl** - 국제화
   - 현재: 없음 (한국어 고정)
   - 도입 제안: 다국어 지원이 필요할 때

---

## 📋 결정 로그 (ADR 스타일)

### ADR-001: Turbopack 비활성화 (webpack 유지)

**결정**: Turbopack을 비활성화하고 webpack 사용

**근거**:
- 기존 webpack 설정 (Tree-shaking 최적화) 유지 필요
- `next.config.ts`에 `turbopack: {}` 추가로 충돌 방지
- `pnpm dev` 실행 시 `--turbo` 플래그 없으면 자동으로 webpack 사용

**파일**: `packages/dashboard/next.config.ts`

---

### ADR-002: Legacy HTML 유지 (Strangler Fig 패턴)

**결정**: `kingdom_dashboard.html`을 `public/legacy/`로 이식하여 유지

**근거**:
- 8000 포트 서버 불필요 (Next.js가 자동 서빙)
- 점진적 이식을 위한 참조 자료로 유지
- `next.config.ts`의 8000 프록시 제거

**파일**: 
- `packages/dashboard/public/legacy/kingdom_dashboard.html`
- `packages/dashboard/next.config.ts` (rewrites 제거)

---

### ADR-003: Widget Registry 도입

**결정**: Widget Registry 시스템 도입

**근거**:
- 중구난방 components 폴더 정리 필요
- 페이지가 직접 컴포넌트 조립하는 문제 해결
- HTML 섹션을 위젯으로 자동 매핑 필요

**파일**: 
- `packages/dashboard/src/widgets/types.ts`
- `packages/dashboard/src/widgets/registry.ts`

---

## 🔗 Widget Registry + HTML 자동파싱(/docs) 구조 연결

### 현재 구조

```
packages/dashboard/
├── src/
│   ├── app/
│   │   └── docs/          # 페이지 (조립만)
│   ├── widgets/          # 레고 블럭 (재사용 UI)
│   │   ├── registry.ts   # 위젯 목록/메타/권한/정렬
│   │   └── types.ts
│   └── components/       # 기존 (점진적 이식)
└── public/
    └── legacy/
        └── kingdom_dashboard.html  # HTML (위젯화 예정)
```

### HTML → 위젯 매핑 규칙

1. **섹션 ID → 위젯 ID 매핑**
   - `id="philosophy"` → `widget-id="philosophy-widget"`
   - `id="architecture"` → `widget-id="architecture-widget"`

2. **data-widget-id 속성 표준화**
   - 모든 핵심 섹션에 `data-widget-id` 부여
   - 형식: `{section-id}-widget`

3. **자동 파싱 → Registry 등록**
   - HTML 파서가 `data-widget-id` 읽어서
   - `generated/widgets.json` 생성
   - Registry에 "Generated" 위젯으로 자동 등록

---

## 📊 HTML 규격 표준화

### 현재 상태

- `data-widget-id` 있는 섹션: 3개 (philosophy, organs, integrity)
- `data-widget-id` 없는 섹션: 10개 이상

### 표준화 규칙

1. **핵심 섹션 (최소 10개)에 `data-widget-id` 부여**
   - philosophy, architecture, chancellor, organs-map, ssot, realtime-status, git-tree, project-structure, mcp-tools, tools

2. **Slug 규칙**
   - 형식: `{section-id}-widget`
   - 예: `philosophy-widget`, `architecture-widget`

3. **충돌 방지**
   - 기존 `data-widget-id`와 중복 확인
   - Registry에 이미 등록된 ID와 중복 확인

---

**상태**: SSOT 문서 생성 완료. 레포 증거 기반으로 확정.

