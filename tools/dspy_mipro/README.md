# DSPy MIPROv2 격리 환경

AFO 왕국 DSPy MIPROv2를 메인 프로젝트와 격리하여 안전하게 사용하는 환경입니다.

## 설치 및 사용법

### 1. 격리 환경 설치
```bash
cd tools/dspy_mipro
poetry install
```

### 2. DSPy MIPROv2 사용
```bash
# 격리 환경에서 실행
poetry run python -c "
import dspy
from dspy.teleprompt import MIPROv2
print('DSPy 버전:', dspy.__version__)
print('MIPROv2 import 성공')
"
```

### 3. AFO 왕국 통합
격리 환경에서 최적화된 결과를 메인 프로젝트의 `packages/afo-core/afo/dspy_optimizer.py`로 가져옵니다.

## 목적

- 메인 프로젝트의 의존성 충돌 방지
- DSPy MIPROv2 안전한 실험 환경 제공
- 프로덕션 GO LIVE에 영향 없음

## Trinity Score 통합

MIPROv2 최적화 결과는 Trinity Score 기반 메트릭으로 평가됩니다:

```python
from afo.dspy_optimizer import AFOMIPROv2

optimizer = AFOMIPROv2(trinity_score=87.3)
optimized_rag = optimizer.compile(rag_module, trainset=trainset)
