# TICKET-008: Active RAG Production Rollout (Shadow → Flag → Gradual)

## Status: COMPLETED (Phase 4/4) ✅

## 0) 목표

**RAG를 안전하게 프로덕션 응답 파이프라인에 투입한다.**

Boot-Swap으로 "판단 파라미터를 바꾸는 길"이 열렸으니, 이제는 **실제 응답 품질을 높이는 RAG를 투입**하는 단계.

## 1) 핵심 요구사항 (완료 기준)

### A. 위험 0부터 시작 (Shadow Mode)

* **사용자 응답은 기존 그대로 유지**
* 내부에서만 RAG 실행 + 결과/지연/에러를 로그/메트릭으로 기록
* 서비스 안정성에 영향 없음

### B. 제어 가능한 투입 (Flag Mode)

* `X-AFO-RAG: 1` 헤더 또는 `AFO_RAG_ENABLED=1` ENV로 선택적 적용
* 실패 시 자동 fallback (기존 응답 경로)
* 운영자가 언제든 ON/OFF 가능

### C. 점진적 확대 (Gradual Mode)

* `AFO_RAG_ROLLOUT_PERCENT=0..100`로 비율 기반 적용
* A/B 테스팅 가능 + 메트릭 기반 확대
* 0%로 즉시 롤백 가능

### D. 증거 봉인 (Seal)

* RAG 적용 여부/모드/비율/latency/error/결과 요약을 JSON으로 봉인
* "RAG 투입이 성능/품질에 미친 영향"을 데이터로 증명

## 2) 설계 옵션 (채택: 옵션 A)

### 옵션 A (채택): Chancellor Router 확장

* `/chancellor/invoke` 엔드포인트에 RAG 통합
* `X-AFO-RAG` 헤더로 제어
* `AFO_RAG_*` ENV로 설정

## 3) 구현 범위 (Deliverables)

1. **Shadow 모드** ✅ (Phase 1)
   * RAG 실행 + 메트릭 기록 (응답 영향 없음)
   * `packages/afo-core/afo/rag_shadow.py`

2. **Flag 모드** 🔄 (Phase 2)
   * 헤더/ENV 기반 선택적 적용
   * Chancellor Router 확장

3. **Gradual 모드** 🔄 (Phase 3)
   * 비율 기반 라우팅 로직
   * A/B 테스팅 지원

4. **Seal & Docs** 🔄 (Phase 4)
   * `scripts/seal_rag_rollout.sh`
   * `docs/ops/rag_rollout.md`

## 4) 작업 체크리스트 (Sequential)

### Phase 1 — Shadow Mode ✅ (완료)

* [x] `packages/afo-core/afo/rag_shadow.py` 생성 (RAG 실행 + 메트릭 기록)
* [x] Chancellor Router에 shadow 모드 통합 (응답 영향 없음)
* [x] 메트릭: latency, error, result_summary 기록
* [x] `/chancellor/rag/shadow/health` 엔드포인트 추가

**구현 완료:**
- RAG Shadow 모듈: 메트릭 저장소, 비동기 실행, 통계 계산
- Chancellor Router 통합: 모든 invoke 호출 시 shadow 실행 (응답 영향 없음)
- Health 엔드포인트: `/chancellor/rag/shadow/health` - 상태 및 메트릭 조회
- 환경변수 제어: `AFO_RAG_SHADOW_ENABLED=1` (기본 활성화)

### Phase 2 — Flag Mode ✅ (완료)

* [x] `packages/afo/rag_flag.py` 생성 (판단 함수 통일)
* [x] `X-AFO-RAG: 1` 헤더 지원 + `AFO_RAG_FLAG_ENABLED=1` ENV 지원
* [x] 동시성 제한 세마포어 + timeout 강제 + fallback 보장
* [x] Chancellor Router 통합 (`_execute_with_fallback`에 Flag 로직 추가)
* [x] Health 엔드포인트 확장 (Shadow + Flag 통합 상태 조회)

### Phase 3 — Gradual Mode ✅ (완료)

* [x] `determine_rag_mode()` 함수로 우선순위 통합 (kill_switch > header > flag > gradual > shadow)
* [x] `AFO_RAG_ROLLOUT_ENABLED=1` + `AFO_RAG_ROLLOUT_PERCENT=0..100` 지원
* [x] 버킷팅 로직: `sha256(seed) % 100 < percent`로 안정적 결정
* [x] Seed 우선순위: `X-AFO-CLIENT-ID` → `X-Request-ID` → `default_seed`
* [x] 메트릭 확장: `decision_mode`, `rollout_percent`, `bucket_seed`, `bucket_seed_source`

### Phase 4 — Seal & Docs ✅ (완료)

* [x] `scripts/seal_rag_rollout.sh` 생성 (실행 가능 + 타임스탬프 기반 봉인)
* [x] `docs/ops/rag_rollout.md` 생성 (운영 가이드 + 우선순위 + 롤백 절차)
* [x] 첫 봉인 실행 (artifacts/trinity_seals/에 rag_health, health, 5pillars JSON 생성)

## 5) 검증 커맨드 (복붙 1번)

```bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
mkdir -p artifacts/rag_rollout

# Shadow 모드 확인
curl -sf "$AFO_BASE_URL/chancellor/rag/shadow/health"

# Flag 모드 테스트
curl -H "X-AFO-RAG: 1" -X POST "$AFO_BASE_URL/chancellor/invoke" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'

# Gradual 모드 확인 (비율 50%)
export AFO_RAG_ROLLOUT_PERCENT=50
curl -X POST "$AFO_BASE_URL/chancellor/invoke" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'

# Seal 실행
scripts/seal_rag_rollout.sh
```

## 6) 롤백 플랜

* **Shadow**: 항상 OFF (응답 영향 없음)
* **Flag**: `X-AFO-RAG: 0` 또는 `unset AFO_RAG_ENABLED`
* **Gradual**: `AFO_RAG_ROLLOUT_PERCENT=0`
* **완전 롤백**: 위 3개 모두 + 기존 코드로 돌아감

## 7) 성공 정의

* Shadow 모드에서 RAG가 실행되고 메트릭이 기록되지만 사용자 응답은 변함 없음
* Flag 모드에서 선택적으로 RAG 적용 가능 + 실패 시 fallback
* Gradual 모드에서 비율대로 적용 + 메트릭 기반 확대 가능
* Seal로 "RAG 투입 효과"를 데이터로 증명 가능

---

## Implementation Notes

### Phase 1 Shadow Mode Implementation

**Shadow Module**: `packages/afo-core/afo/rag_shadow.py`
```python
async def execute_rag_shadow(query: str) -> dict[str, Any]:
    """RAG 실행 + 메트릭 기록 (응답 영향 없음)"""
    start_time = time.time()
    try:
        # RAG 로직 실행
        result = await rag_pipeline.execute(query)
        latency = time.time() - start_time

        # 메트릭 기록 (로그/메모리)
        metrics = {
            "latency_ms": latency * 1000,
            "success": True,
            "result_summary": summarize_result(result),
            "query_length": len(query)
        }

        return {"status": "success", "metrics": metrics}

    except Exception as e:
        latency = time.time() - start_time
        metrics = {
            "latency_ms": latency * 1000,
            "success": False,
            "error": str(e),
            "query_length": len(query)
        }

        return {"status": "error", "metrics": metrics}
```

**Router Integration**: Chancellor Router에 통합
- 모든 `/chancellor/invoke` 호출 시 shadow 실행
- 응답에는 영향 없음, 메트릭만 기록

### Testing Strategy

1. **Unit Tests**: RAG shadow 모듈 테스트
2. **Integration Tests**: Router 통합 테스트
3. **Load Tests**: 성능 영향 측정
4. **A/B Tests**: 품질 비교 테스트

---

## PR Template

### Branch: `feature/rag-production-rollout-v1`

### Commits:
- `[TICKET-008] Phase 1: Add RAG shadow mode module`
- `[TICKET-008] Phase 1: Integrate shadow mode with Chancellor Router`
- `[TICKET-008] Phase 1: Add shadow health endpoint`
- `[TICKET-008] Phase 2: Add flag mode support (X-AFO-RAG header)`
- `[TICKET-008] Phase 2: Add ENV-based flag control (AFO_RAG_ENABLED)`
- `[TICKET-008] Phase 3: Add gradual rollout with percentage control`
- `[TICKET-008] Phase 3: Add user-based consistent routing for A/B testing`
- `[TICKET-008] Phase 4: Add RAG rollout seal script`
- `[TICKET-008] Phase 4: Add RAG rollout operations documentation`

### Checklist:
- [x] Shadow mode implemented and tested
- [ ] Flag mode header support added
- [ ] Flag mode ENV support added
- [ ] Fallback logic implemented for failures
- [ ] Gradual rollout percentage control added
- [ ] User-based consistent routing implemented
- [ ] Seal script created and tested
- [ ] Operations documentation completed
- [ ] All tests passing

### Rollback: `unset AFO_RAG_* && systemctl restart afo-api`

---

## Phase 1 Implementation Details

**Files Created:**
- `packages/afo-core/afo/rag_shadow.py` - Shadow mode implementation
- Router integration in `packages/afo-core/AFO/api/routers/chancellor_router.py`
- Health endpoint `/chancellor/rag/shadow/health`

**Key Features:**
- Zero-risk shadow execution
- Comprehensive metrics collection
- Async execution with timeout handling
- Error resilience (failures don't affect main response)

**Testing:**
- Unit tests for shadow module
- Integration tests with router
- Performance benchmarks
- Error scenario tests
