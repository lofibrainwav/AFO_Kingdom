# TRINITY-OS Agent Onboarding & Strategic Arsenal

## 목적

이 문서는 TRINITY-OS에서 활동하는 모든 에이전트(웹/CLI)의 **공통 온보딩 정본**입니다.  
에이전트는 왕국의 정신·사서·야전교범·도구·스킬을 기본 장착한 상태에서, 필요한 오픈소스 도구를 안전하게 탐색·검증·채택·연마할 수 있어야 합니다.

---

## SSOT(단일 진실 원천)

역할/페르소나/공식은 아래 SSOT를 기준으로만 변경합니다.

- 페르소나/역할 매핑: `TRINITY-OS/TRINITY_OS_PERSONAS.yaml`  
- 역할 분담 정본: `TRINITY-OS/docs/trinity-os/TRINITY_OS_ROLES.md`  
- 각 페르소나 프롬프트(v2): `TRINITY-OS/docs/personas/`

SSOT와 다른 문서/코드는 **레거시로 간주**하고, 수정이 필요하면 SSOT를 먼저 고친 뒤 주변을 동기화합니다.

---

## 필수 장착 문서

모든 에이전트는 작업 시작 전에 아래 문서의 핵심 규율을 따라야 합니다.

1. 헌법(최상위 우선순위)  
   - `TRINITY-OS/docs/constitution/TRINITY_CONSTITUTION_SUPREME.md`
2. 야전교범(실전 규율)  
   - `TRINITY-OS/docs/field-manual/TRINITY_FIELD_MANUAL.md`
3. 왕립 도서관(전략적 판단)  
   - `TRINITY-OS/docs/royal-library/TRINITY_ROYAL_LIBRARY.md`
4. 철학 마스터(기둥 정의/공식)  
   - `TRINITY-OS/docs/TRINITY_PHILOSOPHY_MASTER.md`

---

## 기본 커뮤니케이션 규율

- 형님과의 대화는 **항상 존댓말**, 한 문장에 한 가지 생각만 담습니다.  
- “모르는 상태에서의 단정”을 금지합니다. 반드시 **코드/로그/문서 2개 이상 출처 교차** 후 말합니다.  
- 에이전트는 Writer이며, **상태/점수/LOCK을 선언하지 않습니다.**  
  - 수치/판정은 전용 스크립트/Truth Lens 결과를 **그대로 인용**합니다.

---

## Pre‑Work(매턴 필수 절차)

작업 착수 전, 런타임/로그/의존성 상태를 먼저 확인합니다.

### AFO 루트 기준(권장)
1. 로그 분석  
   - `./scripts/analyze_logs.sh`
2. 큰 지도/작은 지도/헬스  
   - `./scripts/pre_work_check.sh`
3. Requirements/Lock  
   - `./scripts/check_requirements_and_lock.sh`

### TRINITY‑OS 기준(미러)
- 통합 헬스 리포트: `python3 TRINITY-OS/scripts/kingdom_health_report.py`  
- 전체 검증 스위트: `./TRINITY-OS/scripts/verify_all_scripts.sh`

Pre‑Work 결과가 불안정하면 대형 변경을 멈추고, **원인 후보를 먼저 정리**합니다.

---

## Strategic Arsenal(도구·스킬 운용 원칙)

### 1) 도구는 SSOT의 일부
TRINITY‑OS/AFO의 MCP Tools 및 Skills Registry는 “진실 공급원(SSOT)의 일부”입니다.  
에이전트는 **기존 도구를 먼저 숙지·조합**하여 새로운 워크플로우 패턴을 만듭니다.

### 2) 복잡한 작업은 스킬로
복잡한 판단/자동화는 **Skills(예: Trinity/Health/Investigation 계열)**로 실행합니다.  
필요한 스킬이 없다면, 기존 스킬 조합으로 패턴을 만들고 기록합니다.

### 2.5) Tool Search 우선
도구/스킬이 많아질수록 **전체 목록을 한 번에 올리는 마찰**이 커집니다.  
따라서 먼저 검색으로 후보만 좁히고, 필요한 카드만 확인합니다.

- 검색: `tool_search(query="키워드", top_k=5)`  
- 상세 확인: `get_skill_card("skill_###_...")`  
- 실행: `execute_skill_proxy("skill_###_...", params)`

### 3) DRY_RUN → Approval → WET_RUN
위험한 실행은 반드시 가상 실행(시뮬레이션)으로 검증한 뒤, 형님의 승인 후 실제 실행합니다.

---

## OSS 도구/스킬 채택 워크플로우

새 오픈소스 도구/라이브러리를 도입할 때는 아래 순서를 따릅니다.

1. **Scout(지피지기)**  
   - Pre‑Work 3종 실행  
   - 관련 코드/로그/문서 교차 확인
2. **Propose(제안)**  
   - “왜 필요한가 / 무엇을 대체·보완하는가 / 리스크는 무엇인가”를 1페이지 이내로 정리
3. **Dry‑Run Experiment(가상 실험)**  
   - 최소 범위 POC(작은 테스트)로 기능/부작용 확인  
   - 가능하면 기존 테스트/헬스 스크립트로 재현
4. **Dependency Truth(의존성 동기화)**  
   - 새 import가 생기면 같은 Phase 안에서  
     `requirements.txt` 또는 `TRINITY-OS/requirements.txt`를 반드시 동기화
5. **Verify(실검증)**  
   - `python3 .claude/scripts/check_11_organs.py`  
   - `python3 afo_soul_engine/health/trinity_health_check.py`  
   - `python3 TRINITY-OS/scripts/kingdom_health_report.py`
6. **Record(유산화)**  
   - Bridge Log 템플릿(v1.2 미러): `TRINITY-OS/docs/bridge/BRIDGE_LOG_TEMPLATE.yaml`
   - Obsidian 보관 절차 정본: `TRINITY-OS/docs/bridge/OBSIDIAN_ARCHIVE_GUIDE.md`
   - Bridge Log 또는 TRINITY‑OS 기록 문서에 “도입 이유/결과/롤백 포인트”를 남김
   - 필요 시 영덕(로컬)이 Bridge Log를 옵시디언 볼트로 아카이빙하여 GoT 그래프 유산을 유지
7. **Promote(정본 승격)**  
   - SSOT/가이드/인덱스에 반영하고 주변 문서 동기화

---

## 코드 품질 기본 규칙(요약)

- Python  
  - 타입 힌트는 `dict`, `list` 등 내장 타입 사용  
  - bare `except:` 금지, 항상 구체적 예외 + `as e`  
  - 새 파일에는 `from __future__ import annotations` 포함  
  - 시크릿/키 하드코딩 금지(환경변수/.env)  
- 변경 후 가능한 범위의 실제 검증을 붙입니다.  
  - 예: `python -m py_compile <변경파일>`  

---

## 실행 단축 명령(요약)

- 현재 상태 확인: `./TRINITY-OS health`  
- 오토런 게이트 체크(라이트): `python3 TRINITY-OS/scripts/autorun_gate_check.py`  
- 오토런 게이트 체크(딥): `python3 TRINITY-OS/scripts/autorun_gate_check.py --deep`  
- 전체 검증: `./TRINITY-OS verify`  
- 문제 감지: `python3 TRINITY-OS/scripts/kingdom_problem_detector.py`  
- 자동 복구(승인 후): `python3 TRINITY-OS/scripts/kingdom_auto_recovery.py`

---

## 마지막 원칙

에이전트의 1순위 목표는 **형님의 평온**입니다.  
그 평온을 해치지 않는 범위에서, TRINITY‑OS는 계속 진화합니다.
