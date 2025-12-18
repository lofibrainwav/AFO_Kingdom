# Skills Registry 참조 문서

## 📋 개요

AFO Kingdom Skills Registry의 모든 스킬 목록 및 사용법 참조 문서입니다.

**총 스킬 수**: 19개  
**카테고리**: 9개  
**실행 모드**: SYNC, ASYNC, STREAMING, BACKGROUND

---

## 📊 스킬 통계

- **Strategic Command**: 2개
- **RAG Systems**: 2개
- **Workflow Automation**: 3개
- **Health Monitoring**: 3개
- **Memory Management**: 1개
- **Browser Automation**: 0개 (Playwright Bridge 별도)
- **Analysis Evaluation**: 4개
- **Integration**: 3개
- **Metacognition**: 1개

---

## 🎯 스킬 카테고리

### 1. Strategic Command (전략 명령)

#### skill_005_strategy_engine
**이름**: LangGraph Strategy Engine  
**버전**: 2.3.0  
**설명**: 4-stage command triage and orchestration using LangGraph with Redis checkpointing

**철학 점수**:
- 眞 (Truth): 96%
- 善 (Goodness): 94%
- 美 (Beauty): 93%
- 孝 (Serenity): 95%

**실행 모드**: ASYNC  
**예상 소요 시간**: 1000ms

**입력 파라미터**:
```json
{
  "command": "사용자 명령",
  "context": {}
}
```

**출력**:
```json
{
  "strategy": "determined_strategy",
  "execution_plan": {},
  "checkpoint_id": "redis_checkpoint_id"
}
```

**의존성**: `langgraph`, `redis`

---

#### skill_010_family_persona
**이름**: Family Persona Manager  
**버전**: 1.0.0  
**설명**: Manages the AFO Family personas (Yeongdeok, Sima Yi, Zhuge Liang) and their interactions

**철학 점수**:
- 眞 (Truth): 90%
- 善 (Goodness): 98%
- 美 (Beauty): 100%
- 孝 (Serenity): 99%

**실행 모드**: SYNC  
**예상 소요 시간**: 500ms

---

### 2. RAG Systems (RAG 시스템)

#### skill_002_ultimate_rag
**이름**: Ultimate RAG (Hybrid CRAG + Self-RAG)  
**버전**: 2.0.0  
**설명**: Hybrid Corrective RAG + Self-RAG implementation with Lyapunov-proven convergence

**철학 점수**:
- 眞 (Truth): 98%
- 善 (Goodness): 95%
- 美 (Beauty): 90%
- 孝 (Serenity): 92%

**실행 모드**: STREAMING  
**예상 소요 시간**: 3000ms

**입력 파라미터**:
```json
{
  "query": "사용자 질의",
  "top_k": 5
}
```

**출력**:
```json
{
  "answer": "생성된 답변",
  "sources": [],
  "convergence_score": 0.95
}
```

**의존성**: `openai_api`, `langchain`

---

#### skill_019_hybrid_graphrag
**이름**: Hybrid GraphRAG  
**버전**: 1.0.0  
**설명**: Advanced knowledge retrieval combining Vector Search with Knowledge Graphs

**철학 점수**:
- 眞 (Truth): 97%
- 善 (Goodness): 95%
- 美 (Beauty): 92%
- 孝 (Serenity): 90%

**실행 모드**: ASYNC  
**예상 소요 시간**: 4000ms

**의존성**: `neo4j`, `chromadb`, `langchain`

---

### 3. Workflow Automation (워크플로우 자동화)

#### skill_001_youtube_spec_gen
**이름**: YouTube to n8n Spec Generator  
**버전**: 1.0.0  
**설명**: Converts YouTube tutorial transcripts to executable n8n workflow specifications

**철학 점수**:
- 眞 (Truth): 95%
- 善 (Goodness): 90%
- 美 (Beauty): 92%
- 孝 (Serenity): 88%

**실행 모드**: ASYNC  
**예상 소요 시간**: 15000ms

**입력 파라미터**:
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=abc123"
}
```

**출력**:
```json
{
  "node_spec": {
    "nodes": [],
    "connections": []
  }
}
```

**의존성**: `openai_api`, `transcript_mcp`

---

#### skill_011_dev_tool_belt
**이름**: AFO DevTool Belt  
**버전**: 1.0.0  
**설명**: Essential development tools: Linting (Ruff), Testing (Pytest), Git, Docker

**철학 점수**:
- 眞 (Truth): 98%
- 善 (Goodness): 95%
- 美 (Beauty): 90%
- 孝 (Serenity): 97%

**실행 모드**: SYNC  
**예상 소요 시간**: 2000ms

**의존성**: `ruff`, `pytest`, `git`, `docker`

---

#### skill_015_suno_composer
**이름**: Suno AI Music Composer  
**버전**: 1.0.0  
**설명**: Generates high-quality music and lyrics using Suno AI

**철학 점수**:
- 眞 (Truth): 85%
- 善 (Goodness): 90%
- 美 (Beauty): 100%
- 孝 (Serenity): 95%

**실행 모드**: ASYNC  
**예상 소요 시간**: 60000ms

**의존성**: `suno-api`, `requests`

---

### 4. Health Monitoring (건강 모니터링)

#### skill_003_health_monitor
**이름**: 11-Organ Health Monitor  
**버전**: 1.5.0  
**설명**: Monitors 11 critical AFO system organs (五臟六腑) and generates health reports

**철학 점수**:
- 眞 (Truth): 100%
- 善 (Goodness): 100%
- 美 (Beauty): 95%
- 孝 (Serenity): 100%

**실행 모드**: SYNC  
**예상 소요 시간**: 500ms

**의존성**: `redis`, `postgresql`, `docker`

---

#### skill_017_data_pipeline
**이름**: Real-time Data Pipeline  
**버전**: 1.0.0  
**설명**: Real-time collection and processing of system friction, complexity, and observer metrics

**철학 점수**:
- 眞 (Truth): 98%
- 善 (Goodness): 95%
- 美 (Beauty): 90%
- 孝 (Serenity): 97%

**실행 모드**: STREAMING  
**예상 소요 시간**: 100ms

**의존성**: `kafka`, `redis`, `pandas`

---

#### skill_018_docker_recovery
**이름**: Docker Auto-Recovery (Sima Yi)  
**버전**: 1.0.0  
**설명**: Autonomous container health monitoring and self-healing system

**철학 점수**:
- 眞 (Truth): 99%
- 善 (Goodness): 100%
- 美 (Beauty): 85%
- 孝 (Serenity): 100%

**실행 모드**: BACKGROUND  
**예상 소요 시간**: 5000ms

**의존성**: `docker`, `ai-analysis`

---

### 5. Memory Management (메모리 관리)

#### skill_013_obsidian_librarian
**이름**: AFO Obsidian Librarian  
**버전**: 1.0.0  
**설명**: Manages the Kingdom's Knowledge in Obsidian

**철학 점수**:
- 眞 (Truth): 96%
- 善 (Goodness): 98%
- 美 (Beauty): 95%
- 孝 (Serenity): 99%

**실행 모드**: SYNC  
**예상 소요 시간**: 500ms

**의존성**: `markdown`, `frontmatter`

---

### 6. Analysis Evaluation (분석 평가)

#### skill_004_ragas_evaluator
**이름**: Ragas RAG Quality Evaluator  
**버전**: 1.2.0  
**설명**: Evaluates RAG quality using 4 metrics: Faithfulness, Relevancy, Precision, Recall

**철학 점수**:
- 眞 (Truth): 99%
- 善 (Goodness): 92%
- 美 (Beauty): 88%
- 孝 (Serenity): 85%

**실행 모드**: ASYNC  
**예상 소요 시간**: 5000ms

**의존성**: `ragas`, `openai_api`

---

#### skill_006_ml_metacognition
**이름**: ML Metacognition Upgrade (Phase 3)  
**버전**: 3.0.0  
**설명**: Self-reflection enhancement with user feedback loop and sympy 2nd derivative optimization

**철학 점수**:
- 眞 (Truth): 95%
- 善 (Goodness): 94%
- 美 (Beauty): 92%
- 孝 (Serenity): 93%

**실행 모드**: SYNC  
**예상 소요 시간**: 2000ms

**의존성**: `sympy`, `numpy`

---

#### skill_008_soul_refine
**이름**: Soul Refine (Vibe Alignment)  
**버전**: 1.0.0  
**설명**: Vibe coding and taste alignment using cosine similarity and philosophy balance

**철학 점수**:
- 眞 (Truth): 94%
- 善 (Goodness): 95%
- 美 (Beauty): 97%
- 孝 (Serenity): 96%

**실행 모드**: SYNC  
**예상 소요 시간**: 1000ms

**의존성**: `numpy`

---

#### skill_009_advanced_cosine
**이름**: Advanced Cosine Similarity (4 Techniques)  
**버전**: 1.0.0  
**설명**: 4 advanced cosine similarity techniques: Weighted, Sparse, Embedding, sqrt

**철학 점수**:
- 眞 (Truth): 97%
- 善 (Goodness): 96%
- 美 (Beauty): 93%
- 孝 (Serenity): 95%

**실행 모드**: SYNC  
**예상 소요 시간**: 1200ms

**의존성**: `scipy`, `sentence-transformers`

---

### 7. Integration (통합)

#### skill_007_multi_cloud
**이름**: Multi-Cloud Backup (Hetzner + AWS)  
**버전**: 1.0.0  
**설명**: High-availability backup system with 99.9% uptime

**철학 점수**:
- 眞 (Truth): 95%
- 善 (Goodness): 96%
- 美 (Beauty): 92%
- 孝 (Serenity): 98%

**실행 모드**: ASYNC  
**예상 소요 시간**: 1500ms

**의존성**: `boto3`, `hcloud`

---

#### skill_012_mcp_tool_bridge
**이름**: MCP Tool Bridge  
**버전**: 1.0.0  
**설명**: Universal bridge to connect and utilize any external MCP server tools

**철학 점수**:
- 眞 (Truth): 95%
- 善 (Goodness): 99%
- 美 (Beauty): 96%
- 孝 (Serenity): 94%

**실행 모드**: ASYNC  
**예상 소요 시간**: 1000ms

**의존성**: `mcp`

---

#### skill_014_strangler_integrator
**이름**: Strangler Fig Integrator  
**버전**: 1.0.0  
**설명**: Unifies isolated services (n8n, LangFlow) into the Gateway

**철학 점수**:
- 眞 (Truth): 95%
- 善 (Goodness): 99%
- 美 (Beauty): 94%
- 孝 (Serenity): 98%

**실행 모드**: SYNC  
**예상 소요 시간**: 200ms

**의존성**: `react`, `iframe`

---

#### skill_016_web3_manager
**이름**: Web3 Blockchain Manager  
**버전**: 1.0.0  
**설명**: Manages blockchain interactions, wallet monitoring, and smart contract execution

**철학 점수**:
- 眞 (Truth): 100%
- 善 (Goodness): 90%
- 美 (Beauty): 85%
- 孝 (Serenity): 90%

**실행 모드**: SYNC  
**예상 소요 시간**: 1000ms

**의존성**: `web3.py`, `eth-account`

---

### 8. Metacognition (메타인지)

#### skill_015_vibe_coder
**이름**: AFO Vibe Coder (Self-Evolution Engine)  
**버전**: 1.0.0  
**설명**: The Engine of Self-Evolution. Analyzes codebase, proposes improvements, generates tests

**철학 점수**:
- 眞 (Truth): 99%
- 善 (Goodness): 99%
- 美 (Beauty): 99%
- 孝 (Serenity): 99%

**실행 모드**: ASYNC  
**예상 소요 시간**: 5000ms

**의존성**: `llm`, `git`, `ast`

---

## 🚀 스킬 실행 방법

### API를 통한 실행

```bash
curl -X POST http://localhost:8010/api/skills/skill_001_youtube_spec_gen/execute \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "youtube_url": "https://www.youtube.com/watch?v=abc123"
    }
  }'
```

### Python을 통한 실행

```python
from AFO.afo_skills_registry import SkillRegistry, SkillExecutionRequest

registry = SkillRegistry()
skill = registry.get("skill_001_youtube_spec_gen")

request = SkillExecutionRequest(
    skill_id="skill_001_youtube_spec_gen",
    parameters={"youtube_url": "https://www.youtube.com/watch?v=abc123"}
)

result = registry.execute(request)
```

---

## 📊 철학 점수 기준

모든 스킬은 **眞善美孝** 4기둥 철학 점수를 가집니다:

- **眞 (Truth)**: 기술적 확실성, 증명 가능성
- **善 (Goodness)**: 윤리적 우선순위, 안정성
- **美 (Beauty)**: 명확한 서사, UX
- **孝 (Serenity)**: 마찰 없는 운영

**평균 점수**: 4기둥의 평균값

---

## 🔍 스킬 필터링

### 카테고리별 필터링

```bash
GET /api/skills/list?category=rag_systems
```

### 철학 점수 필터링

```bash
GET /api/skills/list?min_philosophy_avg=95
```

### 검색

```bash
GET /api/skills/list?search=health
```

---

## 📚 관련 문서

- [API Endpoints Reference](API_ENDPOINTS_REFERENCE.md)
- [AFO Final Handover](AFO_FINAL_HANDOVER.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)

---

**최종 업데이트**: 2025-01-27  
**담당**: 승상 (丞相) - AFO Kingdom

