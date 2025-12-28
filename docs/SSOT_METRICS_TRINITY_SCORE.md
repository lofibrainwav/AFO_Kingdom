# SSOT — Trinity Score Metric Consistency (afo_trinity_score_total)

## 목적
Trinity Score의 "값(런타임)"과 "정의/세팅(소스)"이 흔들리지 않도록, CI에서 다음을 검증합니다.

1) Runtime Consistency
- `/health` JSON에서 Trinity Score를 읽고
- `/metrics`에서 `afo_trinity_score_total` 값을 읽어
- 두 값이 `EPS` 이내인지 확인합니다.

2) Source Consistency (active python only)
- Git tracked `*.py` 파일에서만 검색하며
- 경로 중간을 포함해 `docs/`, `legacy/`, `tests/`가 들어간 파일은 제외합니다.
- 아래 패턴이 "활성 코드"에서 각각 정확히 1회인지 확인합니다.
  - create: `get_or_create_metric(... afo_trinity_score_total ...)`
  - set: `trinity_score_total.set(`

## 전제(Prereqs)
- `bash`, `git`, `curl`, `python3`, `grep`, `sed`, `wc`, `tr`

## /health에서 읽는 키
스크립트는 아래 중 하나를 지원합니다.
- `{"trinity_score": 0.9}`
- `{"trinity": {"trinity_score": 0.9}}`

둘 다 없으면 FAIL 입니다.

## 환경변수
- `AFO_BASE_URL` (default: `http://localhost:8010`)
- `TRINITY_EPSILON` (default: `0.0001`)
- `AFO_TRINITY_METRIC_NAME` (default: `afo_trinity_score_total`)
- `AFO_REQUIRE_TRINITY_METRIC` (default: `0`)
  - `1`이면 `/metrics`에 메트릭이 없을 때 FAIL
  - `0`이면 메트릭이 없을 때 runtime 비교는 건너뛰고(경고 출력) PASS 가능

## 왜 "registry 공유"가 중요할 수 있나
Prometheus Python client는 Registry(수집기 집합)에 메트릭을 등록하고, `/metrics`는 Registry를 export합니다.
따라서 메트릭이 "어느 registry에 등록되었는지"와 "어느 registry를 export하는지"가 다르면
/health에서 계산이 되더라도 /metrics에는 보이지 않을 수 있습니다.

(해결 예시는 아래 "FastAPI /metrics 노출" 섹션 참고)

## FastAPI /metrics 노출 (권장)
Prometheus Python client의 ASGI helper로 `/metrics`를 마운트합니다.

- `from prometheus_client import make_asgi_app`
- `app.mount("/metrics", make_asgi_app())`

필요하면 `make_asgi_app(registry=...)`로 특정 registry를 명시할 수 있습니다.

## 환경 변수
- `AFO_BASE_URL` (기본: `http://localhost:8010`)
- `TRINITY_EPSILON` (기본: `0.0001`)
- `AFO_TRINITY_METRIC_NAME` (기본: `afo_trinity_score_total`)