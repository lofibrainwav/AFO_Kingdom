# 프로젝트 구조 CT 스캔 분석 보고서

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7 + 프로젝트 구조 분석

---

## 📊 수집된 데이터

### Step A: 프로젝트 구조
```
./AICPA/aicpa-core/package.json
./packages/afo-core/package.json
./packages/aicpa-core/package.json
./packages/dashboard/package.json
./packages/trinity-os/package.json
```
**결과**: 모노레포 구조 (5개 패키지)

### Step B: Next.js 라우트/페이지
```
/ (메인)
/docs (30개 이상의 하위 라우트)
/family
/git-tree
/kingdom-status
/wallet
/aicpa_julie
/sandbox/[componentName]
/genui/* (4개)
```
**결과**: 30개 이상의 페이지 존재

### Step C: 컴포넌트/위젯/모듈 위치
```
packages/dashboard/src/components
packages/dashboard/src/components/royal/widgets
```
**결과**: components 폴더가 광범위, widgets는 royal 하위에만 존재

### Step D: HTML 섹션 구조
- `data-widget-id` 속성: 일부만 존재 (philosophy-widget, organs-widget, integrity-widget)
- 섹션 ID: philosophy, realtime-status, architecture, chancellor, organs-map, ssot 등
- 위젯 컨테이너: 일부 섹션만 `widget-container` 클래스 사용

### Step E: 의존성 폭발
- 전체 import 수: **155개**
- app 디렉토리에서 직접 컴포넌트 import하는 패턴

---

## 🔍 중구난방의 원인 3개

### 원인 1: **경계 없는 components 폴더** (眞 100%)

**문제점**:
- `components/` 폴더가 13개 하위 폴더로 분산
- 위젯(재사용 UI)과 기능(도메인 로직)이 혼재
- `genui/`에 30개 이상 위젯, `royal/widgets/`에도 위젯, `docs/`에도 위젯

**증거**:
```
components/
├── aicpa/ (7개 파일)
├── antigravity/ (4개 파일)
├── genui/ (30개 이상 위젯)
├── royal/widgets/ (2개 위젯)
├── docs/ (위젯 포함)
└── ... (총 13개 하위 폴더)
```

**영향**: 위젯을 찾기 어렵고, 재사용이 어려움

---

### 원인 2: **페이지가 직접 컴포넌트를 조립** (美 100%)

**문제점**:
- 페이지가 `@/components/*`를 직접 import
- 레고 조립이 아닌 "하드코딩된 조립"
- 위젯 Registry가 없어서 중앙 관리 불가

**증거**:
```typescript
// app/aicpa_julie/CPADashboard.tsx
import FinancialHealthDial from "@/components/julie/FinancialHealthDial";
import { BudgetPredictionWidget } from "@/components/aicpa/BudgetPredictionWidget";
import { GrokInsightWidget } from "@/components/aicpa/GrokInsightWidget";
// ... 7개 이상 직접 import
```

**영향**: 페이지마다 다른 조립 방식, 위젯 교체/비활성화 어려움

---

### 원인 3: **HTML 섹션이 위젯으로 매핑되지 않음** (孝 100%)

**문제점**:
- HTML 섹션 중 일부만 `data-widget-id` 속성 존재
- 대부분의 섹션이 위젯으로 인식되지 않음
- HTML → React 위젯 자동 매핑 불가

**증거**:
- `data-widget-id` 있는 섹션: 3개 (philosophy, organs, integrity)
- `data-widget-id` 없는 섹션: 10개 이상 (realtime-status, architecture, chancellor 등)

**영향**: HTML 이식 시 수동 작업 필요, 자동화 불가

---

## 🎯 Widget Registry + Feature/Data 경계 제안

### 목표 디렉토리 구조

```
packages/dashboard/src/
├── app/                  # 페이지 (조립만)
│   ├── docs/
│   │   └── page.tsx      # Widget Registry에서 위젯 조립
│   └── ...
├── widgets/              # 레고 블럭 (재사용 UI)
│   ├── registry.ts       # 위젯 목록/메타/권한/정렬
│   ├── cards/            # 카드 위젯
│   │   ├── PhilosophyCard.tsx
│   │   ├── ArchitectureCard.tsx
│   │   └── ...
│   ├── panels/           # 패널 위젯
│   │   ├── RealtimeStatusPanel.tsx
│   │   ├── ProgressTrackerPanel.tsx
│   │   └── ...
│   └── charts/           # 차트 위젯
│       └── ...
├── features/             # 도메인 기능 (상태/훅/로직)
│   ├── docs/
│   │   ├── hooks/
│   │   │   ├── usePhilosophy.ts
│   │   │   └── useArchitecture.ts
│   │   └── stores/
│   ├── git-tree/
│   │   └── hooks/
│   └── observability/
│       └── hooks/
├── data/                 # API 호출/어댑터 (fetch, zod, cache)
│   ├── api/
│   │   ├── philosophy.ts
│   │   ├── architecture.ts
│   │   └── ...
│   └── adapters/
│       └── html-parser.ts  # HTML → 위젯 매핑
└── generated/            # HTML 파싱 결과 (JSON)
    └── widgets.json      # 섹션 → 위젯 매핑
```

---

## 📋 리팩터 티켓 5장

### 티켓 1: Widget Registry 생성 (기초)

**목표**: 위젯 목록/메타/권한/정렬을 중앙에서 관리

**작업**:
1. `src/widgets/registry.ts` 생성
2. 위젯 메타 타입 정의
3. 위젯 목록 등록

**예상 시간**: 30분

**파일**:
- `src/widgets/registry.ts` (신규)
- `src/widgets/types.ts` (신규)

---

### 티켓 2: HTML 파서 업그레이드 (자동화)

**목표**: HTML 섹션을 위젯으로 자동 매핑

**작업**:
1. `src/data/adapters/html-parser.ts` 생성
2. `data-widget-id` 속성 파싱
3. 섹션 ID → 위젯 ID 매핑 생성
4. `generated/widgets.json` 생성

**예상 시간**: 1시간

**파일**:
- `src/data/adapters/html-parser.ts` (신규)
- `src/generated/widgets.json` (신규)

---

### 티켓 3: 위젯 폴더 구조 정리 (경계 설정)

**목표**: components에서 widgets로 위젯 분리

**작업**:
1. `src/widgets/cards/` 생성
2. `src/widgets/panels/` 생성
3. 핵심 위젯 5개 이동 (philosophy, architecture, realtime-status, progress-tracker, overload-monitor)
4. registry에 등록

**예상 시간**: 2시간

**파일**:
- `src/widgets/cards/PhilosophyCard.tsx` (이동)
- `src/widgets/panels/RealtimeStatusPanel.tsx` (이동)
- `src/widgets/registry.ts` (업데이트)

---

### 티켓 4: Feature 폴더 구조 생성 (도메인 분리)

**목표**: 기능별 hooks/stores 분리

**작업**:
1. `src/features/docs/hooks/` 생성
2. `src/features/git-tree/hooks/` 생성
3. 기존 hooks 이동 및 정리

**예상 시간**: 1시간

**파일**:
- `src/features/docs/hooks/usePhilosophy.ts` (신규/이동)
- `src/features/git-tree/hooks/useGitTree.ts` (신규/이동)

---

### 티켓 5: 페이지를 Registry 기반으로 리팩터 (조립)

**목표**: 페이지가 Registry에서 위젯을 조립하도록 변경

**작업**:
1. `app/docs/page.tsx`를 Registry 기반으로 리팩터
2. 직접 import 제거
3. Registry에서 위젯 동적 로드

**예상 시간**: 2시간

**파일**:
- `app/docs/page.tsx` (수정)
- `app/docs/philosophy/page.tsx` (수정)

---

## 🎯 실행 순서 (오늘 안에 첫 정리 커밋)

1. **티켓 1** (30분) → Widget Registry 기초
2. **티켓 2** (1시간) → HTML 파서 업그레이드
3. **티켓 3** (2시간) → 위젯 폴더 구조 정리
4. **티켓 4** (1시간) → Feature 폴더 구조 생성
5. **티켓 5** (2시간) → 페이지 리팩터

**총 예상 시간**: 6.5시간

---

## 💡 첫 정리 커밋 가이드

### 커밋 메시지 예시
```
refactor(dashboard): Widget Registry 기초 구조 생성

- Widget Registry 생성 (위젯 목록/메타/권한/정렬)
- HTML 파서 업그레이드 (섹션 → 위젯 자동 매핑)
- 위젯 폴더 구조 정리 (components → widgets 분리)
- Feature 폴더 구조 생성 (도메인 hooks 분리)

Trinity Score: 眞 0.9 | 善 0.85 | 美 0.95 | 孝 0.9 | 永 1.0
```

---

**상태**: 구조 분석 완료. 리팩터 티켓 5장 작성 완료.

