# TRINITY-OS 개발 가이드

## 개발 환경 설정

### 필수 요구사항
- Python 3.12+
- Bash 5.0+
- Git 2.0+

### 권장 도구
- VSCode + Cursor
- Docker Desktop
- GitHub CLI

## 프로젝트 구조

```
TRINITY-OS/
├── scripts/          # 코어 스크립트
├── docs/            # 문서
├── tests/           # 테스트
├── .vscode/         # VSCode 설정
├── .cursor/         # Cursor 설정
└── requirements.txt # 의존성
```

## 개발 워크플로우

### 1. 작업 시작
```bash
# 브랜치 생성
git checkout -b feature/your-feature

# 작업 진행
```

### 2. 코드 작성
```python
# Python 예시
def function_name(param: str) -> dict[str, Any]:
    """함수 설명"""
    # 구현
    pass
```

### 3. 테스트
```bash
# 단위 테스트
python3 -m pytest tests/

# 시스템 테스트
./test_trinity_os.sh
```

### 4. 커밋
```bash
git add .
git commit -m "feat: 새로운 기능

- 기능 설명
- 구현 세부사항

眞善美孝: Truth 95%, Goodness 90%, Beauty 85%, Serenity 95%"
```

### 5. Pull Request
- main 브랜치로 PR 생성
- 리뷰 요청
- 승인 후 병합

## 코드 품질

### Python
- Ruff 포맷터 사용
- 타입 힌트 필수
- 문서화 필수

### Bash
- ShellCheck 통과
- 에러 처리 포함
- 주석 포함

## 테스트

### 단위 테스트
```python
def test_function():
    assert function_name("test") == expected_result
```

### 통합 테스트
```bash
# 시스템 테스트 실행
./test_trinity_os.sh
```

## 문서화

### 코드 문서화
```python
def function_name(param: str) -> dict[str, Any]:
    """
    함수 설명.

    Args:
        param: 파라미터 설명

    Returns:
        반환값 설명
    """
```

### README 업데이트
- 새로운 기능 추가 시 README 업데이트
- 사용 예시 포함

## 기여

1. CONTRIBUTING.md 읽기
2. Issue 선택 또는 생성
3. 개발 진행
4. PR 제출

## 결론

TRINITY-OS 개발에 참여해 주셔서 감사합니다.

**眞善美孝永** ✨