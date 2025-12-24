# 🎯 Ticket 5-A: Runtime 확장 / Live Edit / Edge — SSOT 체크리스트

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A (Runtime 확장)  
**Status:** 🟡 **Planning Phase**

---

## 🧭 지피지기 (현재 상태 파악)

### ✅ 완료된 것 (Ticket 2/3/4)

* **정적 문서 엔진**: 완벽한 규칙 완료
* **SSOT 규칙 고정**: slug, fragment_key, 렌더링 우선순위
* **Gate 강화**: fragment_key 필수, 빌드 차단
* **Override 규칙 봉인**: React → Fragment → 404

### 🔍 비어있는 것

* **"변화가 어떻게 들어오느냐"**
  * Live Edit (실시간 업데이트)
  * Preview (Draft/Publish 분리)
  * Edge Revalidate (On-demand revalidation)

---

## 🔒 안전 범위 명확화 (SSOT 유지)

### ✅ 유지할 것 (절대 건드리지 않음)

1. **SSOT 규칙**
   * slug 검증 (Contract Gate와 동일)
   * fragment_key 필수 (빌드 타임 검증)
   * 렌더링 우선순위 (React → Fragment → 404)

2. **Gate 검증**
   * 빌드 타임 검증 유지
   * Contract Gate 유지
   * fragment_key 검증 유지

3. **기존 Fragment**
   * `public/fragments/{fragment_key}.html` 유지
   * fragment overwrite 없이 테스트

### ✅ 확장 가능한 것 (읽기 경로만)

1. **Live Edit**
   * Edge Runtime에서 fragment 읽기
   * 실시간 업데이트 (WebSocket 또는 Polling)
   * fragment overwrite 없이 테스트

2. **Preview 모드**
   * 쿼리 파라미터 기반 (예: `?preview=true`)
   * Draft/Publish 분리
   * 기존 fragment 유지

3. **Edge Revalidate**
   * On-demand revalidation API
   * 언제 invalidate (트리거)
   * 어디까지 실시간

### 🔒 Preview / Live Edit 접근 제한 (보안 오해 방지)

**SSOT 명시:**

* Preview / Live Edit routes는:
  * **Non-indexed** (no SEO)
  * **Dev / internal usage only**
  * **Not part of canonical SSOT path**
* 기존 `/docs/[slug]` 경로는 **절대 변경 없음**
* Preview/Live Edit은 **읽기 전용 확장**일 뿐

---

## 📋 구현 계획 (커밋 1/2/3)

### Commit 1: Preview 모드 (쿼리 파라미터 기반)

**목표**: Draft/Publish 분리, 기존 fragment 유지

**파일 경로**:

* `packages/dashboard/src/app/docs/[slug]/page.tsx` (Preview 모드 추가)

**구현 내용**:

* 쿼리 파라미터 `?preview=true` 체크
* Preview 모드일 때 Draft fragment 읽기
* 기존 fragment 유지 (overwrite 없음)

**Gate 영향**: 없음 (읽기 경로만 확장)

---

### Commit 2: Live Edit 최소 구현 (Edge Runtime)

**목표**: 실시간 업데이트, fragment overwrite 없이 테스트

**파일 경로**:

* `packages/dashboard/src/app/docs/[slug]/live/page.tsx` (Live Edit 전용 라우트)
* `packages/dashboard/src/app/api/live/[slug]/route.ts` (Live Edit API)

**구현 내용**:

* Edge Runtime에서 fragment 읽기
* 실시간 업데이트 (WebSocket 또는 Polling)
* fragment overwrite 없이 테스트

**Gate 영향**: 없음 (읽기 경로만 확장)

---

### Commit 3: Edge Revalidate 설계 (On-demand revalidation)

**목표**: On-demand revalidation API, 트리거 설계

**파일 경로**:

* `packages/dashboard/src/app/api/revalidate/route.ts` (On-demand revalidation)

**구현 내용**:

* On-demand revalidation API
* 언제 invalidate (트리거)
* 어디까지 실시간

**Gate 영향**: 없음 (읽기 경로만 확장)

---

## ✅ 검증 체크리스트 (재현 가능)

### Gate 영향 없음 보증

```bash
# 1. Contract Gate 검증 (변경 없음)
python3 scripts/validate_widgets_json.py

# 2. TypeScript 타입 체크
pnpm -C packages/dashboard type-check

# 3. Next.js 빌드 (정적 생성 유지)
pnpm -C packages/dashboard build
```

**예상 결과**: 모든 검증 통과 (변경 없음)

---

### Live Edit 최소 구현 검증

```bash
# 1. Live Edit 라우트 테스트
curl http://localhost:3000/docs/philosophy-widget/live

# 2. 실시간 업데이트 테스트
# (WebSocket 또는 Polling 연결 확인)

# 3. fragment overwrite 없이 테스트
# (기존 fragment 유지 확인)
```

---

### Preview 모드 검증

```bash
# 1. Preview 모드 테스트
curl http://localhost:3000/docs/philosophy-widget?preview=true

# 2. Draft/Publish 분리 확인
# (Preview 모드일 때 Draft fragment 읽기)

# 3. 기존 fragment 유지 확인
# (overwrite 없음)
```

---

## 🎯 형님의 원칙 반영

### ✅ 아이디어는 기본값 = '가능'

* Live Edit: **가능** (Edge Runtime, 실시간 업데이트)
* Preview: **가능** (쿼리 파라미터 기반)
* Edge Revalidate: **가능** (On-demand revalidation)

### ✅ 내 역할: "어디까지 지금 안전한가"를 그어주는 것

**안전 범위**:

* SSOT 규칙 유지 (slug, fragment_key, 렌더링 우선순위)
* Gate 영향 없음 (빌드 타임 검증 유지)
* 읽기 경로만 확장 (기존 fragment 유지)

**막는 역할 ❌ → 지금 가능한 범위를 명확히 해주는 역할 ⭕**

---

## 🏁 결론

Ticket 5-A는 **"변화가 어떻게 들어오느냐"**를 구현하는 단계입니다.

**안전 범위**:

* SSOT 규칙 유지
* Gate 영향 없음
* 읽기 경로만 확장

**구현 계획**:

* Commit 1: Preview 모드
* Commit 2: Live Edit 최소 구현
* Commit 3: Edge Revalidate 설계

---

**Status:** 🟡 **Planning Phase**  
**Next Action:** 형님 승인 후 구현 시작
