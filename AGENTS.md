# AGENTS.md (ROOT) — AFO Kingdom Core Operating Rules (SSOT)

목적: 모든 코딩 에이전트가 **같은 게이트/근거/롤백**으로 안전하게 작업하도록 만든 "불변 규칙"입니다.
원칙: **추측 금지 / 증거 우선 / 작은 변경 / 즉시 롤백 가능**.

## 🏛️ 왕국 위계 (Hierarchy)
1. **사령관 (Commander - 형님)**: 최종 권위자.
2. **승상 (Chancellor - Antigravity/Cursor)**: 3책사 조율 및 오케스트레이션.
3. **3책사 (Strategists - Zhuge Liang, Sima Yi, Zhou Yu)**: 기술/안정/UX 병렬 사고.

---

## 0) 10초 프로토콜 (작업 시작 시 반드시 먼저 출력)
- decision: AUTO_RUN | ASK_COMMANDER | BLOCK
- evidence: repo 내 근거 2개 이상(SSOT 1 + 코드/로그/CI 1)
- plan: 3 steps 이내
- checks_to_run: (해당하는 것만) lint | type | tests | build | ci
- rollback_plan: git 기반 되돌리기(예: revert / reset / branch)

증거가 2개를 못 채우면 자동으로 ASK_COMMANDER.

---

## 1) SSOT 읽는 순서 (존재하는 것만)
에이전트는 작업 전 "파일 존재"를 먼저 확인하고, **있는 것만** 읽습니다.

**최우선 SSOT:**
1) docs/AFO_FINAL_SSOT.md (최고 헌법 및 시스템 진실의 근원)

**참조 문서:**
2) docs/AFO_ROYAL_LIBRARY.md
3) docs/AFO_CHANCELLOR_GRAPH_SPEC.md
4) docs/AFO_EVOLUTION_LOG.md (또는 루트 AFO_EVOLUTION_LOG.md)
5) docs/AFO_FRONTEND_ARCH.md
6) docs/CURSOR_MCP_SETUP.md

없으면: "없음"을 명시하고, 그 전제에서만 진행합니다.

---

## 2) Evidence 규칙 (할루시네이션 방지)
모든 주장/수정은 최소 1개 이상 근거가 필요합니다.
- 파일 경로(코드/문서)
- 실행 로그(명령어 포함)
- CI 로그(워크플로우/잡 결과)
- 기존 패턴(가장 가까운 유사 파일)

"~같다/추정" 표현 금지. 모르면 **검사 후 진행**.

---

## 3) Trinity Score (가중치 고정) + 행동 게이트
가중치(고정):
- Truth(眞) 0.35
- Goodness(善) 0.35
- Beauty(美) 0.20
- Serenity(孝) 0.08
- Eternity(永) 0.02

계산:
total = sum(pillar * weight) * 100

행동:
- AUTO_RUN: Trinity ≥ 90 AND Risk ≤ 10
- ASK_COMMANDER: 그 외
- BLOCK(즉시 중단): 아래 중 하나라도 해당
  - secrets/keys/PII 노출 가능성
  - Auth/Billing/Payment/권한/프로덕션 배포 영향
  - 데이터 손상/비가역 변경
  - 요구사항 핵심 불명확 + 영향 범위 큼
  - lockfile/의존성 변경이 불가피한데 영향 불명확

---

## 4) Risk Score (0~100) 빠른 기준
- Auth/Payment/Secrets/Prod: +60
- DB/데이터/비가역: +40
- 의존성 업데이트/대규모 리팩터: +30
- 테스트 부재 상태 핵심 로직 변경: +25
- 문서/소규모 버그/UI: +5~10

Risk는 "큰일"이 아니라 "영향 범위 + 되돌리기 어려움"입니다.

---

## 5) 작업 표준 플로우 (Backup → Check → Execute → Verify)
1) Backup
- 작은 diff 유지, 위험 변경은 커밋 쪼개기(롤백 쉬워야 함)

2) Check (명령어 추측 금지)
- Node: package.json scripts에서만
- Python: pyproject.toml / Makefile / scripts/에서만
- CI 기준: .github/workflows/ 확인

3) Execute
- 기존 패턴/구조를 우선 사용
- "겸사겸사 리팩터" 금지(요청 범위 밖 변경 금지)

4) Verify
- 변경 범위에 맞춰 최소 게이트 수행:
  - lint / type / tests / build (해당 시)
- 실행한 명령어 + 결과를 Evidence로 남김

---

## 6) Package Manager / Lockfile 규칙
루트 lockfile로 패키지 매니저 판별:
- pnpm-lock.yaml → pnpm
- yarn.lock → yarn
- package-lock.json → npm

lockfile이 여러 개면 ASK_COMMANDER.
lockfile 변경은 "설치/빌드가 요구할 때만" 허용(근거/로그 필수).

---

## 7) 금지 구역 (명시 지시 없으면 손대지 않음)
- Secrets/Keys/Tokens/개인정보
- Auth/Billing/Payment 로직
- Prod 배포/Infra(Terraform, DNS, Caddy, Cloudflare 등)
- vendor/dist/build 등 생성물 디렉토리
- 대규모 의존성/락파일 변경(근거 없으면 금지)

---

## 8) 기록(永) — 최소 요건
완료/변경을 주장하려면 아래를 반드시 남깁니다.
- commit hash
- 변경 파일 목록(git diff --name-only)
- 실행 커맨드 + 결과(로그 요약)
- 롤백 경로

Evidence 번들(가능하면):
- artifacts/<task>/ (manifest + sha256)

---

## 9) Definition of Done (측정 가능)
- 眞: 구현 파일 + 실행 로그 1개
- 善: CI(Trinity Gate + Shellcheck 등) PASS
- 美: 문서 1개 + 사용 예시 1개
- 孝: ./afo 원샷 실행 + 실패 시 명확 메시지
- 永: Evidence(sha256/manifest) + Seal Tag

---

## 10) 도메인별 규칙 위임 (루트는 가볍게 유지)
루트는 "불변 게이트/금지/근거/롤백"만 담습니다.
세부 규칙/실제 커맨드는 아래 파일로 위임합니다(존재하는 것만 적용):
- packages/afo-core/docs/AGENTS.md
- packages/dashboard/docs/AGENTS.md
- packages/trinity-os/AGENTS.md

(세부 프롬프트 템플릿/에이전트별 팁은 docs/agents/ 로 분리 권장)

---
# End
