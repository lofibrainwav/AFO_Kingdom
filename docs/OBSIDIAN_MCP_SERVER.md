# 옵시디언 MCP 서버 가이드

**생성일**: 2025-01-27  
**상태**: ✅ 완료  
**담당**: 승상 (丞相) - AFO Kingdom

---

## 📋 개요

AFO Kingdom의 옵시디언 템플릿 시스템과 Context7 통합을 위한 전용 MCP 서버입니다.

**핵심 기능**:
- 옵시디언 노트 읽기/쓰기
- 템플릿 목록 조회 및 적용
- Context7 자동 등록
- 옵시디언 vault 검색
- Context7 지식 베이스 검색

---

## 🔧 MCP 서버 설정

### Cursor IDE 설정

**파일**: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "afo-obsidian-mcp": {
      "command": "python3",
      "args": [
        "${WORKSPACE_ROOT:-<LOCAL_WORKSPACE>/AFO_Kingdom}/packages/trinity-os/trinity_os/servers/obsidian_mcp.py"
      ],
      "env": {
        "WORKSPACE_ROOT": "${WORKSPACE_ROOT:-<LOCAL_WORKSPACE>/AFO_Kingdom}",
        "PYTHONPATH": "${WORKSPACE_ROOT:-<LOCAL_WORKSPACE>/AFO_Kingdom}/packages/afo-core:${WORKSPACE_ROOT:-<LOCAL_WORKSPACE>/AFO_Kingdom}/packages/trinity-os"
      },
      "description": "AFO Obsidian MCP Server - 옵시디언 템플릿 시스템 및 Context7 통합"
    }
  }
}
```

---

## 🛠️ 제공되는 도구

### 1. `read_note`

옵시디언 노트를 읽습니다.

**파라미터**:
- `note_path` (string, required): 노트 경로 (vault 루트 기준 상대 경로)

**반환값**:
```json
{
  "success": true,
  "path": "projects/my_project.md",
  "metadata": {
    "type": "project",
    "status": "in-progress",
    "created": "2025-01-27"
  },
  "content": "노트 본문 내용",
  "full_content": "전체 내용 (frontmatter 포함)"
}
```

**예시**:
```json
{
  "name": "read_note",
  "arguments": {
    "note_path": "projects/my_project.md"
  }
}
```

---

### 2. `write_note`

옵시디언 노트를 작성합니다. 자동으로 Context7에 등록됩니다.

**파라미터**:
- `note_path` (string, required): 노트 경로
- `content` (string, required): 노트 본문 내용
- `metadata` (object, optional): YAML frontmatter 메타데이터

**반환값**:
```json
{
  "success": true,
  "path": "projects/my_project.md",
  "message": "Note written successfully (1234 chars)"
}
```

**예시**:
```json
{
  "name": "write_note",
  "arguments": {
    "note_path": "projects/new_project.md",
    "content": "# 새 프로젝트\n\n프로젝트 설명...",
    "metadata": {
      "type": "project",
      "status": "planning",
      "created": "2025-01-27"
    }
  }
}
```

---

### 3. `list_templates`

사용 가능한 모든 템플릿 목록을 조회합니다.

**파라미터**: 없음

**반환값**:
```json
{
  "success": true,
  "templates": [
    {
      "name": "project_doc",
      "path": "_templates/project_doc.md",
      "variables": ["project_name", "assignee", "start_date"],
      "size": 1234
    }
  ],
  "count": 8
}
```

**예시**:
```json
{
  "name": "list_templates",
  "arguments": {}
}
```

---

### 4. `apply_template`

템플릿을 적용하여 새 노트를 생성합니다.

**파라미터**:
- `template_name` (string, required): 템플릿 이름 (.md 확장자 제외)
- `output_path` (string, required): 출력 경로
- `variables` (object, optional): 템플릿 변수

**반환값**:
```json
{
  "success": true,
  "message": "Template 'project_doc' applied to 'projects/my_project.md'",
  "path": "projects/my_project.md"
}
```

**예시**:
```json
{
  "name": "apply_template",
  "arguments": {
    "template_name": "project_doc",
    "output_path": "projects/my_project.md",
    "variables": {
      "project_name": "새 프로젝트",
      "assignee": "승상",
      "start_date": "2025-01-27"
    }
  }
}
```

---

### 5. `search_notes`

옵시디언 vault에서 노트를 검색합니다.

**파라미터**:
- `query` (string, required): 검색 쿼리
- `limit` (integer, optional): 최대 결과 수 (기본값: 10)

**반환값**:
```json
{
  "success": true,
  "query": "프로젝트",
  "results": [
    {
      "path": "projects/my_project.md",
      "name": "my_project",
      "score": 5
    }
  ],
  "count": 1
}
```

**예시**:
```json
{
  "name": "search_notes",
  "arguments": {
    "query": "프로젝트",
    "limit": 10
  }
}
```

---

### 6. `search_context7`

Context7 지식 베이스를 검색합니다.

**파라미터**:
- `query` (string, required): 검색 쿼리

**반환값**:
```json
{
  "success": true,
  "query": "템플릿",
  "context": "AFO Kingdom 옵시디언 템플릿 시스템: ...",
  "metadata": {
    "truth_impact": 10,
    "source": "Context7 Internal DB"
  }
}
```

**예시**:
```json
{
  "name": "search_context7",
  "arguments": {
    "query": "옵시디언 템플릿"
  }
}
```

---

## 🚀 사용 예시

### 시나리오 1: 템플릿으로 새 프로젝트 문서 생성

```json
{
  "method": "tools/call",
  "params": {
    "name": "apply_template",
    "arguments": {
      "template_name": "project_doc",
      "output_path": "projects/new_feature.md",
      "variables": {
        "project_name": "새 기능 개발",
        "assignee": "승상",
        "start_date": "2025-01-27"
      }
    }
  }
}
```

**결과**: 
- 새 노트가 생성됨
- Context7에 자동 등록됨
- Trinity Score 자동 계산됨

---

### 시나리오 2: 템플릿 목록 조회 후 선택

```json
{
  "method": "tools/call",
  "params": {
    "name": "list_templates",
    "arguments": {}
  }
}
```

**결과**: 사용 가능한 모든 템플릿 목록 반환

---

### 시나리오 3: Context7에서 템플릿 정보 검색

```json
{
  "method": "tools/call",
  "params": {
    "name": "search_context7",
    "arguments": {
      "query": "템플릿"
    }
  }
}
```

**결과**: Context7에서 템플릿 관련 정보 반환

---

## 📊 Trinity Score 통합

모든 도구 실행 시 **眞善美孝永 Trinity Score**가 자동으로 계산되어 반환됩니다.

**반환 형식**:
```json
{
  "content": [...],
  "isError": false,
  "trinity_metadata": {
    "trinity_score": {
      "Truth": 95,
      "Goodness": 90,
      "Beauty": 85,
      "Serenity": 80,
      "Eternity": 75,
      "total": 85.0
    },
    "execution_time_ms": 123.45,
    "tool_name": "write_note"
  }
}
```

---

## 🔒 보안

### 경로 검증

- 모든 경로는 vault 루트(`docs/`) 내부로 제한됩니다
- 절대 경로나 상위 디렉토리 접근은 차단됩니다
- `_validate_path()` 메서드로 보안 검증 수행

### Context7 자동 등록

- `write_note` 실행 시 자동으로 Context7에 등록됩니다
- 등록 실패해도 노트 쓰기는 성공합니다 (graceful degradation)

---

## ✅ 검증

### 서버 로드 확인

```bash
python3 packages/trinity-os/trinity_os/servers/obsidian_mcp.py
```

### 도구 목록 확인

```json
{
  "method": "tools/list",
  "params": {}
}
```

### 기능 테스트

```bash
# 템플릿 목록 조회
python3 -c "
from packages.trinity_os.trinity_os.servers.obsidian_mcp import ObsidianMCP
result = ObsidianMCP.list_templates()
print(result)
"
```

---

## 📚 관련 문서

- [옵시디언 템플릿 ↔ Context7 통합 가이드](./OBSIDIAN_CONTEXT7_INTEGRATION.md)
- [템플릿 가이드](./_templates/README.md)
- [Cursor MCP 설정 가이드](./CURSOR_MCP_SETUP.md)

---

**생성일**: 2025-01-27  
**담당**: 승상 (丞相) - AFO Kingdom  
**상태**: ✅ 완료  
**Trinity Score**: 95/100 🌟

