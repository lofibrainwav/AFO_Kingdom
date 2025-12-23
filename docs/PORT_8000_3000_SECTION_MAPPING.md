# 포트 8000-3000 섹션 매핑 분석 (Phase 0 완료)

> **작성일**: 2025-12-23  
> **목적**: kingdom_dashboard.html (포트 8000)의 모든 섹션을 Next.js Dashboard (포트 3000)로 통합하기 위한 완벽한 매핑

---

## 📊 현재 상태 요약

### 포트 8000 (kingdom_dashboard.html)
- **파일 크기**: HTML 4,304줄, JS 6,022줄, CSS (추정 40KB)
- **총 섹션 수**: 36개 (중복 제거 후)
- **위젯 시스템**: WidgetRegistry 기반 동적 위젯 관리
- **인터랙티브 기능**: Mermaid 다이어그램, SVG 지도, 실시간 상태 업데이트

### 포트 3000 (Next.js Dashboard)
- **프레임워크**: Next.js 16.0.10, React 19.2.1
- **기존 페이지**: 
  - `/` - RoyalLayout (메인 대시보드)
  - `/docs` - 문서 메인 페이지
  - `/docs/philosophy` - 철학 페이지 (✅ 이미 존재)
  - `/docs/git-tree` - Git 트리 분석 (✅ 이미 존재)
  - `/docs/project-structure` - 프로젝트 구조 (✅ 이미 존재)
  - `/docs/architecture` - 시스템 아키텍처 (✅ 이미 존재)
- **컴포넌트**: RoyalPhilosophy, RoyalArchitecture, RoyalLibrary 등 이미 구현됨

---

## 🗺️ 섹션별 매핑 및 통합 전략

### 그룹 A: 핵심 섹션 (즉시 통합 - Phase 2)

| HTML 섹션 ID | 제목 | Next.js 경로 | 상태 | 우선순위 |
|-------------|------|-------------|------|---------|
| `philosophy` | 眞善美孝永 - 왕국의 철학 | `/docs/philosophy` | ✅ 이미 존재 | 🔴 최고 |
| `realtime-status` | 실시간 상태 대시보드 | `/docs/realtime-status` | ❌ 미구현 | 🔴 최고 |
| `architecture` | 시스템 아키텍처 | `/docs/architecture` | ✅ 이미 존재 | 🔴 최고 |
| `chancellor` | 승상 시스템 | `/docs/chancellor` | ❌ 미구현 | 🔴 최고 |
| `ssot` | Single Source of Truth | `/docs/ssot` | ❌ 미구현 | 🔴 최고 |

### 그룹 B: 오장육부 및 MCP (Phase 2 - 병렬)

| HTML 섹션 ID | 제목 | Next.js 경로 | 상태 | 우선순위 |
|-------------|------|-------------|------|---------|
| `organs-map` | 오장육부 지도 | `/docs/organs-map` | ❌ 미구현 | 🟡 높음 |
| `organs` | 11-오장육부 건강 모니터 | `/docs/organs` | ⚠️ 부분 구현 (RoyalLayout에 OrgansMonitor 존재) | 🟡 높음 |
| `mcp-tools` | MCP 도구 | `/docs/mcp-tools` | ❌ 미구현 | 🟡 높음 |
| `tools` | 도구 레지스트리 | `/docs/tools` | ❌ 미구현 | 🟡 높음 |
| `scholars` | 집현전 학자들 | `/docs/scholars` | ❌ 미구현 | 🟡 높음 |

### 그룹 C: 문서 및 매뉴얼 (Phase 2 - 병렬)

| HTML 섹션 ID | 제목 | Next.js 경로 | 상태 | 우선순위 |
|-------------|------|-------------|------|---------|
| `git-tree-analysis` | Git 트리 분석 | `/docs/git-tree` | ✅ 이미 존재 | 🟢 중간 |
| `project-structure` | 프로젝트 구조 | `/docs/project-structure` | ✅ 이미 존재 | 🟢 중간 |
| `agents-md` | AGENTS.md | `/docs/agents-md` | ❌ 미구현 | 🟢 중간 |
| `claude-md` | CLAUDE.md | `/docs/claude-md` | ❌ 미구현 | 🟢 중간 |
| `codex-md` | CODEX.md | `/docs/codex-md` | ❌ 미구현 | 🟢 중간 |
| `cursor-md` | CURSOR.md | `/docs/cursor-md` | ❌ 미구현 | 🟢 중간 |
| `grok-md` | GROK.md | `/docs/grok-md` | ❌ 미구현 | 🟢 중간 |
| `manual` | 야전교범 | `/docs/manual` | ❌ 미구현 | 🟢 중간 |

### 그룹 D: 고급 기능 (Phase 3 - 인터랙티브)

| HTML 섹션 ID | 제목 | Next.js 경로 | 상태 | 우선순위 |
|-------------|------|-------------|------|---------|
| `table-of-contents` | 목차 | `/docs/table-of-contents` | ❌ 미구현 | 🔵 낮음 |
| `architecture-detail` | 아키텍처 상세 | `/docs/architecture-detail` | ❌ 미구현 | 🔵 낮음 |
| `lock` | LOCK 원칙 | `/docs/lock` | ❌ 미구현 | 🔵 낮음 |
| `integrity` | 무결성 체크리스트 | `/docs/integrity` | ❌ 미구현 | 🔵 낮음 |
| `status` | 시스템 상태 | `/docs/status` | ⚠️ 부분 구현 (RoyalLayout에 SystemStatusWidget 존재) | 🔵 낮음 |
| `git` | Git 상태 | `/docs/git` | ⚠️ 부분 구현 (RoyalLayout에 GitWidget 존재) | 🔵 낮음 |
| `library` | 왕국 도서관 | `/docs/library` | ⚠️ 부분 구현 (RoyalLayout에 RoyalLibrary 존재) | 🔵 낮음 |
| `graphrag` | GraphRAG | `/docs/graphrag` | ⚠️ 부분 구현 (RoyalLayout에 GraphRAGQuery 존재) | 🔵 낮음 |

### 그룹 E: 메타 및 위젯 (Phase 3 - 인터랙티브)

| HTML 섹션 ID | 제목 | Next.js 경로 | 상태 | 우선순위 |
|-------------|------|-------------|------|---------|
| `technical-debt` | 기술적 부채 | `/docs/technical-debt` | ❌ 미구현 | 🔵 낮음 |
| `daily-check` | 지속 체크리스트 | `/docs/daily-check` | ❌ 미구현 | 🔵 낮음 |
| `widget-ideas` | 위젯 아이디어 | `/docs/widget-ideas` | ❌ 미구현 | 🔵 낮음 |
| `agent-brotherhood` | 에이전트 형제애 | `/docs/agent-brotherhood` | ❌ 미구현 | 🔵 낮음 |
| `knowledge-learning` | 지식 학습 | `/docs/knowledge-learning` | ❌ 미구현 | 🔵 낮음 |
| `mcp-skill-mastery` | MCP 스킬 숙련도 | `/docs/mcp-skill-mastery` | ❌ 미구현 | 🔵 낮음 |
| `mcp-definition` | MCP 정의 | `/docs/mcp-definition` | ❌ 미구현 | 🔵 낮음 |
| `unified-server-structure` | 통합 서버 구조 | `/docs/unified-server-structure` | ❌ 미구현 | 🔵 낮음 |

---

## 🔍 의존성 분석

### JavaScript 로직 의존성

1. **WidgetRegistry 시스템**
   - 위치: `kingdom_dashboard.js` (라인 2518-2654)
   - 용도: 위젯 등록, 초기화, 업데이트 관리
   - 변환: React Context API + Custom Hook으로 변환

2. **기둥 상세 정보 모달**
   - 함수: `showPillarDetails()`, `getPillarInfo()`
   - 위치: `kingdom_dashboard.js` (라인 7-77, 84-100)
   - 변환: 이미 `RoyalPhilosophy` 컴포넌트에 `PillarModal` 존재 (재사용 가능)

3. **Mermaid 다이어그램**
   - 초기화: `initMermaidLazy()` (라인 5726-5753)
   - 변환: `@mermaid-js/mermaid` + `'use client'` 컴포넌트

4. **실시간 상태 대시보드**
   - 함수: `initRealtimeStatusDashboard()` (라인 5801-5974)
   - API: `http://localhost:8010/api/...`
   - 변환: SWR + React 컴포넌트

5. **오장육부 모니터**
   - 함수: `initializeOrgansMonitor()`
   - 변환: 이미 `OrgansMonitor` 컴포넌트 존재 (재사용 가능)

---

## 📈 변환 복잡도 평가

### 낮은 복잡도 (즉시 변환 가능)
- ✅ `philosophy` - 이미 구현됨
- ✅ `git-tree-analysis` - 이미 구현됨
- ✅ `project-structure` - 이미 구현됨
- ✅ `architecture` - 이미 구현됨
- 🟢 `realtime-status` - 기존 위젯 재사용 가능
- 🟢 `chancellor` - 기존 ChancellorStream 재사용 가능

### 중간 복잡도 (컴포넌트 변환 필요)
- 🟡 `organs-map` - SVG 지도 변환 필요
- 🟡 `mcp-tools` - 위젯 시스템 변환 필요
- 🟡 `tools` - 테이블/리스트 컴포넌트 필요
- 🟡 `scholars` - 카드 그리드 컴포넌트 필요

### 높은 복잡도 (인터랙티브 기능 필요)
- 🔴 `table-of-contents` - 동적 네비게이션 필요
- 🔴 `technical-debt` - 차트/그래프 필요
- 🔴 `daily-check` - 실시간 업데이트 필요
- 🔴 `widget-ideas` - 동적 위젯 생성 필요

---

## 🎯 우선순위 결정 (빌드 성공률 최대화)

### Phase 2 우선순위 (병렬 작업 가능)

**그룹 A (핵심) - 직렬 시작, 병렬 완료**
1. `realtime-status` - 실시간 상태 대시보드
2. `chancellor` - 승상 시스템 (기존 컴포넌트 확장)
3. `ssot` - Single Source of Truth

**그룹 B (오장육부) - 병렬**
4. `organs-map` - SVG 지도 변환
5. `mcp-tools` - MCP 도구 관리
6. `tools` - 도구 레지스트리
7. `scholars` - 집현전 학자들

**그룹 C (문서) - 병렬**
8. `agents-md` - AGENTS.md 뷰어
9. `claude-md` - CLAUDE.md 뷰어
10. `codex-md` - CODEX.md 뷰어
11. `cursor-md` - CURSOR.md 뷰어
12. `grok-md` - GROK.md 뷰어
13. `manual` - 야전교범

### Phase 3 우선순위 (인터랙티브 기능)

14. `table-of-contents` - 동적 목차
15. `technical-debt` - 기술 부채 추적
16. `daily-check` - 지속 체크리스트
17. `widget-ideas` - 위젯 아이디어
18. 기타 메타 섹션들

---

## 🔧 변환 전략

### 1. 공통 컴포넌트 (Phase 1)
- `MermaidDiagram.tsx` - Mermaid 다이어그램 렌더링
- `CodeBlock.tsx` - 코드 블록 하이라이팅
- `SectionCard.tsx` - 섹션 카드 컴포넌트
- `InteractiveSVG.tsx` - 인터랙티브 SVG 래퍼
- `MarkdownViewer.tsx` - Markdown 문서 뷰어

### 2. 유틸리티 함수 (Phase 1)
- `convertHtmlToReact.ts` - HTML → React 변환 유틸
- `extractJavaScript.ts` - JavaScript 로직 추출
- `parseMermaid.ts` - Mermaid 다이어그램 파싱
- `widgetRegistry.ts` - React 기반 위젯 레지스트리

### 3. 스타일 시스템
- Tailwind CSS 변환 (기존 Glassmorphism 유지)
- CSS 변수 → Tailwind config 변환

---

## ✅ Phase 0 완료 기준

- [x] 모든 섹션 ID 파악 (36개)
- [x] Next.js 기존 페이지 매핑 (4개 이미 존재)
- [x] 의존성 분석 완료
- [x] 변환 복잡도 평가 완료
- [x] 우선순위 결정 완료
- [x] 섹션 매핑 문서 작성 완료

---

**다음 단계**: Phase 1 - 공통 컴포넌트 및 인프라 구축

