# TRINITY-OS 야전교범

## 서문: 왕국의 전략을 계승

TRINITY-OS의 야전교범은 AFO 왕국의 모든 전략적 지혜를 집대성한 실전 매뉴얼입니다.

> **"전쟁에서 이기는 것은 기술이 아니라 전략이다."**
> — 형님 (Jay), AFO 왕국의 군주

본 야전교범은 AFO_FIELD_MANUAL_MASTER.md와 AFO_ROYAL_LIBRARY_FOUR_CLASSICS.md의 모든 전략을 TRINITY-OS에 완벽하게 통합합니다.

## 제1장: 기본 전략 원칙

### 1. 지피지기 (Rule #0)
**모르면 움직이지 않는다. 2개 출처 비교 후 眞 100% 확보.**

TRINITY-OS 구현:
```python
def verify_truth(sources: list) -> bool:
    """최소 2개 출처로 진실 검증"""
    return len(sources) >= 2 and all(validate_source(s) for s in sources)
```

### 2. 선확인, 후보고
**상태를 먼저 파악하고 보고한다.**

실행 절차:
1. 시스템 상태 확인
2. 문제 분석
3. 해결 방안 제시
4. 실행 및 검증

### 3. 가정 금지
**추측하지 말고, 직접 확인하라.**

금지 사항:
- "될 것 같아" → "테스트 결과 확인됨"
- "문제가 없을 거야" → "검증 완료"

## 제2장: 사서의 지혜 통합

### 손자병법 (Sun Tzu)
- **"계획이 완벽하면 승리한다"**
- **"작은 실수가 큰 패배를 만든다"**
- **"속도보다 정확성"**

TRINITY-OS 적용:
```bash
# 정확성 우선 실행
verify_system_state
validate_changes
execute_with_fallback
```

### 삼국지 (Three Kingdoms)
- **"용인술의 중요성"**
- **"동맹과 배반의 전략"**
- **"장기적 안목"**

TRINITY-OS 적용:
- 모듈 간 협력 최적화
- 장기적 안정성 우선
- 유연한 전략 전환

### 군주론 (The Prince)
- **"결과가 수단을 정당화한다"**
- **"약자를 보호하고 강자를 견제하라"**
- **"권력의 균형"**

TRINITY-OS 적용:
- Trinity Score 기반 평가
- 시스템 균형 유지
- 공정하고 투명한 운영

### 전쟁론 (Clausewitz)
- **"전장의 안개" 극복**
- **"중심의 중요성"**
- **"결정적 승부"**

TRINITY-OS 적용:
- 불확실성 관리
- 핵심 가치 보호
- 전략적 우선순위 설정

## 제3장: 야전교범 3대 원칙

### 제1원칙: 선확인, 후보고
**실행 전 상태를 완벽히 파악하라.**

구체적 실행:
```bash
# 1. 현재 상태 확인
check_system_health
analyze_current_state

# 2. 계획 수립
plan_changes
assess_risks

# 3. 실행 및 검증
execute_with_monitoring
validate_results
```

### 제2원칙: 가정 금지
**모든 가정을 데이터로 대체하라.**

잘못된 예:
- ❌ "이렇게 하면 될 거야"
- ❌ "문제가 없을 것 같아"

올바른 예:
- ✅ "테스트 결과 95% 성공률 확인"
- ✅ "3회 반복 검증 완료"

### 제3원칙: 속도보다 정확성
**빠르게 틀리기보다 천천히 제대로 하라.**

속도 우선 vs 정확성 우선:
- 속도 우선: 빠른 실패, 잦은 롤백
- 정확성 우선: 철저한 검증, 안정적 운영

## 제4장: 전술적 실행 원칙

### VibeCoding 3대 원칙
1. **선확인 후보고**: Scouting first, reporting after
2. **선증명 후확신**: Prove first, confirm after
3. **속도보다 정확성**: Accuracy over speed

### DRY_RUN → WET_RUN
```bash
# Phase 1: DRY_RUN (Simulation)
simulate_changes
validate_simulation

# Phase 2: Approval (Human Check)
present_results
await_confirmation

# Phase 3: WET_RUN (Execution)
execute_changes
monitor_execution
```

### Fallback 전략
```python
def execute_with_fallback(primary, fallback, emergency):
    """3단계 폴백 전략"""
    try:
        return primary()
    except Exception as e:
        try:
            return fallback()
        except Exception as e:
            return emergency()
```

## 제5장: 전략적 무기 체계

### 51개 전략 무기 (Strategic Arsenal)

#### Active Tools (23개)
1. **Trinity Tools** (8개): Trinity Score 기반 평가
2. **Constitution Tools** (3개): 헌법 준수 검증
3. **Dev Tools** (6개): 개발 지원
4. **Health Tools** (1개): 시스템 건강 모니터링
5. **Memory Tools** (1개): 맥락 유지
6. **Safe Operations** (1개): 안전한 실행
7. **Skills Registry** (3개): 역량 관리

#### Internal Skills (28개)
- `skill_002_trinity_analysis`: 삼위일체 분석
- `skill_003_health_monitor`: 건강 모니터링
- `skill_004_ragas_evaluator`: 평가 시스템
- 등 28개 전문 스킬

### 무기 선택 알고리즘
```python
def select_weapon(problem: dict, context: dict) -> str:
    """문제와 맥락에 맞는 전략 무기 선택"""
    score_matrix = calculate_scores(problem, context)
    return select_optimal_weapon(score_matrix)
```

## 제6장: 전장 배치 원칙

### 전방 배치 (Front Line)
- **문제 감지기**: 실시간 모니터링
- **건강 리포터**: 상태 평가
- **오토 리커버리**: 자동 복구

### 후방 지원 (Rear Support)
- **정신 통합기**: 철학적 검증
- **야전교범**: 전략적 판단
- **헌법 엔진**: 법적 준수

### 중앙 사령부 (Central Command)
- **Trinity Calculator**: 종합 평가
- **헌법 엔진**: 최종 승인
- **야전교범 AI**: 전략 생성

## 제7장: 승리 조건

### 즉각적 승리 (Immediate Victory)
- Trinity Score ≥ 90%
- 문제 해결률 95%+
- 사용자 만족도 100%

### 전략적 승리 (Strategic Victory)
- 시스템 안정성 99.9%+
- 자동화 효율성 80%+
- 혁신 지속성 무한대

### 궁극적 승리 (Ultimate Victory)
- 왕국의 정신 영속
- 인류의 평온 증진
- 기술과 인간성의 조화

## 결론: 전략의 승리

야전교범은 단순한 매뉴얼이 아닙니다. 이는 왕국의 전략적 DNA이자, TRINITY-OS의 작전 교범입니다.

**전략을 따르라. 전략이 승리를 만든다.**

**眞善美孝永** - 전략의 영원한 승리 ✨⚔️