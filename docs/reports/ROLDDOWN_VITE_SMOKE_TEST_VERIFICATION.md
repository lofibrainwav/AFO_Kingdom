# Rolldown-vite 스모크 테스트 CI 검증 가이드

**As-of:** 2025-12-23  
**Scope:** Rolldown-vite 스모크 테스트 CI 검증  
**Status:** 🟡 **Verification Guide**

---

## ✅ 1단계: Workflow 파일 검증 (로컬 완료)

### 파일 존재 확인

- ✅ `.github/workflows/rolldown_vite_smoke.yml` 존재
- ✅ YAML 문법 검증 통과

### Trigger 조건 확인

**Manual 트리거:**
- `workflow_dispatch`
- `input: rolldownViteVersion` (required, pinned version)

**Auto 트리거:**
- `pull_request`
- `paths:`
  - `packages/aicpa-core/**`
  - `.github/workflows/rolldown_vite_smoke.yml`

**Concurrency:**
- `group: rolldown-smoke-${{ github.ref }}`
- `cancel-in-progress: true`

### Matrix Strategy

- `baseline_vite`: 기본 Vite 사용
- `rolldown_vite`: rolldown-vite로 교체

---

## ✅ 2단계: 패키지 확인 (로컬 완료)

### packages/aicpa-core

- ✅ `package.json` 존재
- ✅ `vite: ^6.2.0` (devDependencies)
- ✅ `vite.config.ts` 존재
- ✅ `@vitejs/plugin-react` 사용

---

## ⚠️ 3단계: GitHub Actions 테스트 (수동 실행 필요)

### 수동 실행 테스트 (추천)

**절차:**
1. GitHub Repository → Actions 탭
2. `Rolldown (rolldown-vite) smoke test - aicpa-core` 워크플로우 선택
3. Run workflow 버튼 클릭
4. `rolldownViteVersion` 입력: `0.0.0-...` (실제 핀 버전)
5. Run workflow 클릭

**예상 결과:**
- ✅ Workflow 실행 시작
- ✅ Matrix strategy: `baseline_vite`와 `rolldown_vite` 두 job 실행
- ✅ `baseline_vite`: 기본 Vite로 빌드 성공
- ✅ `rolldown_vite`: rolldown-vite로 빌드 성공
- ✅ Step Summary에 모드/Node/pnpm 정보 표시
- ✅ 빌드 시간 비교 가능

**실패 시 확인 사항:**
- ❌ `rolldownViteVersion` 입력 누락: 필수 입력 확인
- ❌ 빌드 실패: 플러그인 호환성 확인
- ❌ 설치 실패: `--no-frozen-lockfile` 필요 (실험 스모크)

---

## ⚠️ 4단계: 자동 트리거 테스트 (선택)

### 테스트 절차

1. 로컬에서 `packages/aicpa-core` 파일 수정:
   ```bash
   # 예시: vite.config.ts 수정
   echo "// test" >> packages/aicpa-core/vite.config.ts
   ```

2. Git 커밋 및 PR 생성:
   ```bash
   git add packages/aicpa-core/vite.config.ts
   git commit -m "test: trigger rolldown smoke test"
   git push origin feature/test-rolldown
   # PR 생성
   ```

3. GitHub Actions 확인:
   - PR에서 워크플로우 자동 실행 확인
   - `baseline_vite`와 `rolldown_vite` 두 job 실행 확인

**예상 결과:**
- ✅ Workflow 자동 실행 (pull_request 트리거)
- ✅ Matrix strategy: 두 job 모두 실행
- ✅ 빌드 성공

---

## 📋 5단계: 빌드 시간 비교 (결과 분석)

### 측정 지표

- **CI build wall-clock**: `time` 명령으로 측정
- **번들 크기**: (추가 측정 필요)
- **런타임 회귀**: (추가 e2e 테스트 필요)
- **플러그인 호환성**: 빌드 성공/실패로 확인

### Step Summary 확인

워크플로우 실행 후 Step Summary에서:
- Mode: `baseline_vite` 또는 `rolldown_vite`
- Node: Node.js 버전
- pnpm: pnpm 버전

---

## 🔒 SSOT 일관성 보장

### ✅ 유지할 것 (절대 건드리지 않음)

1. **메인 빌드라인**
   - 메인 CI workflow는 그대로 유지
   - `--frozen-lockfile` 유지

2. **패키지 구조**
   - `packages/aicpa-core` 구조 유지
   - `vite.config.ts` 유지

### ✅ 확장 가능한 것 (스모크 테스트만)

1. **Rolldown-vite 스모크 테스트**
   - 별도 workflow로만 실행
   - `--no-frozen-lockfile` (실험 스모크)
   - Lockfile 변경 예상됨

---

## 📋 검증 체크리스트

### 로컬 검증 (완료 ✅)

- [x] Workflow 파일 존재 및 문법 검증
- [x] 패키지 확인 (`packages/aicpa-core`)
- [x] Trigger 조건 확인
- [x] Matrix strategy 확인

### GitHub Actions 테스트 (수동 실행 필요 ⚠️)

- [ ] 수동 실행 테스트 (workflow_dispatch)
- [ ] 자동 트리거 테스트 (pull_request)
- [ ] 빌드 시간 비교 (baseline vs rolldown)
- [ ] Step Summary 확인

---

## 🏁 결론

**로컬 검증:** ✅ 완료  
**GitHub Actions 테스트:** ⚠️ 수동 실행 필요

**다음 단계:**
1. GitHub Actions에서 수동 실행 테스트
2. 빌드 시간 비교 (baseline vs rolldown)
3. 결과 분석 및 결정

---

**Status:** 🟡 **Verification Guide Complete**  
**Next Action:** GitHub Actions 수동 실행 테스트

