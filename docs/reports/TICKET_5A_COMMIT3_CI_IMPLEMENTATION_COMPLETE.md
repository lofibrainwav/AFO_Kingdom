# Ticket 5-A Commit 3: CI 통합 실제 구현 완료

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 3 (CI 통합 실제 구현)  
**Status:** 🟢 **Implementation Complete**

---

## ✅ 구현 완료

### 파일 업데이트

**파일 경로**: `.github/workflows/revalidate.yml`

**구현 내용 (최종 붙여넣기 버전):**
- Guard 단계 추가 (Secret/URL 검증)
- 첫 푸시 케이스 처리 (`0000000...`)
- MAX_KEYS 상한 적용 (25)
- 경로 패턴 단순화 (`fragments/**`)
- 에러 처리 개선 (stderr redirect)

---

## ⚠️ Stage-0 체크 (필수 3개)

### 1. 배포 환경 (dashboard) 설정

**필수:**
- API 서버(대시보드)에 `REVALIDATE_SECRET` 환경 변수 설정 필요
- 예: `.env.local` 또는 배포 환경 변수 설정

**확인 방법:**
```bash
# 로컬 환경에서 확인
echo $REVALIDATE_SECRET

# 배포 환경에서 확인 (실제 배포 환경에 따라 다름)
# 예: Vercel, Railway, Docker 등
```

---

### 2. GitHub Repo 설정

**필수 설정:**

#### Repo Secret 설정
1. GitHub Repository → Settings
2. Secrets and variables → Actions
3. New repository secret
4. Name: `REVALIDATE_SECRET`
5. Value: (실제 secret 값 입력 - 배포 환경과 동일해야 함)
6. Add secret

#### Repo Variable 설정
1. GitHub Repository → Settings
2. Secrets and variables → Actions
3. Variables 탭
4. New repository variable
5. Name: `REVALIDATE_URL`
6. Value: `https://<your-domain>/api/revalidate` (실제 URL 입력)
7. Add variable

> **주의**: `REVALIDATE_URL`은 실제 배포된 도메인을 사용해야 합니다.
> 예: `https://afo.kingdom/api/revalidate` 또는 `https://dashboard.example.com/api/revalidate`

---

### 3. 배포된 URL 접근 가능 확인

**필수:**
- `POST /api/revalidate`가 Edge route로 접근 가능해야 함
- 배포된 URL에서 API 엔드포인트가 정상 동작해야 함

**확인 방법:**
```bash
# 로컬 테스트
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"test"}'

# 배포 환경 테스트 (실제 도메인 사용)
curl -i -X POST "https://<your-domain>/api/revalidate" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"test"}'
```

---

## 📋 실행 플로우 (복붙)

### 1. Workflow 파일 확인

- ✅ `.github/workflows/revalidate.yml` 업데이트 완료
- ✅ 최종 붙여넣기 버전 반영

### 2. GitHub Actions 수동 실행 (workflow_dispatch)

**절차:**
1. GitHub Repository → Actions 탭
2. `Revalidate fragments (dynamic)` 워크플로우 선택
3. Run workflow 버튼 클릭
4. (input 없음 - 자동으로 변경 파일 감지)
5. Run workflow 클릭

**예상 결과:**
- ✅ Workflow 실행 시작
- ✅ Guard 단계: Secret/URL 검증 통과
- ✅ Detect 단계: 변경된 fragment keys 감지 (없으면 "No-op" 메시지)
- ✅ Call revalidate API 단계: API 호출 성공 (200 OK)
- ✅ Workflow 완료

### 3. 자동 트리거 활성화

**성공 후:**
- `on.push.paths: fragments/**` 자동 트리거 활성화됨
- `fragments/*.html` 파일 변경 시 자동 실행

---

## ✅ Verify (팩트 확정)

### 1. Actions 로그 확인

**확인 포인트:**
- curl 응답 200 OK
- Response body: `{"revalidated": true, "paths": [...]}`

**로그 예시:**
```
Revalidating keys: architecture-widget
{"revalidated":true,"paths":["/fragments/architecture-widget.html"]}
```

### 2. Fragment 내용 변경 확인 (SHA 해시)

**절차:**
```bash
# 1. 현재 fragment 내용 확인
curl -fsS "https://<your-domain>/fragments/architecture-widget.html" | shasum -a 256

# 2. Fragment 파일 수정 후 revalidate 호출
# (GitHub Actions에서 자동 또는 수동 실행)

# 3. 변경 후 fragment 내용 확인
curl -fsS "https://<your-domain>/fragments/architecture-widget.html" | shasum -a 256
```

**예상 결과:**
- SHA 해시가 변경됨 (revalidate 성공)
- 또는 동일 (revalidate 실패 또는 내용 미변경)

---

## 📋 커밋 메시지 (확정)

```txt
ci: add fragment revalidate workflow (guarded, manual-first)
```

---

## 🔒 SSOT 일관성 보장

### ✅ 유지할 것 (절대 건드리지 않음)

1. **SSOT 규칙**
   - slug 검증 (Contract Gate와 동일)
   - fragment_key 필수 (빌드 타임 검증)
   - 렌더링 우선순위 (React → Fragment → 404)

2. **Gate 검증**
   - 빌드 타임 검증 유지
   - Contract Gate 유지
   - fragment_key 검증 유지

3. **기존 Fragment**
   - `public/fragments/{fragment_key}.html` 유지
   - fragment overwrite 없음

### ✅ 확장 가능한 것 (읽기 경로만)

1. **CI 통합**
   - 변경된 fragmentKey 자동 감지
   - revalidate API 자동 호출

---

## ⚠️ 주의사항

- **Secret/URL 설정 필수**: Guard 단계에서 검증 실패 시 즉시 중단
- **첫 푸시 케이스**: `0000000...` 케이스 자동 처리
- **MAX_KEYS 제한**: 25개 초과 시 자동 제한
- **경로 패턴**: `fragments/**`만 감지 (단순화)

---

## 🏁 결론

**구현 완료:**
- Guard 단계 추가 ✅
- 첫 푸시 케이스 처리 ✅
- MAX_KEYS 상한 적용 ✅
- 경로 패턴 단순화 ✅

**다음 단계:**
1. GitHub Secrets/Vars 설정
2. 수동 실행 테스트 (workflow_dispatch)
3. 자동 트리거 테스트 (fragment 파일 수정 후 push)
4. Fragment 내용 변경 확인 (SHA 해시)

---

**Status:** 🟢 **Implementation Complete**  
**Next Action:** GitHub Secrets/Vars 설정 후 수동 실행 테스트

