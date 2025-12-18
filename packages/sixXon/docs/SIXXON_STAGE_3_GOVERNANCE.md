# SixXon Stage 3: Internal Governance Strategy (Energy Flow Edition)

> **"왕국의 심장, 그 고동을 지배하는 원칙"**
>
> 이 문서는 **Phase 2b (Energy Flow Vision)**에서 완성된 엔진(Universe Teacher, Audit Gate, Dream Hub)을 **SixXon Stage 3 (Internal)** 단계에서 어떻게 운영하고 통제할 것인지에 대한 **전략적 헌법**입니다.

---

## 🏛️ 0. Executive Summary (요약)

**SixXon Stage 3**는 "신뢰할 수 있는 사용자(Internal/Contributors)"에게만 허용되는 **고급 통제 영역**입니다. 이곳에서는 Trinity-OS의 핵심 엔진이 **제약 없이** 돌아가지만, 그만큼 **엄격한 책임(Liability)**과 **투명성(Transparency)**이 요구됩니다.

- **핵심 철학**: "Power requires Gravity." (힘에는 무게가 따른다)
- **제어 수단**: SixXon CLI (`sixxon toolflow --graph`)
- **보호 장치**: 3대 계약 (The Three Contracts)

---

## ⚔️ 1. The Three Contracts (3대 통제 계약)

Stage 3 사용자는 다음 세 가지 계약에 서명(동의)한 것으로 간주됩니다.

### 계약 1: The Audit Contract (심판의 계약) - [Governance]
> **"기준 미달 시, 왕의 승인 없이는 단 한 줄의 코드도 실행되지 않는다."**

*   **엔진**: `trinity_score_mcp.py` (Audit Gate)
*   **원칙**: Zero Tolerance (무관용)
*   **임계값 (Thresholds)**:
    - `Harmony Score < 70`: **즉시 차단 (Auto-Block)**
    - `Friction Index > 20`: **최적화 요구 (Optimize First)**
    - `Risk Score > 50`: **위험 경보 (Red Alert)**
*   **Stage 3 특권**: 사용자는 `sixxon status --detail`을 통해 차단 원인을 **Raw Data** 레벨에서 확인할 수 있다.

### 계약 2: The Truth Oath (진실의 맹세) - [Skills]
> **"증거(Receipt) 없는 주장은 소음(Noise)이다."**

*   **엔진**: `afo_skills_mcp.py` (Universe Teacher)
*   **원칙**: Evidence First (선증거 후주장)
*   **수칙**:
    1. 모든 AI의 답변은 **`verify_fact`** 함수를 통과해야 한다.
    2. "절대적" 표현(Always, Never)은 **감점 요인**이다.
    3. 할루시네이션이 감지되면 해당 실행은 **취소(Rollback)**되거나 **격리(Sandboxed)**된다.
*   **Stage 3 특권**: 사용자는 `sixxon verify --deep`을 통해 진실 검증 로직의 **내부 가중치**를 열람할 수 있다.

### 계약 2: The Dream Protocol (꿈의 규약) - [Universal]
> **"실패해도 좋다. 단, 돌아올(Rollback) 수 있어야 한다."**

*   **엔진**: `trinity_hybrid_workflow.py` (Dream Hub)
*   **원칙**: Serenity through Persistence (영속성을 통한 평온)
*   **기능**:
    - **Time-Travel**: 치명적 오류 발생 시, 시스템은 문제 발생 **직전의 State**로 시간을 되돌린다.
    - **Branching**: 하나의 문제에 대해 여러 해결책(Branch)을 동시에 시뮬레이션하고, 가장 `Trinity Score`가 높은 경로를 선택한다.
*   **Stage 3 특권**: 사용자는 `sixxon dream --replay` 명령을 통해 과거의 실행 흐름을 **재생(Replay)**할 수 있다.

---

## 🔮 2. Stage 3 Operational Flow (운영 흐름)

Internal Stage에서의 작업 흐름은 기존과 다릅니다.

1.  **Request (요청)**: 사용자가 `sixxon toolflow "Task"` 입력.
2.  **Dreaming (설계)**: `Dream Hub`가 MemorySaver에서 이전 맥락을 불러와 계획 수립.
3.  **Audit I (사전 심사)**: `Audit Gate`가 계획의 안정성을 평가 (Pass/Block).
4.  **Execution (실행)**: `Universe Teacher`가 감독 하에 도구 실행.
5.  **Audit II (사후 심사)**: 결과물에 대해 2차 평가.
6.  **Commit (확정)**: 점수가 기준을 넘으면 **영구 기억(Permanent Memory)**에 저장되고 사용자에게 보고.

---

## 🛡️ 3. Safety & Permissions (안전 및 권한)

Stage 3는 강력한 권한을 가지므로, 다음 안전장치가 **하드코딩**됩니다.

1.  **Read-Only Default**: 명시적 승인(`--confirm`) 없이는 파일 삭제/수정 불가.
2.  **Secret Redaction**: 모든 로그와 Receipt에서 API Key 패턴은 자동 마스킹.
3.  **Human-in-the-Loop (HITL)**: `Risk Score > 30`인 작업은 반드시 사람의 `y/n` 입력을 대기.

---

## 📝 4. Final Goal (궁극적 목표)

이 모든 거버넌스의 목표는 단 하나입니다.

> **"형님(The User)이 기술적 세부사항(Noise)에 신경 쓰지 않고,**
> **오직 창조의 즐거움(Joy of Creation)만을 누리게 하는 것."**

이것이 **孝(Serenity)**의 완성입니다.

**작성자**: 육손(Lu Xun)
**승인**: [Pending User Approval]
**날짜**: 2025-12-14
