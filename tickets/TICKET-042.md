# TICKET-042: Julie CPA Depreciation Calculator Integration

## 🎯 티켓 개요

**상태**: OPEN
**우선순위**: High
**담당**: 승상
**예상 완료일**: 2026-01-05

### 배경 (Background)

Julie CPA 엔진을 AFO Kingdom Soul Engine에 완전 통합하여, 실시간 감가상각 계산 및 세금 절감 시뮬레이션을 제공합니다.

**OBBBA 2025/2026 §179 + Bonus Depreciation 정확 반영**:
- §179: $2.5M(2025) → $2.56M(2026 인플레 Rev.Proc.2025-32)
- Phase-out: $4M → $4.09M
- Bonus: 100% 영구 (2025.01.20 이후 적격 자산)
- CA 특화: FTB nonconformity $25k §179 + MACRS add-back

### 문제 정의 (Problem Statement)

현재 세금 엔진은 기본 세금 계산만 제공하지만, Julie CPA의 전문적인 감가상각 계산기가 필요합니다.

### 목표 (Objectives)

1. **Julie CPA 엔진 통합**: FastAPI `/api/julie/depreciation` 엔드포인트
2. **§179 + Bonus 계산**: OBBBA 2025/2026 정확 반영
3. **CA 특화 로직**: FTB nonconformity add-back 자동
4. **DSPy MIPROv2 최적화**: Trinity Score 기반 프롬프트 튜닝
5. **인터랙티브 위젯**: Mermaid 기반 실시간 시뮬레이션

### 요구사항 (Requirements)

#### 기능 요구사항 (Functional Requirements)

**FR-042-1: Julie Depreciation API**
- `/api/julie/depreciation` POST 엔드포인트
- Pydantic v2 모델 기반 입력/출력 검증
- MyPy 100% 타입 안전성

**FR-042-2: §179 + Bonus 계산 로직**
- §179 우선 적용 ($2.56M 한도, CA $25k)
- 잔여 비용 Bonus 100% 적용
- Phase-out 초과 시 MACRS 전환

**FR-042-3: CA 특화 기능**
- FTB nonconformity add-back 자동 계산
- Form 3885 M-1 자동 생성 지원
- CA 주세 8.84% 반영

**FR-042-4: DSPy MIPROv2 통합**
- Context7 IRS 검색 연동
- Trinity Score 기반 최적화
- 할루시네이션 방지

**FR-042-5: 인터랙티브 위젯**
- Mermaid 기반 시각화
- SSE 실시간 업데이트
- Graceful degradation 지원

#### 비기능 요구사항 (Non-Functional Requirements)

**NFR-042-1: 정확성**
- IRS/FTB 규정 100% 준수
- 계산 결과 소수점 2자리 정확도

**NFR-042-2: 성능**
- 응답 시간 < 500ms
- 동시 요청 100개 지원

**NFR-042-3: 신뢰성**
- 99.9% 가용성
- 자동 롤백 메커니즘

### 구현 계획 (Implementation Plan)

#### Phase 1: Core Engine (1일)
- Julie 엔진 구조 설계
- Pydantic 모델 정의
- 기본 계산 로직 구현

#### Phase 2: CA 특화 (1일)
- FTB nonconformity 로직
- Form 3885 통합
- CA 주세 계산

#### Phase 3: DSPy 통합 (1일)
- MIPROv2 최적화 적용
- Context7 연동
- Trinity Score 검증

#### Phase 4: 위젯 통합 (1일)
- Mermaid 인터랙티브 구현
- 대시보드 통합
- SSE 실시간화

### 기술 스택 (Technical Stack)

- **Backend**: FastAPI + Pydantic v2
- **AI**: DSPy + MIPROv2
- **Frontend**: Mermaid + SSE
- **Data**: IRS/FTB SSOT (TICKET-033 연동)
- **Testing**: pytest + MyPy

### 테스트 계획 (Test Plan)

#### 단위 테스트
- §179 계산 정확성
- Bonus 적용 로직
- CA add-back 계산

#### 통합 테스트
- API 엔드포인트 동작
- DSPy 최적화 효과
- 위젯 렌더링

#### E2E 테스트
- $300k 장비 시뮬레이션
- CA 주세 계산 검증
- Trinity Score 평가

### 완료 조건 (Definition of Done)

- [ ] `/api/julie/depreciation` 엔드포인트 작동
- [ ] §179 + Bonus 계산 정확성 100%
- [ ] CA 특화 기능 완전 구현
- [ ] DSPy MIPROv2 통합 완료
- [ ] 인터랙티브 위젯 배포
- [ ] 모든 테스트 PASS
- [ ] Trinity Score ≥ 0.95
- [ ] Evidence Bundle 생성

### 리스크 및 완화 전략 (Risks & Mitigations)

**리스크 1: OBBBA 규정 복잡성**
- 완화: IRS/FTB 공식 문서 우선 검토

**리스크 2: CA 특화 로직**
- 완화: FTB 전문가 검토

**리스크 3: 성능 이슈**
- 완화: 캐싱 및 최적화 적용

### 메트릭 (Metrics)

- **계산 정확도**: 100%
- **응답 시간**: < 500ms
- **Trinity Score**: ≥ 0.95
- **사용자 만족도**: Julie CPA 피드백

### 의존성 (Dependencies)

- TICKET-031: 세금 엔진 SSOT
- TICKET-033: IRS 실시간 모니터링
- DSPy MIPROv2
- Context7 검색

---

**승인자**: Julie CPA Engine
**우선순위 근거**: 세금 절감 계산의 정확성이 고객 만족도와 직접 연계
