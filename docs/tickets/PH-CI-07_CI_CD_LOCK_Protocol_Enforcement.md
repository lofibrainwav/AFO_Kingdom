# [PH-CI-07] CI/CD LOCK Protocol Enforcement

> **眞善美孝永** - 제국의 무결성을 수호하는 4대 관문 강제화

## 📋 개요
`LOCK.md`에 명시된 **Pyright → Ruff → pytest → SBOM** 순서의 CI/CD 파이프라인 불변 원칙을 실제 시스템에 강제 적용합니다. 현재 분산되어 있고 순서가 어긋난 검증 절차를 단일 프로토콜로 통합하여 무결성을 달성합니다.

## 🎯 목표
- CI/CD 파이프라인 실행 순서 정정 (**Pyright -> Ruff -> pytest -> SBOM**)
- SBOM 생성 및 보안 스캔 단계 정식 통합
- 로컬과 CI 환경의 검증 로직 일원화 (`scripts/ci_lock_protocol.sh`)

## 🛠️ 작업 내용

### 0. 도구 버전 핀 (永 - Eternity)
제국의 무결성을 유지하기 위해 핵심 도구의 버전을 고정합니다.
- **Pyright**: `1.1.391` (pinned)
- **Ruff**: `0.1.6` (pinned)
- **pytest**: `7.4.3` (pinned)

### 1. 통합 검증 스크립트 작성 (眞/善/美/永)
- **파일**: `scripts/ci_lock_protocol.sh`
- **로컬/CI 일원화**: 모든 보고서는 `artifacts/ci/`에 저장되며, SBOM은 `artifacts/sbom/`에 보관됩니다.
- **Pyright 정책 (Option A: Baseline)**: 
    - 현재의 타입 오류를 **Baseline**으로 인정합니다. (`pyright_baseline.txt`)
    - CI 단계에서는 신규 추가되는 코드에 의한 **Type Regression**을 엄격히 차단합니다.
- **Ruff 정책**: 
    - CI 모드에서는 `--fix` 없이 엄격한 검출만 수행합니다. 
    - 포맷팅(`ruff format --check`) 일관성을 강제합니다.

### 2. Makefile 정렬
- `check` 타겟의 순서를 Pyright → Ruff → pytest → SBOM 순으로 변경
- `sbom` 타겟 추가
- 모든 산출물을 `artifacts/` 하위로 표준화

### 3. CI 워크플로우 업데이트
- `.github/workflows/ci.yml`의 `quality-gate` 잡을 신규 프로토콜 순서에 맞게 재구성

## ✅ 성공 기준
- `bash scripts/ci_lock_protocol.sh` 실행 시 4단계가 순차적으로 통과
- `make check` 실행 시 동일한 순서로 검증 수행
- CI 파이프라인에서 SBOM 산출물이 정상적으로 업로드됨

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: ✅ SEALED (ENFORCED)
