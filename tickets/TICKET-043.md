# TICKET-043: Julie CPA AI 에이전트 군단 운영 시스템 구축

## 🎯 티켓 개요

**상태**: OPEN
**우선순위**: High
**담당**: 승상
**예상 완료일**: 2026-01-15

### 배경 (Background)

현재 Julie CPA 시스템을 Big 4 벤치마크 수준으로 발전시켜 **완전 자동화된 세무 서비스**를 제공합니다. IRS 실시간 세법 모니터링과 AI 에이전트 군단을 통합하여 고객에게 최고 수준의 세무 솔루션을 제공합니다.

**핵심 요구사항**:
- Big 4 벤치마크형 3단계 AI 검토 계층 구축
- R.C.A.T.E. 구조화된 프롬프트/워크플로우 적용
- IRS 실시간 세법 모니터링 강화
- 휴밀리티 프로토콜 적용으로 사용자 경험 최적화

### 문제 정의 (Problem Statement)

현재 Julie CPA 시스템은 기본적인 감가상각 계산만 제공하지만, Big 4 수준의 종합 세무 서비스를 위해서는 AI 에이전트 군단 기반의 자동화된 검토와 IRS 실시간 모니터링이 필요합니다.

### 목표 (Objectives)

1. **Big 4 구조 AI 에이전트 군단 구축**: Associate/Manager/Auditor 3단계 검토 계층
2. **R.C.A.T.E. 워크플로우 적용**: 구조화된 프롬프트로 일관성 확보
3. **IRS 실시간 모니터링 강화**: Critical/High/Medium 우선순위별 세법 감시
4. **휴밀리티 프로토콜 구현**: DOING/DONE/NEXT 3줄 보고로 인지부하 최소화
5. **Evidence Bundle 기반 감사 추적**: 완전한 재현 가능성 보장

### 요구사항 (Requirements)

#### 기능 요구사항 (Functional Requirements)

**FR-043-1: Big 4 구조 AI 에이전트 군단**
- **Associate 레벨**: 데이터 수집 및 초안 작성 (정형 데이터 + 근거 목록)
- **Manager 레벨**: 전략 검토 및 품질 게이트 (리스크 체크리스트 + 고객 목적 검증)
- **Auditor 레벨**: 규정 준수 감사 (IRS/FTB 근거로 판정 + Evidence Bundle 생성)

**FR-043-2: R.C.A.T.E. 구조화 워크플로우**
- **Role**: 각 에이전트의 역할 명확히 정의
- **Context**: IRS/FTB SSOT + 고객 데이터 + 비즈니스 목적
- **Action**: 구체적인 실행 계획
- **Task**: 세부 작업 분해
- **Execution**: 단계별 실행 및 검증

**FR-043-3: IRS 실시간 세법 모니터링**
- **Critical 항목**: 주거용 청정에너지 크레딧(25D), 에너지 효율 개선 크레딧(25C)
- **High 항목**: 클린 차량 크레딧(25E/30D), 보너스 감가상각, ERC 환급
- **Medium 항목**: 자동차 대출 이자 공제(OBBB)
- **감시 포인트**: Placed-in-service 날짜, 계약서 조항, VIN/조립 요건

**FR-043-4: 휴밀리티 프로토콜**
- **DOING**: 현재 처리 중인 작업 표시
- **DONE**: 완료된 결과 + Evidence Bundle 위치
- **NEXT**: Julie 승인 필요한 액션 (최대 3개)

**FR-043-5: Evidence Bundle 시스템**
- **근거 요약**: why in 3 bullets + 인용 링크
- **계산 로그**: 수식 및 파라미터 버전
- **버전 해시**: 입력/출력/사용 근거 해시

#### 비기능 요구사항 (Non-Functional Requirements)

**NFR-043-1: 정확성**
- IRS/FTB 규정 준수율: 100%
- AI 판정 정확도: 99% 이상 (Auditor 레벨)

**NFR-043-2: 신뢰성**
- 시스템 가용성: 99.9%
- Human-in-the-loop 필수 (AI 최종 판정 금지)

**NFR-043-3: 사용자 경험**
- 응답 시간: < 3초 (Associate/Manager), < 10초 (Auditor)
- 인지부하: 최소화 (3줄 보고 프로토콜)

### 구현 계획 (Implementation Plan)

#### Phase 1: AI 에이전트 군단 구조 설계 (3일)
- Big 4 구조 데이터 모델 설계
- R.C.A.T.E. 워크플로우 프레임워크 구축
- 각 레벨별 프롬프트 템플릿 개발

#### Phase 2: IRS 실시간 모니터링 강화 (4일)
- 세법 대조표 데이터베이스 구축
- 감시 포인트 자동화 시스템 구현
- Critical/High/Medium 우선순위 분류

#### Phase 3: 휴밀리티 프로토콜 통합 (3일)
- 3줄 보고 시스템 구현
- Evidence Bundle 자동 생성
- Julie 승인 워크플로우 구축

#### Phase 4: 통합 테스트 및 배포 (3일)
- 종단간 테스트 수행
- Trinity Score 검증
- 운영 모니터링 시스템 구축

### 기술 스택 (Technical Stack)

- **AI Framework**: DSPy MIPROv2 (프롬프트 최적화)
- **Backend**: FastAPI + Pydantic v2
- **Database**: PostgreSQL (세법 데이터 + Evidence Bundle)
- **Monitoring**: IRS/FTB 실시간 크롤링
- **Frontend**: 휴밀리티 프로토콜 UI 컴포넌트
- **Testing**: pytest + MyPy + Trinity Score 검증

### 테스트 계획 (Test Plan)

#### 단위 테스트
- 각 AI 에이전트 레벨 기능 검증
- R.C.A.T.E. 구조 준수도 테스트
- Evidence Bundle 생성 정확성

#### 통합 테스트
- 3단계 검토 워크플로우 종단간 테스트
- IRS 모니터링 정확성 검증
- 휴밀리티 프로토콜 UI/UX 테스트

#### E2E 테스트
- 실제 세무 시나리오 풀 체인 테스트
- Critical 세법 변경 감지 및 대응
- Julie 승인 워크플로우 검증

### 완료 조건 (Definition of Done)

- [ ] Big 4 구조 AI 에이전트 군단 작동
- [ ] R.C.A.T.E. 워크플로우 적용 완료
- [ ] IRS 실시간 모니터링 시스템 구축
- [ ] 휴밀리티 프로토콜 구현 및 적용
- [ ] Evidence Bundle 자동 생성 시스템
- [ ] 모든 테스트 PASS (99% 이상 정확도)
- [ ] Trinity Score ≥ 0.95 달성
- [ ] Julie 승인 워크플로우 완전 구현

### 리스크 및 완화 전략 (Risks & Mitigations)

**리스크 1: AI 판정 신뢰성**
- 완화: Auditor 레벨에서만 IRS/FTB 직접 근거 사용, Human-in-the-loop 필수

**리스크 2: IRS 규정 복잡성**
- 완화: 세법 대조표 우선순위 적용, Two-source rule 준수

**리스크 3: 사용자 경험 복잡도**
- 완화: 휴밀리티 프로토콜로 인지부하 최소화

### 메트릭 (Metrics)

- **AI 판정 정확도**: 99% 이상
- **응답 시간**: Associate < 3초, Auditor < 10초
- **Trinity Score**: ≥ 0.95
- **사용자 만족도**: Julie 피드백 기반 측정

### 의존성 (Dependencies)

- TICKET-042: Julie CPA 기본 시스템
- TICKET-033: IRS 실시간 모니터링
- DSPy MIPROv2 최적화 프레임워크

---

**승인자**: Julie CPA Chief AI Officer
**우선순위 근거**: Big 4 수준 세무 서비스로 고객 신뢰도 및 시장 경쟁력 극대화
