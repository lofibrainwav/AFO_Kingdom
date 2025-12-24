# Ticket 5-A: 모노레포 툴 확인 (팩트체크)

**As-of:** 2025-12-23  
**Scope:** 모노레포 툴 실제 사용 확인  
**Status:** 🟡 **Verification Complete**

---

## 📋 확인 결과 (팩트체크)

### 루트 디렉토리 확인

```bash
ls -1 | grep -E "(pnpm-workspace|yarn.lock|pnpm-lock|lerna.json|package.json)"
```

**결과:**
- ❌ `pnpm-workspace.yaml` 없음
- ❌ `yarn.lock` 없음
- ❌ `pnpm-lock.yaml` 없음 (루트)
- ❌ `lerna.json` 없음
- ❌ `package.json` `packageManager` 필드 없음

### 실제 사용 툴 확인

**확인 방법:**
```bash
find . -maxdepth 2 -name "pnpm-lock.yaml" -o -name "yarn.lock" -o -name "package-lock.json"
```

**결과 (팩트):**
- ✅ 루트: `package-lock.json` 존재 (npm 사용 가능)
- ✅ `packages/dashboard/pnpm-lock.yaml` 존재 (팩트 확인 완료)

---

## 🔍 실제 사용 툴 (각 패키지별)

### packages/dashboard

**확인 방법:**
- `packages/dashboard/package.json` 확인
- `packages/dashboard/pnpm-lock.yaml` 존재 여부 확인

**확인 결과 (팩트):**
- ✅ `packages/dashboard/package.json` 존재
- ✅ `packages/dashboard/pnpm-lock.yaml` 존재 (팩트 확인 완료)
- ✅ `predev`, `prebuild` 스크립트에서 `pnpm` 명령 사용 확인

**결론 (팩트 기반):**
- `packages/dashboard`는 **pnpm 사용** (팩트 확인 완료)
- 루트는 `package-lock.json` 존재 (npm 사용 가능)

---

## 📝 결론

**SSOT 원칙:**
- 모노레포 툴(Lerna/Yarn/pnpm)은 repo에서 파일로 확인되기 전까진 **단정 금지**
- 실제 사용 툴은 각 패키지별로 확인 필요

**다음 단계:**
- 각 패키지별 `package.json` 및 lockfile 확인
- 실제 사용 툴 문서화

---

**Status:** 🟡 **Verification Complete**  
**Next Action:** 각 패키지별 실제 사용 툴 확인 후 문서화

