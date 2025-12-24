# Ticket 5-A Commit 3: CI 통합 검증 가이드

**As-of:** 2025-12-23  
**Scope:** Commit 3 실제 CI 구현 검증  
**Status:** 🟡 **Verification Guide**

---

## ✅ 1단계: Workflow 파일 검증 (로컬 완료)

### 파일 존재 확인

- ✅ `.github/workflows/revalidate.yml` 존재
- ✅ YAML 문법 검증 통과
- ✅ 파일 크기: 99줄

### Trigger 조건 확인

**Push 트리거:**
- `branches: [main]`
- `paths:`
  - `**/fragments/**`
  - `**/fragments/*.html`
  - `docs/**`

**Manual 트리거:**
- `workflow_dispatch`
- `input: fragmentKeys` (optional, space-separated)

**Concurrency:**
- `group: revalidate-${{ github.ref }}`
- `cancel-in-progress: true`

---

## ✅ 2단계: Fragment 파일 확인 (로컬 완료)

### Fragment 디렉토리

- ✅ `packages/dashboard/public/fragments/` 존재
- ✅ Fragment 파일들 존재 확인

### 테스트용 Fragment

- `home-hero.html` (존재 확인 필요)
- 또는 다른 fragment 파일 사용 가능

---

## ✅ 3단계: Fragment Key 추출 로직 시뮬레이션 (로컬 완료)

### 정규식 검증

- ✅ 정규식: `/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/`
- ✅ Key 추출 로직 검증 통과
- ✅ 경로 패턴 매칭 확인

---

## ⚠️ 4단계: GitHub Secrets/Vars 설정 (수동 작업 필요)

### Repo Secret 설정

1. GitHub Repository → Settings
2. Secrets and variables → Actions
3. New repository secret
4. Name: `REVALIDATE_SECRET`
5. Value: (실제 secret 값 입력)
6. Add secret

### Repo Variable 설정

1. GitHub Repository → Settings
2. Secrets and variables → Actions
3. Variables 탭
4. New repository variable
5. Name: `REVALIDATE_URL`
6. Value: `https://YOUR_DOMAIN/api/revalidate` (실제 URL 입력)
7. Add variable

### 배포 환경 설정

- API 서버(대시보드)에 `REVALIDATE_SECRET` 환경 변수 설정 필요
- 예: `.env.local` 또는 배포 환경 변수 설정

---

## 📋 5단계: 수동 실행 테스트 (GitHub Actions)

### 테스트 절차

1. GitHub Repository → Actions 탭
2. `Revalidate changed fragments` 워크플로우 선택
3. Run workflow 버튼 클릭
4. `fragmentKeys` 입력: `home-hero` (또는 존재하는 fragment key)
5. Run workflow 클릭

### 예상 결과

- ✅ Workflow 실행 시작
- ✅ "Detect fragment keys" 단계: `Detected keys (manual): home-hero`
- ✅ "Trigger revalidate API" 단계: `Revalidating: home-hero`
- ✅ API 호출 성공 (200 OK)
- ✅ Workflow 완료

### 실패 시 확인 사항

- ❌ `Missing vars.REVALIDATE_URL`: Variable 설정 확인
- ❌ `401 Unauthorized`: Secret 설정 확인
- ❌ `Connection refused`: REVALIDATE_URL 확인

---

## 📋 6단계: 자동 트리거 테스트 (GitHub Actions)

### 테스트 절차

1. 로컬에서 fragment 파일 수정:
   ```bash
   # 예시: home-hero.html 수정
   echo "<!-- test -->" >> packages/dashboard/public/fragments/home-hero.html
   ```

2. Git 커밋 및 Push:
   ```bash
   git add packages/dashboard/public/fragments/home-hero.html
   git commit -m "test: trigger revalidate workflow"
   git push origin main
   ```

3. GitHub Actions 확인:
   - Actions 탭 → `Revalidate changed fragments` 워크플로우 실행 확인
   - "Detect fragment keys" 단계에서 자동 감지 확인

### 예상 결과

- ✅ Workflow 자동 실행 (push 트리거)
- ✅ "Detect fragment keys" 단계: `Detected keys (auto): home-hero`
- ✅ "Trigger revalidate API" 단계: `Revalidating: home-hero`
- ✅ API 호출 성공 (200 OK)
- ✅ Workflow 완료

### 실패 시 확인 사항

- ❌ Workflow가 실행되지 않음: paths 조건 확인
- ❌ Key가 감지되지 않음: 파일 경로 확인
- ❌ API 호출 실패: Secrets/Vars 확인

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

## 📋 검증 체크리스트

### 로컬 검증 (완료 ✅)

- [x] Workflow 파일 존재 및 문법 검증
- [x] Fragment 파일 존재 확인
- [x] Fragment key 추출 로직 시뮬레이션
- [x] Trigger 조건 확인

### GitHub 설정 (수동 작업 필요 ⚠️)

- [ ] Repo Secret: `REVALIDATE_SECRET` 설정
- [ ] Repo Variable: `REVALIDATE_URL` 설정
- [ ] 배포 환경: `REVALIDATE_SECRET` env 변수 설정

### GitHub Actions 테스트 (수동 실행 필요 ⚠️)

- [ ] 수동 실행 테스트 (workflow_dispatch)
- [ ] 자동 트리거 테스트 (fragment 파일 수정 후 push)

---

## 🏁 결론

**로컬 검증:** ✅ 완료  
**GitHub 설정:** ⚠️ 수동 작업 필요  
**GitHub Actions 테스트:** ⚠️ 수동 실행 필요

**다음 단계:**
1. GitHub Secrets/Vars 설정
2. 수동 실행 테스트
3. 자동 트리거 테스트

---

**Status:** 🟡 **Verification Guide Complete**  
**Next Action:** GitHub 설정 및 테스트 실행

