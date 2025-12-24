# 🏛️ Ticket 4 — SSOT IMPERIAL ARCHITECTURE SEALED

**정적 생성 강화 & Override 규칙 봉인 (Verified Edition)**

**As-of:** 2025-12-23  
**Scope:** Ticket 4 (Track2 확장)  
**Status:** 🟢 **Gate checks passed (validate + type-check + build)**

---

## 🎯 목적 (SSOT 선언)

Ticket 4의 목적은 **문서 렌더링 경로를 단 하나의 진실(SSOT)**로 고정하여,
런타임 분기·암묵적 규칙·우연적 동작을 **구조적으로 제거**하는 것이다.

> **결과:**
> `/docs/[slug]` 경로는 더 이상 "추론"이 아닌 **결정된 규칙**만 따른다.

---

## 1️⃣ 眞 (Truth) — 정적 생성 강화로 진실 고정

### 구현 내용

* **`generateStaticParams()` 도입**
  * 모든 slug를 **빌드 타임에 고정**
  * 런타임 slug 추론/탐색 제거
  * **증거**: `packages/dashboard/src/app/docs/[slug]/page.tsx` (라인 26-37)

* **slug 검증**
  * Contract Gate와 **동일 규칙 재사용**
  * 허용 문자: `a-z, 0-9, -, 가-힣`
  * 연속 하이픈, 양끝 하이픈 불가
  * **증거**: `isValidSlug()` 함수 (라인 17-24)

* **존재하지 않는 fragment**
  * 즉시 `notFound()` → 404
  * **증거**: `getFragmentContent()` 실패 시 `notFound()` (라인 67-69)

### 메타데이터 자동화

* `generateMetadata()`로 title 자동 생성
* slug 기반 일관된 문서 식별자 유지
* **증거**: `generateMetadata()` 함수 (라인 39-52)

---

## 2️⃣ 善 (Goodness) — 안전장치 격상 (Warning → Error)

### Gate 강화

* **`fragment_key`**
  * ❌ 경고 → ✅ **에러(Error)로 승격**
  * 표준 키 누락 시 **빌드 차단**
  * **증거**: `scripts/validate_widgets_json.py` (라인 101-169)
  * **검증 결과**: `fragment_key` 없으면 `return 1` (빌드 실패)

* **중복 slug**
  * 기존 Gate 유지 (에러)
  * **증거**: `scripts/validate_widgets_json.py` (라인 56-61)

* **규칙 불일치**
  * Contract Gate에서 즉시 차단
  * **증거**: slug 규칙 위반 시 `return 1` (라인 93-97)

> 이 단계부터 **불완전한 JSON은 아예 왕궁에 입장 불가**.

---

## 3️⃣ 美 & 永 (Beauty & Eternity) — Override 규칙 봉인

### SSOT 렌더링 우선순위 (고정)

1. **React Override**
   * `widgetRegistry[slug]`에 컴포넌트가 존재하면 **무조건 최우선**
   * **증거**: `packages/dashboard/src/app/docs/[slug]/page.tsx` (라인 55-61)

2. **HTML Fragment**
   * `public/fragments/{fragment_key}.html`
   * **증거**: `getFragmentContent()` 호출 (라인 65)

3. **404**
   * 둘 다 없으면 `notFound()`
   * **증거**: `fragmentContent` 없으면 `notFound()` (라인 67-69)

> 이 규칙은 **예외 없음 / 암묵적 fallback 없음**.

---

## 🔒 핵심 SSOT 규칙 (명문화)

### Identifier 규칙

* **slug**
  * `widget-{name}` → `{name}`
  * 허용 문자셋 엄격 고정
  * **증거**: `isValidSlug()` 함수 (라인 17-24)

* **fragment_key**
  * **slug와 1:1**
  * 생성(Node): `fragment_key`만 사용
  * 읽기: fallback 없음 (Ticket 4부터 완전 표준화)
  * **증거**: `generate_widgets_from_html.mjs` (라인 132-145, 172-185)

---

## ✅ 검증 체크리스트 (재현 가능)

### 실행된 검증

1. **Contract Gate 검증**
   ```bash
   python3 scripts/validate_widgets_json.py
   ```
   **결과**: ✅ 통과
   - 표준 키 `fragment_key` 사용: **35 / 35**
   - slug 규칙 통과 (한글 포함)
   - Fragment 경로 검증 완료

2. **TypeScript 타입 체크**
   ```bash
   pnpm -C packages/dashboard type-check
   ```
   **결과**: ✅ 통과 (에러 없음)

3. **Next.js 빌드 검증**
   ```bash
   pnpm -C packages/dashboard build
   ```
   **결과**: ✅ 통과 (정적 생성 성공)

### 검증 결과 요약

* ✅ 표준 키 `fragment_key` 사용: **35 / 35**
* ✅ slug 규칙 통과 (허용 문자: a-z, 0-9, -, 가-힣)
* ✅ Fragment 경로 검증 완료
* ✅ TypeScript 타입 체크 통과
* ✅ 빌드 타임 정적 생성 성공

---

## 🗂️ 변경 파일 (SSOT)

### 수정된 파일

1. **`packages/dashboard/src/app/docs/[slug]/page.tsx`**
   * `generateStaticParams()` 추가 (라인 26-37)
   * `generateMetadata()` 추가 (라인 39-52)
   * Override 규칙 구현 (라인 55-61)
   * **변경 라인 수**: +30줄

2. **`scripts/validate_widgets_json.py`**
   * `fragment_key` 필수 → error (라인 101-169)
   * Ticket 4 Gate 추가
   * **변경 라인 수**: +65줄

### 생성된 파일

* 없음 (기존 파일 수정만)

---

## 📋 재현 가능한 실행 명령어

### 개발 환경에서 재검증

```bash
# 1. Contract Gate 검증
python3 scripts/validate_widgets_json.py

# 2. TypeScript 타입 체크
pnpm -C packages/dashboard type-check

# 3. Next.js 빌드 (정적 생성 확인)
pnpm -C packages/dashboard build

# 4. 생성된 정적 페이지 확인
ls packages/dashboard/.next/server/app/docs/
```

### 예상 출력

```
✅ Validation passed!
   Widget count: 35
   Validated widgets: 35
✅ Slug 규칙 통과 (허용 문자: a-z, 0-9, -, 가-힣)
✅ 표준 키(fragment_key) 사용: 35개
✅ Fragment 경로 필드 검증 완료
```

---

## 🏁 결론 (봉인 선언)

Ticket 4는 **기능 추가가 아니라 질서의 봉인**이다.
이제 `/docs/[slug]`는:

* 추측하지 않고
* 탐색하지 않으며
* 오직 **SSOT 규칙만 따른다**

> **Status:** 🟢 **SSOT IMPERIAL ARCHITECTURE SEALED**
> *(Validated · Type-safe · Deterministic)*

---

## 📚 관련 문서

* `docs/reports/TICKET_3_COMPLETE.md` - HTML Fragment 추출 및 렌더
* `docs/reports/TICKET_3_GATE_BOOSTER_COMPLETE.md` - Gate 보강 완료
* `docs/reports/TICKET_3_GATE_BOOSTER_FINAL.md` - Gate 보강 최종 완료

---

**작성일**: 2025-12-23  
**승인**: SSOT 검증 완료  
**봉인**: 🟢 **IMPERIAL ARCHITECTURE SEALED**

