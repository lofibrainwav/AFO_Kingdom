#!/usr/bin/env python3
"""
AFO Skills Registry MCP Server
Skills Registry의 모든 스킬을 MCP 도구로 제공하는 서버
"""

import json
import os
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# AFO Core 경로 추가
afo_core_path = os.path.join(project_root, "packages", "afo-core")
if afo_core_path not in sys.path:
    sys.path.insert(0, afo_core_path)

try:
    from AFO.services.mcp_tool_trinity_evaluator import \
        mcp_tool_trinity_evaluator
    from afo_skills_registry import register_core_skills

    SKILLS_REGISTRY_AVAILABLE = True
except ImportError:
    SKILLS_REGISTRY_AVAILABLE = False
    mcp_tool_trinity_evaluator = None


class AfoSkillsRegistryMCP:
    """
    AFO Skills Registry MCP Server
    Skills Registry의 모든 스킬을 MCP 도구로 제공
    """

    @classmethod
    def run_loop(cls) -> None:
        """JSON-RPC Main Loop"""
        if not SKILLS_REGISTRY_AVAILABLE:
            print("❌ Skills Registry를 로드할 수 없습니다.", file=sys.stderr)
            sys.exit(1)

        registry = register_core_skills()
        all_skills = registry.list_all()

        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                request = json.loads(line.strip())
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")

                if method == "initialize":
                    result = {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {},
                        },
                        "serverInfo": {
                            "name": "afo-skills-registry-mcp",
                            "version": "1.0.0",
                        },
                    }

                elif method == "notifications/initialized" or method == "initialized":
                    # 'initialized' 알림은 응답이 필요 없음 (notification)
                    continue

                elif method == "tools/list":
                    tools = []
                    for skill in all_skills:
                        # 스킬을 MCP 도구로 변환
                        tool = {
                            "name": skill.skill_id,
                            "description": f"{skill.name}: {skill.description}",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "input": {
                                        "type": "string",
                                        "description": "스킬 실행 입력 파라미터 (JSON 문자열)",
                                    },
                                },
                                "required": ["input"],
                            },
                        }
                        tools.append(tool)

                    result = {"tools": tools}

                elif method == "tools/call":
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    input_data = arguments.get("input", "{}")

                    # 스킬 찾기
                    skill = registry.get(tool_name)
                    if not skill:
                        result = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"❌ 스킬을 찾을 수 없습니다: {tool_name}",
                                }
                            ],
                            "isError": True,
                        }
                    else:
                        # 스킬 실행 (실제 구현은 Skills Service를 통해)
                        try:
                            import time

                            start_time = time.time()

                            # 실제 스킬 실행은 API를 통해 (여기서는 시뮬레이션)
                            execution_result = {
                                "skill_id": skill.skill_id,
                                "name": skill.name,
                                "status": "success",
                                "message": f"스킬 {skill.name} 실행 완료",
                                "philosophy_scores": {
                                    "truth": skill.philosophy_scores.truth,
                                    "goodness": skill.philosophy_scores.goodness,
                                    "beauty": skill.philosophy_scores.beauty,
                                    "serenity": skill.philosophy_scores.serenity,
                                },
                            }

                            execution_time_ms = (time.time() - start_time) * 1000

                            # Trinity Score 계산
                            trinity_score = None
                            if mcp_tool_trinity_evaluator:
                                trinity_eval = mcp_tool_trinity_evaluator.evaluate_execution_result(
                                    tool_name,
                                    execution_result,
                                    execution_time_ms,
                                    False,
                                )
                                trinity_score = trinity_eval.get("combined_scores", {})

                            result_content = {
                                "type": "text",
                                "text": json.dumps(
                                    {
                                        "result": execution_result,
                                        "trinity_score": trinity_score,
                                    },
                                    ensure_ascii=False,
                                    indent=2,
                                ),
                            }

                            result = {
                                "content": [result_content],
                                "isError": False,
                            }

                        except Exception as e:
                            result = {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"❌ 스킬 실행 오류: {e!s}",
                                    }
                                ],
                                "isError": True,
                            }

                else:
                    result = {
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}",
                        }
                    }

                response = {"jsonrpc": "2.0", "id": request_id, "result": result}
                print(json.dumps(response))
                sys.stdout.flush()

            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request_id if "request_id" in locals() else None,
                    "error": {"code": -32603, "message": str(e)},
                }
                print(json.dumps(error_response))
                sys.stdout.flush()


if __name__ == "__main__":
    AfoSkillsRegistryMCP.run_loop()
