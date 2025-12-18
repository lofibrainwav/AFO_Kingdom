import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Enhance Path for Sibling Imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Sibling Modules (The Fragments)
try:
    from afo_skills_mcp import AfoSkillsMCP
    from trinity_score_mcp import TrinityScoreEngineHybrid

    MODULES_LOADED = True
except ImportError as e:
    MODULES_LOADED = False
    print(f"⚠️ Failed to load sibling modules: {e}", file=sys.stderr)

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
        abs_path = Path(path).resolve()
        # For now, allow access, but in prod we restrict to WORKSPACE_ROOT
        # if not str(abs_path).startswith(WORKSPACE_ROOT):
        #     raise ValueError(f"Access Denied: Path outside workspace ({path})")
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
                command, shell=True, capture_output=True, text=True, timeout=60, executable="/bin/zsh"
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Exit {result.returncode}\nstderr: {result.stderr.strip()}\nstdout: {result.stdout.strip()}"
        except Exception as e:
            return f"Execution Failure: {str(e)}"

    @staticmethod
    def read_file(path: str) -> str:
        """Reads a file from the filesystem."""
        try:
            target = AfoUltimateMCPServer._validate_path(path)
            if not target.exists():
                return f"Error: File not found ({path})"
            return target.read_text(encoding="utf-8")
        except Exception as e:
            return f"Read Error: {str(e)}"

    @staticmethod
    def write_file(path: str, content: str) -> str:
        """Writes content to a file (Overwrites)."""
        try:
            target = AfoUltimateMCPServer._validate_path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return f"Success: Wrote {len(content)} chars to {path}"
        except Exception as e:
            return f"Write Error: {str(e)}"

    @staticmethod
    def kingdom_health() -> str:
        """Runs the verify_kingdom_core protocol."""
        script_path = os.path.join(WORKSPACE_ROOT, "scripts", "verify_kingdom_core.py")
        if not os.path.exists(script_path):
            # Fallback to status script if core script missing
            script_path = os.path.join(WORKSPACE_ROOT, "scripts", "verify_kingdom_status.py")
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
                                "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                                "required": ["path", "content"],
                            },
                        },
                        {
                            "name": "kingdom_health",
                            "description": "Run the Kingdom Core Health Check protocol.",
                            "inputSchema": {"type": "object", "properties": {}},
                        },
                    ]

                    if MODULES_LOADED:
                        # Trinity Tools
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
                        # Skills Tools
                        tools.append(
                            {
                                "name": "verify_fact",
                                "description": "Verify a factual claim against context (Hallucination Defense).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"claim": {"type": "string"}, "context": {"type": "string"}},
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
                                        "data": {"type": "array", "items": {"type": "number"}},
                                        "weights": {"type": "array", "items": {"type": "number"}},
                                    },
                                    "required": ["data", "weights"],
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
                            content = cls.write_file(args.get("path"), args.get("content"))
                        elif tool_name == "kingdom_health":
                            content = cls.kingdom_health()

                        # 에러 메시지 확인
                        if "Error" in content or "error" in content.lower():
                            is_error = True

                    except Exception as e:
                        content = f"Execution Error: {str(e)}"
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
                            trinity_eval = mcp_tool_trinity_evaluator.evaluate_execution_result(
                                tool_name=tool_name,
                                execution_result=content,
                                execution_time_ms=execution_time_ms,
                                is_error=is_error,
                            )
                            trinity_metadata = trinity_eval["trinity_metrics"]
                        except Exception:
                            trinity_metadata = None

                    # 2. Advanced Tools (from siblings)
                    if MODULES_LOADED and tool_name not in ["shell_execute", "read_file", "write_file", "kingdom_health"]:
                        if tool_name == "calculate_trinity_score":
                            # Convert args to kwargs
                            res = TrinityScoreEngineHybrid.evaluate(**args)
                            content = json.dumps(res, indent=2, ensure_ascii=False)
                            trinity_metadata = res  # Use result as metadata itself

                        elif tool_name == "verify_fact":
                            res = AfoSkillsMCP.verify_fact(args.get("claim"), args.get("context", ""))
                            content = json.dumps(res, indent=2, ensure_ascii=False)
                            # Implied Trinity Score for fact verification
                            trinity_metadata = {"truth_impact": 10 if res["verdict"] == "PLAUSIBLE" else -10}

                        elif tool_name == "cupy_weighted_sum":
                            res = AfoSkillsMCP.cupy_weighted_sum(args.get("data", []), args.get("weights", []))
                            content = str(res)
                        else:
                            content = f"Unknown tool: {tool_name}"
                    elif tool_name not in ["shell_execute", "read_file", "write_file", "kingdom_health"]:
                        content = f"Tool not available (Modules failed to load): {tool_name}"

                    # Core Tools에 대한 Trinity Score 계산 (眞善美孝永 5기둥)
                    if mcp_tool_trinity_evaluator and tool_name in ["shell_execute", "read_file", "write_file", "kingdom_health"]:
                        try:
                            trinity_eval = mcp_tool_trinity_evaluator.evaluate_execution_result(
                                tool_name=tool_name,
                                execution_result=content,
                                execution_time_ms=execution_time_ms,
                                is_error=is_error,
                            )
                            trinity_metadata = trinity_eval["trinity_metrics"]
                        except Exception:
                            trinity_metadata = None

                    # Construct Response
                    result_body = [{"type": "text", "text": str(content)}]

                    # Append Trinity Metadata if available (Serenity Injection)
                    if trinity_metadata:
                        result_body.append({
                            "type": "text",
                            "text": f"\n\n[眞善美孝永 Trinity Score]\n"
                            f"眞 (Truth): {trinity_metadata.get('truth', 0):.2%}\n"
                            f"善 (Goodness): {trinity_metadata.get('goodness', 0):.2%}\n"
                            f"美 (Beauty): {trinity_metadata.get('beauty', 0):.2%}\n"
                            f"孝 (Serenity): {trinity_metadata.get('filial_serenity', 0):.2%}\n"
                            f"永 (Eternity): {trinity_metadata.get('eternity', 0):.2%}\n"
                            f"Trinity Score: {trinity_metadata.get('trinity_score', 0):.2%}\n"
                            f"Balance: {trinity_metadata.get('balance_status', 'unknown')}",
                        })

                    result = {
                        "content": result_body,
                        "isError": is_error,
                        "trinity_score": trinity_metadata,  # 메타데이터를 직접 포함
                    }

                else:
                    # Ignore other messages or return error?
                    pass

                if msg_id is not None:
                    print(json.dumps({"jsonrpc": "2.0", "result": result, "id": msg_id}))
                    sys.stdout.flush()

            except Exception as e:
                # Catch-all to prevent crash
                if msg_id is not None:
                    error_resp = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": msg_id}
                    print(json.dumps(error_resp))
                    sys.stdout.flush()


if __name__ == "__main__":
    AfoUltimateMCPServer.run_loop()
