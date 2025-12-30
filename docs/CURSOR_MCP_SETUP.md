# Cursor IDE MCP 설정 가이드

## 📋 개요

AFO Kingdom의 모든 MCP (Model Context Protocol) 서버가 Cursor IDE에 등록되어 있습니다.

---

## 🔧 등록된 MCP 서버

### 1. 외부 MCP 서버 (표준)

#### memory
- **설명**: Knowledge graph memory for persistent context
- **명령어**: `npx -y @modelcontextprotocol/server-memory`
- **기능**: 지식 그래프 기반 영구 컨텍스트 저장

#### filesystem
- **설명**: File system access for AFO Kingdom
- **명령어**: `npx -y @modelcontextprotocol/server-filesystem <LOCAL_WORKSPACE>/AFO_Kingdom`
- **기능**: 파일 시스템 접근

#### sequential-thinking
- **설명**: Step-by-step reasoning
- **명령어**: `npx -y @modelcontextprotocol/server-sequential-thinking`
- **기능**: 단계별 추론

#### brave-search
- **설명**: Web search via Brave
- **명령어**: `npx -y @modelcontextprotocol/server-brave-search`
- **환경 변수**: `BRAVE_API_KEY`
- **기능**: 웹 검색

#### context7
- **설명**: Library documentation context injection
- **명령어**: `npx -y @upstash/context7-mcp`
- **기능**: 라이브러리 문서 컨텍스트 주입

---

### 2. AFO Kingdom 전용 MCP 서버

#### afo-ultimate-mcp
- **설명**: AFO Ultimate MCP Server - Universal connector with Trinity Score evaluation (眞善美孝永)
- **경로**: `<LOCAL_WORKSPACE>/AFO_Kingdom/packages/trinity-os/trinity_os/servers/afo_ultimate_mcp_server.py`
- **도구**:
  - `shell_execute`: Shell 명령어 실행
  - `read_file`: 파일 읽기
  - `write_file`: 파일 쓰기
  - `kingdom_health`: 왕국 건강 체크
- **특징**: 모든 도구 실행 시 **眞善美孝永 Trinity Score 자동 계산 및 반환**

#### afo-skills-mcp
- **설명**: AFO Skills MCP Server - CuPy acceleration & core skills with Trinity Score evaluation
- **경로**: `<LOCAL_WORKSPACE>/AFO_Kingdom/packages/trinity-os/trinity_os/servers/afo_skills_mcp.py`
- **도구**:
  - `cupy_weighted_sum`: GPU 가속 가중 합 계산
  - `read_file`: 파일 읽기
  - `verify_fact`: 사실 검증 (Hallucination Defense)
- **특징**: 모든 도구 실행 시 **眞善美孝永 Trinity Score 자동 계산 및 반환**

#### trinity-score-mcp
- **설명**: Trinity Score MCP Server - Calculate 眞善美孝永 5-pillar scores with GPU acceleration (CuPy)
- **경로**: `<LOCAL_WORKSPACE>/AFO_Kingdom/packages/trinity-os/trinity_os/servers/trinity_score_mcp.py`
- **기능**: 眞善美孝永 5기둥 점수 계산 (GPU 가속 지원)

#### afo-obsidian-mcp
- **설명**: AFO Obsidian MCP Server - 옵시디언 템플릿 시스템 및 Context7 통합
- **경로**: `<LOCAL_WORKSPACE>/AFO_Kingdom/packages/trinity-os/trinity_os/servers/obsidian_mcp.py`
- **도구**:
  - `read_note`: 옵시디언 노트 읽기
  - `write_note`: 옵시디언 노트 쓰기 (Context7 자동 등록)
  - `list_templates`: 템플릿 목록 조회
  - `apply_template`: 템플릿 적용
  - `search_notes`: 옵시디언 vault 검색
  - `search_context7`: Context7 지식 베이스 검색
- **특징**: 모든 도구 실행 시 **眞善美孝永 Trinity Score 자동 계산 및 반환**

---

## 🎯 Skills (API Endpoints)

### calculate_trinity_score
- **엔드포인트**: `${SOUL_ENGINE_URL:-http://localhost:8010}/api/trinity/calculate`
- **메서드**: POST
- **설명**: 眞善美孝永 5기둥 Trinity Score 계산 (SSOT 가중치: 35/35/20/8/2)

### health_check
- **엔드포인트**: `${SOUL_ENGINE_URL:-http://localhost:8010}/health`
- **메서드**: GET
- **설명**: 시스템 건강 체크 및 실시간 Trinity 메트릭 조회

### chancellor_invoke
- **엔드포인트**: `${SOUL_ENGINE_URL:-http://localhost:8010}/chancellor/invoke`
- **메서드**: POST
- **설명**: 3책사(제갈량/사마의/주유)를 통한 승상 호출

---

## 📝 설정 파일 위치

**파일**: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "afo-ultimate-mcp": {
      "command": "python3",
      "args": [
        "<LOCAL_WORKSPACE>/AFO_Kingdom/packages/trinity-os/trinity_os/servers/afo_ultimate_mcp_server.py"
      ],
      "env": {
        "WORKSPACE_ROOT": "<LOCAL_WORKSPACE>/AFO_Kingdom"
      }
    },
    ...
  }
}
```

---

## ✅ 검증 방법

### 1. MCP 서버 목록 확인
Cursor IDE에서 MCP 서버 목록을 확인할 수 있습니다:
- Cursor Settings → MCP Servers

### 2. 도구 테스트
```bash
# AFO Ultimate MCP 서버 테스트
python3 scripts/test_all_mcp_tools_trinity_score.py

# 전체 스킬 검증
python3 scripts/verify_all_skills_trinity_score.py
```

---

## 🔄 업데이트 내역

### 2025-01-27
- ✅ `afo-ultimate-mcp` 추가 (Trinity Score 통합)
- ✅ `afo-skills-mcp` 추가 (Trinity Score 통합)
- ✅ `trinity-score-mcp` 추가
- ✅ 모든 MCP 도구가 眞善美孝永 점수를 반환하도록 구현 완료

---

## 🎉 특징

### Trinity Score 자동 계산
모든 AFO MCP 서버의 도구는 실행 시 자동으로:
- **眞 (Truth)**: 기술적 확실성
- **善 (Goodness)**: 윤리·안정성
- **美 (Beauty)**: 단순함·우아함
- **孝 (Serenity)**: 평온 수호
- **永 (Eternity)**: 영속성

점수를 계산하여 반환합니다.

---

**설정 완료일**: 2025-01-27  
**담당**: 승상 (丞相) - AFO Kingdom

