# TRINITY-OS: 완전한 왕국 운영체제

## 시스템 개요

TRINITY-OS는 AFO 왕국의 통합 자동화 운영체제입니다. 기존 AFO 시스템을 완전히 재구성하여 독립적인 운영체제로 발전시켰습니다.

## 핵심 특징

### 🧠 철학적 기반
- **眞善美孝永 (Truth, Goodness, Beauty, Serenity, Eternity)**
- 인간 중심의 윤리적 자동화
- 지속 가능한 시스템 운영

### ⚙️ 기술적 특징
- **완전 자동화**: 문제 감지부터 해결까지 자동 실행
- **모듈화 아키텍처**: 각 컴포넌트 독립 실행 가능
- **실시간 모니터링**: Trinity Score 기반 건강도 추적
- **자가 치유**: 자동 복구 및 재시도 메커니즘

### 🎯 운영 방식
- **DRY_RUN → WET_RUN**: 안전한 실행 보장
- **Trinity Score 기반 의사결정**: 5가지 척도 평가
- **끝까지 오토런**: 목표 달성까지 지속 실행

## 시스템 구성

### Core Scripts (Python)
- `kingdom_problem_detector.py` - 지능형 문제 감지 엔진
- `kingdom_auto_recovery.py` - 자동 복구 시스템
- `kingdom_spirit_integration.py` - 왕국 정신 통합
- `kingdom_health_report.py` - 건강 상태 리포트

### Automation Scripts (Bash)
- `kingdom_unified_autorun.sh` - 통합 자동화 오케스트레이터
- `kingdom_infinite_autorun.sh` - 끝까지 오토런 엔진
- `verify_all_scripts.sh` - 검증 스위트
- `test_unified_autorun.sh` - 통합 테스트

### Interface Scripts
- `run_trinity_os.sh` - 인터랙티브 실행기 (Bash)
- `run_trinity_os.py` - Python 인터페이스
- `init_trinity_os.sh` - 시스템 초기화
- `test_trinity_os.sh` - 시스템 테스트

### Documentation
- `README.md` - 메인 가이드
- `TRINITY_MANIFEST.md` - 시스템 명세서
- `TRINITY_CONSTITUTION.md` - 헌법
- `CHANGELOG.md` - 변경 이력

## 설치 및 실행

### 1. 환경 준비
```bash
# Python 3.12+ 확인
python3 --version

# Bash 5.0+ 확인
bash --version
```

### 2. 초기화
```bash
# 권한 설정 및 초기화
./init_trinity_os.sh
```

### 3. 실행
```bash
# 인터랙티브 모드 (권장)
./run_trinity_os.sh

# 또는 Python 인터페이스
python3 run_trinity_os.py
```

## 주요 기능

### 1. 문제 감지 (Problem Detection)
```bash
python3 scripts/kingdom_problem_detector.py
```
- 성능 모니터링 (CPU, 메모리, 디스크)
- 연결 상태 확인 (데이터베이스, API)
- 보안 취약점 스캔
- 우선순위 기반 문제 분류

### 2. 건강 리포트 (Health Report)
```bash
python3 scripts/kingdom_health_report.py
```
- Trinity Score 계산 (眞善美孝永)
- 시스템 건강도 평가
- 개선 권고사항 제시

### 3. 통합 자동화 (Unified Autorun)
```bash
./scripts/kingdom_unified_autorun.sh
```
- 7단계 자동화 파이프라인
- DRY_RUN 모드 지원
- 세종 애민정신 자동화 통합

### 4. 끝까지 오토런 (Infinite Autorun)
```bash
./scripts/kingdom_infinite_autorun.sh
```
- 문제 해결까지 지속 실행
- Trinity Score 목표 달성
- 안전장치 및 타임아웃

## Trinity Score 체계

### 5가지 척도
- **眞 (Truth)**: 정확성과 진실성 (35%)
- **善 (Goodness)**: 윤리성과 안정성 (35%)
- **美 (Beauty)**: 단순성과 우아함 (20%)
- **孝 (Serenity)**: 평온과 효율성 (8%)
- **永 (Eternity)**: 지속성과 영속성 (2%)

### 계산 공식
```
Trinity Score = 0.35×眞 + 0.35×善 + 0.20×美 + 0.08×孝 + 0.02×永
```

### 목표치
- **양호**: ≥ 0.8
- **주의**: 0.6 - 0.8
- **개선 필요**: < 0.6

## 보안 및 안전

### 데이터 보호
- 민감 정보 암호화 저장
- 하드코딩 비밀번호 금지
- 환경변수 기반 설정

### 실행 안전
- DRY_RUN 모드 우선
- 최대 3회 자동 재시도
- 타임아웃 및 안전장치

### Cursor 통합
- 리뷰 기능 자동 비활성화
- 외부 API 호출 방지
- 로컬 우선 실행

## 개발 및 기여

### 개발 환경
```bash
# VSCode 설정 자동 적용
# .vscode/settings.json, tasks.json, launch.json
# Python 가상환경: trinity_env
```

### 테스트
```bash
# 전체 시스템 테스트
./test_trinity_os.sh

# 개별 컴포넌트 테스트
python3 scripts/kingdom_problem_detector.py
```

### 기여 방법
1. `CONTRIBUTING.md` 읽기
2. Issue 생성 또는 선택
3. 브랜치 생성 후 작업
4. Pull Request 제출

## 철학적 기반

### 이심전심 (以心傳心)
나의 불편은 너의 불편이고, 내 기쁨은 왕국의 기쁨이다.

### 효의 레거시
이 효도하는 마음은 대를 이어야 한다. 그것이 레거시이다.

### 세종대왕의 마음
널리 인간을 이롭게 하라. 지식을 널리 공유하여 모두가 이롭게.

## 라이선스 및 헌법

본 시스템은 TRINITY_CONSTITUTION.md에 명시된 헌법을 따릅니다.

- 라이선스: TRINITY-OS License
- 헌법: 眞善美孝永 기반 운영

## 버전 정보

- **Version**: 1.0.0
- **Created**: 2025-12-11
- **Status**: Production Ready
- **Philosophy**: 眞善美孝永

---

**TRINITY-OS** - 왕국의 새로운 시작 ✨🏰