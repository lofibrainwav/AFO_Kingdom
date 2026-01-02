# 🔬 SSOT 증거 확보 표준 템플릿

**AFO 왕국 SSOT (Single Source of Truth) 증거 확보 표준 템플릿**

## 🎯 목적

허위 확정 방지, SSOT 정확도 100% LOCKED 보장, 미래 작업 표준화

## 📋 템플릿 구조

### 1. 증거 수집 대상 식별

**환경 상태:**
- Python 버전, venv 상태, 패키지 설치
- 격리 환경 정상성, import 시간

**실행 상태:**
- 명령어 timeout, 실행 결과, exit codes
- faulthandler 스택 덤프, 병목 지점

**시스템 상태:**
- Docker daemon, 컨테이너 상태
- 리소스 사용량, 메모리/CPU

**외부 상태:**
- API 연결, 네트워크 상태
- 외부 서비스 응답 시간

### 2. 증거 수집 스크립트 템플릿

```bash
#!/bin/bash
set -euo pipefail

# 로그 파일 생성
LOG_DIR="artifacts"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/ssot_$(date +%Y%m%d_%H%M%S).log"

# Python 증거 수집 스크립트
.venv-dspy/bin/python - <<'PY' | tee "$LOG_FILE"
import subprocess, time, os, sys

def run(cmd, timeout=40):
    print(f"\n$ {cmd}")
    t0 = time.time()
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        dt = time.time() - t0
        print(f"EXIT={p.returncode} SECONDS={dt:.3f}")
        out = (p.stdout + p.stderr).strip()
        if out:
            print(out[:6000])
        else:
            print("(no output)")
    except subprocess.TimeoutExpired:
        dt = time.time() - t0
        print(f"TIMEOUT SECONDS={dt:.3f}")

print("DATE_START=", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
print("PY_EXEC=", sys.executable)
print("PY_VER =", sys.version)

# [필수] 글로벌 timeout 캡 확인
run("sleep 35; echo SLEEP35_OK", timeout=60)

# [필수] Python 환경 확인
run("python -V; python -c \"import sys; print(sys.executable)\"")

# [선택] venv 환경 확인
run("which python; python -V; python -c \"import sys; print(sys.executable)\"")

# [선택] Docker 환경 확인
run("docker --version", timeout=20)
run("docker info", timeout=15)
run("docker ps", timeout=15)

# [선택] DSPy/torch 등 주요 패키지 import
run("python -c \"import time; t=time.time(); import dspy; print('DSPY_IMPORT_SECONDS', round(time.time()-t, 3))\"", timeout=60)

# [선택] 패키지 설치 확인
run("python -m pip freeze | head -n 60", timeout=30)

print("DATE_END=", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
PY

echo "SSOT_LOG_PATH=$LOG_FILE"
```

### 3. 증거 분석 및 LOCKED 판정 템플릿

#### ✅ LOCKED 가능한 것
- `sleep N OK`: 글로벌 30초 kill 없음
- `venv python OK`: 격리 환경 Python 정상
- `docker CLI OK`: Docker CLI 설치 확인
- `docker runtime OK`: daemon + 컨테이너 정상
- `DSPy import X초 OK`: 빠른 import (timeout 문제 없음)
- `packages installed verified`: pip freeze 정상

#### ❌ LOCKED 불가능한 것
- `external timeout cap verified`: sleep 성공 ≠ 캡 존재 증거
- `packages installed verified`: pip freeze 없음
- `execution environment ready`: 실제 실행 결과 없음

### 4. 티켓 생성 템플릿

```markdown
# 🎫 TICKET-XXX: [작업 제목]

**우선순위**: [HIGH/MEDIUM/LOW]
**상태**: PARTIAL (implementation done, execution blocked; SSOT evidence locked)
**담당**: 연구팀
**의존성**: [TICKET-XXX]
**예상 소요시간**: [X시간]
**완료도**: ~XX% (X/X AC implemented; X/X blocked)

## 🎯 목표 (Goal)

[SSOT 정정]: [핵심 팩트]

## ✅ Acceptance Criteria

- [x] [완료된 항목] (SSOT evidence verified)
- [ ] [보류된 항목] (blocked: [root cause])

## ⚠️ 실행 제한 사항 (SSOT 기반)

### 환경 Timeout 현상
- **[증거 기반 설명]**

### 현재 구현 상태
- **코드 완성도**: ✅ 100% LOCKED
- **환경 준비도**: ✅ 100% LOCKED ([SSOT evidence])
- **실행 검증도**: ❌ 0% LOCKED ([SSOT evidence])

## 📊 Trinity Score 영향

**Trinity Score:** `pending (blocked by execution; cannot measure)`

## 📝 구현 파일 현황

**Verified (SSOT):**
* `[증거 항목]` ([세부 설명])

**Not yet verified (pending SSOT):**
* `[보류 항목]` *(blocked: [root cause])*

## 🔍 SSOT 기반 최종 평가

**코드 완성도**: ✅ 100% LOCKED
**환경 준비도**: ✅ 100% LOCKED ([SSOT evidence])
**실행 검증도**: ❌ 0% LOCKED ([SSOT evidence])
**SSOT 정확도**: ✅ 100% LOCKED
```

## 📋 적용 예시 (MIPROv2 사례)

### 증거 수집 결과
```
DATE_START= 2026-01-01T17:42:21-0800
PY_EXEC= /Users/brnestrm/AFO_Kingdom/.venv-dspy/bin/python
PY_VER = 3.12.12

$ sleep 35; echo SLEEP35_OK
EXIT=0 SECONDS=35.015
SLEEP35_OK

$ python -V; python -c "import sys; print(sys.executable)"
EXIT=0 SECONDS=0.050
Python 3.12.12
/Users/brnestrm/AFO_Kingdom/.venv-dspy/bin/python

$ docker --version
EXIT=0 SECONDS=0.015
Docker version 29.1.3, build f52814d

$ docker info
EXIT=0 SECONDS=0.391
[22개 컨테이너 실행 중]

$ python -c "import time; t=time.time(); import dspy; print('DSPY_IMPORT_SECONDS', round(time.time()-t, 3))"
EXIT=0 SECONDS=1.608
DSPY_IMPORT_SECONDS 1.608

$ python -m pip freeze | head -n 60
EXIT=0 SECONDS=0.199
dspy==3.0.4
optuna==4.6.0
torch==2.5.1
[등등 정상 설치]
```

### LOCKED 판정
- ✅ `sleep 35 OK`: 글로벌 timeout 캡 없음
- ✅ `venv python OK`: 격리 환경 정상
- ✅ `docker CLI/runtime OK`: Docker 환경 정상
- ✅ `DSPy import 1.608s OK`: 빠른 import
- ✅ `packages installed verified`: pip freeze 확인

## 🎯 적용 프로세스

1. **증거 수집 대상 식별** (위 템플릿 1번)
2. **스크립트 실행** (위 템플릿 2번)
3. **증거 분석** (위 템플릿 3번)
4. **티켓 생성** (위 템플릿 4번)
5. **SSOT LOCKED 선언**

## 🔍 SSOT 원칙 준수

- **허위 확정 금지**: "LOCKED"는 원문 로그로만 선언
- **증거 우선**: 추정/주장은 "pending"으로 표기
- **완전성 검증**: 모든 포인트에 대한 증거 확보
- **재현성 보장**: 스크립트로 자동화된 증거 수집

---

**SSOT Evidence Collection Standard Template - AFO Kingdom**
