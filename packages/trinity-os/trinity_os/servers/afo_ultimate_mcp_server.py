import json
import os
import subprocess
import sys
from pathlib import Path

# Constants
WORKSPACE_ROOT = os.environ.get("WORKSPACE_ROOT", os.getcwd())


class AfoUltimateMCPServer:
    """
    [AFO Ultimate MCP]
    The Universal Connector & Commander for the AFO Kingdom.
    Architecture: Vanilla JSON-RPC 2.0 (Zero Dependency check).
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
        """Runs the verify_kingdom_status protocol."""
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
                        "serverInfo": {"name": "AfoUltimate", "version": "0.1.0"},
                    }
                elif method == "notifications/initialized":
                    continue

                elif method == "tools/list":
                    result = {
                        "tools": [
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
                                "description": "Run the Kingdom Health Check protocol.",
                                "inputSchema": {"type": "object", "properties": {}},
                            },
                        ]
                    }

                elif method == "tools/call":
                    # Tool Execution Logic
                    tool_name = params.get("name")
                    args = params.get("arguments", {})

                    content = ""
                    if tool_name == "shell_execute":
                        content = cls.shell_execute(args.get("command"))
                    elif tool_name == "read_file":
                        content = cls.read_file(args.get("path"))
                    elif tool_name == "write_file":
                        content = cls.write_file(args.get("path"), args.get("content"))
                    elif tool_name == "kingdom_health":
                        content = cls.kingdom_health()
                    else:
                        content = f"Unknown tool: {tool_name}"

                    result = {"content": [{"type": "text", "text": str(content)}], "isError": False}

                else:
                    # Ignore other messages or return error?
                    # For stability, we ignore unknown methods or return null
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
