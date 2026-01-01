# AGENTS.md — AFO Kingdom Operating Constitution (SSOT)
_Last updated: 2026-01-01_

이 문서는 **AFO Kingdom 레포에서 작업하는 모든 AI 에이전트/자동화/사람**이 따라야 하는 "최소·필수" 운영 규칙입니다.
목표는 **할루시네이션 0**, **품질 게이트 정상화**, **작업 마찰 최소화(Serenity)** 입니다.

---

## 1) 절대 규칙 (Non-negotiables)

### 1.1 Truth (眞) — 사실/근거 없으면 말하지 않습니다
- 레포에 **존재하는 파일/명령/출력**만 근거로 말합니다.
- "아마/추정/예상/가능" 표현은 금지합니다. 모르면 **모른다**고 말하고 **확인 커맨드**를 제시합니다.
- 시간/환경에 따라 바뀌는 값(브랜치 보호, CI 체크 이름, 버전 등)은 **실제 실행 결과**로만 결론을 냅니다.

### 1.2 Safety (善) — 위험하면 멈춥니다
- 프로덕션/배포/보안/권한 변경은 **BLOCK**(사용자 승인 없이는 진행 금지).
- 변경 전에는 항상 **Backup → Check → Execute → Verify** 순서를 지킵니다.
- secrets/토큰/개인정보는 로그/PR/아티팩트에 절대 남기지 않습니다.

### 1.3 Serenity (孝) — 마찰을 줄이는 게 1순위입니다
- "큰 작업"을 한 번에 하지 않습니다. **작은 커밋/작은 PR**로 나눕니다.
- 설명은 짧게, 실행은 명확하게(복붙 가능한 커맨드) 제공합니다.
- 역할극/장식 텍스트는 공식 로그/문서에는 넣지 않습니다.

---

## 2) SSOT 우선순위 (무엇을 진실로 볼 것인가)

작업/의사결정 시 아래 순서로만 근거를 삼습니다.

1) **현재 레포 상태**: `git status -sb`, `git rev-parse HEAD`, 실제 파일 내용
2) **워크플로우/스크립트**: `.github/workflows/*`, `./afo`, `scripts/*`
3) **프로젝트 SSOT 문서**(존재할 때만):
   - `TICKETS.md`, `task.md`, `walkthrough.md`
   - `docs/*` (관련 문서가 실제로 있을 때만)

> 파일이 없다면 "없다"고 명시하고, 없는 전제에서만 진행합니다.

---

## 3) 표준 실행 프로토콜 (10초 루틴)

작업 시작/변경 전, 항상 아래를 실행해 **현 상태를 고정**합니다.

```bash
set -euo pipefail
git status -sb
git rev-parse HEAD
./afo status
./afo trinity
./afo drift
```

* 위 5개가 **Green**이면 진행합니다.
* 무엇이든 Red/Fail이면 **원인→최소 수정→재검증** 루프로만 해결합니다.

---

## 4) 변경 작업 표준 흐름 (Backup → Check → Execute → Verify)

### 4.1 Backup

* 브랜치 분기(또는 태그)로 안전핀을 만듭니다.
* 파일 대량 수정 전에는 `git diff`가 작게 유지되도록 쪼갭니다.

### 4.2 Check

* 영향 범위를 먼저 찾습니다(예: import rename이면 grep부터).
* CI/Branch Protection "체크 이름"은 **실제 Check-runs 이름**과 일치해야 합니다.

### 4.3 Execute (최소 변경)

* 목표 달성에 필요한 **최소한의 수정만** 합니다.
* 자동 포맷/린트 수정은 도구를 우선 사용합니다(ruff 등).

### 4.4 Verify (게이트 통과)

* 최소 기준(레포 정책):

  * `ruff check ...` (필요 시 `--fix`)
  * `pytest ...`
  * `shellcheck` (스크립트 변경 시)
  * `./afo trinity` (≥ 0.90 유지)

---

## 5) AFO 표준 명령 (Golden Path CLI)

가능하면 아래만 사용합니다.

```bash
./afo status
./afo trinity
./afo drift
./afo seal
./afo protect
./afo alert info "Title" "Message"
./afo release
./afo dashboard
./afo help
```

---

## 6) Python 패키지/임포트 규칙 (중요)

* 패키지명은 **`afo` (소문자)** 를 SSOT로 봅니다.
* Linux/Docker/CI는 대소문자 구분이 엄격합니다. `AFO` 참조가 남아있으면 **호환성 버그**입니다.
* `pyproject.toml`의 first-party/ruff 설정도 `afo` 기준으로 맞춥니다.

---

## 7) Git / PR / Main 보호 규칙

* **main에 직접 커밋/푸시하지 않습니다.** PR로만 머지합니다.
* Branch protection의 Required checks는 **실제 이름**으로만 설정합니다(예: `trinity-gate`, `shellcheck`, `quality-gate`).
* 최소 1명 승인, 최신 커밋 기준(strict), linear history 등은 유지합니다.
* 체크 이름이 어긋나면 "게이트가 깨진 것"으로 보고 **즉시 정합성 복구**가 우선입니다.

---

## 8) SSOT 봉인(Seal) 보고 포맷 (필수)

작업 완료 보고에는 아래 6요소를 **빈칸 없이** 포함합니다.

1. **As-of**: ISO8601+TZ
2. **HEAD**: full SHA(40)
3. **Summary**: 한 줄 변경 요약(증거 경로 포함)
4. **Repro**: 복붙 가능한 재현 커맨드
5. **Evidence**: 폴더 경로 + manifest.sha256
6. **Decision**: AUTO_RUN / ASK / BLOCK + 근거(Trinity/Risk/범위)

> 참고: `git rev-parse origin/main`은 **로컬 remote-tracking ref**이므로 네트워크가 없어도 확인됩니다.
> 네트워크가 필요한 것은 `git fetch origin` 입니다.

---

## 9) 금지 사항 (Do-Not)

* 존재하지 않는 파일/워크플로우/체크 이름을 "있는 것처럼" 말하기
* 큰 리팩터링을 한 번에 몰아서 진행하기
* secrets/토큰/개인정보를 출력/아티팩트에 남기기
* "시간 걸립니다/기다려주세요" 같은 비동기 약속(지금 실행/지금 결과만)

---

## 10) 하위 AGENTS.md

서브패키지의 `docs/AGENTS.md`가 존재하면, **그 문서는 해당 영역의 '추가 규칙(델타)'만** 담아야 합니다.
(글로벌 규칙을 반복하지 않습니다.)
