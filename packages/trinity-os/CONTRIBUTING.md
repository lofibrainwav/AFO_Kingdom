# TRINITY-OS 기여 가이드

## 환영합니다! 🎉

TRINITY-OS에 기여해 주셔서 감사합니다. 이 가이드는 프로젝트에 기여하는 방법을 설명합니다.

## 기여 전 준비사항

### 1. 철학 동의
TRINITY-OS는 **眞善美孝永** 철학을 따릅니다:

- **眞 (Truth)**: 정확성과 진실성
- **善 (Goodness)**: 윤리성과 인간 중심성
- **美 (Beauty)**: 단순성과 우아함
- **孝 (Serenity)**: 평온과 마찰 제거
- **永 (Eternity)**: 지속성과 영속성

### 2. 개발 환경 설정
```bash
# 저장소 클론
git clone https://github.com/lofibrainwav/TRINITY-OS.git
cd TRINITY-OS

# 초기화
./init_trinity_os.sh

# 테스트 실행
./test_trinity_os.sh
```

### 3. 코드 품질 기준
- **Python**: Ruff 준수, 타입 힌트 필수
- **Bash**: ShellCheck 통과
- **문서**: 마크다운 형식 준수

## 기여 유형

### 🐛 버그 리포트
1. `Issues` 탭에서 "Bug Report" 템플릿 사용
2. 버그 재현 단계 상세히 설명
3. 환경 정보 포함 (OS, Python 버전 등)

### ✨ 기능 제안
1. `Issues` 탭에서 "Feature Request" 템플릿 사용
2. 제안하는 기능의 목적과 필요성 설명
3. 구현 아이디어 (선택사항)

### 🛠️ 코드 기여
1. `Issues`에서 작업할 이슈 선택 또는 생성
2. 브랜치 생성: `git checkout -b feature/your-feature-name`
3. 코드 작성 및 테스트
4. Pull Request 생성

## 개발 워크플로우

### 1. 작업 시작
```bash
# 최신 코드 가져오기
git pull origin main

# 브랜치 생성
git checkout -b feature/your-feature

# 작업 진행
```

### 2. 코드 작성 규칙
```python
# Python 예시
def function_name(param: str) -> dict[str, Any]:
    """
    함수 설명을 docstring으로 작성
    """
    try:
        # 실제 로직 구현
        result = {"status": "success"}
        return result
    except Exception as e:
        # 예외 처리
        raise SomeError(f"작업 실패: {e}") from e
```

### 3. 테스트
```bash
# 전체 테스트 실행
./test_trinity_os.sh

# 특정 스크립트 테스트
python3 scripts/your_script.py
```

### 4. 커밋
```bash
# 변경사항 스테이징
git add .

# 커밋 (형식 준수)
git commit -m "feat: 새로운 기능 추가

- 기능 설명
- 구현 세부사항

眞善美孝: Truth 95%, Goodness 90%, Beauty 85%, Serenity 95%"
```

### 5. Pull Request
1. `main` 브랜치로 PR 생성
2. 상세한 설명 작성
3. 리뷰어 태그
4. CI/CD 통과 확인

## 코드 리뷰 기준

### ✅ 승인 기준
- [ ] Trinity Score ≥ 90%
- [ ] 테스트 통과
- [ ] 코드 품질 준수
- [ ] 문서화 완료

### ❌ 거부 기준
- [ ] 철학 위반 (眞善美孝永)
- [ ] 보안 취약점
- [ ] 성능 저하
- [ ] 유지보수성 저하

## 커뮤니케이션

### 언어
- 기본: 한국어
- 코드/기술: 영어

### 태도
- **존중**: 모든 기여자를 존중
- **건설적**: 비판 시 해결책 제시
- **개방적**: 새로운 아이디어 환영

## 보상

### 인정
- 모든 기여자는 `CONTRIBUTORS.md`에 등재
- 주요 기여자는 헌법 개정 권한 부여

### 혜택
- TRINITY-OS 우선 사용권
- AFO 왕국 특별 회원 자격
- 기술 지원 우선권

## 문의

질문이나 도움이 필요하시면:
- `Issues`에 질문 등록
- 이메일: trinity-os@afo-kingdom.org

---

**眞善美孝永** - 함께 왕국을 만들어 갑시다! 🏰✨