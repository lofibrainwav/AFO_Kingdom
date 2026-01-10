# 🛡️ AFO Kingdom 보안 프로토콜 (SSOT)

## 개요

AFO Kingdom은 眞善美孝永 철학에 기반한 보안 우선 시스템입니다.
모든 개발자는 이 프로토콜을 준수하여 시스템 보안을 유지합니다.

## 1. 시크릿 관리 원칙

### 1.1 절대 금지사항
- **절대 하드코딩 금지**: 코드에 API 키, 비밀번호, 토큰을 직접 작성하지 마세요
- **Git 히스토리 노출 금지**: 이미 커밋된 시크릿은 즉시 회전하세요
- **공유 금지**: 시크릿을 Slack, 이메일, 문서로 공유하지 마세요

### 1.2 환경변수 사용 원칙
```python
# ✅ 올바른 방법
import os
api_key = os.getenv("OPENAI_API_KEY")
db_password = os.getenv("POSTGRES_PASSWORD")

# ❌ 잘못된 방법
api_key = "sk-proj-xxxxx"  # 하드코딩 절대 금지
```

### 1.3 환경변수 네이밍 규칙
- 대문자 + 언더스코어: `OPENAI_API_KEY`
- 설명적이고 명확하게: `JWT_SECRET_KEY`, `POSTGRES_PASSWORD`
- 접두사 사용: `AFO_*` (AFO Kingdom 전용)

## 2. 개발 워크플로우

### 2.1 새로운 시크릿 추가 시
1. **환경변수 정의**: `.env` 파일에 추가
2. **템플릿 업데이트**: `.env.example`에 주석과 함께 추가
3. **코드 수정**: `os.getenv()`로 접근
4. **문서화**: 이 파일의 시크릿 목록에 추가

### 2.2 기존 시크릿 회전 시
1. **새 값 생성**: openssl rand 또는 서비스 대시보드에서 생성
2. **환경변수 업데이트**: `.env` 파일 수정
3. **서비스 재시작**: 새 시크릿 적용
4. **기존 값 무효화**: 이전 시크릿 폐기

## 3. 시크릿 목록 (SSOT)

### 3.1 필수 시크릿
| 환경변수 | 목적 | 예시 값 |
|---------|------|--------|
| `JWT_SECRET_KEY` | JWT 토큰 서명 | 랜덤 64바이트 hex |
| `POSTGRES_PASSWORD` | 데이터베이스 접속 | 랜덤 16바이트 hex |
| `AFO_PASSPHRASE` | SSL 인증서 암호 | 랜덤 패스프레이즈 |

### 3.2 선택 시크릿
| 환경변수 | 목적 | 필수 여부 |
|---------|------|----------|
| `OPENAI_API_KEY` | OpenAI API | 선택 |
| `ANTHROPIC_API_KEY` | Claude API | 선택 |
| `OLLAMA_BASE_URL` | Ollama 서버 | 선택 |

## 4. CI/CD 보안 게이트

### 4.1 Gitleaks 스캔
- **실행 시점**: 모든 PR과 푸시에서
- **실패 정책**: "Fail Loud" - 시크릿 발견 시 즉시 실패
- **예외 처리**: `.gitleaksignore`에 테스트 파일만 허용

### 4.2 환경변수 검증
```bash
# CI에서 실행되는 검증
./scripts/verify_env_security.sh
```

## 5. 보안 사고 대응

### 5.1 시크릿 노출 의심 시
1. **즉시 보고**: 팀 채널에 알림
2. **시크릿 회전**: 새 값으로 즉시 교체
3. **범위 파악**: 영향을 받은 시스템 식별
4. **모니터링 강화**: 이상 징후 모니터링

### 5.2 Git 히스토리 정화
```bash
# 노출된 커밋 제거 (주의: 히스토리 변경)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch secrets.txt' \
  --prune-empty --tag-name-filter cat -- --all
```

## 6. 모니터링 및 감사

### 6.1 정기 감사
- **주기**: 매주 월요일
- **범위**: 전체 코드베이스 시크릿 스캔
- **보고**: `artifacts/security_audit_$(date +%Y%m%d).txt`

### 6.2 자동 모니터링
- **CI 실패 알림**: 시크릿 검출 시 Slack 알림
- **주기적 스캔**: 매일 artifacts/secret_scan.log 생성
- **대시보드**: 보안 메트릭 모니터링

## 7. 교육 및 책임

### 7.1 신규 개발자 교육
- **필수 교육**: 이 문서 완독
- **실습**: 시크릿 관리 워크숍
- **책임**: 코드 리뷰에서 시크릿 검증

### 7.2 책임 분담
- **개발자**: 코드에 시크릿 미포함
- **DevOps**: 환경변수 관리 및 CI/CD 유지
- **보안 담당**: 감사 및 사고 대응

## 8. 참고 자료

- [OWASP 시크릿 관리 가이드](https://owasp.org/www-project-top-ten/)
- [GitHub 시크릿 스캔](https://docs.github.com/en/code-security/secret-scanning)
- [12 Factor App Config](https://12factor.net/config)

---

## SSOT 정보

- **생성일**: 2026-01-09
- **관리자**: AFO Kingdom 승상
- **다음 검토**: 2026-02-09
- **버전**: 1.0.0