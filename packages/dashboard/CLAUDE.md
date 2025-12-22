# CLAUDE.md — Dashboard Frontend (Claude Override)

> Next.js 대시보드 전용 Claude 지침 (루트 `CLAUDE.md` 상속).  
> 충돌 시 **루트 규칙이 우선**한다.

이 문서는 `packages/dashboard/` 폴더에서 작업하는 Claude 에이전트를 위한 세부 지침입니다.

---

## 0) Scope (이 폴더의 책임)

- Next.js 기반 Dashboard UI, Tailwind 스타일, 상태관리, API 연동 UI
- UX/일관성/접근성(키보드/스크린리더) 유지

---

## 1) SSOT (이 폴더에서 최우선으로 보는 근거)

에이전트는 작업 전 아래 파일의 **존재 여부를 확인하고** 존재하는 것만 읽는다.

- `./packages/dashboard/README.md`
- `./packages/dashboard/package.json`
- `./packages/dashboard/tsconfig*.json`
- `./packages/dashboard/next.config.*`
- `./packages/dashboard/tailwind.config.*`
- 루트: `./CLAUDE.md`, `./AGENTS.md`, `./docs/AFO_FRONTEND_ARCH.md`(존재 시)

---

## 2) Setup Commands (이 폴더 전용)

### 설치

- `pnpm install` (pnpm-lock.yaml 존재)

### 실행

- Dev: `pnpm dev` (port 3000)
- Build: `pnpm build`
- Start: `pnpm start` (프로덕션 모드)

---

## 3) Quality Gates (이 폴더의 완료 기준)

### Lint

- `pnpm lint` (ESLint 실행)

### Type-check

- `pnpm type-check` (TypeScript 컴파일러 체크)
- 또는 `tsc --noEmit` (직접 실행)

### Tests

- `pnpm test` (존재 시)

### Build

- `pnpm build` (변경이 빌드 결과에 영향 있으면 필수)

---

## 4) Beauty Rules (UI 미학 = 구조/일관성)

- 컴포넌트는 "재사용 가능한 최소 단위"로 분리한다.
- 기존 디자인 시스템/패턴이 있으면 그대로 따른다.
- "겸사겸사 리디자인/리팩터" 금지(요청 범위 밖 변경 금지).
- Tailwind를 이미 쓰고 있으면 Tailwind 우선, 임의의 CSS/새 라이브러리 도입은 ASK.

### 스타일 가이드

- **Tailwind CSS**: 기본 스타일링
- **Glassmorphism**: 카드/모달 등에 적용
- **Trinity Glow**: Trinity Score 표시 시 사용
- **Atomic 컴포넌트 패턴**: 작은 단위부터 조합

---

## 5) 핵심 경로 (Core Paths)

- **페이지**: `packages/dashboard/src/app/`
- **컴포넌트**: `packages/dashboard/src/components/`
- **훅**: `packages/dashboard/src/hooks/`
- **라이브러리**: `packages/dashboard/src/lib/`
- **타입**: `packages/dashboard/src/types/`
- **스타일**: `packages/dashboard/src/app/globals.css`

---

## 6) Goodness Rules (안전/접근성/데이터)

- 접근성:
  - 클릭 요소는 키보드/포커스 가능해야 한다.
  - 아이콘 버튼은 `aria-label`을 제공한다.
- 데이터 표시:
  - 로딩/에러/빈 상태를 반드시 명확히 처리한다.
  - 민감정보(키/토큰/개인정보)를 UI/로그에 노출 금지.

---

## 7) Performance & Serenity (마찰 제거)

- 불필요한 리렌더/중복 fetch 금지. 기존 캐시/상태관리 패턴을 따른다.
- 큰 컴포넌트는 쪼개되, 과도한 추상화는 금지(읽기 쉬움 우선).
- "측정 없는 성능 주장" 금지. 개선은 관측 가능해야 한다(예: 로딩 시간/렌더 횟수).

---

## 8) 금지구역 (추가)

루트 `CLAUDE.md`의 금지구역에 추가:

- `packages/dashboard/src/app/globals.css` 무단 수정 금지
- Trinity Score UI 로직 변경 금지 (명시 지시 없이)
- Glassmorphism 디자인 시스템 핵심 변경 금지

---

## 9) Claude-Specific Tips (이 폴더 작업 시)

- **컴포넌트 계층 구조**: 페이지 → 레이아웃 → 컴포넌트 순서로 계획
- **타입 우선 설계**: TypeScript 타입을 먼저 정의하고, 그 다음 구현
- **재사용성 고려**: Atomic 컴포넌트 패턴으로 작은 단위부터 조합

---

## 10) Output Contract (보고 포맷)

작업 결과는 반드시 아래 JSON 요약을 포함한다.

```json
{
  "decision": "AUTO_RUN | ASK_COMMANDER | BLOCK",
  "risk_score": 0,
  "trinity_score": 0,
  "evidence": ["..."],
  "files_changed": ["..."],
  "checks_ran": ["..."],
  "rollback_plan": ["..."]
}
```

---

**작성일**: 2025-12-21  
**Claude 팁**: 컴포넌트 설계 시 타입을 먼저 정의하고, 재사용 가능한 작은 단위부터 조합하세요.

---

# End of ./packages/dashboard/CLAUDE.md
