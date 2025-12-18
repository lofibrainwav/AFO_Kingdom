# SIXXON TRINITY CODEX v1 (DRAFT → SSOT 분리본)

```
As-of: 2025-12-12 (America/Los_Angeles)
Scope: Trinity-OS + SixXon + Bridge
Rule: 정책(문서)과 구현(SSOT)은 분리한다.
```

## 0) 한 줄 정의 (왕국 표준)

- **Trinity-OS** = AFO 왕국 “전체 운영체제(두뇌+몸)”
- **SixXon** = 그 OS를 **겸손하게(美)**, **증거로(眞)**, **안전하게(善)**, **평온하게(孝)** 통제하는 조종석
- **Bridge** = 에이전트가 손댈 수 없는 **진실의 눈(오라클/감사 레이어)**
  - 에이전트는 Bridge를 “수정” 못 하고, **증거(Receipt)**만 “추가”합니다.

## 1) SSOT (진실의 기준선)

아래 3개가 “실제로 돌아가는 사실(眞)”의 기준입니다.

- Receipt Contract: `schemas/bridge_receipt_v1.json`
- Receipt Generator: `scripts/receipt_bundle.py`
- SixXon 구현(명령어/출력/판정): `TRINITY-OS/trinity_os/cli/sixxon.py`

> 문서에 없는 기능을 “있다”고 쓰지 않습니다.  
> 문서에 있어도 구현이 없으면 **Roadmap**으로 분류합니다.

## 2) 헌법/법전/권리장전 (요약)

- 眞(Truth): **증거 없으면 0** (주장/서술은 인정하지 않음)
- 善(Goodness): 위험/권한/비용은 DRY_RUN/ASK로 통제
- 美(Beauty): 기본 출력은 **3줄 요약** (과잉 노출 금지)
- 孝(Serenity): 형님의 평온이 최종 판단 변수
- 永(Eternity): 재현 가능(Receipt) + 감사 가능(로그) + 롤백 가능

상세(정본): `docs/TRINITY_COMPENDIUM.md`
권리장전(정본 부록): `docs/AFO_BRIDGE_BILL_OF_RIGHTS_v1.md`
교육자 어머니 2인제(정책 부록): `docs/TRINITY_COMPENDIUM_APPENDIX_E_EDUCATOR_MOTHERS.md`
파도 기록 조항(정책 부록): `docs/TRINITY_COMPENDIUM_APPENDIX_F_WAVE_RECORDING.md`

## 3) 샌드박스 vs 실환경 불일치 표준

- permission_denied / docker.sock 불가 / localhost 접근 불가:
  - **DOWN 단정 금지**
  - **UNKNOWN(context)** 로 기록
- 비교/결정은 **Receipt** 기준으로만 수행

정본(Contract): `docs/BRIDGE_RECEIPT_CONTRACT.md`

## 4) SixXon (현재 구현 범위)

정본: `docs/SIXXON_CLI_SPEC.md`

현재 구현된 명령(요약):
- `sixxon receipt` : Receipt 생성(증거 번들)
- `sixxon status` : Receipt 기반 상태 판정(Receipt 없으면 BLOCK)
- `sixxon toolflow` : TRINITY Toolflow 실행(기존 deps/graph 기반)

## 5) Roadmap (미구현: 문서/설계 항목)

아래는 “원하는 방향”이며, 구현되기 전까지는 **자동 집행/단정 금지**입니다.

- Cost Guard: `--budget`/`--approve` 기반 비용 가드
- `sixxon lens`: Bridge 오라클(MCP) 결과를 Receipt evidence로 첨부
- `sixxon ritual`: 아침 점호/정리 루틴 통합
- `sixxon dry-run`: 위험 작업 모의 실행 표준화

## 7) 반성(Reflection) 패턴에 대한 왕국 표준 해석 (정책)

형님이 말씀하신 “반성 패턴”은 **진실(眞)을 새로 만들어내는 엔진**이 아니라,
출력/절차를 **겸손하고 재현 가능하게 정리**하는 패턴으로 쓰는 것이 안전합니다.

- 반성(Reflection)은 **Receipt를 대체하지 않습니다.**
- 반성(Reflection)은 **UNKNOWN을 DOWN으로 바꾸지 않습니다.**
- 반성(Reflection)의 목적은:
  - (1) evidence 경로를 빠뜨리지 않기
  - (2) 3줄 요약을 지키기
  - (3) 다음 행동(Next)을 1개로 고정하기

즉, Bridge의 판정 로직은 그대로 두고(오라클),
에이전트/CLI는 “읽기 쉬운 보고(美/孝)”를 강화하는 용도로만 사용합니다.

## 6) 자룡(Claude)에게 주는 작업 방식(리밋 회피)

- “합본 전체 재작성” 금지 → **SSOT 파일에 링크/짧은 패치만** 반영
- 큰 문서는 **부록 파일로 분리**하고 본문은 1~2단락 요약만 유지
- 새 명령어를 문서에 추가할 때는:
  - (1) `TRINITY-OS/trinity_os/cli/sixxon.py`에 구현
  - (2) `docs/SIXXON_CLI_SPEC.md`에 “현재 구현”으로 이동
  - (3) 그 전까지는 Roadmap으로만 표기
