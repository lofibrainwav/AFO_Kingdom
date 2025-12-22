# 🏛️ 왕궁 대통합 프로젝트: 포트 8000 → 3000 통합 계획

> **眞善美孝永** - AFO Kingdom 포트 통합 전략  
> **작성일**: 2025-12-22  
> **목적**: 포트 8000 (문서)과 포트 3000 (프론트엔드) 단일화

---

## 📊 현재 상태 분석

### 포트 8000 (kingdom_dashboard.html)
- **파일 크기**: HTML 328KB, CSS 40KB, JS 232KB (총 600KB)
- **주요 섹션**: 36개 섹션
  - 철학 (眞善美孝永)
  - 아키텍처
  - 승상 시스템
  - SSOT
  - Git 트리 분석
  - 프로젝트 구조
  - MCP 도구
  - Skills 레지스트리
- **서빙 방식**: Python HTTP 서버 (`python3 -m http.server 8000`)

### 포트 3000 (Next.js Dashboard)
- **프레임워크**: Next.js 16.0.10, React 19.2.1
- **스타일**: Tailwind CSS, Glassmorphism
- **기존 페이지**:
  - `/` - RoyalLayout (메인 대시보드)
  - `/git-tree` - Git 트리 분석
  - `/family` - Family Hub
  - `/wallet` - API Wallet
  - `/kingdom-status` - Kingdom Status
- **API 라우트**: `/api/health`, `/api/family`, `/api/git-tree` 등

---

## 🎯 통합 전략: Strangler Fig 패턴

### Phase 1: Git 트리 분석 완벽화 (眞)
**목표**: Git 히스토리 재분석 및 문서 업데이트

#### 작업 내용
1. **Git 히스토리 재분석**
   - 총 커밋: 121개 (기존 120개 → 업데이트 필요)
   - 기간: 2025-12-16 ~ 2025-12-21
   - Phase별 분류 재검증

2. **문서 업데이트**
   - `docs/GIT_TREE_ANALYSIS.md` - 커밋 수 정정 (120 → 121)
   - `AFO_EVOLUTION_LOG.md` - Git 트리 분석 결과 요약 업데이트
   - `docs/AFO_ROYAL_LIBRARY.md` - Git 트리 분석 결과 요약 업데이트
   - `docs/AFO_CHANCELLOR_GRAPH_SPEC.md` - Git 트리 분석 결과 요약 업데이트

#### 예상 소요 시간: 30분

---

### Phase 2: kingdom_dashboard.html 구조 분석 (眞)
**목표**: 섹션별 컴포넌트 매핑 및 변환 계획 수립

#### 작업 내용
1. **섹션 분류**
   - **핵심 섹션** (즉시 통합):
     - `#philosophy` - 眞善美孝永 철학
     - `#git-tree-analysis` - Git 트리 분석
     - `#project-structure` - 프로젝트 구조
     - `#architecture` - 시스템 아키텍처
   
   - **중요 섹션** (2차 통합):
     - `#chancellor` - 승상 시스템
     - `#ssot` - Single Source of Truth
     - `#mcp-tools` - MCP 도구
     - `#tools` - 도구 레지스트리
   
   - **참고 섹션** (3차 통합):
     - `#agents-md`, `#claude-md`, `#codex-md` 등 에이전트 문서
     - `#manual` - 필드 매뉴얼
     - `#technical-debt` - 기술 부채

2. **컴포넌트 매핑**
   - 각 섹션을 React 컴포넌트로 변환 계획
   - 기존 Next.js 컴포넌트 재사용 가능 여부 확인

#### 예상 소요 시간: 1시간

---

### Phase 3: Next.js /docs 라우트 생성 (美)
**목표**: kingdom_dashboard.html의 핵심 섹션을 React 컴포넌트로 변환

#### 작업 내용
1. **라우트 구조 생성**
   ```
   packages/dashboard/src/app/docs/
   ├── page.tsx                    # 메인 문서 페이지
   ├── philosophy/
   │   └── page.tsx               # 眞善美孝永 철학
   ├── git-tree/
   │   └── page.tsx               # Git 트리 분석 (기존 /git-tree 통합)
   ├── project-structure/
   │   └── page.tsx               # 프로젝트 구조
   └── architecture/
       └── page.tsx               # 시스템 아키텍처
   ```

2. **컴포넌트 생성**
   - `src/components/docs/PhilosophySection.tsx`
   - `src/components/docs/GitTreeSection.tsx` (기존 `/git-tree` 재사용)
   - `src/components/docs/ProjectStructureSection.tsx`
   - `src/components/docs/ArchitectureSection.tsx`

3. **스타일 통합**
   - Tailwind CSS로 kingdom_dashboard.css 스타일 변환
   - Glassmorphism 디자인 시스템 적용

#### 예상 소요 시간: 2-3시간

---

### Phase 4: Strangler Fig 패턴 적용 (孝)
**목표**: skill_014_strangler_integrator 활용하여 점진적 통합

#### 작업 내용
1. **Next.js rewrites 설정**
   ```typescript
   // next.config.ts
   async rewrites() {
     return [
       {
         source: '/api/proxy/:path*',
         destination: `${soulEngineUrl}/:path*`,
       },
       // 8000번 포트의 정적 파일을 3000번으로 프록시 (임시)
       {
         source: '/docs/legacy/:path*',
         destination: 'http://localhost:8000/:path*',
       },
     ];
   }
   ```

2. **점진적 마이그레이션**
   - Phase 1: 핵심 섹션 통합 (philosophy, git-tree, project-structure)
   - Phase 2: 중요 섹션 통합 (chancellor, ssot, mcp-tools)
   - Phase 3: 참고 섹션 통합 (agents-md, manual, technical-debt)

3. **RoyalLayout 네비게이션 업데이트**
   - `/docs` 경로를 메인 네비게이션에 추가
   - 기존 `/git-tree`를 `/docs/git-tree`로 리다이렉트

#### 예상 소요 시간: 1-2시간

---

### Phase 5: RoyalLayout 통합 (美)
**목표**: /docs 경로를 RoyalLayout 네비게이션에 추가하고 통합 대시보드 완성

#### 작업 내용
1. **네비게이션 업데이트**
   - `RoyalLayout.tsx`에 `/docs` 메뉴 추가
   - 드롭다운 메뉴로 하위 섹션 표시

2. **통합 대시보드 완성**
   - 메인 페이지 (`/`)에서 `/docs` 섹션 미리보기
   - 위젯 형태로 핵심 문서 표시

#### 예상 소요 시간: 1시간

---

### Phase 6: 검증 및 테스트 (眞)
**목표**: 통합 후 모든 기능 정상 작동 확인

#### 작업 내용
1. **기능 검증**
   - 모든 `/docs` 하위 경로 접근 확인
   - Mermaid 다이어그램 렌더링 확인
   - 반응형 디자인 확인

2. **포트 8000 종료 스크립트 작성**
   - `scripts/stop_port_8000.sh` 생성
   - Python HTTP 서버 종료 스크립트

3. **문서 업데이트**
   - `DASHBOARD_README.md` 업데이트
   - 포트 통합 완료 기록

#### 예상 소요 시간: 30분

---

## 📋 전체 작업 계획 요약

| Phase | 작업 | 예상 시간 | 우선순위 |
|-------|------|-----------|----------|
| Phase 1 | Git 트리 분석 완벽화 | 30분 | 🔴 높음 |
| Phase 2 | kingdom_dashboard.html 구조 분석 | 1시간 | 🔴 높음 |
| Phase 3 | Next.js /docs 라우트 생성 | 2-3시간 | 🟡 중간 |
| Phase 4 | Strangler Fig 패턴 적용 | 1-2시간 | 🟡 중간 |
| Phase 5 | RoyalLayout 통합 | 1시간 | 🟢 낮음 |
| Phase 6 | 검증 및 테스트 | 30분 | 🔴 높음 |
| **총계** | | **6-8시간** | |

---

## 🎯 Trinity Score 예상

### 眞 (Truth) - 35%
- ✅ Git 트리 분석 완벽화
- ✅ 구조 분석 및 컴포넌트 매핑
- ✅ 타입 안전성 (TypeScript)
- **예상 점수**: 95/100

### 善 (Goodness) - 35%
- ✅ 점진적 마이그레이션 (리스크 최소화)
- ✅ 롤백 경로 확보
- ✅ 기존 기능 보존
- **예상 점수**: 98/100

### 美 (Beauty) - 20%
- ✅ Tailwind CSS 통합
- ✅ Glassmorphism 디자인 시스템
- ✅ 일관된 UI/UX
- **예상 점수**: 94/100

### 孝 (Serenity) - 8%
- ✅ 단일 포트로 운영 마찰 제거
- ✅ 자동화된 통합 프로세스
- **예상 점수**: 99/100

### 永 (Eternity) - 2%
- ✅ 문서화 완료
- ✅ 재현 가능한 통합 프로세스
- **예상 점수**: 96/100

### **예상 총점**: 96.0/100 ✅

---

## 🚀 실행 명령

### Phase 1 실행
```bash
# Git 트리 재분석
cd /Users/brnestrm/AFO_Kingdom
git log --format="%H|%ai|%an|%s" --all > /tmp/git_full_log.txt
# 문서 업데이트 (자동화)
```

### Phase 3 실행
```bash
# Next.js 개발 서버 시작
cd packages/dashboard
pnpm dev
# 브라우저에서 http://localhost:3000/docs 확인
```

### Phase 6 실행
```bash
# 포트 8000 종료
./scripts/stop_port_8000.sh
# 또는 수동으로
lsof -ti:8000 | xargs kill -9
```

---

## 📝 참고 사항

1. **기존 kingdom_dashboard.html 보존**
   - 통합 완료 전까지 포트 8000 유지
   - 백업: `.backup/kingdom_dashboard_legacy/`

2. **점진적 마이그레이션**
   - 한 번에 모든 섹션을 통합하지 않음
   - 핵심 섹션부터 순차적으로 통합

3. **롤백 계획**
   - Git 커밋으로 롤백 가능
   - 포트 8000은 통합 완료 전까지 유지

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: 🚦 **READY FOR PORT UNIFICATION (TRINITY 96.0/100)**

