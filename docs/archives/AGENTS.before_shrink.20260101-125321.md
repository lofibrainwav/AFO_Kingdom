# AGENTS.md — AFO Kingdom (Root)

이 문서는 **레포 전역(루트) 공통 규칙**입니다.
세부 구현 규칙은 하위 도메인 문서를 우선합니다:

- `./packages/afo-core/docs/AGENTS.md`
- `./packages/dashboard/docs/AGENTS.md`
- `./packages/trinity-os/AGENTS.md`

---

## 0) 10초 프로토콜 (작업 시작 전 필수)

작업을 시작할 때 아래 5가지를 **짧게** 먼저 제시합니다.

1) `decision`: AUTO_RUN / ASK_COMMANDER / BLOCK
2) `evidence`: (읽은 SSOT/코드/로그 경로 2개 이상)
3) `plan`: (3~7 step)
4) `checks_to_run`: (실행할 검증 커맨드 1~4개)
5) `rollback_plan`: (git 기반 되돌리기 경로)

권장: 아래 JSON Contract로 동일 내용을 구조화합니다.

```json
{
  "decision": "AUTO_RUN | ASK_COMMANDER | BLOCK",
  "trinity_score": 0,
  "risk_score": 0,
  "assumptions": [],
  "evidence": [],
  "plan": [],
  "files_to_touch": [],
  "checks_to_run": [],
  "rollback_plan": [],
  "open_questions": []
}
```

---

## 1) SSOT 읽는 순서 (존재하는 것만)

작업 전, 아래 파일의 **존재 여부를 repo에서 확인**하고, 있는 것만 근거로 사용합니다.

1. `docs/AFO_ROYAL_LIBRARY.md`
2. `docs/AFO_CHANCELLOR_GRAPH_SPEC.md`
3. `docs/AFO_EVOLUTION_LOG.md` 또는 `AFO_EVOLUTION_LOG.md`
4. `docs/AFO_FRONTEND_ARCH.md`
5. `docs/CURSOR_MCP_SETUP.md`

---

## 2) 결정 게이트 (AUTO_RUN / ASK / BLOCK)

* **AUTO_RUN**: Trinity Score ≥ 0.90 AND Risk Score ≤ 10
* **ASK_COMMANDER**: 위 조건 미충족
* **BLOCK**: 아래 중 하나라도 해당하면 즉시 중단(명시 승인 전까지)

  * Secrets/Keys/Tokens/PII
  * Auth/Billing/Payment
  * Prod 배포/Infra(DNS/Terraform/Caddy/Cloudflare 등)
  * DB/데이터 삭제 등 비가역 변경
  * lockfile/의존성 변경이 불가피한데 영향 범위가 불명확

Risk Score 가이드(요약):

* Auth/Payment/Secrets/Prod: +60
* DB/데이터/비가역: +40
* 의존성 업데이트/대규모 리팩터: +30
* 테스트 부재 상태에서 핵심 로직 변경: +25
* 문서/소규모 버그/UI: +5~10

---

## 3) 안전 파이프라인 (고정)

**Backup → Check → Execute → Verify**

* Backup: 변경 전 롤백 경로 확보(브랜치/태그/커밋)
* Check: 현상 재현 + "커맨드/스크립트"는 추측하지 말고 발견
* Execute: 최소 변경(요청 범위 밖 "겸사겸사 정리" 금지)
* Verify: 변경 영역에 맞는 검증을 실제로 실행하고 로그를 남김

---

## 4) Boundaries (명시 지시 없이는 금지)

* Secrets/Keys/Tokens/개인정보
* Auth/Billing/Payment 로직
* Prod 배포/Infra(Terraform, DNS, Caddy, Cloudflare 등)
* `vendor/`, `dist/`, `build/` 등 생성물/외부 의존 디렉토리
* lockfile은 "설치/빌드가 요구할 때만" 변경(근거/로그 필수)

---

## 5) 커맨드/스크립트 규칙 (추측 금지)

* Node/TS: `package.json`의 `scripts`에서만 실행
* Python: `pyproject.toml` / `Makefile` / `scripts/`에서만 실행
* CI 기준은 `.github/workflows/`로 확인

lockfile로 패키지 매니저 판별:

* `pnpm-lock.yaml` → pnpm
* `yarn.lock` → yarn
* `package-lock.json` → npm
* lockfile이 여러 개면 **ASK_COMMANDER**

---

## 6) 완료(DoD) & 보고 규칙

### ⚠️ 완료 선언 금지 (증거 없으면 "완료"라고 말하지 않습니다)

완료 선언 조건(아래 4개 모두 필요):

1. git commit hash
2. 변경 파일 목록
3. 실행 커맨드 + 결과
4. 테스트 통과 증거

허용 표현: "분석 결과", "제안", "검증 필요"
금지 표현: "완료", "implemented", "resolved", "completed"

### Definition of Done (측정 가능)

* 眞: 구현 파일 + 실행 로그 1개
* 善: CI(Trinity Gate + Shellcheck 등) PASS
* 美: 문서 1개 + 사용 예시
* 孝: `./afo` 원샷 실행 + 실패 시 명확 메시지
* 永: Evidence(sha256/manifest) + Seal Tag

---

## 7) 절대 금지

* 시크릿/토큰/PII를 로그/커밋/리포트에 포함
* force push / history rewrite (명시 승인 전 금지)
* "이미 푸시/머지했다" 같은 비동기 완료 주장
* 테스트 미통과 상태에서 "해결" 단정

끝.
