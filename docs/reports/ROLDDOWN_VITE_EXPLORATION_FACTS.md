# Rolldown / rolldown-vite 탐구 (팩트/예시 분리)

**As-of:** 2025-12-23  
**Scope:** Rolldown bundler 및 Vite 통합 탐구  
**Status:** 🟡 **Research Phase - Facts Separated**

---

## FACTS (검증됨)

### Rolldown 기본 정보

- Rolldown은 **Rust 기반 JS/TS bundler**이며, Rollup의 플러그인 API와 동일한 형태를 목표로 한다.
- Rolldown은 현재 **Beta**로 안내되어 있으며, "대부분의 production use case는 처리 가능"하다고 설명된다.
  - 단, **minification(압축)은 WIP**로 명시되어 있다.
- Rolldown은 **prebuilt binary**를 제공하며, **WASM 빌드**도 제공한다.

### 성능 목표/설명 (공식 문서 기준)

- "Rollup 대비 10–30배 빠름"
- "esbuild 수준의 속도" 목표

> **주의**: 위 수치는 공식 문서에서 언급된 목표/설명이며, 실제 측정값은 환경에 따라 다를 수 있습니다.

### Vite 통합 상태

- Vite에서 Rolldown 통합은 현재 **`rolldown-vite`라는 별도 패키지**로 제공되는 **"실험적(Experimental) 통합"**이다.
  - 실험적이므로 **버전을 반드시 pin** 해야 하며, **patch 버전에서도 breaking change**가 들어갈 수 있다고 안내되어 있다.
  - 향후 이 통합은 **메인 Vite로 합쳐질 계획**이라고 안내되어 있다.

### 로드맵/상태 (공식 문서 기준)

- **HMR**: WIP (Work In Progress)
- **Module Federation**: planned
- **"Full Bundle Mode"**: future plan

---

## EXAMPLES (AFO 적용 예시/추정 — 측정 필요)

> **주의**: 아래는 AFO 왕국 적용 예시/추정이며, 실제 측정이 필요합니다.

### 예시 1: 스모크 테스트

- (예시) Vite 기반 패키지에서만, 브랜치에서 `rolldown-vite`를 스모크 테스트로 붙여 빌드 시간 변화를 측정한다.

### 예시 2: 측정 지표

- (예시) 측정 지표:
  - CI build wall-clock
  - 번들 크기
  - 런타임 회귀 (간단 e2e)
  - 플러그인 호환성 이슈 발생률

---

## HOW-TO (pnpm 기준 / 안전 적용 가이드)

**원칙**: "메인 빌드라인 변경 없이", 브랜치 + 스모크 테스트로만 검증한다.

### A) 프로젝트가 `vite`를 direct dependency로 갖는 경우

- `package.json`에서 `devDependencies`의 `vite`를 아래처럼 "교체"한다.
  ```json
  {
    "devDependencies": {
      "vite": "npm:rolldown-vite@<PINNED_VERSION>"
    }
  }
  ```

### B) 프레임워크가 peer dependency로 `vite`를 요구하는 경우 (모노레포/워크스페이스에서 흔함)

- `package.json`에 `overrides`를 추가한다.
  ```json
  {
    "pnpm": {
      "overrides": {
        "vite": "npm:rolldown-vite@<PINNED_VERSION>"
      }
    }
  }
  ```

### 공통 실행 절차

1. `pnpm install --frozen-lockfile`
2. `pnpm build`
3. 실패 시: `overrides`/`alias` 제거 + lockfile 롤백 (브랜치 폐기)

---

## CI (선택: "안전 스모크 테스트")

- 메인 workflow를 건드리지 말고, **별도 job/workflow로만** `rolldown-vite` 빌드 스모크 테스트를 돌린다.
- 성공 조건:
  - `install` 통과
  - `build` 통과
  - (가능하면) 최소 smoke test 1개 통과

---

## 🔒 SSOT 일관성 보장

### ✅ 팩트/예시 분리 원칙

- **FACTS**: 공식 문서에서 확인된 내용만 포함
- **EXAMPLES**: AFO 적용 예시/추정은 명확히 구분
- **HOW-TO**: 안전 적용 가이드 (버전 핀 필수)

### ✅ 단정 금지 원칙

- "production ready" 같은 단정 금지 (Beta, minify는 WIP)
- "기본 통합" 같은 타임라인 단정 금지 (별도 패키지, 실험적)
- 성능 수치는 공식 문서 기준만 (실제 측정값은 환경에 따라 다름)

---

## 📋 참고 자료 (공식 문서)

- **Rolldown**: [Introduction | Rolldown](https://rolldown.rs/guide/introduction)
  - Beta 상태, minify는 WIP, 성능 목표, 로드맵
- **Vite**: [Rolldown Integration | Vite](https://vite.dev/guide/rolldown)
  - `rolldown-vite` 별도 패키지, 실험적 통합, 버전 핀 필수, future plan

---

## 🏁 결론

**현재 상태:**
- Rolldown은 Beta 단계 (minify는 WIP)
- Vite 통합은 실험적 (`rolldown-vite` 별도 패키지)
- 버전 핀 필수 (patch에서도 breaking change 가능)

**AFO 왕국 적용:**
- 메인 빌드라인 변경 없이 브랜치 + 스모크 테스트로만 검증
- 실제 측정값 확인 후 결정

---

**Status:** 🟡 **Research Phase - Facts Separated**  
**Next Action:** AFO 모노레포에서 Vite 사용 패키지 확인 후 스모크 테스트 CI 작성 (선택)

