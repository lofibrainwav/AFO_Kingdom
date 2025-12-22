# 🏰 AFO Kingdom 대시보드

## 메인 대시보드

**`kingdom_dashboard.html`** - 최적화된 메인 대시보드 (v2.0)

### 특징
- ✅ 완전히 리팩터링된 구조 (CSS/JS 분리)
- ✅ 인라인 스타일 제거 (96.6% 감소)
- ✅ 반응형 디자인
- ✅ 시스템 아키텍처 상세 설명 포함
- ✅ Mermaid 다이어그램 통합
- ✅ 眞善美孝永 5기둥 철학 시각화

### 파일 구조
```
kingdom_dashboard.html  (231 KB) - 메인 HTML
kingdom_dashboard.css   (19 KB)  - 스타일시트
kingdom_dashboard.js    (216 KB) - JavaScript 로직
md/                     - 마크다운 콘텐츠 (외부화)
```

### 사용법
```bash
# 로컬 서버 실행
python3 -m http.server 8000

# 브라우저에서 접속
open http://localhost:8000/kingdom_dashboard.html
```

### 주요 섹션
1. **眞善美孝永 철학** - 5기둥 시각화
2. **시스템 전체 지도** - 아키텍처 개요
3. **아키텍처 상세** - 4계층, 재상 그래프, 오장육부 시스템
4. **승상 시스템 구도** - 3책사, 5호장군
5. **SSOT** - Single Source of Truth
6. **MCP 도구** - Model Context Protocol 관리
7. **Skills & 도구** - 19개 스킬 레지스트리
8. **🔍 Git 트리 분석** - Git 히스토리 전체 분석, Phase별 진화, 주요 마일스톤
9. **📦 프로젝트 구조** - 패키지별 상세 분석, 디렉토리 트리, 아키텍처 매핑

### 최적화 내역
- 인라인 스타일: 29개 → 1개 (96.6% 감소)
- CSS 클래스 구조화
- 반응형 그리드 레이아웃
- Mermaid 다이어그램 통합
- 접근성 개선

### 백업 파일
기존 대시보드 파일들은 `.backup/dashboard_legacy/`에 백업되어 있습니다.

### Git 트리 분석 섹션 (2025-12-22 추가)
- Git 히스토리 전체 분석 (120개 커밋, 2025-12-16 ~ 2025-12-21)
- Phase별 진화 타임라인 (Mermaid Gantt)
- Phase별 진화 과정 플로우차트
- 주요 마일스톤 하이라이트
- 상세 시각화 링크: `docs/git_tree_visualization.html`

### 프로젝트 구조 섹션 (2025-12-22 추가)
- 전체 통계 (Python 1,506개, TypeScript 5,439개, Markdown 1,005개)
- 패키지 구조 다이어그램 (Mermaid)
- 주요 디렉토리 설명
- 상세 문서 링크: `docs/PROJECT_STRUCTURE_COMPLETE.md`, `docs/ARCHITECTURE_MAP.md`

---
**생성일**: 2025-12-22  
**버전**: 2.1 (Git 트리 분석 및 프로젝트 구조 섹션 추가)
