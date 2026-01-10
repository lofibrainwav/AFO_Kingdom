# AFO Kingdom 타입 시스템 교육 가이드

## 개요

이 가이드는 AFO Kingdom 프로젝트의 타입 시스템 사용법과 모범 사례를 설명합니다.

## Ⅰ. 기본 타입 힌트

### 1. 변수 타입 힌트

```python
# 좋음: 명시적 타입 힌트
name: str = "Alice"
age: int = 30
scores: list[float] = [85.5, 92.0, 78.5]

# 피해야 할: 암시적 타입 (타입 추론에 의존)
name = "Alice"  # 타입 추론됨
age = 30        # 타입 추론됨
```

### 2. 함수 시그니처

```python
# 좋음: 완전한 타입 힌트
def calculate_score(base_score: float, multiplier: float = 1.0) -> float:
    return base_score * multiplier

# 좋음: 제네릭 함수
from typing import TypeVar
T = TypeVar('T')
def find_item(items: list[T], predicate: Callable[[T], bool]) -> T | None:
    return next((item for item in items if predicate(item)), None)
```

## Ⅱ. 고급 타입 패턴 (Phase 11)

### 1. 제네릭 타입 활용

```python
from packages.afo_core.utils.generic_api import APIResponse, PaginatedResponse

# API 응답 표준화
def get_user(user_id: str) -> APIResponse[dict[str, Any]]:
    user = find_user_by_id(user_id)
    if user:
        return APIResponse(success=True, data=user)
    return APIResponse(success=False, error="User not found")

# 페이지네이션 표준화
def list_users(page: int = 1, limit: int = 20) -> PaginatedResponse[User]:
    users = get_users_from_db(page, limit)
    total = count_total_users()
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=limit,
        has_next=(page * limit) < total,
        has_prev=page > 1
    )
```

### 2. 프로토콜 인터페이스

```python
from packages.afo_core.utils.protocols import IService, IRepository, IValidator

class UserService(IService[User]):
    """사용자 서비스 구현"""

    def __init__(self, repository: IRepository[User, str]):
        self.repository = repository

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.repository.get(user_id)

    async def create(self, user: User) -> User:
        # 검증
        validator = UserValidator()
        result = validator.validate(user)
        if not result.is_valid:
            raise ValueError(f"Invalid user data: {result.errors}")

        return await self.repository.add(user)
```

### 3. 타입 가드 함수

```python
from packages.afo_core.utils.type_guards import (
    is_valid_email, is_positive_int, is_valid_priority, validate_types
)

class TaskService:
    @validate_types(
        title=str,  # is_string
        priority=str,  # is_valid_priority로 검증
        complexity=int  # is_positive_int
    )
    def create_task(self, title: str, priority: str, complexity: int) -> Task:
        # 런타임 타입 검증이 자동으로 수행됨
        if not is_valid_priority(priority):
            raise ValueError(f"Invalid priority: {priority}")

        if not is_positive_int(complexity) or complexity > 10:
            raise ValueError(f"Complexity must be 1-10, got: {complexity}")

        # ... 태스크 생성 로직
```

## Ⅲ. 타입 안전성 모범 사례

### 1. Union 타입 대신 discriminated unions 사용

```python
# 피해야 할: 넓은 Union 타입
def process_result(result: str | int | float | dict | None) -> str:
    if isinstance(result, str):
        return result
    elif isinstance(result, (int, float)):
        return str(result)
    elif isinstance(result, dict):
        return json.dumps(result)
    else:
        return "unknown"

# 좋음: 좁은 타입 사용
from typing import Literal

ResultType = Literal["success", "error", "pending"]

def process_result(result: dict[str, Any]) -> str:
    result_type = result.get("type")
    if result_type == "success":
        return result["message"]
    elif result_type == "error":
        return f"Error: {result['error']}"
    else:
        return "Processing..."
```

### 2. Optional 타입 처리

```python
# 좋음: 명시적 None 처리
def get_user_name(user: dict[str, Any] | None) -> str:
    if user is None:
        return "Anonymous"
    return user.get("name", "Unknown")

# 피해야 할: 암시적 None 처리 (mypy 에러 유발)
def get_user_name_bad(user: dict[str, Any] | None) -> str:
    return user["name"]  # None일 수 있음
```

### 3. 제네릭 제약

```python
from typing import TypeVar

# 기본 제네릭
T = TypeVar('T')

# 제약된 제네릭
NumericType = TypeVar('NumericType', bound=float | int)

def sum_values(values: list[NumericType]) -> NumericType:
    return sum(values)  # 타입 안전하게 합계 계산
```

## Ⅳ. MyPy 에러 패턴과 해결

### 1. attr-defined 에러

```python
# 문제: 속성이 정의되지 않음
class User:
    def __init__(self, name: str):
        self.name = name

user = User("Alice")
print(user.email)  # attr-defined 에러

# 해결: 속성 정의 또는 타입 힌트
class User:
    def __init__(self, name: str):
        self.name = name
        self.email: str | None = None  # 명시적 타입 힌트
```

### 2. assignment 에러

```python
# 문제: 타입 불일치 할당
score: int = "100"  # assignment 에러

# 해결: 올바른 타입 변환
score: int = int("100")
```

### 3. call-overload 에러

```python
# 문제: 함수 호출 시그니처 불일치
def process_data(data: str | int) -> str:
    return str(data)

result = process_data([1, 2, 3])  # call-overload 에러

# 해결: 타입 힌트 수정 또는 변환
def process_data(data: str | int | list) -> str:
    if isinstance(data, list):
        return ",".join(str(x) for x in data)
    return str(data)
```

## Ⅴ. CI/CD 통합

### 1. pre-commit 설정

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--config-file=pyproject.toml]
```

### 2. GitHub Actions

```yaml
# .github/workflows/type-check.yml
name: Type Check
on: [push, pull_request]

jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install mypy
      - run: python scripts/type_audit_automation.py
```

## Ⅵ. 교육 리소스

### 1. 온라인 자료
- [MyPy 공식 문서](https://mypy.readthedocs.io/)
- [Python Typing 모듈](https://docs.python.org/3/library/typing.html)
- [Real Python: Type Hints](https://realpython.com/python-type-checking/)

### 2. 도구
- `mypy --help`: MyPy 명령어 도움말
- `python scripts/type_audit_automation.py`: 자동 감사 실행
- `mypy --show-error-codes`: 에러 코드 표시

### 3. 워크숍 일정
- 주간 타입 리뷰: 매주 금요일 15:00
- 월간 심층 워크숍: 매월 첫째 주 화요일
- 온보딩 세션: 신규 팀원 입사 시

## Ⅶ. 자주 묻는 질문 (FAQ)

### Q: MyPy가 너무 엄격한가요?
A: `--no-strict-optional`, `--ignore-missing-imports` 플래그를 사용하거나, `pyproject.toml`에서 설정을 조정하세요.

### Q: 기존 코드를 타입 힌트로 마이그레이션하는 방법은?
A: 점진적 접근을 권장합니다. 먼저 `__future__ annotations`를 import하고, 주요 함수부터 시작하세요.

### Q: 제네릭 타입이 복잡해 보입니다.
A: 간단한 패턴부터 시작하세요. `list[str]`처럼 기본적인 제네릭부터 사용해보세요.

### Q: 타입 가드를 언제 사용해야 하나요?
A: 런타임 타입 검증이 필요할 때 사용하세요. 특히 사용자 입력이나 외부 API 응답 처리 시 유용합니다.

---

## 결론

타입 시스템은 코드의 안정성과 가독성을 크게 향상시킵니다. 이 가이드를 참고하여 점진적으로 타입 시스템을 도입해보세요.

궁금한 점이 있으시면 팀 채널이나 코드 리뷰를 통해 질문해주세요! 🎯