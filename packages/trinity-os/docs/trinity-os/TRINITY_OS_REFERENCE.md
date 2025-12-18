# TRINITY-OS API 레퍼런스

## Python API

### TrinityOS 클래스

```python
from run_trinity_os import TrinityOS

# 초기화
trinity = TrinityOS()

# 문제 감지
result = trinity.run_problem_detector()
# 반환: {'total_problems': int, 'summary': dict}

# 건강 리포트
result = trinity.run_health_report()
# 반환: {'overall_score': float, 'balanced': bool}

# 정신 통합
result = trinity.run_spirit_integration()
# 반환: {'constitution_status': dict}

# 통합 자동화
result = trinity.run_unified_autorun()
# 반환: str (실행 로그)

# 검증 실행
result = trinity.run_verification()
# 반환: str (검증 결과)

# 끝까지 실행
result = trinity.run_infinite_autorun()
# 반환: str (실행 로그)

# 시스템 테스트
result = trinity.run_system_test()
# 반환: str (테스트 결과)

# 초기화
result = trinity.run_initialization()
# 반환: str (초기화 로그)
```

### 유틸리티 함수들

```python
# 사용 가능한 명령어 목록
commands = trinity.get_available_commands()
# 반환: {'1': '문제 감지...', '2': '건강 리포트...'}

# 시스템 상태 조회
status = trinity.get_system_status()
# 반환: {'philosophy': dict, 'health_score': float, 'status': str}
```

## Bash API

### 메인 인터페이스

```bash
# 인터랙티브 모드
./run_trinity_os.sh

# 직접 실행 옵션들
./run_trinity_os.sh --detect      # 문제 감지
./run_trinity_os.sh --health      # 건강 리포트
./run_trinity_os.sh --spirit      # 정신 통합
./run_trinity_os.sh --unified     # 통합 자동화
./run_trinity_os.sh --verify      # 검증 실행
./run_trinity_os.sh --infinite    # 끝까지 실행
./run_trinity_os.sh --test        # 시스템 테스트
./run_trinity_os.sh --init        # 초기화
```

### 단축 명령어

```bash
# TRINITY-OS 명령어들
./TRINITY-OS detect    # 문제 감지
./TRINITY-OS health    # 건강 리포트
./TRINITY-OS spirit    # 정신 통합
./TRINITY-OS unified   # 통합 자동화
./TRINITY-OS verify    # 검증 실행
./TRINITY-OS infinite  # 끝까지 실행
./TRINITY-OS test      # 시스템 테스트
./TRINITY-OS init      # 초기화
./TRINITY-OS help      # 도움말
```

## REST API (향후 지원)

### 엔드포인트

```
GET  /api/v1/health          # 시스템 건강 상태
GET  /api/v1/problems        # 문제 목록
POST /api/v1/detect          # 문제 감지 실행
POST /api/v1/recover         # 자동 복구 실행
POST /api/v1/automate        # 자동화 실행
GET  /api/v1/trinity-score   # Trinity Score 조회
```

### 응답 형식

```json
{
  "status": "success|error",
  "data": {},
  "message": "string",
  "timestamp": "ISO8601"
}
```

## 설정 API

### 환경변수

```bash
# Python 경로
export PYTHONPATH=/path/to/trinity-os

# 환경 설정
export TRINITY_ENV=production|development

# 로깅
export LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
export LOG_FILE=trinity_os.log

# 모니터링
export HEALTH_CHECK_INTERVAL=60
export PROBLEM_SCAN_INTERVAL=300
```

### 설정 파일

#### .vscode/settings.json
```json
{
  "cursor.codeReview.enabled": false,
  "python.defaultInterpreterPath": "${workspaceFolder}/trinity_env/bin/python",
  "editor.formatOnSave": false
}
```

#### .cursor/environment.json
```json
{
  "agentCanUpdateSnapshot": true,
  "codeReview": {
    "enabled": false,
    "autoReview": false
  }
}
```

## 확장 API

### 플러그인 인터페이스

```python
# 플러그인 기본 구조
class TrinityPlugin:
    def __init__(self, trinity_os):
        self.trinity = trinity_os

    def execute(self, params: dict) -> dict:
        """플러그인 실행 로직"""
        raise NotImplementedError

    def get_info(self) -> dict:
        """플러그인 정보"""
        return {
            'name': 'plugin_name',
            'version': '1.0.0',
            'description': 'Plugin description'
        }
```

### 이벤트 시스템

```python
# 이벤트 리스너 등록
trinity.on('problem_detected', lambda data: print(f"Problem: {data}"))
trinity.on('health_changed', lambda score: print(f"Score: {score}"))
trinity.on('automation_complete', lambda result: print(f"Done: {result}"))
```

## 데이터 형식

### 문제 감지 결과

```json
{
  "total_problems": 2,
  "critical_problems": 0,
  "summary": {
    "critical": 0,
    "high": 0,
    "medium": 2,
    "low": 0
  },
  "problems": [
    {
      "id": "PROB_001",
      "type": "performance",
      "severity": "medium",
      "description": "High CPU usage detected",
      "solution": "Optimize CPU intensive operations",
      "timestamp": "2025-12-11T10:30:00Z"
    }
  ],
  "recommendation": "💡 개선 권장: Medium 문제 2개 중기 개선 권장"
}
```

### 건강 리포트 결과

```json
{
  "overall_score": 0.95,
  "balance_gap": 0.05,
  "balanced": true,
  "recommendation": "✅ 양호: 시스템 상태 우수",
  "timestamp": "2025-12-11T10:30:00Z",
  "components": {
    "truth": 0.98,
    "goodness": 0.96,
    "beauty": 0.92,
    "serenity": 0.95,
    "eternity": 0.97
  }
}
```

### Trinity Score 계산

```python
def calculate_trinity_score(metrics: dict) -> dict:
    """
    Trinity Score 계산

    Args:
        metrics: 각 척도의 점수 (0.0-1.0)

    Returns:
        계산된 점수와 평가
    """
    weights = {
        'truth': 0.35,
        'goodness': 0.35,
        'beauty': 0.20,
        'serenity': 0.08,
        'eternity': 0.02
    }

    score = sum(metrics.get(k, 0) * v for k, v in weights.items())

    # 평가 기준
    if score >= 0.95:
        grade = "완벽"
        status = "perfect"
    elif score >= 0.90:
        grade = "우수"
        status = "excellent"
    elif score >= 0.80:
        grade = "양호"
        status = "good"
    elif score >= 0.70:
        grade = "보통"
        status = "fair"
    else:
        grade = "개선 필요"
        status = "needs_improvement"

    return {
        'score': score,
        'grade': grade,
        'status': status,
        'components': metrics
    }
```

## 오류 처리

### 표준 오류 코드

```python
ERROR_CODES = {
    'SUCCESS': 0,
    'GENERAL_ERROR': 1,
    'CONFIG_ERROR': 2,
    'NETWORK_ERROR': 3,
    'PERMISSION_ERROR': 4,
    'VALIDATION_ERROR': 5,
    'TIMEOUT_ERROR': 6,
    'DEPENDENCY_ERROR': 7
}
```

### 오류 응답 형식

```json
{
  "status": "error",
  "error_code": 1,
  "message": "General system error",
  "details": "Additional error information",
  "timestamp": "2025-12-11T10:30:00Z"
}
```

## 성능 사양

### 권장 사양
- **CPU**: 1 core 이상
- **RAM**: 512MB 이상
- **Storage**: 100MB 이상
- **Network**: 1Mbps 이상

### 성능 지표
- **부팅 시간**: < 5초
- **문제 감지**: < 10초
- **건강 평가**: < 3초
- **메모리 사용**: < 200MB
- **CPU 사용**: < 20%

---

**TRINITY-OS API 레퍼런스**  
**완전한 프로그래밍 인터페이스 가이드**  
**眞善美孝永** ✨