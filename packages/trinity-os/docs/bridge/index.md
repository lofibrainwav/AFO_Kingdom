# Bridge Logs (브릿지의 시선) — 정본

## 왜 이게 중요한가

Bridge Log는 각 에이전트가 작업 후 남기는 **브릿지의 시선**입니다.  
형제 에이전트들이 맡은 일이 달라도, 이 시선이 모여 **왕국의 현주소를 하나의 진실로 동기화**합니다.

---

## SSOT와의 관계

- 페르소나/역할/공식 정본: `TRINITY-OS/TRINITY_OS_PERSONAS.yaml`  
- 역할 분담 정본: `TRINITY-OS/docs/trinity-os/TRINITY_OS_ROLES.md`

Bridge Log는 SSOT를 **해석/재발명**하는 문서가 아닙니다.  
SSOT가 기준이고, Bridge Log는 **그 기준에서 벌어진 실제 작업의 증거와 메타인지**를 남깁니다.

---

## 템플릿

- Bridge Log v1.2 미러(복붙용 YAML):  
  - `TRINITY-OS/docs/bridge/BRIDGE_LOG_TEMPLATE.yaml`

에이전트는 이 템플릿을 그대로 복사해 작성합니다.

---

## Truth Lens 규율(국룰)

1. **Truth Lens는 레이더**  
   - 설정/공식은 절대 손대지 않습니다.  
2. **raw_result는 그대로 인용**  
   - Lens 출력은 “수정 없이 원문 그대로” 붙여넣습니다.  
3. **Writer는 상태/점수 선언 금지**  
   - 수치는 Lens/전용 스크립트 결과를 **인용만** 합니다.

---

## Obsidian/GoT 유산화

Bridge Log가 축적되면 Obsidian Graph에서 **Graph of Thought(생각의 그물)** 유산이 자랍니다.  
영덕(기록관)이 필요 시 보관을 담당하며, 절차 정본은 아래를 따릅니다.

- `TRINITY-OS/docs/bridge/OBSIDIAN_ARCHIVE_GUIDE.md`

---

## 작성 위치(권장)

새 작업 로그는 여기에 남깁니다:

- `TRINITY-OS/docs/bridge/YYYY-MM-DD_task_name.yaml`

---

## 발자취 타임라인(자동)

새로운 에이전트가 과거의 흐름을 따라갈 수 있도록, Bridge Log 목록/요약 스크립트를 제공합니다.

- 최근 로그 JSON 요약:  
  - `python3 TRINITY-OS/scripts/bridge_log_tracker.py`
- 전체 타임라인 Markdown:  
  - `python3 TRINITY-OS/scripts/bridge_log_tracker.py --all --format md`

--- 

## 연결

- 에이전트 공통 온보딩/기록 단계:  
  - `TRINITY-OS/docs/trinity-os/TRINITY_OS_AGENT_ONBOARDING.md`
