# 🎫 TICKET-MIPROv2-EXECUTION: MIPROv2 실행 재점화 및 성능 검증

**우선순위**: HIGH
**상태**: READY (실행 준비 완료)
**담당**: 연구팀
**의존성**: TICKET-005 (MIPROv2 구현 완료), TICKET-SSOT-TEMPLATE (증거 수집 표준화)
**예상 소요시간**: 2시간
**완료도 목표**: 100% (실행 + 성능 검증)

## 🎯 목표 (Goal)

**SSOT LOCKED 기반 MIPROv2 실전 실행 재점화**
35배 효율 달성 + Trinity Score 87.3+ 검증

## 📋 작업 내용

### 1. Docker 환경 검증 (Step 1)
```bash
# Docker 이미지 상태 확인
docker image inspect afo-mipro:latest
docker images | grep afo-mipro

# Docker daemon 상태 확인
docker info
docker ps
```

### 2. 컨테이너 실행 테스트 (Step 2)
```bash
# 격리 환경 컨테이너 실행
docker run --rm -it afo-mipro:latest /bin/bash

# Python 환경 검증
python --version
python -c "import dspy; print('DSPy OK')"

# 패키지 설치 확인
python -m pip freeze | grep -E "(dspy|optuna|torch)"
```

### 3. TrinityAwareMIPROv2 compile 실행 (Step 3)
```python
# MIPROv2 기본 테스트
import dspy
from dspy.teleprompt import MIPROv2
from packages.afo_core.afo.dspy.trinity_mipro_v2 import TrinityAwareMIPROv2

# 기본 DSPy 설정
lm = dspy.DummyLM()  # 테스트용
dspy.configure(lm=lm)

# TrinityAwareMIPROv2 인스턴스 생성
teleprompter = TrinityAwareMIPROv2()

# 샘플 프로그램 생성
class BasicQA(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.generate(question=question)

# compile 실행 (샘플 데이터)
program = BasicQA()
trainset = [
    dspy.Example(question="What is 2+2?", answer="4").with_inputs("question")
]
compiled_program = teleprompter.compile(program, trainset=trainset)
```

### 4. Optuna TPE 최적화 적용 (Step 4)
```python
# Optuna TPE sampler 적용
import optuna

# MIPROv2에 TPE 적용
teleprompter_tpe = MIPROv2(sampler=optuna.samplers.TPESampler())
optimized_program = teleprompter_tpe.compile(program, trainset=trainset, max_bootstrapped_demos=3)
```

### 5. 멀티모달 MIPROv2 테스트 (Step 5)
```python
# base64 이미지 + Q&A 테스트
from packages.afo_core.afo.dspy.trinity_mipro_v2 import TrinityAwareMIPROv2

# 멀티모달 데이터 예시
multimodal_data = [
    dspy.Example(
        question="What do you see in this image?",
        image="base64_encoded_image_data",
        answer="A cat sitting on a chair"
    ).with_inputs("question", "image")
]

# 멀티모달 MIPROv2 적용
teleprompter = TrinityAwareMIPROv2()
multimodal_program = teleprompter.compile(program, trainset=multimodal_data)
```

### 6. Boot-Swap 저장 포맷 구현 (Step 6)
```python
# Trinity Config 형식으로 결과 저장
import json
from datetime import datetime

def save_mipro_result(result, task_name="mipro_v2_test"):
    """MIPROv2 결과를 Trinity Config 형식으로 저장"""

    config = {
        "task": task_name,
        "timestamp": datetime.now().isoformat(),
        "trinity_score": result.get("trinity_score", 0),
        "efficiency_gain": result.get("efficiency_gain", 0),
        "optimized_program": str(result.get("program", {})),
        "metadata": {
            "sampler": "TPE",
            "version": "2.0",
            "environment": "docker"
        }
    }

    # SHA 기반 버전키 생성
    import hashlib
    config_str = json.dumps(config, sort_keys=True)
    sha_key = hashlib.sha256(config_str.encode()).hexdigest()[:16]

    filename = f"artifacts/mipro_result_{task_name}_{sha_key}.json"

    with open(filename, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"MIPROv2 result saved: {filename}")
    return filename
```

## ✅ Acceptance Criteria

- [ ] Docker 이미지 상태 확인 (afo-mipro:latest 검증)
- [ ] 컨테이너 실행 테스트 (격리 환경 MIPROv2 테스트)
- [ ] TrinityAwareMIPROv2 compile 실행 (Optuna TPE 적용)
- [ ] 멀티모달 MIPROv2 테스트 (base64 이미지 + Q&A)
- [ ] Boot-Swap 저장 포맷 구현 (Trinity Config 연동)
- [ ] 최종 성능 검증 (35배 효율 + Trinity Score 87.3+)

## ⚠️ 실행 제한 사항 (SSOT 기반)

### 환경 Timeout 현상 재확인
- **SSOT evidence**: artifacts/ssot_timeout_pack_20260101_174221.log
- **sleep 35 OK**: 글로벌 30초 kill 없음
- **DSPy import 1.608s OK**: 빠른 import (timeout 문제 없음)
- **Docker runtime OK**: 22개 컨테이너 정상 실행

### 현재 실행 가능성
- **컨테이너 격리**: timeout 제한 없이 MIPROv2 실행 가능
- **DSPy 정상**: 1.608초 빠른 import로 최적화 루프 가능
- **환경 준비**: venv + Docker 모두 SSOT verified

## 📊 Trinity Score 영향

**현재 기준점**: 78.3 (MIPROv2 구현 완료)
**예상 상승분**: +9 (실행 검증 + 성능 달성)

*실행 성공 시 Trinity Score 목표: 87.3+*

## 📝 구현 파일 현황

**Verified (SSOT):**
* `packages/afo-core/afo/dspy/trinity_mipro_v2.py` (TrinityAwareMIPROv2)
* `packages/afo-core/afo/custom_bo_gp.py` (GP+EI BO)
* `Dockerfile.mipro` (컨테이너 환경)
* `.venv-dspy/` (격리 Python 환경)
* `artifacts/ssot_timeout_pack_20260101_174221.log` (SSOT 증거)

## 🔍 SSOT 기반 최종 평가

**코드 완성도**: ✅ 100% LOCKED
**환경 준비도**: ✅ 100% LOCKED
**실행 준비도**: ✅ 100% LOCKED
**SSOT 정확도**: ✅ 100% LOCKED

## 📋 실행 순서 및 체크포인트

### Phase 1: 환경 검증 (10분)
- [ ] Docker 이미지 inspect
- [ ] 컨테이너 bash 실행
- [ ] Python 환경 확인
- [ ] DSPy import 테스트

### Phase 2: MIPROv2 기본 실행 (20분)
- [ ] TrinityAwareMIPROv2 import
- [ ] 기본 compile 테스트
- [ ] Optuna TPE 적용
- [ ] 성능 측정

### Phase 3: 고급 기능 테스트 (20분)
- [ ] 멀티모달 데이터 테스트
- [ ] Boot-Swap 저장 구현
- [ ] Trinity Score 계산

### Phase 4: 최종 검증 (10분)
- [ ] 35배 효율 달성 확인
- [ ] Trinity Score 87.3+ 검증
- [ ] 결과 artifacts/ 저장

## 🎯 성공 기준

### 기능적 성공
- TrinityAwareMIPROv2 compile 성공
- Optuna TPE 최적화 적용 성공
- 멀티모달 데이터 처리 성공

### 성능적 성공
- 35배 효율 달성 (baseline vs optimized 비교)
- Trinity Score 87.3+ 달성
- Boot-Swap 저장 성공

### SSOT 성공
- 모든 실행 로그 artifacts/ 저장
- Trinity Score 측정 결과 기록
- 재현 가능한 실행 환경 확보

---

**MIPROv2 Execution Re-ignition - AFO Kingdom**
