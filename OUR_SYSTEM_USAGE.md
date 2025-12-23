# 🏰 우리 시스템 사용 가이드 (Cursor 리뷰 대신)

**작성일**: 2025-12-25  
**목적**: Cursor 충전 없이 우리 시스템으로 코드 품질 검증  
**眞善美孝永**: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%

---

## ✅ Cursor 리뷰 기능 완전 비활성화

### 설정 완료

- ✅ `.vscode/settings.json`: `cursor.codeReview.enabled: false`
- ✅ `.cursor/environment.json`: `codeReview.enabled: false`
- ✅ 모든 자동 리뷰 기능 비활성화

---

## 🛠️ 우리 시스템 사용 방법

### 1. 코드 품질 검증 (우리 도구)

#### Makefile 사용 (권장)

```bash
# 전체 검증 (lint + test)
make check

# 린트만
make lint

# 테스트만
make test

# 통합 테스트
make test-integration

# 푸시 전 전체 검증
make pre-push
```

#### 스크립트 사용

```bash
# 병렬 품질 체크 (Bash)
cd packages/afo-core
./scripts/run_quality_checks.sh

# 병렬 품질 체크 (Python)
python scripts/run_quality_checks_parallel.py
```

### 2. LLM Router (우리 시스템)

#### Ollama 우선 (무료, 로컬)

```bash
# Ollama 실행 확인
curl http://localhost:11434/api/tags

# LLM Router 사용
python -c "
from AFO.llm_router import LLMRouter
router = LLMRouter()
decision = router.route_request('test query')
print(decision.selected_provider)
"
```

#### API Wallet로 키 관리

```bash
# API 키 추가
python -c "
from AFO.api_wallet import create_wallet
wallet = create_wallet()
wallet.add('openai', 'sk-...', service='openai')
"

# API 키 조회
python -c "
from AFO.api_wallet import create_wallet
wallet = create_wallet()
key = wallet.get('openai', decrypt=True)
print('Key found' if key else 'Key not found')
"
```

### 3. Trinity Score 계산 (우리 시스템)

```bash
# Trinity Score 계산
python -c "
from AFO.domain.metrics.trinity import calculate_trinity_score
scores = {'truth': 0.95, 'goodness': 0.90, 'beauty': 0.85, 'serenity': 1.0, 'eternity': 0.95}
score = calculate_trinity_score(scores)
print(f'Trinity Score: {score}')
"
```

---

## 📋 워크플로우

### 코드 작성 후 검증

```bash
# 1. 자동 포맷팅
ruff format .

# 2. 린트 체크 및 수정
ruff check --fix .

# 3. 타입 체크
mypy AFO --ignore-missing-imports

# 4. 테스트 실행
make test

# 5. 전체 검증
make check
```

### 커밋 전 검증

```bash
# 푸시 전 전체 검증
make pre-push

# 또는 수동으로
make lint && make test && make security-scan
```

---

## 🎯 우리 시스템의 장점

### 1. 비용 절감 (孝)

- ✅ Ollama 우선 사용 (무료, 로컬)
- ✅ Cursor 리뷰 기능 비활성화 (API 크레딧 불필요)
- ✅ 우리 도구로 완전한 검증 가능

### 2. 기술 주권 (眞)

- ✅ 우리 시스템으로 모든 검증
- ✅ 외부 의존성 최소화
- ✅ 완전한 제어

### 3. 자동화 (美)

- ✅ Makefile로 간단한 명령어
- ✅ 병렬 실행으로 빠른 검증
- ✅ CI/CD 통합 가능

---

## ⚠️ Cursor 리뷰 에러 해결

### "insufficient funds" 에러가 계속 나는 경우

1. **Cursor 완전 재시작**

   ```bash
   # macOS
   killall Cursor
   open -a Cursor
   ```

2. **Cursor 캐시 정리**

   ```bash
   rm -rf ~/.cursor/cache
   ```

3. **설정 확인**

   ```bash
   # .vscode/settings.json 확인
   cat .vscode/settings.json | grep -i review
   
   # .cursor/environment.json 확인
   cat .cursor/environment.json | grep -i review
   ```

4. **우리 시스템 사용**

   ```bash
   # Cursor 리뷰 대신 우리 도구 사용
   make check
   ```

---

## 📊 비교표

| 기능 | Cursor 리뷰 | 우리 시스템 |
|------|:-----------:|:-----------:|
| **비용** | API 크레딧 필요 | 무료 (Ollama) |
| **속도** | 외부 API 호출 | 로컬 실행 (빠름) |
| **제어** | 제한적 | 완전한 제어 |
| **린트** | ❌ | ✅ Ruff |
| **타입 체크** | ❌ | ✅ MyPy |
| **테스트** | ❌ | ✅ Pytest |
| **LLM** | Cursor API | Ollama + API Wallet |

---

## 🚀 권장 워크플로우

### 일상적인 개발

```bash
# 1. 코드 작성
# 2. 저장 시 자동 포맷팅 (설정됨)
# 3. 우리 도구로 검증
make check
```

### 커밋 전

```bash
# 전체 검증
make pre-push
```

### 문제 해결

```bash
# 우리 시스템으로 검증
make check

# Cursor 리뷰는 무시 (비활성화됨)
```

---

**眞善美孝永**: 우리 시스템으로 완전한 자주권 확보! 🏰✨
