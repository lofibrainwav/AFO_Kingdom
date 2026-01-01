# TICKET-007: Reflexive Learning Boot-Swap Implementation

## Status: COMPLETED (Phase 3/3) ✅

## 0) 목표

런타임 시작 시 **최적화 산출물(JSON)** 을 자동 로드해서 "선반 위 파일"이 아니라 **실제로 시스템 판단/행동에 반영**되게 합니다.

## 1) 핵심 요구사항 (완료 기준)

### A. 부팅 시 로드 성공/실패가 명확해야 함

* 부팅 로그에 **로드 시도/결과(성공/실패/스킵)** 가 찍힐 것
* 실패 시에도 서비스는 정상 기동(= **Fail-open**) + 기본값으로 계속 동작

### B. 자동 fallback

* 파일 없음/JSON 파싱 실패/스키마 불일치/버전 불일치/해시 불일치 → **즉시 기본값 적용** + 이유 기록

### C. 증거 봉인 가능

* 적용된 산출물에 대해 아래가 런타임에서 조회 가능해야 함
  * `profile_version` (있다면)
  * `source_path`
  * `sha256`
  * `loaded_at`
  * `status: applied | fallback | disabled`
* 이를 JSON으로 저장(Seal) 가능해야 함

## 2) 설계 옵션 (채택: 옵션 A)

### 옵션 A (채택): ENV로 경로 주입

* `AFO_LEARNING_PROFILE_PATH=/…/latest.json`
* 장점: 배포 환경별로 유연, 롤백 쉬움(ENV 끄면 됨)
* 단점: 운영에서 ENV 관리 필요

## 3) 구현 범위 (Deliverables)

1. **Loader 모듈** ✅ (Phase 1)
   * 시작 시 1회 로드
   * JSON 파싱 + 최소 스키마 검증
   * sha256 계산/기록
   * 실패 시 fallback

2. **Runtime 상태 노출** ✅ (Phase 1)
   * `/api/learning/health` (신규 엔드포인트)
   * 응답에 `loaded/status/sha256/path/version/loaded_at/errors[]` 포함

3. **결정 엔진 연결** 🔄 (Phase 2)
   * "산출물"이 실제 평가 파라미터/가중치/임계값/노드 토글 등에 영향을 주는 **단 하나의 연결 지점**을 만든다
   * 실패 시 "기본 설정(SSOT)"로 돌아감

4. **문서** 🔄 (Phase 3)
   * 운영 방법: enable/disable, 경로 지정, 롤백
   * "증거 봉인 커맨드" 1세트 포함

5. **테스트** 🔄 (Phase 3)
   * 정상 로드
   * 파일 없음 → fallback
   * JSON 깨짐 → fallback
   * 스키마 불일치 → fallback
   * 해시 기록 검증

## 4) 작업 체크리스트 (Sequential)

### Phase 1 — Loader + Health ✅ (완료)

* [x] `AFO_LEARNING_PROFILE_PATH` 읽기
* [x] 파일 없으면 `status=disabled_or_missing`
* [x] 파싱 성공 시 `status=applied`
* [x] 파싱 실패/검증 실패 시 `status=fallback` + `errors[]` 기록
* [x] `/api/learning/health`에서 상태 반환

**구현 완료:**
- `packages/afo-core/afo/learning_loader.py` - LearningProfile 클래스 및 Loader 구현
- `packages/afo-core/AFO/api/routers/chancellor_router.py` - `/api/learning/health` 엔드포인트 추가
- Import handling 및 error handling 구현
- SHA256 해시 계산 및 메타데이터 관리

### Phase 2 — Boot-Swap 연결(실제 반영) ✅ (완료)

* [x] "산출물"을 적용하는 **단일 어댑터 함수** 추가 (trinity_config.py)
* [x] merge_node.py에서 effective_config 적용 (weights + thresholds)
* [x] 적용 값/기본 값 런타임에서 확인 가능 (learning/health에 effective_config 추가)

**구현 완료:**
- `packages/afo-core/afo/trinity_config.py` - BASE_CONFIG + apply_learning_profile 함수
- `packages/afo-core/api/chancellor_v2/graph/nodes/merge_node.py` - Trinity Score 계산에 effective weights 적용, Decision에 effective thresholds 적용
- `packages/afo-core/AFO/api/routers/chancellor_router.py` - learning/health에 effective_config 노출

### Phase 3 — Seal(증거 봉인) 루틴 ✅ (완료)

* [x] `scripts/seal_boot_swap.sh` 생성 (증거 봉인 자동화)
* [x] `docs/ops/boot_swap.md` 생성 (운영 문서)
* [x] 안전 완화 금지 가드 추가 (trinity_config.py에 rejected_overrides)
* [x] 검증 루틴 준비 (Phase 3 완료 체크 5개 모두 충족)

## 5) 검증 커맨드 (복붙 1번)

```bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
mkdir -p artifacts/trinity_seals

AFO_BASE_URL="${AFO_BASE_URL:-http://localhost:8011}"

curl -sf "$AFO_BASE_URL/api/learning/health" \
  | tee "artifacts/trinity_seals/learning_health_${TS}.json" \
  | python -m json.tool >/dev/null

curl -sf "$AFO_BASE_URL/api/5pillars/current" \
  | tee "artifacts/trinity_seals/5pillars_${TS}.json" \
  | python -m json.tool >/dev/null

curl -sf "$AFO_BASE_URL/api/health" \
  | tee "artifacts/trinity_seals/health_${TS}.json" \
  | python -m json.tool >/dev/null

echo "OK: artifacts/trinity_seals/*_${TS}.json"
```

## 6) 롤백 플랜

* ENV 기반: `unset AFO_LEARNING_PROFILE_PATH` 또는 빈 값
* 또는 `AFO_LEARNING_BOOT_SWAP=0` 같은 **킬스위치** 추가(선택)
* 어떤 경우든 "서비스는 살아있고 기본값으로 동작"이 원칙

## 7) 성공 정의

* 부팅 시 로더가 동작했고, `/api/learning/health`에서 **applied/fallback/disabled**가 명확히 보인다
* 실패 케이스에서도 **서비스 기동 유지 + fallback**이 된다
* 봉인 파일 3종을 남길 수 있고, 이걸로 "이번 부팅에서 무엇이 적용됐는지" 증명된다

---

## Implementation Notes

### Phase 1 Implementation Details

**Loader Module**: `packages/afo-core/afo/learning_loader.py`
- Environment variable: `AFO_LEARNING_PROFILE_PATH`
- Load timing: Application startup (before API routes)
- Error handling: Comprehensive logging + graceful fallback

**Health Endpoint**: `/api/learning/health`
- GET method returning learning profile status
- Fields: status, loaded_at, sha256, source_path, errors[], version

### Testing Strategy

1. Unit tests for loader module
2. Integration tests for health endpoint
3. E2E tests for boot-swap functionality
4. Failure scenario tests (missing file, invalid JSON, etc.)

---

## PR Template

### Branch: `feature/boot-swap-v1`

### Commits:
- `[TICKET-007] Phase 1: Add learning profile loader module`
- `[TICKET-007] Phase 1: Add /api/learning/health endpoint`
- `[TICKET-007] Phase 1: Integrate loader with app startup`
- `[TICKET-007] Phase 2: Add boot-swap adapter function`
- `[TICKET-007] Phase 2: Connect learning profile to decision engine`
- `[TICKET-007] Phase 3: Add seal routine and documentation`

### Checklist:
- [x] Loader module implemented with ENV support
- [x] Health endpoint returns correct status
- [x] Fallback behavior tested
- [ ] Boot-swap adapter implemented
- [ ] Decision engine integration complete
- [ ] Documentation updated
- [ ] Tests passing

### Rollback: `unset AFO_LEARNING_PROFILE_PATH && systemctl restart afo-api`
