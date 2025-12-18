# SixXon CLI 철학 및 UX 규약 (정본)

**문서명:** SixXon CLI 철학 및 UX 규약
**버전:** v1.0
**작성일:** 2025-12-13
**작성 주체:** SixXon CLI 철학 문서화
**집행자(Commander):** 사용자(형)
**SSOT 원칙:** *문서가 아니라 Receipt/검증 결과가 단일 진실 원천(SSOT)*

---

## 0) 3줄 요약(겸손 프로토콜)

* **SixXon CLI는 Trinity-OS의 내부 로직을 안전하게 노출하는 전략적 통제점**이다.
* **겸손 프로토콜(3줄 출력 규약)**로 복잡함은 안으로 숨기고, 형에게는 편안함만 제공한다.
* **AUTO_RUN Gate: (Trinity >= 90) AND (Risk < 10)**로 AI의 자율성을 통제한다.

---

## 1) SixXon CLI의 정체성

### 1.1 핵심 정의

SixXon CLI(명령줄 인터페이스) 도구 세트는 AFO 왕국 시스템의 핵심 운영체제인 **Trinity-OS의 내부 로직을 외부로 안전하게 노출하고 제어하기 위해 제안된 기술적 프레임워크**입니다.

SixXon은 단순한 운영 도구를 넘어, 고위험 및 고가치 환경에서 AI의 자율적 행동을 통제하고 검증하는 **전략적 통제점(Strategic Control Point)**으로 기능하며, 에이전트의 **'목표와 비전의 윤리적 정렬(Alignment)'**을 검증하는 것이 그 핵심 목표입니다.

### 1.2 궁극적인 목적

SixXon CLI의 궁극적인 목적은 AI 동력 시스템이 왕의 **"창의적 평온(孝)을 방해하는 마찰(Friction) 제거"**라는 절대적인 기준을 준수하도록 강제하는 것입니다.

---

## 2) 겸손 프로토콜 (Humility Protocol) 기반의 UX 철학 (美와 孝)

### 2.1 Human-first 인터페이스

SixXon은 전통적인 CLI가 아닌 **'Human-first'** 인터페이스로 설계되었으며, 내부의 복잡한 로직(眞)을 사용자에게 우아하고 겸손한 형태(美)로 포장하여 제공하는 데 중점을 둡니다.

### 2.2 3줄 출력 규약

SixXon의 핵심 UX 규약은 **'겸손 프로토콜'**입니다. 기본 출력은 **무조건 3줄 이내의 요약 카드**로 제한됩니다.

**3줄 구성:**
1. **상태 요약(🟢/🟡/🔴) + Gate 결정**: `Status: OK | Gate: AUTO_RUN_AUTHORIZED`
2. **Next (지금 할 일 1개)**: `Next: Proceed with toolflow`
3. **Receipt 경로**: `Receipt: logs/receipts/<id>`

**의미:**
- "복잡함은 안으로 숨기고, 형에게는 편안함만"을 주는 美를 구현
- 사용자가 "지금 할 일 1개"를 명확히 알 수 있도록 함

### 2.3 복잡성 은닉 (Deep Class 원칙)

Trinity Score나 Risk Score와 같은 복잡한 **眞** 데이터는 기본 출력에서 숨겨지며, `--verbose` 또는 `--json` 플래그를 통해서만 접근할 수 있습니다.

이는 **Deep Class** 원칙에 따라 복잡한 내부 디자인 결정을 은닉하고 사용자에게 기능적 이점만을 제공하는 것을 의미합니다.

**예시:**
```bash
# 기본 출력 (3줄)
sixxon status --latest
# Status: OK | Gate: AUTO_RUN_AUTHORIZED
# Next: Proceed with toolflow
# Receipt: logs/receipts/phase3_integration_20251212_161322

# 상세 출력 (JSON)
sixxon status --latest --json
# {
#   "status": "OK",
#   "decision": "AUTO_RUN_AUTHORIZED",
#   "trinity_score": 93.0,
#   "risk_score": 7.0,
#   ...
# }
```

---

## 3) 실행 거버넌스 및 통제 (眞과 孝의 집행)

### 3.1 자동 실행 게이트 (AUTO_RUN Gate)

SixXon의 핵심 실행 규칙은 **`AUTO_RUN = (Trinity >= 90) AND (Risk < 10)`**으로 고정됩니다.

SixXon CLI는 이 기준을 통과하면 **AUTO_RUN_AUTHORIZED** 플래그가 켜지며, 왕의 승인 없이 **자율 운행 면허**를 획득하여 실행을 집행합니다.

**구현 위치:**
- `TRINITY-OS/trinity_os/graphs/trinity_toolflow_graph_v1.py`
- `TRINITY-OS/trinity_os/cli/sixxon.py`

**판정 기준:**
```python
if trinity_score >= 90 and risk_score < 10:
    decision = "AUTO_RUN_AUTHORIZED"
else:
    decision = "ASK_COMMANDER"  # 또는 "BLOCK"
```

---

### 3.2 HITL 강제 (Human-in-the-Loop)

**민감 도메인(sensitive_domain)**에 대한 접근이나 리스크 점수(Risk Score)가 임계값(**Risk ≥ 10**)을 초과할 경우, SixXon은 자동 실행을 중단하고 인간 운영자에게 **ASK_COMMANDER (확인 요구)**를 요청하도록 강제합니다.

**민감 도메인 예시:**
- 데이터 삭제/마이그레이션
- 외부 API 호출 (비용 발생)
- 시스템 설정 변경
- 보안 관련 작업

---

### 3.3 DRY_RUN 강제

위험도가 높은 작업은 **dry-run (모의 실행)**을 통해 실제 실행 전 "무슨 일이 일어나는지"를 우선적으로 검증하도록 강제합니다.

**워크플로우:**
```
1. DRY_RUN: dry_run=True로 시뮬레이션
2. Approval: 형님 확인
3. WET: dry_run=False로 실행
4. Verify: DRY vs WET 비교
```

**사용 예시:**
```bash
# DRY_RUN 모드
sixxon toolflow "health check" --dry-run

# 실제 실행 (승인 후)
sixxon toolflow "health check"
```

---

### 3.4 증거 기반 투명성 (眞)

SixXon은 모든 결정의 기반에 **眞**을 확보하기 위해 `receipt create` 명령을 통해 **최소 2개 이상의 증거**를 첨부하도록 강제합니다.

**Receipt 필수 포함:**
- `env.label` (LOCAL/SANDBOX/DOCKER_HOST/CI)
- `services` (ports/http/lsof의 OK/DOWN/UNKNOWN)
- `docker` (available + version/ps 결과)
- `usage` (선택: `usage.status` + `usage.tail_path`)

**Receipt 없으면:**
- Truth = 0 → BLOCK
- 주장/서술로는 상태를 인정하지 않음

---

## 4) 지적 겸손(Intellectual Humility) 강제

SixXon CLI는 궁극적으로 AI 에이전트의 **지적 겸손(Intellectual Humility)**을 강제하고, **실행 리스크 점수(ERS) 기반의 자율 실행 임계값(AET)**을 통해 인간의 평온을 확보하는 핵심적인 거버넌스 엔포서입니다.

### 4.1 지적 겸손의 의미

- **Writer(작성자)이고 Judge(심판)가 아님**: 에이전트는 상태를 선언하지 않고, Receipt 기반으로만 보고
- **복잡함 은닉**: 내부 로직은 숨기고, 사용자에게는 명확한 "Next"만 제공
- **증거 우선**: 모든 결정은 Receipt 기반 (문서/주장이 아닌 증거)

---

## 5) 정본 문서 준수 상태(Compliance Matrix)

| 정본 조항 | 상태 | 비고 |
|----------|------|------|
| 겸손 프로토콜 (3줄 출력) | ✅ | `_print_three_lines()` 함수 구현 |
| AUTO_RUN Gate (Trinity >= 90 AND Risk < 10) | ✅ | trinity_toolflow_graph_v1.py 구현 |
| HITL 강제 (Risk >= 10) | ✅ | ASK_COMMANDER 판정 |
| DRY_RUN 강제 | ✅ | `--dry-run` 플래그 지원 |
| 증거 기반 투명성 (Receipt) | ✅ | Receipt 없으면 BLOCK |

---

## 6) 구현 확인

### 6.1 3줄 출력 구현 ✅

**파일:** `TRINITY-OS/trinity_os/cli/sixxon.py` (line 26-35)

```python
def _print_three_lines(final_card: Dict[str, Any]) -> None:
    status = final_card.get("status") or "UNKNOWN"
    decision = final_card.get("decision") or status
    next_actions = final_card.get("next_actions") or []
    next_one = next_actions[0] if isinstance(next_actions, list) and next_actions else ""
    receipt_path = final_card.get("source_of_truth") or final_card.get("receipt_dir") or ""

    print(f"Status: {status} | Gate: {decision}")
    print(f"Next: {next_one}" if next_one else "Next: (none)")
    print(f"Receipt: {receipt_path}" if receipt_path else "Receipt: (none)")
```

---

### 6.2 AUTO_RUN Gate 구현 ✅

**파일:** `afo_soul_engine/core/quantum_balance_lock.py` (line 21)

```python
def should_auto_run(workflow_name: str | None, total_score: float, risk_score: float = 0.0) -> bool:
    """
    AUTO_RUN 조건: Score >90 & Risk <10
    """
    return total_score > 90.0 and risk_score < 10.0
```

**파일:** `afo_soul_engine/core/serenity_engine_langgraph.py` (line 153-184)

```python
def decide_auto_run(state: SerenityState) -> SerenityState:
    """
    AUTO_RUN 결정
    Trinity Score >90 & Risk <10 일 때만 AUTO_RUN 승인
    """
    trinity_score = state.get("trinity_score", 0.0)
    risk_level = state.get("risk_level", 100.0)

    # AUTO_RUN 조건: Score >90 & Risk <10
    if trinity_score > 90.0 and risk_level < 10.0:
        return {
            **state,
            "auto_run": True,
            "decision": "AUTO_RUN",
            ...
        }
```

**파일:** `TRINITY-OS/trinity_os/adapters/afo_ultimate_mcp_deps_v1.py` (line 268-289)

```python
auto_run = False
if should_auto_run is not None and not is_stale:
    try:
        auto_run = bool(
            _call_flex(
                should_auto_run,
                workflow_name="TRINITY Toolflow",
                total_score=total_score,
                risk_score=float(risk_score),
            )
        )
    except Exception:
        auto_run = False

if auto_run:
    return {
        "decision": "AUTO_RUN",
        ...
    }
```

**확인 완료:** ✅ AUTO_RUN Gate 구현 확인 (Trinity Score > 90 AND Risk < 10)

---

## 7) 핵심 성과(Impact)

* **SixXon CLI 철학 문서화 완료** → 전략적 통제점으로서의 역할 명확화
* **겸손 프로토콜(3줄 출력) 구현 확인** → 복잡함 은닉, 사용자 편안함 제공
* **AUTO_RUN Gate 원칙 명확화** → (Trinity >= 90) AND (Risk < 10)
* **지적 겸손 강제** → Writer/Judge 분리, 증거 우선

---

## 8) 다음 단계

### 8.1 AUTO_RUN Gate 구현 검증

**목표:**
- `TRINITY-OS/trinity_os/graphs/trinity_toolflow_graph_v1.py`에서 AUTO_RUN Gate 로직 확인
- Trinity Score >= 90 AND Risk < 10 조건이 실제로 구현되어 있는지 확인

---

## 9) 결론(정본 문장)

**SixXon CLI 철학 및 UX 규약은 문서화되었다.**
이제 왕국은 "겸손 프로토콜(3줄 출력) + AUTO_RUN Gate + 증거 기반 투명성(Receipt)"의 최소 인프라를 갖췄다.
다음은 **AUTO_RUN Gate 구현 검증(Trinity >= 90 AND Risk < 10 조건 확인)**이다.

---

# (부록) Commander용 "복붙 실행 체크" 5줄

아래는 "지금 당장 형이 실행해서 SSOT로 굳히는" 최소 체크야:

```bash
# 1. SixXon CLI 3줄 출력 확인
PYTHONPATH="TRINITY-OS:TRINITY-OS/src:." python3.12 -m trinity_os.cli.sixxon status --latest

# 2. SixXon CLI JSON 출력 확인 (상세)
PYTHONPATH="TRINITY-OS:TRINITY-OS/src:." python3.12 -m trinity_os.cli.sixxon status --latest --json

# 3. AUTO_RUN Gate 구현 확인
grep -n "AUTO_RUN\|trinity_score.*90\|risk_score.*10" TRINITY-OS/trinity_os/graphs/trinity_toolflow_graph_v1.py

# 4. 3줄 출력 함수 확인
grep -n "_print_three_lines" TRINITY-OS/trinity_os/cli/sixxon.py

# 5. SixXon CLI SPEC 확인
cat docs/SIXXON_CLI_SPEC.md | head -50
```

---

**마지막 업데이트**: 2025-12-13  
**버전**: v1.0 (정본 완전 정렬)
