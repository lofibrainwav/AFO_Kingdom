# AGENTS.md — AFO Kingdom (Ops-Only, SSOT)

이 문서는 **이 레포에서 작업하는 모든 AI 에이전트/자동화**의 "운영 규칙"입니다.
목표는 **실수(환각/추측/대충) 없이**, **증거(SSOT)로만** 작업을 끝내는 것입니다.

---

## 0) 절대 금지 (Non-negotiables)

- **추측 금지**: 파일/경로/커맨드/환경변수/버전은 **직접 확인** 후 진행합니다.
- **증거 없는 완료 선언 금지**: "완료/성공"은 **재현 커맨드 + 원본 출력 + 증거 파일**이 있을 때만.
- **CI가 자동 수정해줄 거라는 가정 금지**: CI는 보통 "검사/차단"만 합니다. 자동 fix는 로컬/전용 봇에서만.
- **보안/프로덕션 영향 작업은 무조건 보수적으로**: 위험하면 멈추고 ASK.
- **실존하지 않는 링크/URL/기능 언급 금지**.

---

## 1) 의사결정 게이트 (Decision Gate)

- **AUTO_RUN**: Trinity ≥ 0.92 **AND** Risk < 10 **AND** 변경 범위가 작음
- **ASK**: 위 조건 미달(불확실/큰 변경/증거 부족)
- **BLOCK**: 보안/배포/브랜치 보호/권한/데이터 손상 위험이 크거나 증거가 없을 때

> Risk 예시: force-push, branch protection 변경, secrets 처리, 대규모 리팩터링, 마이그레이션

---

## 2) 표준 실행 루프 (Status → Plan → Backup → Execute → Verify → Seal)

### Phase-0: Status (현상 파악)
필수 확인(최소):
```bash
git status -sb
git rev-parse HEAD
./afo status
./afo trinity
./afo drift
```

### Phase-1: Plan (작업 계획)

* "무엇을/왜/어떻게/어떻게 검증할지"를 **짧은 체크리스트**로 먼저 씁니다.
* 큰 변경은 **작게 쪼개서** 커밋/롤백 가능하게 합니다.

### Phase-2: Backup (롤백 확보)

* 파일 변경 전 백업/브랜치/커밋으로 롤백 경로를 만듭니다.

### Phase-3: Execute (최소 변경)

* **diff 최소화**, 불필요한 리포맷/대규모 이동 금지(필요할 때만).

### Phase-4: Verify (증거 수집)

최소 검증 세트(프로젝트가 있는 도구만 사용):

```bash
./afo trinity
./afo drift

# 프로젝트가 사용하는 경우에만 실행
ruff check .
pytest -q

# 스크립트가 있는 경우에만 실행
shellcheck -x scripts/*.sh
```

### Phase-5: Seal (SSOT 봉인)

```bash
./afo seal
./afo alert info "SSOT Seal" "sealed evidence bundle created"
```

---

## 3) SSOT 리포트 포맷 (에이전트 출력 규격)

에이전트는 결과 보고 시 아래 6개를 **항상 포함**합니다.

1. **As-of(ISO8601)**
2. **HEAD(커밋 SHA)** / **origin 동기화 여부**
3. **변경 요약(한 줄)**
4. **재현 커맨드(복붙 가능)**
5. **Evidence 경로(artifacts/…)** + manifest/sha256 존재
6. **Decision(AUTO_RUN/ASK/BLOCK)** + 근거

---

## 4) 레포 불변 규칙 (Repo Invariants)

* Python 패키지/모듈 이름은 **`afo`(소문자)** 를 기준으로 합니다.
  (Linux/CI는 대소문자 구분. `AFO` 참조가 남아있으면 깨질 수 있습니다.)
* 스크립트는 기본적으로 `set -euo pipefail` + fail-fast를 유지합니다.
* Branch Protection Required Checks의 **이름은 실제 Check-run 이름과 100% 일치**해야 합니다.
  (이름이 다르면 "통과했는데도 머지 차단"이 발생합니다.)

---

## 5) CI / Branch Protection (체크 이름 표준)

As-of **2026-01-01**, main 보호에서 사용하는 대표 Required Checks 예시:

* `trinity-gate`
* `shellcheck`
* `quality-gate`

> 체크 이름을 바꾸면: **워크플로우(job name) 변경 + Branch Protection 설정**을 같이 수정합니다.

---

## 6) 커밋/PR 규칙 (실수 줄이기)

* 커밋은 작게(롤백 쉬움), 메시지는 "무엇을 바꿨는지"가 바로 보이게.
* PR에는 최소:

  * 변경 이유
  * 검증 로그(또는 CI 링크)
  * evidence bundle 경로(있으면)

---

## 7) 빠른 커맨드 레퍼런스 (Golden Path)

```bash
./afo help
./afo status
./afo trinity
./afo drift
./afo seal
./afo protect
./afo alert info "Title" "Message"
./afo release
./afo dashboard
