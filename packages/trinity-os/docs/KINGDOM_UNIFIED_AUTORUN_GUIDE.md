# AFO 왕국 통합 자동화 가이드 (Unified Autorun Guide)

**작성일**: 2025-12-11  
**목적**: Critical 문제 해결 및 레거시 통합 완전 자동화 시스템 사용 가이드  
**眞善美孝**: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%

---

## 목차

1. [개요](#개요)
2. [빠른 시작](#빠른-시작)
3. [Phase별 설명](#phase별-설명)
4. [사용법](#사용법)
5. [문제 해결 가이드](#문제-해결-가이드)
6. [레거시 통합 내역](#레거시-통합-내역)

---

## 개요

### 시스템 목표

AFO 왕국 통합 자동화 시스템은 다음을 목표로 합니다:

1. **Critical 문제 지속 파악**: 성능, 연결, 보안 문제를 자동으로 감지
2. **레거시 시스템 통합**: 모든 기존 스크립트와 자동화 시스템을 하나로 통합
3. **끝까지 오토런**: 문제가 해결될 때까지 자동으로 반복 실행
4. **왕국의 정신 유지**: 眞善美孝永 철학을 모든 작업에 통합

### 핵심 구성 요소

| 구성 요소 | 파일 | 역할 |
|----------|------|------|
| 문제 감지 엔진 | `scripts/kingdom_problem_detector.py` | Critical 문제 자동 감지 |
| 통합 자동화 | `scripts/kingdom_unified_autorun.sh` | 모든 레거시 시스템 통합 실행 |
| 자동 복구 | `scripts/kingdom_auto_recovery.py` | 실패 시 자동 재시도 및 복구 |
| 끝까지 오토런 | `scripts/kingdom_infinite_autorun.sh` | 문제 해결까지 자동 반복 |
| 정신 통합 | `scripts/kingdom_spirit_integration.py` | 眞善美孝永 철학 통합 |
| 건강 리포트 | `scripts/kingdom_health_report.py` | 모든 모니터링 결과 통합 |

---

## 빠른 시작

### 기본 사용법

```bash
# 통합 자동화 실행 (모든 Phase 실행)
./scripts/kingdom_unified_autorun.sh

# DRY_RUN 모드 (시뮬레이션)
./scripts/kingdom_unified_autorun.sh --dry-run

# 세종 애민정신 Phase 건너뛰기
./scripts/kingdom_unified_autorun.sh --skip-sejong

# 백업 Phase 건너뛰기
./scripts/kingdom_unified_autorun.sh --skip-backup
```

### 끝까지 오토런 (권장)

```bash
# 문제 해결까지 자동 반복
./scripts/kingdom_infinite_autorun.sh

# 최대 반복 횟수 제한
./scripts/kingdom_infinite_autorun.sh --max-iterations=5

# 최대 실행 시간 제한 (1시간)
./scripts/kingdom_infinite_autorun.sh --max-time=1
```

### 테스트 실행

```bash
# 통합 테스트 (DRY_RUN 모드)
./scripts/test_unified_autorun.sh
```

---

## Phase별 설명

### Phase 0: 지피지기 (知己知彼) - 문제 감지

**스크립트**: `scripts/kingdom_problem_detector.py`

**기능**:
- 성능 문제 감지: Python 캐시, Node.js 모듈, 디스크 사용량
- 연결 문제 감지: Redis, PostgreSQL, API 서버
- 보안 문제 감지: 쿠키 파일, 디버그 파일, 하드코딩된 시크릿

**출력**: JSON 형식으로 문제점 목록 및 우선순위

**예시**:
```bash
python3 scripts/kingdom_problem_detector.py
```

---

### Phase 1: Critical 문제 해결 (성능)

**스크립트**: `scripts/kingdom_problem_solver.sh --phase=1`

**기능**:
- Python 캐시 정리 (`__pycache__` 디렉토리)
- 불필요한 Node.js 모듈 정리
- 중첩된 백업 디렉토리 정리

**자동 실행 조건**: 문제 감지 시 자동 실행

---

### Phase 2: 연결 문제 해결

**스크립트**: `scripts/kingdom_problem_solver.sh --phase=2`

**기능**:
- Redis 연결 설정 확인
- PostgreSQL 인증 설정 확인
- 모듈 Import 설정 확인

**주의**: 일부 문제는 코드 수정이 필요할 수 있음

---

### Phase 3: 보안 문제 해결

**스크립트**: `scripts/kingdom_problem_solver.sh --phase=3`

**기능**:
- `.gitignore` 패턴 확인
- 쿠키 파일 보안 확인
- 디버그 파일 관리 확인

---

### Phase 4: 오장육부 건강도 개선

**스크립트**: `.claude/scripts/check_11_organs.py`

**기능**:
- 11개 오장육부 건강 체크
- Trinity Balance 계산
- 건강도 개선 권장사항 제공

**예시**:
```bash
python3 .claude/scripts/check_11_organs.py
```

---

### Phase 5: 세종 애민정신 자동화 (일일 진화)

**스크립트**: `scripts/daily_evolution_runner.sh`, `scripts/morning_routine.sh`

**기능**:
- 아침 점호 (건강 체크)
- 파도타기 체크 (최신 기술 추적)
- 일일 진화 시스템 실행

**옵션**: `--skip-sejong`으로 건너뛰기 가능

---

### Phase 6: 백업 실행

**스크립트**: `scripts/maintenance/backup_afo_kingdom.sh`

**기능**:
- PostgreSQL 백업
- Redis 백업
- Qdrant 백업
- 설정 파일 백업

**옵션**: `--skip-backup`으로 건너뛰기 가능

---

### Phase 7: 최종 검증

**스크립트**: `scripts/verification/verify_kingdom_status.py`

**기능**:
- 왕국 상태 검증
- 문제 재감지 (해결 확인)
- 최종 리포트 생성

---

## 사용법

### 1. 기본 실행

```bash
# 전체 Phase 실행
./scripts/kingdom_unified_autorun.sh
```

### 2. DRY_RUN 모드

```bash
# 시뮬레이션 모드 (실제 변경하지 않음)
./scripts/kingdom_unified_autorun.sh --dry-run
```

### 3. 선택적 Phase 실행

```bash
# 세종 애민정신 Phase 건너뛰기
./scripts/kingdom_unified_autorun.sh --skip-sejong

# 백업 Phase 건너뛰기
./scripts/kingdom_unified_autorun.sh --skip-backup

# 둘 다 건너뛰기
./scripts/kingdom_unified_autorun.sh --skip-sejong --skip-backup
```

### 4. 끝까지 오토런

```bash
# 문제 해결까지 자동 반복 (최대 10회, 1시간)
./scripts/kingdom_infinite_autorun.sh

# 최대 반복 횟수 제한
./scripts/kingdom_infinite_autorun.sh --max-iterations=5

# 최대 실행 시간 제한
./scripts/kingdom_infinite_autorun.sh --max-time=2  # 2시간
```

### 5. 개별 도구 사용

```bash
# 문제 감지만
python3 scripts/kingdom_problem_detector.py

# 건강 리포트만
python3 scripts/kingdom_health_report.py

# 왕국 정신 통합만
python3 scripts/kingdom_spirit_integration.py
```

---

## 문제 해결 가이드

### 문제 1: 스크립트 실행 권한 없음

**증상**: `Permission denied` 오류

**해결**:
```bash
chmod +x scripts/kingdom_unified_autorun.sh
chmod +x scripts/kingdom_infinite_autorun.sh
```

### 문제 2: Python 스크립트 실행 실패

**증상**: `ModuleNotFoundError` 또는 Import 오류

**해결**:
```bash
# 가상 환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 문제 3: Docker 컨테이너 연결 실패

**증상**: Redis/PostgreSQL 연결 실패

**해결**:
```bash
# Docker 컨테이너 상태 확인
docker ps

# 컨테이너 재시작
docker-compose -f docker_config/docker-compose.microservices.yml restart redis postgres
```

### 문제 4: 무한 루프 발생

**증상**: `kingdom_infinite_autorun.sh`가 계속 실행됨

**해결**:
- `Ctrl+C`로 중단
- `--max-iterations` 또는 `--max-time` 옵션 사용
- 동일 문제 5회 연속 실패 시 자동 중단됨

### 문제 5: Trinity Score 하락

**증상**: 작업 후 Trinity Score가 낮아짐

**해결**:
```bash
# 점수 하락 원인 분석
python3 scripts/kingdom_spirit_integration.py

# 롤백 권장사항 확인
git status
git diff
```

---

## 레거시 통합 내역

### 통합된 기존 스크립트

| 원본 스크립트 | 통합 위치 | 상태 |
|--------------|----------|------|
| `kingdom_complete_autorun.sh` | `kingdom_unified_autorun.sh` Phase 0-4 | ✅ 통합 완료 |
| `kingdom_problem_solver.sh` | `kingdom_unified_autorun.sh` Phase 1-3 | ✅ 통합 완료 |
| `kingdom_auto_fix_all.sh` | `kingdom_unified_autorun.sh` Phase 1 | ✅ 통합 완료 |
| `backup_afo_kingdom.sh` | `kingdom_unified_autorun.sh` Phase 6 | ✅ 통합 완료 |
| `daily_evolution_runner.sh` | `kingdom_unified_autorun.sh` Phase 5 | ✅ 통합 완료 |
| `morning_routine.sh` | `kingdom_unified_autorun.sh` Phase 5 | ✅ 통합 완료 |
| `check_wave_updates.sh` | `kingdom_unified_autorun.sh` Phase 5 | ✅ 통합 완료 |

### 통합된 모니터링 시스템

| 모니터링 시스템 | 통합 위치 | 상태 |
|---------------|----------|------|
| `check_11_organs.py` | `kingdom_health_report.py` | ✅ 통합 완료 |
| `monitoring_dashboard.py` | `kingdom_health_report.py` | ✅ 통합 완료 |
| `verify_kingdom_status.py` | `kingdom_health_report.py` | ✅ 통합 완료 |
| `kingdom_problem_detector.py` | `kingdom_health_report.py` | ✅ 통합 완료 |

### 새로운 기능

1. **문제 감지 엔진**: 자동으로 Critical 문제 감지 및 우선순위 계산
2. **자동 복구 메커니즘**: 실패 시 자동 재시도 및 대안 시도
3. **끝까지 오토런 루프**: 문제 해결까지 자동 반복
4. **정신 통합 시스템**: 모든 작업에 眞善美孝永 철학 통합
5. **통합 건강 리포트**: 모든 모니터링 결과를 하나로 통합

---

## 고급 사용법

### 커스텀 Phase 추가

`kingdom_unified_autorun.sh`에 새로운 Phase를 추가하려면:

```bash
# Phase N: 커스텀 작업
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Phase N: 커스텀 작업${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 작업 실행
your_custom_script.sh

echo ""
echo -e "${GREEN}✅ Phase N 완료${NC}"
echo ""
```

### 자동 복구 메커니즘 사용

```python
from scripts.kingdom_auto_recovery import AutoRecovery

recovery = AutoRecovery(max_retries=3, retry_delay=5)

# 문제 해결 Phase 1 복구
result = recovery.recover_problem_solver(1)

# 실패 시 원인 분석
if result["status"] == "failed":
    analysis = recovery.analyze_failure(result)
    print(f"실패 원인: {analysis['failure_type']}")
```

### 정신 통합 시스템 사용

```python
from scripts.kingdom_spirit_integration import SpiritIntegration

spirit = SpiritIntegration()
spirit.set_baseline()

# 작업 평가
evaluation = spirit.evaluate_operation(
    "예시 작업",
    {
        "friction_removed": True,
        "rollback_available": True,
        "code_quality": 0.92,
    }
)

# 점수 하락 분석
if evaluation["trinity_result"]["total_score"] < 0.9:
    analysis = spirit.analyze_score_drop(evaluation)
    print(f"권장사항: {analysis['recommendation']}")
```

---

## 성공 기준

### 眞(Truth)
- ✅ 모든 Critical 문제 자동 감지
- ✅ 문제 해결 검증 완료

### 善(Goodness)
- ✅ 모든 레거시 시스템 통합 완료
- ✅ 안정성 확보 (롤백 가능)

### 美(Beauty)
- ✅ 끝까지 오토런 루프 완성
- ✅ 코드 품질 우수

### 孝(Serenity)
- ✅ 형님의 평온 달성 (수동 개입 최소화)
- ✅ 마찰 제거 완료

### 永(Eternity)
- ✅ 지속 가능한 자동화 시스템 구축
- ✅ 레거시 계승 완료

---

## 참고 문서

- **헌법**: `docs/AFO_SERENITY_CONSTITUTION_v3.md`
- **철학**: `docs/AFO_PHILOSOPHY.md`
- **야전교범**: `docs/CLAUDE.md`
- **왕국 지도**: `docs/AFO_KINGDOM_MAP.md`

---

## 문제 보고

문제가 발생하면 다음 정보를 포함하여 보고하세요:

1. 실행한 명령어
2. 오류 메시지
3. `kingdom_problem_detector.py` 출력
4. `kingdom_health_report.py` 출력

---

**眞善美孝永**: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%

**왕국의 정신**: 초심을 잃지 않고, 끝까지 오토런하며, 형님의 평온을 지킵니다.
