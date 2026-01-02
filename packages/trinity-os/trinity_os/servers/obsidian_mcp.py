#!/usr/bin/env python3
"""AFO Kingdom Obsidian MCP Server
옵시디언 템플릿 시스템과 Context7 통합을 위한 MCP 서버

표준 MCP 프로토콜 준수 (Raycast, Cursor, Claude Desktop 호환)
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

# 프로젝트 루트를 Python 경로에 추가
# __file__ = packages/trinity-os/trinity_os/servers/obsidian_mcp.py
# parent = servers
# parent.parent = trinity_os
# parent.parent.parent = trinity-os
# parent.parent.parent.parent = packages
# parent.parent.parent.parent.parent = 프로젝트 루트
_current_file = Path(__file__).resolve()
project_root = _current_file.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "packages" / "trinity-os"))

# Context7 및 기타 모듈 import
try:
    from trinity_os.servers.context7_mcp import Context7MCP

    CONTEXT7_AVAILABLE = True
except ImportError:
    CONTEXT7_AVAILABLE = False
    Context7MCP = None

# Trinity Score Evaluator
try:
    sys.path.insert(0, str(project_root / "packages" / "afo-core"))
    from AFO.services.mcp_tool_trinity_evaluator import mcp_tool_trinity_evaluator
except ImportError:
    mcp_tool_trinity_evaluator = None

# 옵시디언 vault 경로
# WORKSPACE_ROOT 환경 변수 확인
workspace_root = os.environ.get("WORKSPACE_ROOT")
if workspace_root:
    OBSIDIAN_VAULT_PATH = Path(workspace_root) / "docs"
else:
    # 환경 변수가 없으면 프로젝트 루트 기준
    OBSIDIAN_VAULT_PATH = project_root / "docs"

TEMPLATES_PATH = OBSIDIAN_VAULT_PATH / "_templates"


class ObsidianMCP:
    """AFO Kingdom Obsidian MCP Server
    옵시디언 템플릿 시스템과 Context7 통합을 위한 MCP 서버
    """

    @staticmethod
    def _validate_path(path: str) -> Path:
        """보안: workspace 외부 접근 방지"""
        if not path:
            raise ValueError("Path cannot be empty")

        # 상대 경로인 경우 vault 기준으로 변환
        if not os.path.isabs(path):
            abs_path = OBSIDIAN_VAULT_PATH / path
        else:
            abs_path = Path(path)

        abs_path = abs_path.resolve()

        # Vault 내부인지 확인
        try:
            abs_path.relative_to(OBSIDIAN_VAULT_PATH.resolve())
        except ValueError:
            raise ValueError(f"Access Denied: Path outside vault ({path})") from None

        return abs_path

    @staticmethod
    def read_note(note_path: str) -> dict[str, Any]:
        """옵시디언 노트 읽기"""
        try:
            target = ObsidianMCP._validate_path(note_path)
            if not target.exists():
                return {
                    "success": False,
                    "error": f"Note not found: {note_path}",
                }

            content = target.read_text(encoding="utf-8")

            # Frontmatter 추출
            metadata = {}
            body = content
            if content.startswith("---"):
                frontmatter_end = content.find("---", 3)
                if frontmatter_end != -1:
                    frontmatter_text = content[3:frontmatter_end].strip()
                    body = content[frontmatter_end + 3 :].strip()

                    # 간단한 YAML 파싱
                    for line in frontmatter_text.split("\n"):
                        line = line.strip()
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            metadata[key] = value

            return {
                "success": True,
                "path": str(target.relative_to(OBSIDIAN_VAULT_PATH)),
                "metadata": metadata,
                "content": body,
                "full_content": content,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    @staticmethod
    def write_note(note_path: str, content: str, metadata: dict[str, Any] = None) -> dict[str, Any]:
        """옵시디언 노트 쓰기"""
        try:
            target = ObsidianMCP._validate_path(note_path)
            target.parent.mkdir(parents=True, exist_ok=True)

            # Frontmatter 생성
            frontmatter = ""
            if metadata:
                frontmatter = "---\n"
                for key, value in metadata.items():
                    if isinstance(value, (list, dict)):
                        value = json.dumps(value, ensure_ascii=False)
                    frontmatter += f"{key}: {value}\n"
                frontmatter += "---\n\n"

            full_content = frontmatter + content
            target.write_text(full_content, encoding="utf-8")

            # Context7에 자동 등록
            if CONTEXT7_AVAILABLE:
                try:
                    script_path = project_root / "scripts" / "register_obsidian_doc_to_context7.py"
                    if script_path.exists():
                        import subprocess

                        subprocess.run(
                            ["python3", str(script_path), str(target)],
                            capture_output=True,
                            timeout=10,
                        )
                except Exception:
                    pass  # Context7 등록 실패해도 노트 쓰기는 성공

            return {
                "success": True,
                "path": str(target.relative_to(OBSIDIAN_VAULT_PATH)),
                "message": f"Note written successfully ({len(full_content)} chars)",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    @staticmethod
    def list_templates() -> dict[str, Any]:
        """템플릿 목록 조회"""
        try:
            templates = []
            if TEMPLATES_PATH.exists():
                for template_file in TEMPLATES_PATH.glob("*.md"):
                    if template_file.name == "README.md":
                        continue

                    content = template_file.read_text(encoding="utf-8")

                    # 템플릿 변수 추출 ({{variable}} 형식)
                    import re

                    variables = re.findall(r"\{\{(\w+)\}\}", content)

                    templates.append(
                        {
                            "name": template_file.stem,
                            "path": str(template_file.relative_to(OBSIDIAN_VAULT_PATH)),
                            "variables": list(set(variables)),
                            "size": len(content),
                        }
                    )

            return {
                "success": True,
                "templates": templates,
                "count": len(templates),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    @staticmethod
    def apply_template(template_name: str, output_path: str, variables: dict[str, str] = None) -> dict[str, Any]:
        """템플릿 적용"""
        try:
            template_file = TEMPLATES_PATH / f"{template_name}.md"
            if not template_file.exists():
                return {
                    "success": False,
                    "error": f"Template not found: {template_name}",
                }

            template_content = template_file.read_text(encoding="utf-8")

            # 변수 치환
            if variables:
                for key, value in variables.items():
                    template_content = template_content.replace(f"{{{{{key}}}}}", str(value))

            # 날짜 변수 자동 치환
            from datetime import datetime

            template_content = template_content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
            template_content = template_content.replace("{{time}}", datetime.now().strftime("%H:%M"))

            # 노트 쓰기
            result = ObsidianMCP.write_note(output_path, template_content)

            if result["success"]:
                return {
                    "success": True,
                    "message": f"Template '{template_name}' applied to '{output_path}'",
                    "path": result["path"],
                }
            else:
                return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    @staticmethod
    def search_notes(query: str, limit: int = 10) -> dict[str, Any]:
        """옵시디언 노트 검색"""
        try:
            results = []
            query_lower = query.lower()

            # Vault 내 모든 마크다운 파일 검색
            for md_file in OBSIDIAN_VAULT_PATH.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding="utf-8")
                    if query_lower in content.lower():
                        # 관련성 점수 계산 (간단한 구현)
                        score = content.lower().count(query_lower)

                        results.append(
                            {
                                "path": str(md_file.relative_to(OBSIDIAN_VAULT_PATH)),
                                "name": md_file.stem,
                                "score": score,
                            }
                        )
                except Exception:
                    continue

            # 점수 기준 정렬
            results.sort(key=lambda x: x["score"], reverse=True)
            results = results[:limit]

            return {
                "success": True,
                "query": query,
                "results": results,
                "count": len(results),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    @staticmethod
    def search_context7(query: str) -> dict[str, Any]:
        """Context7을 통한 검색"""
        if not CONTEXT7_AVAILABLE:
            return {
                "success": False,
                "error": "Context7 not available",
            }

        try:
            result = Context7MCP.retrieve_context(query)
            return {
                "success": result.get("found", False),
                "query": query,
                "context": result.get("context", ""),
                "metadata": result.get("metadata", {}),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    @classmethod
    def run_loop(cls):
        """JSON-RPC Main Loop"""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                request = json.loads(line.strip())
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")

                result = None
                trinity_score = None
                execution_time_ms = 0.0

                if method == "initialize":
                    result = {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {"listChanged": False},
                        },
                        "serverInfo": {
                            "name": "afo-obsidian-mcp",
                            "version": "1.0.0",
                        },
                    }
                elif method == "notifications/initialized":
                    continue

                elif method == "tools/list":
                    result = {
                        "tools": [
                            {
                                "name": "read_note",
                                "description": "Read an Obsidian note from the vault.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "note_path": {
                                            "type": "string",
                                            "description": "Path to the note (relative to vault root)",
                                        },
                                    },
                                    "required": ["note_path"],
                                },
                            },
                            {
                                "name": "write_note",
                                "description": "Write an Obsidian note to the vault (auto-registers to Context7).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "note_path": {
                                            "type": "string",
                                            "description": "Path to the note (relative to vault root)",
                                        },
                                        "content": {
                                            "type": "string",
                                            "description": "Note content (body, without frontmatter)",
                                        },
                                        "metadata": {
                                            "type": "object",
                                            "description": "YAML frontmatter metadata",
                                        },
                                    },
                                    "required": ["note_path", "content"],
                                },
                            },
                            {
                                "name": "list_templates",
                                "description": "List all available Obsidian templates.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {},
                                },
                            },
                            {
                                "name": "apply_template",
                                "description": "Apply a template to create a new note.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "template_name": {
                                            "type": "string",
                                            "description": "Name of the template (without .md extension)",
                                        },
                                        "output_path": {
                                            "type": "string",
                                            "description": "Output path for the new note",
                                        },
                                        "variables": {
                                            "type": "object",
                                            "description": "Template variables to substitute",
                                        },
                                    },
                                    "required": ["template_name", "output_path"],
                                },
                            },
                            {
                                "name": "search_notes",
                                "description": "Search for notes in the Obsidian vault.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "Search query",
                                        },
                                        "limit": {
                                            "type": "integer",
                                            "description": "Maximum number of results",
                                            "default": 10,
                                        },
                                    },
                                    "required": ["query"],
                                },
                            },
                            {
                                "name": "search_context7",
                                "description": "Search Context7 knowledge base for Obsidian-related information.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "Search query (e.g., '템플릿', '옵시디언 템플릿')",
                                        },
                                    },
                                    "required": ["query"],
                                },
                            },
                        ]
                    }

                elif method == "tools/call":
                    start_time = time.time()
                    tool_name = params.get("name")
                    # MCP 표준: arguments는 params 안에 직접 있거나 arguments 키로 전달됨
                    arguments = params.get("arguments", params)

                    is_error = False
                    tool_result = None

                    try:
                        if tool_name == "read_note":
                            tool_result = cls.read_note(arguments.get("note_path", ""))
                        elif tool_name == "write_note":
                            tool_result = cls.write_note(
                                arguments.get("note_path", ""),
                                arguments.get("content", ""),
                                arguments.get("metadata"),
                            )
                        elif tool_name == "list_templates":
                            tool_result = cls.list_templates()
                        elif tool_name == "apply_template":
                            tool_result = cls.apply_template(
                                arguments.get("template_name", ""),
                                arguments.get("output_path", ""),
                                arguments.get("variables"),
                            )
                        elif tool_name == "search_notes":
                            tool_result = cls.search_notes(
                                arguments.get("query", ""),
                                arguments.get("limit", 10),
                            )
                        elif tool_name == "search_context7":
                            tool_result = cls.search_context7(arguments.get("query", ""))
                        else:
                            tool_result = {
                                "success": False,
                                "error": f"Unknown tool: {tool_name}",
                            }
                            is_error = True

                        if not tool_result.get("success", False):
                            is_error = True

                    except Exception as e:
                        tool_result = {
                            "success": False,
                            "error": str(e),
                        }
                        is_error = True

                    execution_time_ms = (time.time() - start_time) * 1000

                    # Trinity Score 계산
                    if mcp_tool_trinity_evaluator:
                        try:
                            trinity_eval = mcp_tool_trinity_evaluator.evaluate_execution_result(
                                tool_name,
                                tool_result,
                                execution_time_ms,
                                is_error,
                            )
                            trinity_score = trinity_eval.get("combined_scores", {})
                        except Exception:
                            trinity_score = None
                    else:
                        trinity_score = None

                    # 결과 포맷팅
                    result_content = json.dumps(tool_result, ensure_ascii=False, indent=2)
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": result_content,
                            }
                        ],
                        "isError": is_error,
                    }

                    # Trinity Score 메타데이터 추가
                    if trinity_score:
                        result["trinity_metadata"] = {
                            "trinity_score": trinity_score,
                            "execution_time_ms": round(execution_time_ms, 2),
                            "tool_name": tool_name,
                        }

                else:
                    result = {"error": f"Unknown method: {method}"}

                # 응답 전송
                response = {"jsonrpc": "2.0", "id": request_id}
                if result:
                    response["result"] = result
                else:
                    response["error"] = {"code": -32601, "message": "Method not found"}

                print(json.dumps(response, ensure_ascii=False))
                sys.stdout.flush()

            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if "request" in locals() else None,
                    "error": {"code": -32603, "message": f"Internal error: {e!s}"},
                }
                print(json.dumps(error_response, ensure_ascii=False))
                sys.stdout.flush()


if __name__ == "__main__":
    ObsidianMCP.run_loop()
