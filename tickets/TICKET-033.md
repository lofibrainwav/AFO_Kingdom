# TICKET-033: IRS 실시간 SSOT 동기화 시스템 (IRS Real-time SSOT Synchronization)

## 🎯 티켓 개요

**상태**: OPEN
**우선순위**: Critical
**담당**: 승상
**예상 완료일**: 2026-01-15

### 배경 (Background)

LA 베테랑 CPA (30년 경력)의 실시간 IRS 웹사이트 검토 결과, **5개 Critical/High 불일치 사항** 발견:

| 항목 | 이전 SSOT | IRS 확정 정보 | 영향도 |
|------|----------|---------------|--------|
| **주택 에너지 크레딧** | 2034년까지 30% 유지 | **2025년 12월 31일 종료** | Critical |
| **전기차 크레딧** | 2025년 말까지 유지 | **2025년 9월 30일 종료** | High |
| **보너스 감가상각** | 2025년 40% 적용 | **1월 20일 이후 100% 영구화** | High |
| **ERC 환급** | 소급 청구 가능 | **2024년 1월 31일 이후 금지** | High |
| **자동차 대출 이자** | 모든 차량 공제 | **미국 최종 조립 신차만** | Medium |

### 문제 정의 (Problem Statement)

현재 SSOT 시스템은 **스냅샷 기반**으로 IRS 변경사항을 실시간으로 반영하지 못함.
CPA 전문가 검토 결과, "할루시네이션 없는 컨택스트7"을 위해 **메타인지 기반 IRS 모니터링 시스템** 필요.

### 목표 (Objectives)

1. **IRS 실시간 모니터링**: 주요 세법 문서 24/7 자동 모니터링
2. **변경 자동 감지**: 해시 비교 기반 변경 탐지 (1시간 내)
3. **SSOT 자동 업데이트**: Trinity Score 검증 후 안전한 업데이트
4. **Julie CPA 알림**: 변경사항 실시간 알림 및 영향 평가
5. **감사 추적**: 모든 변경사항 완전한 Evidence Bundle 기록

### 요구사항 (Requirements)

#### 기능 요구사항 (Functional Requirements)

**FR-033-1: IRS Monitor Agent**
- IRS 주요 Publication 자동 다운로드 (Publication 17, Rev. Proc. 2024-40, FTB 문서 등)
- SHA256 해시 기반 변경 감지
- 모니터링 주기: 6시간 (Critical 문서), 24시간 (일반 문서)

**FR-033-2: Change Detector**
- 이전 버전 vs 신규 버전 diff 생성
- 세법 파라미터 자동 추출 및 비교
- 변경 영향도 자동 평가 (Critical/High/Medium/Low)

**FR-033-3: SSOT Auto-Updater**
- 변경 감지 시 파라미터 자동 파싱
- Trinity Score 기반 검증 (Test Suite 자동 실행)
- 안전한 업데이트 (롤백 메커니즘 내장)
- 버전 관리 및 마이그레이션 지원

**FR-033-4: Notification System**
- Julie CPA 대시보드 실시간 알림
- 변경 내용 요약 + 고객 영향 평가
- Evidence Bundle ID 기반 감사 추적
- 이메일/SMS 알림 옵션

#### 비기능 요구사항 (Non-Functional Requirements)

**NFR-033-1: 신뢰성**
- 가동률: 99.9% (IRS 다운타임 제외)
- 거짓 긍정: < 0.1%
- 변경 감지 정확도: 100%

**NFR-033-2: 보안**
- IRS 데이터 암호화 저장
- 변경 감사 로그 완전성
- 민감한 세법 정보 적절한 접근 제어

**NFR-033-3: 성능**
- 변경 감지 응답시간: < 1시간
- 업데이트 적용 시간: < 30분
- 시스템 부하: < 5% CPU/Memory

### 구현 계획 (Implementation Plan)

#### Phase 1: Core Infrastructure (1주)
- IRS Monitor Agent 기본 구조 구현
- 주요 문서 URL 및 모니터링 대상 정의
- 해시 기반 변경 감지 로직 구현

#### Phase 2: Change Detection (1주)
- Diff 생성 및 파싱 로직
- 세법 파라미터 자동 추출
- 영향도 평가 알고리즘

#### Phase 3: Auto-Update System (1주)
- SSOT 업데이트 메커니즘
- Trinity Score 기반 검증
- 롤백 및 버전 관리

#### Phase 4: Notification & Integration (1주)
- Julie CPA 대시보드 알림 위젯
- 이메일/SMS 알림 시스템
- Evidence Bundle 통합

### 기술 스택 (Technical Stack)

- **언어**: Python 3.12+
- **웹 크롤링**: requests + beautifulsoup4 + selenium (대안)
- **모니터링**: APScheduler (주기적 실행)
- **저장소**: PostgreSQL (변경 히스토리) + Redis (캐시)
- **알림**: FastAPI WebSocket + SMTP
- **테스트**: pytest + responses (모킹)

### 테스트 계획 (Test Plan)

#### 단위 테스트 (Unit Tests)
- IRS Monitor Agent 기능 검증
- 해시 비교 로직 정확성
- 파라미터 파싱 정확성

#### 통합 테스트 (Integration Tests)
- 전체 모니터링 → 감지 → 업데이트 플로우
- Julie CPA 알림 시스템
- 롤백 메커니즘

#### E2E 테스트 (End-to-End Tests)
- 실제 IRS 문서 변경 시뮬레이션
- 전체 시스템 동작 검증
- 성능 및 신뢰성 테스트

### 완료 조건 (Definition of Done)

- [ ] IRS 주요 문서 24/7 모니터링 성공
- [ ] 변경 감지 정확도 100% 달성
- [ ] SSOT 자동 업데이트 메커니즘 작동
- [ ] Julie CPA 실시간 알림 시스템 구축
- [ ] 모든 테스트 케이스 PASS
- [ ] Trinity Score ≥ 0.95 달성
- [ ] Evidence Bundle 완전 추적
- [ ] CPA 전문가 승인 획득

### 리스크 및 완화 전략 (Risks & Mitigations)

**리스크 1: IRS 웹사이트 변경**
- 완화: 다중 URL 모니터링 + API 폴백 전략

**리스크 2: 거짓 긍정**
- 완화: 다중 검증 단계 + 전문가 승인 게이트

**리스크 3: 업데이트 실패**
- 완화: 트랜잭션 기반 업데이트 + 자동 롤백

### 메트릭 (Metrics)

- **모니터링 커버리지**: 주요 세법 문서 100%
- **감지 정확도**: True Positive 100%
- **업데이트 성공률**: 99.9%
- **응답 시간**: 변경 감지 후 1시간 내 업데이트
- **사용자 만족도**: Julie CPA 피드백 기반

### 의존성 (Dependencies)

- TICKET-031: 세금 엔진 SSOT (완료)
- TICKET-032: 세금 API + Julie 위젯 (완료)
- 외부: IRS.gov API 안정성

---

**승인자**: LA 베테랑 CPA (30년 경력)
**승인 일자**: 2026-01-01
**우선순위 근거**: 세법 정확성 = 세금 신뢰성 = 고객 만족도
