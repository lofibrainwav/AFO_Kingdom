# STAGE 6 — Security & Secrets Standardization SSOT

**As-of: 2025-12-27**  
**Version: 1.0**  
**Based on: EXP_006 Rollback Prevention + Security Gate Hardening**

## 📋 목적

EXP_006에서 겪었던 "시크릿 누락으로 인한 보안 게이트 위반"을 **구조적으로 재발 불가**하게 만들기.

## 🎯 핵심 원칙

1. **시크릿 절대 추적 금지**: `.env.afo`는 Git에 절대 올라가지 않음
2. **환경 일관성 유지**: 로컬/CI 동일한 환경변수 구조
3. **보안 게이트 강제**: 401/401/200 위반 시 Hard-Fail
4. **재발 방지 자동화**: CI에서 회귀를 즉시 차단

---

## 🔍 1. 구현된 시크릿 관리 체계

### 1.1 파일 구조

| 파일 | 용도 | Git 추적 | 보안 레벨 |
|------|------|----------|----------|
| `.env.afo` | 실제 시크릿 파일 | ❌ 금지 | 🔴 Critical |
| `.env.afo.example` | 구조 샘플 | ✅ 필수 | 🟢 Public |
| `.gitignore` | 추적 방지 | ✅ 필수 | 🟢 Public |

### 1.2 검증 결과 (PASS)

```bash
# .env.afo 추적 상태 검증
$ git ls-files .env.afo
# (아무것도 출력되지 않음 - 추적되지 않음)

$ git check-ignore -v .env.afo
# .gitignore:60:.env.afo	.env.afo (무시 규칙 적용됨)

$ git status --porcelain | grep -E '\.env\.afo'
# (아무것도 출력되지 않음 - 상태에 언급되지 않음)
```

### 1.3 환경변수 구조

**환경변수 이름:** `AFO_INTERNAL_SECRET`  
**용도:** API 인증 토큰 (보안 게이트용)  
**형식:** 자유 텍스트 (영숫자 + 특수문자 허용)  
**예시 값:** `CHANGE_ME` (실제 값은 절대 노출되지 않음)

---

## 🏭 2. CI/CD 통합 (GitHub Actions)

### 2.1 워크플로우 동작

```yaml
# ops-smoke.yml에서 실행되는 방식
- name: Create .env.afo from secrets
  run: |
    echo "AFO_INTERNAL_SECRET=${{ secrets.AFO_INTERNAL_SECRET }}" > .env.afo
    chmod 600 .env.afo
```

### 2.2 GitHub Secrets 설정 요구사항

**Repository Settings → Secrets and variables → Actions** 에서:

```
AFO_INTERNAL_SECRET = [실제 시크릿 값]
```

**참고:** 실제 시크릿 값은 이 문서에 절대 기록되지 않습니다.

---

## 🔒 3. 보안 게이트 구현

### 3.1 Hard-Fail 보안 검증

**scripts/ops_smoke.sh**에서 강제 적용:

```bash
check_security() {
    # ...
    if [[ "$code" != "$expected" ]]; then
        echo -e "${RED}🚨 SECURITY GATE FAIL: $desc must return $expected, got $code${NC}"
        return 1  # Hard-Fail: 테스트 전체 실패
    fi
}
```

### 3.2 검증 케이스 (3종 필수)

| 케이스 | 헤더 | 예상 결과 | 목적 |
|--------|------|----------|------|
| Unauthorized | 없음 | 401 | 인증 요구 확인 |
| Wrong Secret | `X-Internal-Secret: wrong` | 401 | 잘못된 인증 거부 |
| Correct Secret | `X-Internal-Secret: [정확한 값]` | 200 | 올바른 인증 허용 |

### 3.3 검증 엔드포인트

**URL:** `http://localhost:8010/api/revalidate/status`  
**메서드:** GET  
**인증 방식:** 헤더 기반 (`X-Internal-Secret`)

---

## 🚀 4. 배포/런타임 전략

### 4.1 로컬 실행 (직접 환경변수 주입)

```bash
# 로컬에서 실행 시
export AFO_INTERNAL_SECRET="your_secret_here"
python -m AFO.api_server
```

### 4.2 CI/CD 실행 (런타임 파일 생성)

GitHub Actions에서 자동 생성:
- `.env.afo` 파일 생성
- 환경변수 주입
- 서비스 기동

### 4.3 Docker Compose 결정

**선택된 전략: B (명시 주입 유지)**

- **이유:** compose 파일이 파일 존재에 의존하지 않도록 함
- **장점:** 로컬/CI 환경 차이 최소화
- **단점:** 로컬에서 export 누락 가능성 (런북으로 커버)

**참고:** docker-compose.yml에 env_file 지시자를 추가하지 않음.

---

## 📊 5. 성공 기준 및 모니터링

### 5.1 성공 판정

- ✅ Git 추적 검증 PASS
- ✅ CI/CD 워크플로우 실행 성공
- ✅ 보안 게이트 3종 모두 401/401/200 반환
- ✅ 시크릿 값 로그/코드에 노출되지 않음

### 5.2 모니터링 지표

**주간 검토 대상:**
- CI 실행 성공률: > 95%
- 보안 게이트 위반: 0건
- 시크릿 누출 사고: 0건

### 5.3 장애 대응

**시크릿 관련 장애 발생 시:**

1. **즉시 판정:** 보안 게이트 결과 확인
2. **원인 분석:** 환경변수 설정 상태 검증
3. **복구:** 올바른 시크릿 값으로 재설정
4. **예방:** 관련 문서 업데이트

---

## 🔄 6. 롤백 및 재발 방지

### 6.1 롤백 절차

```bash
# 시크릿 문제 발생 시
unset AFO_INTERNAL_SECRET  # 잘못된 값 제거
export AFO_INTERNAL_SECRET="correct_value"  # 올바른 값 설정
# 서비스 재시작
```

### 6.2 재발 방지 조치

- **CI 강화:** 보안 게이트 Hard-Fail 유지
- **문서화:** 이 SSOT를 운영 가이드로 활용
- **교육:** 팀원 대상 시크릿 관리 교육

---

## 🎯 7. 결론 및 준수 사항

### 7.1 달성된 목표

- ✅ EXP_006 재발 루프 구조적 제거
- ✅ 시크릿 관리 표준화 완료
- ✅ 보안 게이트 자동화 구현
- ✅ 로컬/CI 환경 일관성 확보

### 7.2 준수 사항 (필수)

1. **`.env.afo` 절대 Git 커밋 금지**
2. **실제 시크릿 값 코드/문서에 기록 금지**
3. **보안 게이트 검증 주기적 실행**
4. **시크릿 변경 시 GitHub Secrets 동시 업데이트**

### 7.3 다음 단계 (선택적 확장)

- 모니터링 알람 채널 연결
- 다중 환경 시크릿 관리 (dev/staging/prod)
- 시크릿 로테이션 자동화

---

**이 SSOT는 EXP_006 재발 방지를 위한 완전한 시크릿 관리 체계를 정의합니다.**  
**모든 시크릿 관련 작업은 이 문서를 준수합니다.**