# [PH-CI-08] Type-Checking Migration (myPy -> Pyright)

> **眞善美孝永** - 제국의 검(mypy)을 마이크로소프트의 예리한 창(Pyright)으로 교체

## 📋 개요
현재 사용 중인 `mypy`는 성숙하지만 대형 프로젝트에서 속도가 느리고 stub 설치 마찰이 큽니다. 이를 2025년 업계 표준인 `Pyright`로 전환하여 타입 추론의 정확성을 높이고 CI 속도를 3~5배 향상시키며, 실시간 IDE 지원(Pylance)을 강화합니다.

## 🎯 목표
- `mypy` 게이트를 `Pyright` 게이트로 전면 교체
- `pyproject.toml` 내 `tool.pyright` 설정 SSOT 구축
- CI/CD LOCK 4대 원칙의 '眞 (Truth)' 관문 고도화
- Ruff와의 완벽한 병행 구조 확립

## 🛠️ 작업 내용

### 1. Pyright 환경 구성
- **설치**: `pyright` (pip wrapper)를 `requirements.txt` 및 `pyproject.toml`에 추가
- **설정**: `pyproject.toml`에 `[tool.pyright]` 섹션 구축 (Standard 모드 시작)
- **Baseline**: 초기 에러를 baseline으로 기록하여 Regression 차단 메커니즘 유지

### 2. CI/CD LOCK 프로토콜 업데이트
- `scripts/ci_lock_protocol.sh` 내 `mypy` 호출을 `pyright`로 변경
- `mypy_baseline.txt`를 `pyright_baseline.txt`로 전환
- `Makefile` 타겟 및 CI 워크플로우(`ci.yml`) 동기화

### 3. Ruff 통합
- Ruff (린팅/포매팅) + Pyright (타입 검증)의 2025 표준 조합 완성

## ✅ 성공 기준
- `bash scripts/ci_lock_protocol.sh` 실행 시 Pyright 게이트가 첫 번째 관문으로 정상 작동
- Pyright 실행 속도가 기존 mypy 대비 유의미하게 향상됨
- 신규 타입 오류 발생 시 LOCK이 정확히 작동하여 배포 차단

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: ✅ SEALED (ENFORCED)
