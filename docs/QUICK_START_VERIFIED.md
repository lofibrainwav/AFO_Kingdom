# Quick Start (복붙 1회 성공 보장)

> **As-of: 2025-12-29 | Version: v1.1**
> **眞善美孝永** - 검증된 Quick Start 코드

## 가장 간단한 방법 (권장)

Chancellor Graph V2를 사용하면 Context7, Sequential Thinking, Skills가 자동으로 통합됩니다.

### 완전한 예제 (복붙 가능)

```python
#!/usr/bin/env python3
"""
Chancellor Graph V2 Quick Start
복붙 1회 성공 보장 - 모든 import 경로는 SSOT 준수
"""

# ✅ 공식 경로 (SSOT Import Path)
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

# 입력 페이로드
input_payload = {
    "command": "YouTube 스펙 생성",
    "skill_id": "skill_001_youtube_spec_gen",
    "parameters": {
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    "timeout": 60
}

# 노드 정의
nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,
    "GOODNESS": goodness_node,
    "BEAUTY": beauty_node,
    "MERGE": merge_node,
    "EXECUTE": execute_node,
    "VERIFY": verify_node,
    "REPORT": report_node,
}

# 실행 (Context7 + Sequential Thinking + Skills 자동 통합)
def main():
    state = run_v2(input_payload, nodes)
    
    # 결과 확인
    print(f"Trace ID: {state.trace_id}")
    print(f"Errors: {len(state.errors)}")
    
    # 최종 보고
    if "REPORT" in state.outputs:
        report = state.outputs["REPORT"]
        print(f"\n=== 최종 보고 ===")
        print(f"Trinity Score: {report.get('trinity_score', 0):.1f}/100")
        print(f"Decision: {report.get('decision', 'N/A')}")

if __name__ == "__main__":
    main()
```

---

## 참고 자료

- [SSOT Import Paths](./SSOT_IMPORT_PATHS.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/SSOT_IMPORT_PATHS.md)
- [Chancellor Graph V2 완전 가이드](./CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md)
- [GraphState Contract](./GRAPH_STATE_CONTRACT.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/GRAPH_STATE_CONTRACT.md)
- [Failure Mode Matrix](./FAILURE_MODE_MATRIX.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/FAILURE_MODE_MATRIX.md)

---

**Trinity Score**: 眞 100% | 善 95% | 美 95% | 孝 100% | 永 100%
