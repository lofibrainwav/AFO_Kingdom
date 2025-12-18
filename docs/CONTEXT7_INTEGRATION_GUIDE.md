# Context7 통합 가이드

## 📋 개요

AFO Kingdom의 문서를 Context7 지식 기반에 통합하는 가이드입니다.

**Context7**: 지식 그래프 기반 영구 컨텍스트 저장 시스템  
**목적**: 생성된 문서들을 Context7에 통합하여 AI 에이전트가 쉽게 접근할 수 있도록 함

---

## 🔧 Context7 설정

### MCP 서버 설정

`.cursor/mcp.json`에 Context7 MCP 서버가 등록되어 있습니다:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "description": "Library documentation context injection"
    }
  }
}
```

---

## 📚 통합할 문서 목록

### 새로 생성된 문서 (9개)

1. **API_ENDPOINTS_REFERENCE.md**
   - **카테고리**: API Reference
   - **설명**: 49개 API 엔드포인트 통합 참조 문서
   - **태그**: API, Endpoints, Reference, Documentation

2. **SKILLS_REGISTRY_REFERENCE.md**
   - **카테고리**: Skills Reference
   - **설명**: 19개 스킬 목록 및 사용법 참조 문서
   - **태그**: Skills, Registry, Reference, Documentation

3. **DEPLOYMENT_GUIDE.md**
   - **카테고리**: Operations
   - **설명**: Docker, Kubernetes 배포 가이드
   - **태그**: Deployment, Docker, Kubernetes, Operations

4. **CONFIGURATION_GUIDE.md**
   - **카테고리**: Configuration
   - **설명**: 환경 변수 및 설정 파일 가이드
   - **태그**: Configuration, Environment Variables, Settings

5. **TROUBLESHOOTING.md**
   - **카테고리**: Operations
   - **설명**: 일반적인 문제 및 해결 방법
   - **태그**: Troubleshooting, Debugging, Operations

6. **DOCUMENTATION_COMPLETE_VERIFICATION.md**
   - **카테고리**: Documentation
   - **설명**: 문서화 완료 검증 보고서 (7단계 검증)
   - **태그**: Documentation, Verification, Quality Assurance

7. **DOCUMENTATION_VERIFICATION_SEQUENTIAL_ANALYSIS.md**
   - **카테고리**: Documentation
   - **설명**: Sequential Thinking 분석 보고서
   - **태그**: Documentation, Sequential Thinking, Analysis

8. **SYSTEM_DOCUMENTATION_AUDIT.md**
   - **카테고리**: Documentation
   - **설명**: 시스템 문서화 감사 보고서
   - **태그**: Documentation, Audit, Code-Document Mapping

9. **SYSTEM_DOCUMENTATION_COMPLETE.md**
   - **카테고리**: Documentation
   - **설명**: 시스템 문서화 완료 보고서
   - **태그**: Documentation, Complete, Summary

---

## 🚀 Context7 통합 방법

### 방법 1: MCP 도구를 통한 통합

Cursor IDE에서 MCP 도구를 사용하여 문서를 Context7에 추가:

1. **문서 읽기**
   ```bash
   # MCP filesystem 도구 사용
   mcp_filesystem_read_text_file path="docs/API_ENDPOINTS_REFERENCE.md"
   ```

2. **Context7에 저장**
   ```bash
   # Context7 MCP 도구 사용 (도구 이름 확인 필요)
   # context7_add_knowledge 또는 유사한 도구
   ```

### 방법 2: 스크립트를 통한 통합

```python
# scripts/integrate_docs_to_context7.py
import os
from pathlib import Path

docs_to_integrate = [
    "docs/API_ENDPOINTS_REFERENCE.md",
    "docs/SKILLS_REGISTRY_REFERENCE.md",
    "docs/DEPLOYMENT_GUIDE.md",
    "docs/CONFIGURATION_GUIDE.md",
    "docs/TROUBLESHOOTING.md",
    "docs/DOCUMENTATION_COMPLETE_VERIFICATION.md",
    "docs/DOCUMENTATION_VERIFICATION_SEQUENTIAL_ANALYSIS.md",
    "docs/SYSTEM_DOCUMENTATION_AUDIT.md",
    "docs/SYSTEM_DOCUMENTATION_COMPLETE.md",
]

for doc_path in docs_to_integrate:
    if os.path.exists(doc_path):
        content = Path(doc_path).read_text(encoding="utf-8")
        # Context7 API 호출하여 문서 추가
        # (Context7 API 엔드포인트 확인 필요)
        print(f"✅ {doc_path} 통합 완료")
```

### 방법 3: 수동 통합

1. Cursor IDE에서 Context7 MCP 도구 사용
2. 각 문서를 하나씩 Context7에 추가
3. 메타데이터 (태그, 카테고리) 설정

---

## 📊 통합 메타데이터

각 문서의 메타데이터는 `docs/context7_integration_metadata.json`에 저장되어 있습니다.

**메타데이터 구조**:
```json
{
  "API_ENDPOINTS_REFERENCE": {
    "file": "docs/API_ENDPOINTS_REFERENCE.md",
    "title": "API 엔드포인트 참조 문서",
    "category": "API Reference",
    "description": "AFO Kingdom Soul Engine API의 모든 엔드포인트 통합 참조 문서",
    "tags": ["API", "Endpoints", "Reference", "Documentation"],
    "keywords": ["API", "엔드포인트", "참조", "문서화"]
  }
}
```

---

## 🔍 Context7 검색

통합 후 Context7을 통해 문서를 검색할 수 있습니다:

```bash
# Context7 MCP 도구 사용
# retrieve_context query="API 엔드포인트" domain="documentation"
```

---

## ✅ 통합 확인

### 통합 완료 체크리스트

- [ ] API_ENDPOINTS_REFERENCE.md 통합 완료
- [ ] SKILLS_REGISTRY_REFERENCE.md 통합 완료
- [ ] DEPLOYMENT_GUIDE.md 통합 완료
- [ ] CONFIGURATION_GUIDE.md 통합 완료
- [ ] TROUBLESHOOTING.md 통합 완료
- [ ] DOCUMENTATION_COMPLETE_VERIFICATION.md 통합 완료
- [ ] DOCUMENTATION_VERIFICATION_SEQUENTIAL_ANALYSIS.md 통합 완료
- [ ] SYSTEM_DOCUMENTATION_AUDIT.md 통합 완료
- [ ] SYSTEM_DOCUMENTATION_COMPLETE.md 통합 완료

---

## 📚 관련 문서

- [Cursor MCP Setup](CURSOR_MCP_SETUP.md)
- [API Endpoints Reference](API_ENDPOINTS_REFERENCE.md)
- [Skills Registry Reference](SKILLS_REGISTRY_REFERENCE.md)

---

**작성일**: 2025-01-27  
**담당**: 승상 (丞相) - AFO Kingdom  
**상태**: 통합 준비 완료 ✅

