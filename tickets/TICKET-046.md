# TICKET-046: 코드 검증 시스템 모듈화 및 AST 심층 분석 구현

## 🎯 티켓 개요

**TICKET-045 Baseline Code Review** 완료 후, 코드 검증 시스템의 **모듈화와 심층 분석 기능**을 추가 구현한다.

## 📋 요구사항

### 기능 요구사항
- [ ] **코드 모듈화**: 단일 파일 구조 → 패키지 기반 모듈화
- [ ] **AST 심층 분석**: 코드 복잡도, 보안 취약점, 중복 분석 추가
- [ ] **SOLID 원칙 준수**: 단일 책임 분리 및 의존성 역전
- [ ] **재사용성 향상**: 테스트 용이성 및 유지보수성 개선

### 비기능 요구사항
- [ ] **Trinity Score 목표**: 美 1.0, 眞 0.9 달성
- [ ] **호환성 유지**: 기존 SSOT 결과와의 호환성 보장
- [ ] **성능 영향 최소화**: 분석 시간 2초 이내 유지

## 🔍 현재 상태 분석 (메타인지 검증 결과)

### ✅ 구현 가능한 부분
- validation 패키지 구조 생성
- AST 기반 코드 분석 모듈
- 모듈 로더/러너/로거 분리

### ⚠️ 선행 구현 필요한 부분
- ChancellorContext/ChancellorNode (Phase 2)
- 멀티 에이전트 Coordinator (Phase 2)
- LangGraph 통합 (Phase 2)

## 📁 구현 계획

### Phase 1: 코드 모듈화 + AST 분석 (즉시 구현)
```
packages/afo-core/validation/
├── __init__.py           # 패키지 초기화
├── loader.py            # 모듈 로딩 책임
├── runner.py            # 실행 로직 책임
├── logger.py            # 로깅 책임
└── ast_analyzer.py      # AST 심층 분석
```

### Phase 2: 멀티 에이전트 통합 (향후 구현)
- CodeReviewCoordinator 구현
- Chancellor 그래프 통합
- LangGraph 기반 워크플로우

## 🎯 성공 기준

### 기능적 성공 기준
- [ ] `python scripts/ticket045_modular_validation.py` 실행 성공
- [ ] AST 분석 결과에 복잡도/취약점/중복 정보 포함
- [ ] 기존 SSOT 로그 형식 유지 및 확장

### 비기능적 성공 기준
- [ ] 모듈 간 의존성 명확한 분리
- [ ] 코드 라인 수 20% 이상 감소 (중복 제거)
- [ ] 테스트 커버리지 80% 이상

## 🔄 작업 단계

### 1. 패키지 구조 생성
```bash
mkdir -p packages/afo-core/validation
```

### 2. AST 분석 모듈 구현
- ASTAnalyzer 클래스 구현
- 복잡도/취약점/중복 분석 기능

### 3. 모듈화 리팩토링
- loader.py: 모듈 로딩 책임
- runner.py: 실행 로직 책임
- logger.py: 로깅 책임

### 4. 통합 테스트
- 기존 스크립트와의 호환성 검증
- SSOT 로그 생성 확인

## 📊 Trinity Score 목표

| 기둥 | 현재 | 목표 | 개선사항 |
|-----|------|------|----------|
| 眞 | 0.7 | 0.9 | AST 기반 정확한 분석 |
| 善 | 0.8 | 0.9 | 모듈화로 안정성 향상 |
| 美 | 0.7 | 1.0 | Clean Architecture 준수 |
| 孝 | 1.0 | 1.0 | 형님 요구 즉시 반영 |
| 永 | 0.8 | 1.0 | 모듈화로 유지보수성 극대화 |

## 🎯 예상 결과

### 실행 결과 예시
```json
{
  "ticket": "TICKET-046",
  "ast_analysis": {
    "complexity_score": 2.0,
    "vulnerabilities": [],
    "duplicates": ["calculate_sum"],
    "approved": true,
    "score": 0.9
  },
  "modular_validation": true
}
```

## 📋 체크리스트

### 코드 구현
- [ ] validation 패키지 생성
- [ ] ASTAnalyzer 클래스 구현
- [ ] loader/runner/logger 모듈 구현
- [ ] 통합 테스트 스크립트 작성

### 문서화
- [ ] 모듈별 README 작성
- [ ] API 문서 업데이트
- [ ] 사용 예제 추가

### 검증
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 실행
- [ ] 성능 테스트 (분석 시간 측정)

## 🔗 관련 티켓

- **TICKET-045**: Baseline Code Review 구현 (완료)
- **향후**: 멀티 에이전트 통합 티켓

## 📅 일정

- **시작일**: 2026-01-01
- **완료 목표**: 2026-01-01 (당일 완료)
- **담당**: AFO 왕국 승상 시스템

---

**SSOT Report Gate**: 준비 중
**Decision**: **AUTO_RUN APPROVED** (단계적 구현)
