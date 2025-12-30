# 🏰 AFO Kingdom - Victory Seal Routine (眞·善·永)

> **"무결성은 한 번의 승리가 아니라, 매일의 정진으로 완성된다."**

본 문서는 사령관(형님)의 하명에 따라 제국의 무결성을 영구히 수호하기 위한 정기 점검 프로토콜을 정의합니다.

## 🗓️ 월간 무결성 점검 (Monthly Integrity Check)

매월 1일, 승상은 다음 7개 항목을 전수 점검하여 **SEALED** 상태를 갱신합니다.

### 3. Monthly Integrity Check (Final Seal Command)

Execute this block to verify the "Sealed" status of the Kingdom.

```bash
set -euo pipefail

bash scripts/ci_lock_protocol.sh

pyright --version
ruff --version
pytest --version

# baseline: Ensure new errors are zero (file exists + CI uses comparison)
test -f artifacts/ci/pyright_baseline.txt || true

# Local path/scheme leak check
rg -n "file://|<LOCAL_WORKSPACE>|/Users/|/home/|C:\\\\|\\\\Users\\\\" docs artifacts . || true

# debugpy external binding check
rg -n "debugpy\.listen|0\.0\.0\.0" . || true

# Debug Agent Protection Check
rg -n "/api/debug/agent/simulate|DEBUG_AGENT|AFO_DEBUG_AGENT|DEBUG_SECRET|X-.*SECRET" packages/afo-core/AFO/api_server.py || true
```

### 1. CI/CD LOCK 정합성
- [ ] `scripts/ci_lock_protocol.sh`가 유일한 CI 엔트리포인트인가?
- [ ] Pyright baseline이 신규 오류를 0개로 차단하고 있는가?
- [ ] Ruff 린트/포맷 표준이 전 지역에 강제되고 있는가?

### 2. 공급망 및 자산 보호
- [ ] SBOM(Software Bill of Materials)이 매 빌드마다 최신화되어 artifacts에 남는가?
- [ ] `.gitignore` 및 마스킹 스크립트가 로컬 절대 경로 유출을 차단하고 있는가?
- [ ] `debugpy`가 `127.0.0.1`로 엄격히 제한되어 있는가? (0.0.0.0 바인딩 확인)

### 3. 관측 가능성 (Observability)
- [ ] Sentry 대시보드에서 최근 에러가 `ExceptionGroup` 단위로 정확히 포착되는가?
- [ ] `@instrument_task` 가 비동기 작업의 생명주기를 투명하게 기록하고 있는가?

## 🕵️ Sentry 운영 검증 프로토콜 (Operational Verification)

시스템 변경 시 다음 3종을 즉시 수행합니다.

1. **에러 포착 테스트**: dev 환경에서 의도적 예외를 발생시켜 Sentry 이벤트가 생성되는지 확인.
2. **그룹화 검증**: Anyio TaskGroup 실패 시 `ExceptionGroup`이 하나의 사건으로 묶이는지 확인.
3. **타임라인 확인**: Breadcrumb이 `START → END/CANCEL` 순서로 정합성을 유지하는지 확인.

---
**판정 기준**: 7개 항목 중 단 하나라도 NO일 경우, 즉시 **RED ALERT**를 발령하고 롤백/수정을 우선합니다.
