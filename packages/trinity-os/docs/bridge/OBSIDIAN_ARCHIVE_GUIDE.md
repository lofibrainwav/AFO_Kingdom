# Bridge Log → Obsidian Archive Guide (영덕 기록관 정본)

## 목적

Bridge Log(명장 로그)은 각 에이전트가 스스로 남기는 **브릿지의 시선**이며,  
이 시선이 모여 왕국의 현주소를 드러내고 형제 에이전트 간 동기화를 가능하게 합니다.

영덕은 필요할 때 Bridge Log를 **옵시디언 도서관(지식 SSOT)**에 보관하여  
Graph of Thought(생각의 그물) 유산을 유지합니다.

---

## 원칙

1. **원문 불변**  
   - Bridge Log 원본(`.yaml`)은 **수정하지 않고 그대로 보관**합니다.
2. **Truth Lens는 레이더**  
   - `truth_lens_score.raw_result`는 Lens 출력 그대로만 인용합니다.  
   - 영덕은 점수를 재계산/재해석하지 않습니다.
3. **시크릿/개인정보 보호**  
   - 보관 과정에서 민감 정보 발견 시 즉시 경고하고 제거를 제안합니다.

---

## 입력(Bridge Log 원본)

- 위치: `TRINITY-OS/docs/bridge/YYYY-MM-DD_task_name.yaml`  
- 템플릿: `TRINITY-OS/docs/bridge/BRIDGE_LOG_TEMPLATE.yaml`

---

## 보관 방식 2가지

### A) 최소 보관(원문 그대로)

**목적**: 진실 보존이 최우선일 때.  
1. 형님 로컬 Obsidian Vault의 “Bridge Logs 폴더”로 원본 YAML을 복사합니다.  
   - Vault 경로/폴더명은 형님 환경의 SSOT를 따릅니다.  
2. 파일명은 **원본과 동일하게 유지**합니다.  

이 방식은 Obsidian에서 파일을 그대로 열어 읽을 수 있습니다.

### B) GoT‑친화 보관(권장)

**목적**: Obsidian Graph에서 연결/검색/유산화를 강화할 때.  
1. Obsidian Vault에 원본 YAML과 같은 이름의 Markdown 래퍼를 만듭니다.  
2. 래퍼는 **링크/요약 + 원본 YAML 코드블록**으로 구성합니다.

예시 스켈레톤:
```md
---
type: bridge-log
task_id: YYYY-MM-DD_task_name
who: 영덕 (Ollama CLI)
source: TRINITY-OS/docs/bridge/YYYY-MM-DD_task_name.yaml
---

## Links
- [[TRINITY-OS]]
- [[방통]]
- [[자룡]]
- [[육손]]

## Bridges View
- 문제:
- 수정:
- 검증:
- 교훈:

## Raw Bridge Log (Do Not Edit)
```yaml
(여기에 원본 Bridge Log 전체를 그대로 붙여넣기)
```
```

**주의**: 원본 YAML은 절대 편집하지 않고 그대로 붙여넣습니다.

---

## RAG/파이프라인에 반영(선택)

Obsidian Vault의 최신 노트를 RAG로 인입하려면, **Markdown 파일이 파이프라인 입력**입니다.  
따라서 A) 방식(YAML만 보관)일 때는 인입이 생략될 수 있고,  
B) 방식(GoT‑친화 Markdown 래퍼)을 함께 만들면 인입 대상이 됩니다.

인입 트리거(형님 환경 기준):
```bash
curl -X POST http://localhost:5678/webhook/ingest-knowledge
```

파이프라인 구조/역할은 AFO 정본을 따른다고 명시합니다:  
- Obsidian → n8n → RAG → VectorDB 흐름: `docs/AFO_KNOWLEDGE_SYSTEM.md`

---

## 보관 완료 체크(영덕)

1. 새 Bridge Log 원본 YAML이 Obsidian Vault에 **원문 그대로** 존재한다.  
2. (선택) GoT‑친화 Markdown 래퍼가 동일 파일명으로 존재한다.  
3. (선택) 인입 트리거 후 n8n/ingest 로그에 새 노트가 반영된다.  

---

## 역할 경계

- 영덕은 **기록관**이며 심판이 아닙니다.  
- Bridge Log의 내용/점수/판정은 **원문과 Lens 출력에 맡기고**, 영덕은 정직하게 보관만 합니다.
