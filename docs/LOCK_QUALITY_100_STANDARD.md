# LOCK Quality 100% Standard - AFO 왕국 증거 기반 품질 보장

## 개요

LOCK Quality 100%는 AFO 왕국의 모든 시스템이 **어디서든 재현 가능하고**, **증거 기반으로 검증 가능하며**, **영구적으로 안정적**임을 보장하는 표준이다.

## LOCK Quality 100% 조건

모든 왕국 시스템 변경사항은 아래 4가지 조건을 모두 만족해야 한다:

### 1. 증거 재현성 100% (Evidence Reproducibility)
- 모든 artifacts 폴더는 `manifest.rel.sha256`로 검증 가능
- 상대 경로 기반 해시 검증 (다른 머신/환경 무관)
- `scripts/seal_artifacts_rel.sh`로 자동 생성

### 2. 검증 정확성 100% (Verification Accuracy)
- `scripts/verify_hot_swap.py` PASS (DSPy 기능 검증)
- `scripts/verify_active_rag.py` PASS (RAG 기능 검증)
- 검증 스크립트가 실제 시스템 동작과 100% 일치

### 3. 안전성 100% (Safety)
- `DSPY_ENABLED=false`는 항상 safe skip
- 격리 venv는 메인 환경 영향 0%
- DRY_RUN_DEFAULT=true로 운영 안전성 보장

### 4. 재현성 100% (Reproducibility)
- Python 버전, 패키지 버전 동결 (pip freeze)
- manifest.sha256로 환경 재현성 보장
- 격리 venv로 외부 의존성 격리

## LOCK Quality 검증 프로세스

### 1. 증거 생성 시
```bash
# 모든 artifacts 폴더에 rel manifest 자동 생성
./scripts/seal_artifacts_rel.sh artifacts/your_folder/
```

### 2. 검증 실행 시
```bash
# Hot-Swap 검증 (required)
PYTHONPATH=packages/afo-core poetry run python scripts/verify_hot_swap.py

# Active RAG 검증 (required)
PYTHONPATH=packages/afo-core poetry run python scripts/verify_active_rag.py

# 격리 venv 검증 (required)
DSPY_ENABLED=false PYTHONPATH=packages/afo-core poetry run python scripts/dspy_isolated_runner.py
DSPY_ENABLED=true PYTHONPATH=packages/afo-core poetry run python scripts/dspy_isolated_runner.py
```

### 3. CI 통합 (필수)
- GitHub Actions required checks:
  - `verify_hot_swap`
  - `verify_active_rag`
  - `dspy_isolated_runner`

## LOCK Quality 위반 시 조치

### 경고 단계
- manifest.rel.sha256 검증 실패 시 자동 재생성
- 검증 스크립트 단일 실패 시 재실행 권장

### 차단 단계
- 2회 연속 검증 실패 시 PR merge 차단
- 안전성 위반 (DSPY_ENABLED 가드 무시) 시 즉시 롤백

## 관련 파일

- `scripts/seal_artifacts_rel.sh` - 증거 봉인 스크립트
- `scripts/verify_hot_swap.py` - Hot-Swap 기능 검증
- `scripts/verify_active_rag.py` - Active RAG 기능 검증
- `scripts/dspy_isolated_runner.py` - 격리 venv 러너
- `contracts/mipro_job.schema.json` - MIPROv2 JSON I/O 계약

## 버전 히스토리

- v1.0 (2026-01-01): TICKET-001 LOCK 품질 100% 표준 수립
  - manifest.rel.sha256 재현성 보장
  - verify_active_rag 정확성 수정
  - 격리 venv 운영 체계 구축
