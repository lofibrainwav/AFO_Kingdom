import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Enhance Path for Sibling Imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Sibling Modules (The Fragments)
# Import individually so optional deps (e.g., playwright) don't disable the entire server.
AfoSkillsMCP = None
Context7MCP = None
PlaywrightBridgeMCP = None
SequentialThinkingMCP = None
TrinityScoreEngineHybrid = None

SKILLS_LOADED = False
CONTEXT7_LOADED = False
SEQUENTIAL_LOADED = False
TRINITY_LOADED = False
PLAYWRIGHT_LOADED = False

try:
    from afo_skills_mcp import AfoSkillsMCP as _AfoSkillsMCP

    AfoSkillsMCP = _AfoSkillsMCP
    SKILLS_LOADED = True
except ImportError as e:
    print(f"⚠️ Failed to load AfoSkillsMCP: {e}", file=sys.stderr)

try:
    from context7_mcp import Context7MCP as _Context7MCP

    Context7MCP = _Context7MCP
    CONTEXT7_LOADED = True
except ImportError as e:
    print(f"⚠️ Failed to load Context7MCP: {e}", file=sys.stderr)

try:
    from sequential_thinking_mcp import SequentialThinkingMCP as _SequentialThinkingMCP

    SequentialThinkingMCP = _SequentialThinkingMCP
    SEQUENTIAL_LOADED = True
except ImportError as e:
    print(f"⚠️ Failed to load SequentialThinkingMCP: {e}", file=sys.stderr)

try:
    from trinity_score_mcp import TrinityScoreEngineHybrid as _TrinityScoreEngineHybrid

    TrinityScoreEngineHybrid = _TrinityScoreEngineHybrid
    TRINITY_LOADED = True
except ImportError as e:
    print(f"⚠️ Failed to load TrinityScoreEngineHybrid: {e}", file=sys.stderr)

try:
    from playwright_bridge_mcp import PlaywrightBridgeMCP as _PlaywrightBridgeMCP

    PlaywrightBridgeMCP = _PlaywrightBridgeMCP
    PLAYWRIGHT_LOADED = True
except ImportError as e:
    print(f"⚠️ Failed to load PlaywrightBridgeMCP: {e}", file=sys.stderr)

# Trinity Score Evaluator (동적 점수 계산)
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../afo-core"))
    from AFO.services.mcp_tool_trinity_evaluator import mcp_tool_trinity_evaluator
except ImportError:
    try:
        from AFO.services.mcp_tool_trinity_evaluator import mcp_tool_trinity_evaluator
    except ImportError:
        mcp_tool_trinity_evaluator = None

# Constants
WORKSPACE_ROOT = os.environ.get("WORKSPACE_ROOT", os.getcwd())


class AfoUltimateMCPServer:
    """
    [AFO Ultimate MCP]
    The Universal Connector & Commander for the AFO Kingdom.
    Architecture: Vanilla JSON-RPC 2.0 (Zero Dependency check).
    Integrates: Trinity Score Engine, Afo Skills, and Core Shell Tools.
    """

    @staticmethod
    def _validate_path(path: str) -> Path:
        """Security: Prevent path traversal outside workspace."""
        if not path or path.strip() == "":
            raise ValueError("Empty path not allowed")

        abs_path = Path(path).resolve()

        # CRITICAL SECURITY: Prevent path traversal attacks
        workspace_path = Path(WORKSPACE_ROOT).resolve()
        try:
            # Check if the resolved path is within workspace
            abs_path.relative_to(workspace_path)
        except ValueError:
            raise ValueError(f"Access Denied: Path outside workspace ({path}) -> {abs_path}")

        return abs_path

    @staticmethod
    def shell_execute(command: str) -> str:
        """Executes a shell command and returns output. (Power Tool)"""
        if not command:
            return "Error: Empty command"

        # Security: Allow only explicitly safe or all?
        # Jipijigi Rule: "Power requires Trust". We allow it for now.
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
                executable="/bin/zsh",
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Exit {result.returncode}\nstderr: {result.stderr.strip()}\nstdout: {result.stdout.strip()}"
        except Exception as e:
            return f"Execution Failure: {e!s}"

    @staticmethod
    def read_file(path: str) -> str:
        """Reads a file from the filesystem."""
        try:
            target = AfoUltimateMCPServer._validate_path(path)
            if not target.exists():
                return f"Error: File not found ({path})"
            return target.read_text(encoding="utf-8")
        except Exception as e:
            return f"Read Error: {e!s}"

    @staticmethod
    def write_file(path: str, content: str) -> str:
        """Writes content to a file (Overwrites)."""
        try:
            target = AfoUltimateMCPServer._validate_path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return f"Success: Wrote {len(content)} chars to {path}"
        except Exception as e:
            return f"Write Error: {e!s}"

    @staticmethod
    def kingdom_health() -> str:
        """Runs the verify_kingdom_core protocol."""
        script_path = os.path.join(WORKSPACE_ROOT, "scripts", "verify_kingdom_core.py")
        if not os.path.exists(script_path):
            # Fallback to status script if core script missing
            script_path = os.path.join(
                WORKSPACE_ROOT, "scripts", "verify_kingdom_status.py"
            )
            if not os.path.exists(script_path):
                return "Error: Health Script Missing"

        return AfoUltimateMCPServer.shell_execute(f"python3 {script_path}")

    @classmethod
    def run_loop(cls):
        """JSON-RPC Main Loop"""
        for line in sys.stdin:
            try:
                if not line.strip():
                    continue
                request = json.loads(line)
                method = request.get("method")
                msg_id = request.get("id")
                params = request.get("params", {})

                result = None

                if method == "initialize":
                    result = {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": {"name": "AfoUltimate", "version": "0.2.0"},
                    }
                elif method == "notifications/initialized":
                    continue

                elif method == "tools/list":
                    tools = [
                        # Core Tools
                        {
                            "name": "shell_execute",
                            "description": "Execute a shell command (zsh). Use with caution.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"command": {"type": "string"}},
                                "required": ["command"],
                            },
                        },
                        {
                            "name": "read_file",
                            "description": "Read file content.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"path": {"type": "string"}},
                                "required": ["path"],
                            },
                        },
                        {
                            "name": "write_file",
                            "description": "Write text to file.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string"},
                                    "content": {"type": "string"},
                                },
                                "required": ["path", "content"],
                            },
                        },
                        {
                            "name": "kingdom_health",
                            "description": "Run the Kingdom Core Health Check protocol.",
                            "inputSchema": {"type": "object", "properties": {}},
                        },
                    ]

                    if TRINITY_LOADED:
                        tools.append(
                            {
                                "name": "calculate_trinity_score",
                                "description": "Calculate the 5-Pillar Trinity Score (Truth, Goodness, Beauty, Serenity, Eternity).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "truth_base": {"type": "integer"},
                                        "goodness_base": {"type": "integer"},
                                        "beauty_base": {"type": "integer"},
                                        "risk_score": {"type": "integer"},
                                        "friction": {"type": "integer"},
                                        "eternity_base": {"type": "integer"},
                                    },
                                    "required": [],
                                },
                            }
                        )

                    if SKILLS_LOADED:
                        tools.append(
                            {
                                "name": "verify_fact",
                                "description": "Verify a factual claim against context (Hallucination Defense).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "claim": {"type": "string"},
                                        "context": {"type": "string"},
                                    },
                                    "required": ["claim"],
                                },
                            }
                        )
                        tools.append(
                            {
                                "name": "cupy_weighted_sum",
                                "description": "Calculate weighted sum (GPU accelerated if available).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                        },
                                        "weights": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                        },
                                    },
                                    "required": ["data", "weights"],
                                },
                            }
                        )

                    if SEQUENTIAL_LOADED:
                        tools.append(
                            {
                                "name": "sequential_thinking",
                                "description": "Execute sequential thinking step (Step-by-Step Reasoning).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "thought": {"type": "string"},
                                        "thought_number": {"type": "integer"},
                                        "total_thoughts": {"type": "integer"},
                                        "next_thought_needed": {"type": "boolean"},
                                    },
                                    "required": [
                                        "thought",
                                        "thought_number",
                                        "total_thoughts",
                                        "next_thought_needed",
                                    ],
                                },
                            }
                        )

                    if CONTEXT7_LOADED:
                        tools.append(
                            {
                                "name": "retrieve_context",
                                "description": "Retrieve pinned technical context (Context7 Knowledge Injector).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "domain": {"type": "string"},
                                    },
                                    "required": ["query"],
                                },
                            }
                        )

                    if PLAYWRIGHT_LOADED:
                        tools.append(
                            {
                                "name": "browser_navigate",
                                "description": "Navigate to a URL using Playwright.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"url": {"type": "string"}},
                                    "required": ["url"],
                                },
                            }
                        )
                        tools.append(
                            {
                                "name": "browser_screenshot",
                                "description": "Capture a screenshot of the current page.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"path": {"type": "string"}},
                                    "required": ["path"],
                                },
                            }
                        )
                        tools.append(
                            {
                                "name": "browser_click",
                                "description": "Click an element on the current page.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"selector": {"type": "string"}},
                                    "required": ["selector"],
                                },
                            }
                        )
                        tools.append(
                            {
                                "name": "browser_type",
                                "description": "Type text into an element on the current page.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "selector": {"type": "string"},
                                        "text": {"type": "string"},
                                    },
                                    "required": ["selector", "text"],
                                },
                            }
                        )
                        tools.append(
                            {
                                "name": "browser_scrape",
                                "description": "Scrape text content from a selector.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"selector": {"type": "string"}},
                                    "required": ["selector"],
                                },
                            }
                        )

                    result = {"tools": tools}

                elif method == "tools/call":
                    # Tool Execution Logic with Trinity Score Evaluation
                    tool_name = params.get("name")
                    args = params.get("arguments", {})

                    # 실행 시간 측정 시작
                    start_time = time.time()
                    is_error = False
                    content = ""
                    trinity_metadata = None

                    try:
                        # 1. Core Tools
                        if tool_name == "shell_execute":
                            content = cls.shell_execute(args.get("command"))
                        elif tool_name == "read_file":
                            content = cls.read_file(args.get("path"))
                        elif tool_name == "write_file":
                            content = cls.write_file(
                                args.get("path"), args.get("content")
                            )
                        elif tool_name == "kingdom_health":
                            content = cls.kingdom_health()

                        # 에러 메시지 확인
                        if "Error" in content or "error" in content.lower():
                            is_error = True

                    except Exception as e:
                        content = f"Execution Error: {e!s}"
                        is_error = True

                    # 실행 시간 계산
                    execution_time_ms = (time.time() - start_time) * 1000

                    # Core Tools에 대한 Trinity Score 계산 (眞善美孝永 5기둥)
                    if mcp_tool_trinity_evaluator and tool_name in [
                        "shell_execute",
                        "read_file",
                        "write_file",
                        "kingdom_health",
                    ]:
                        try:
                            trinity_eval = (
                                mcp_tool_trinity_evaluator.evaluate_execution_result(
                                    tool_name=tool_name,
                                    execution_result=content,
                                    execution_time_ms=execution_time_ms,
                                    is_error=is_error,
                                )
                            )
                            trinity_metadata = trinity_eval["trinity_metrics"]
                        except Exception:
                            trinity_metadata = None

                    # 2. Advanced Tools (from siblings)
                    if tool_name not in [
                        "shell_execute",
                        "read_file",
                        "write_file",
                        "kingdom_health",
                    ]:
                        if tool_name == "calculate_trinity_score":
                            if not TRINITY_LOADED or TrinityScoreEngineHybrid is None:
                                content = (
                                    "Tool not available: trinity_score_mcp not loaded"
                                )
                                is_error = True
                            else:
                                res = TrinityScoreEngineHybrid.evaluate(**args)
                                content = json.dumps(res, indent=2, ensure_ascii=False)
                                trinity_metadata = res

                        elif tool_name == "verify_fact":
                            if not SKILLS_LOADED or AfoSkillsMCP is None:
                                content = (
                                    "Tool not available: afo_skills_mcp not loaded"
                                )
                                is_error = True
                            else:
                                res = AfoSkillsMCP.verify_fact(
                                    args.get("claim"), args.get("context", "")
                                )
                                content = json.dumps(res, indent=2, ensure_ascii=False)
                                trinity_metadata = {
                                    "truth_impact": (
                                        10 if res["verdict"] == "PLAUSIBLE" else -10
                                    )
                                }

                        elif tool_name == "cupy_weighted_sum":
                            if not SKILLS_LOADED or AfoSkillsMCP is None:
                                content = (
                                    "Tool not available: afo_skills_mcp not loaded"
                                )
                                is_error = True
                            else:
                                res = AfoSkillsMCP.cupy_weighted_sum(
                                    args.get("data", []), args.get("weights", [])
                                )
                                content = str(res)

                        elif tool_name == "sequential_thinking":
                            if not SEQUENTIAL_LOADED or SequentialThinkingMCP is None:
                                content = "Tool not available: sequential_thinking_mcp not loaded"
                                is_error = True
                            else:
                                # Create instance and call method
                                st_instance = SequentialThinkingMCP()
                                res = st_instance.process_thought(
                                    args.get("thought", ""),
                                    args.get("thought_number", 1),
                                    args.get("total_thoughts", 1),
                                    args.get("next_thought_needed", False),
                                )
                                content = json.dumps(res, indent=2, ensure_ascii=False)
                                if "metadata" in res:
                                    trinity_metadata = {
                                        "truth_impact": res["metadata"].get(
                                            "truth_impact", 0
                                        ),
                                        "serenity_impact": res["metadata"].get(
                                            "serenity_impact", 0
                                        ),
                                    }

                        elif tool_name == "retrieve_context":
                            if not CONTEXT7_LOADED or Context7MCP is None:
                                content = "Tool not available: context7_mcp not loaded"
                                is_error = True
                            else:
                                # Create instance and call method
                                ctx_instance = Context7MCP()
                                res = ctx_instance.retrieve_context(
                                    args.get("query", ""),
                                    args.get("domain", "general"),
                                )
                                content = json.dumps(res, indent=2, ensure_ascii=False)
                                if "metadata" in res:
                                    trinity_metadata = {
                                        "truth_impact": res["metadata"].get(
                                            "truth_impact", 0
                                        )
                                    }

                        # Browser Bridge Tools
                        elif tool_name == "browser_navigate":
                            if not PLAYWRIGHT_LOADED or PlaywrightBridgeMCP is None:
                                content = "Tool not available: playwright_bridge_mcp not loaded"
                                is_error = True
                            else:
                                content = json.dumps(
                                    PlaywrightBridgeMCP.navigate(args.get("url")),
                                    indent=2,
                                )
                        elif tool_name == "browser_screenshot":
                            if not PLAYWRIGHT_LOADED or PlaywrightBridgeMCP is None:
                                content = "Tool not available: playwright_bridge_mcp not loaded"
                                is_error = True
                            else:
                                content = json.dumps(
                                    PlaywrightBridgeMCP.screenshot(
                                        args.get("path", "screenshot.png")
                                    ),
                                    indent=2,
                                )
                        elif tool_name == "browser_click":
                            if not PLAYWRIGHT_LOADED or PlaywrightBridgeMCP is None:
                                content = "Tool not available: playwright_bridge_mcp not loaded"
                                is_error = True
                            else:
                                content = json.dumps(
                                    PlaywrightBridgeMCP.click(args.get("selector")),
                                    indent=2,
                                )
                        elif tool_name == "browser_type":
                            if not PLAYWRIGHT_LOADED or PlaywrightBridgeMCP is None:
                                content = "Tool not available: playwright_bridge_mcp not loaded"
                                is_error = True
                            else:
                                content = json.dumps(
                                    PlaywrightBridgeMCP.type_text(
                                        args.get("selector"), args.get("text")
                                    ),
                                    indent=2,
                                )
                        elif tool_name == "browser_scrape":
                            if not PLAYWRIGHT_LOADED or PlaywrightBridgeMCP is None:
                                content = "Tool not available: playwright_bridge_mcp not loaded"
                                is_error = True
                            else:
                                content = json.dumps(
                                    PlaywrightBridgeMCP.scrape(args.get("selector")),
                                    indent=2,
                                )

                        else:
                            content = f"Unknown tool: {tool_name}"
                            is_error = True

                    # Construct Response
                    result_body = [{"type": "text", "text": str(content)}]

                    # Append Trinity Metadata if available (Serenity Injection)
                    if trinity_metadata:
                        result_body.append(
                            {
                                "type": "text",
                                "text": f"\n\n[眞善美孝永 Trinity Score]\n"
                                f"眞 (Truth): {trinity_metadata.get('truth', 0):.2%}\n"
                                f"善 (Goodness): {trinity_metadata.get('goodness', 0):.2%}\n"
                                f"美 (Beauty): {trinity_metadata.get('beauty', 0):.2%}\n"
                                f"孝 (Serenity): {trinity_metadata.get('filial_serenity', 0):.2%}\n"
                                f"永 (Eternity): {trinity_metadata.get('eternity', 0):.2%}\n"
                                f"Trinity Score: {trinity_metadata.get('trinity_score', 0):.2%}\n"
                                f"Balance: {trinity_metadata.get('balance_status', 'unknown')}",
                            }
                        )

                    result = {
                        "content": result_body,
                        "isError": is_error,
                        "trinity_score": trinity_metadata,  # 메타데이터를 직접 포함
                    }

                else:
                    # Ignore other messages or return error?
                    pass

                if msg_id is not None:
                    print(
                        json.dumps({"jsonrpc": "2.0", "result": result, "id": msg_id})
                    )
                    sys.stdout.flush()

            except Exception as e:
                # Catch-all to prevent crash
                if msg_id is not None:
                    error_resp = {
                        "jsonrpc": "2.0",
                        "error": {"code": -32603, "message": str(e)},
                        "id": msg_id,
                    }
                    print(json.dumps(error_resp))
                    sys.stdout.flush()


if __name__ == "__main__":
    AfoUltimateMCPServer.run_loop()
