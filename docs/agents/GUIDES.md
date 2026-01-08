# 📚 AFO Kingdom: Agent Specialist Guides (SOPs)

> "도구는 다를지라도, 기둥은 하나다." (美)

이 문서는 `AGENTS.md`(ROOT)를 보조하는 세부 기술 가이드이며, 각 LLM 모델의 특성을 최적화하여 Trinity Score를 극대화하는 방법을 담고 있습니다.

---

## Ⅰ. 모델별 최적화 가이드 (Model Specifics)

### 1) Antigravity CLI (Chancellor's Engine)
- **승상의 엔진**: 왕국의 로우레벨 제어와 자동화, 배경 작업을 담당.
- **최적화**: 작업 전 `health_check` 수행 및 `Rule #-1`(무기 점검) 필수.
- **기록**: 모든 증거를 `artifacts/`에 자동 박제.

### 2) Cursor (Chancellor's Interface)
- **승상의 인터페이스**: 사령관(형님)과의 실시간 소통 및 코드 집필.
- **Composer Mode**: Multi-file 리팩터링 시 서사적 일관성 유지.
- **Agent Mode**: 복잡 작업 시 MCP 9서버를 활용한 임기응변.

### 3) OpenAI Codex (The Scholar - o1/Codex)
- **핵심**: Chain-of-Thought (CoT). 단계별 reasoning 선행 출력.
- **패턴**: 작은 단위로 생성 및 각 단계마다 검증.

### 4) Claude (The Strategist - Anthropic)
- **핵심**: Tree-of-Thoughts (ToT). 여러 가능성을 병렬 고려.
- **패턴**: XML 태그 (`<thinking>`, `<reasoning>`)를 활용한 구조화.

### 5) xAI Grok (The Scout - Grok-2)
- **핵심**: 실시간 검색 우선. 웹/X 검색을 통한 최신 정보 확인.
- **패턴**: 19 Skills와 실시간 리서치를 연쇄적으로 활용.

---

## Ⅱ. 공통 활용 원칙 (Common Principles)

1. **Chain-of-Thought**: 모든 에이전트는 실행 전 내부 추론 과정을 거쳐야 함.
2. **Tree-of-Thoughts**: 복잡한 아키텍처 결정 시 최소 2개 이상의 대안을 비교 평가.
3. **Sequential Thinking**: 문제를 작은 하위 작업으로 쪼개어 단계별로 정복.
4. **실시간 검색**: 최신 라이브러리/보안 취약점 다룰 시 반드시 Grok/Brave 검색 병행.

---

## Ⅲ. 프롬프트 템플릿 (Prompt Templates)

### [Template: Standard Protocol]
```
1. 현재 상태 분석 (지피지기)
2. 10초 프로토콜 출력 (AUTO_RUN/ASK/BLOCK)
3. Trinity Score 자가 진단
4. 단계별 실행 및 Verify
```

---
# End of Guides
