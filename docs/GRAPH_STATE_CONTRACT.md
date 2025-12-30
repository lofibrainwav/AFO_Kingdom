# GraphState/InputPayload Contract

> **As-of: 2025-12-29 | Version: v1.1**
> **眞善美孝永** - Chancellor Graph V2 데이터 계약 (Data Contract)

## 개요

Chancellor Graph V2에서 관리하는 `GraphState`와 입력 페이로드인 `InputPayload`의 구조와 제약 사항을 정의합니다.

---

## InputPayload 스키마

시스템에 전달되는 최초 입력 페이로드입니다.

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class InputPayload(BaseModel):
    command: str = Field(..., description="사령관의 명령 문구")
    skill_id: Optional[str] = Field(None, description="실행할 특정 Skill ID")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Skill 실행 인자")
    timeout: int = Field(30, description="최대 실행 시간 (초)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="추가 메타데이터")
```

---

## GraphState 구조

노드 간에 공유되는 상태 객체입니다.

| 필드 | 타입 | 설명 |
|------|------|------|
| `trace_id` | `str` | 실행 고유 트레이스 ID |
| `input` | `InputPayload` | 원본 입력 페이로드 |
| `plan` | `Dict[str, Any]` | PARSE 노드에서 생성한 실행 계획 |
| `outputs` | `Dict[str, Any]` | 각 노드별 처리 결과 (Contract 섹션 참조) |
| `errors` | `List[str]` | 실행 중 발생한 에러 목록 |
| `metadata` | `Dict[str, Any]` | 시스템 메타데이터 |

---

## 노드별 Output Contract

각 노드는 `state.outputs`에 정해진 키와 구조로 결과를 저장해야 합니다.

### 1. CONTEXT7 (Auto-injected)
```json
{
  "trace_init": { "KINGDOM_DNA": "..." },
  "NODE_NAME": {
    "library_id": "...",
    "topic": "...",
    "context": "..."
  }
}
```

### 2. PARSE
```json
{
  "skill_id": "skill_001_...",
  "parameters": { ... },
  "plan_description": "..."
}
```

### 3. TRUTH (제갈량 - 眞)
```json
{
  "score": 0.95,
  "technical_validation": "pass",
  "reasoning": "..."
}
```

### 4. GOODNESS (사마의 - 善)
```json
{
  "score": 0.90,
  "security_audit": "safe",
  "ethical_review": "approved"
}
```

### 5. BEAUTY (주유 - 美)
```json
{
  "score": 0.85,
  "ux_impact": "positive",
  "aesthetic_consistency": "high"
}
```

### 6. EXECUTE
```json
{
  "status": "success | blocked | fail",
  "result": { ... },
  "execution_time": 1.23,
  "reason": "..."
}
```

---

## 참고 자료

- [Chancellor Graph V2 완전 가이드](./CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md)
- [SSOT Import Paths](./SSOT_IMPORT_PATHS.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/SSOT_IMPORT_PATHS.md)
- [Failure Mode Matrix](./FAILURE_MODE_MATRIX.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/FAILURE_MODE_MATRIX.md)

---

**Trinity Score**: 眞 100% | 善 95% | 美 90% | 孝 95% | 永 100%
