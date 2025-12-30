# SSOT Import Paths (Single Source of Truth)

> **As-of: 2025-12-29 | Version: v1.1**
> **眞善美孝永** - AFO 왕국의 공식 임포트 경로 선언

## 공식 Import Path (SSOT)

### Chancellor Graph V2

```python
# ✅ 공식 경로 (SSOT)
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.state import GraphState
from api.chancellor_v2.graph.nodes import (
    execute_node,
    verify_node,
    rollback_node,
)
from api.chancellor_v2.context7 import inject_context, inject_kingdom_dna
from api.chancellor_v2.thinking import apply_sequential_thinking
```

### Context7

```python
# ✅ 공식 경로 (SSOT) - 서비스 레이어 사용
from AFO.services.context7_service import get_context7_instance, get_context7_health

# 사용
context7 = get_context7_instance()
knowledge = context7.retrieve_context("query")
```

### Sequential Thinking

```python
# ✅ 공식 경로 (SSOT) - MCP 클라이언트 사용
from AFO.services.mcp_stdio_client import call_tool

# 사용
result = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={"thought": "...", "thoughtNumber": 1, "totalThoughts": 1, "nextThoughtNeeded": False}
)
```

### Skills Registry

```python
# ✅ 공식 경로 (SSOT)
from AFO.afo_skills_registry import (
    SkillRegistry,
    AFOSkillCard,
    SkillCategory,
    ExecutionMode,
    PhilosophyScore,
    register_core_skills,
)

# 사용
registry = SkillRegistry()
if registry.count() < 5:
    register_core_skills()
skill = registry.get("skill_001_youtube_spec_gen")
```

### Settings & Config

```python
# ✅ 공식 경로 (SSOT)
from AFO.config.settings import get_settings

# 사용
settings = get_settings()
```

---

## 레거시/내부 경로 (사용 금지)

다음 경로들은 내부 구현용이며, 문서에 명시된 경우 외에는 사용을 금지합니다. 발견 시 즉시 마이그레이션이 필요합니다.

```python
# ⚠️ 레거시/내부 경로 (사용 금지)
# (Legacy import patterns are deprecated to ensure architectural purity.)
# (See AFO_V2_MIGRATION_GUIDE.md if needed.)

# ✅ 대신 서비스 레이어 사용
from AFO.services.context7_service import get_context7_instance  # ✅ 권장
from AFO.services.mcp_stdio_client import call_tool  # ✅ 권장
```

---

## Import Path 매핑표

| 컴포넌트 | 공식 경로 (SSOT) | 내부 구현 레이어 | 비고 |
|---------|-----------------|-----------------|------|
| Chancellor Graph V2 | `api.chancellor_v2.*` | - | 공식 경로만 존재 |
| Context7 Service | `AFO.services.context7_service` | Legacy servers (Hidden) | 서비스 레이어 사용 권장 |
| Sequential Thinking | `AFO.services.mcp_stdio_client` | Legacy servers (Hidden) | MCP 클라이언트 사용 권장 |
| Skills Registry | `AFO.afo_skills_registry` | - | 공식 경로만 존재 |
| Settings | `AFO.config.settings` | - | 공식 경로만 존재 |

---

## 사용 예제

### 예제 1: 완전한 통합 (권장)

```python
# ✅ 모든 공식 경로 사용
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import (
    cmd_node,
    parse_node,
    truth_node,
    goodness_node,
    beauty_node,
    merge_node,
    execute_node,
    verify_node,
    report_node,
)

# 실행 (Context7 + Sequential Thinking 자동 통합)
state = run_v2(input_payload, nodes)
```

---

## 참고 자료

- [Context7 완벽 활용 가이드](./CONTEXT7_COMPLETE_USAGE_GUIDE.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/CONTEXT7_COMPLETE_USAGE_GUIDE.md)
- [Sequential Thinking 완벽 활용 가이드](./SEQUENTIAL_THINKING_COMPLETE_USAGE_GUIDE.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/SEQUENTIAL_THINKING_COMPLETE_USAGE_GUIDE.md)
- [Skills 완벽 활용 가이드](./SKILLS_COMPLETE_USAGE_GUIDE.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/SKILLS_COMPLETE_USAGE_GUIDE.md)
- [Chancellor Graph V2 완전 가이드](./CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md)

---

**Trinity Score**: 眞 100% | 善 100% | 美 90% | 孝 95% | 永 100%
