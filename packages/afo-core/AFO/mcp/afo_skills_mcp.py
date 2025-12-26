#!/usr/bin/env python3
"""
AFO Skills MCP Server
MCP (Model Context Protocol) server for AFO Kingdom skills and GenUI functionality.
Implements stdio-based MCP protocol for Cursor IDE integration.
"""

import json
import logging
import os
import socket
import sys
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

# Configure logging for production
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Custom timeout exception for cross-platform compatibility
class MCPTimeoutError(Exception):
    """Custom timeout exception for MCP operations"""
    pass


def _base_url() -> str:
    """Get base URL for AFO API with validation"""
    base_url = os.environ.get("AFO_API_BASE_URL", "http://127.0.0.1:8010")
    if not base_url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid AFO_API_BASE_URL: {base_url}")
    return base_url.rstrip("/")


def _http(method: str, path: str, body: Optional[dict] = None, timeout: float = 5.0, max_retries: int = 2) -> Any:
    """HTTP helper for AFO API calls with retry logic and better error handling"""
    if not isinstance(method, str) or method.upper() not in ['GET', 'POST', 'PUT', 'DELETE']:
        raise ValueError(f"Invalid HTTP method: {method}")

    url = f"{_base_url()}{path}"
    headers = {"Accept": "application/json", "User-Agent": "AFO-Skills-MCP/1.0.0"}

    data = None
    if body is not None:
        if not isinstance(body, dict):
            raise ValueError("Request body must be a dictionary")
        try:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid request body: {e}")

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                if not raw:
                    return {"ok": True, "http_status": resp.status, "body": ""}

                try:
                    return json.loads(raw)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response: {e}")
                    return {"ok": False, "http_status": resp.status, "body": raw, "parse_error": str(e)}

        except urllib.request.HTTPError as e:
            if e.code >= 500 and attempt < max_retries:  # Retry on server errors
                logger.warning(f"HTTP {e.code} on attempt {attempt + 1}, retrying...")
                time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                continue
            return {"ok": False, "http_status": e.code, "body": e.read().decode("utf-8"), "error": str(e)}

        except (urllib.request.URLError, socket.timeout, OSError) as e:
            if attempt < max_retries:
                logger.warning(f"Network error on attempt {attempt + 1}: {e}, retrying...")
                time.sleep(0.5 * (attempt + 1))
                continue
            return {"ok": False, "http_status": None, "body": "", "error": f"Network error: {e}"}

    return {"ok": False, "http_status": None, "body": "", "error": "Max retries exceeded"}


def send_response(request_id: Any, result: Any) -> None:
    """Send JSON-RPC response with immediate flush"""
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }
    print(json.dumps(response), flush=True)
    sys.stdout.flush()  # Ensure immediate flush


def send_error(request_id: Any, code: int, message: str) -> None:
    """Send JSON-RPC error"""
    error = {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message
        }
    }
    print(json.dumps(error), flush=True)


def handle_initialize(request_id: Any, params: Dict[str, Any]) -> None:
    """Handle initialize request"""
    result = {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {"listChanged": False}
        },
        "serverInfo": {
            "name": "AFO Skills MCP Server",
            "version": "1.0.0"
        }
    }
    send_response(request_id, result)


def handle_tools_list(request_id: Any, params: Dict[str, Any]) -> None:
    """Handle tools/list request"""
    tools = [
        {
            "name": "skills_list",
            "description": "List available AFO skills with optional filtering",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "category": {"type": "string", "description": "Category filter"},
                    "limit": {"type": "integer", "description": "Max results", "default": 200}
                }
            }
        },
        {
            "name": "skills_detail",
            "description": "Get detailed information about a specific skill",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "skill_id": {"type": "string", "description": "Skill ID"}
                },
                "required": ["skill_id"]
            }
        },
        {
            "name": "skills_execute",
            "description": "Execute a skill with given parameters",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "skill_id": {"type": "string", "description": "Skill ID"},
                    "inputs": {"type": "object", "description": "Skill inputs"},
                    "dry_run": {"type": "boolean", "description": "Dry run mode", "default": True}
                },
                "required": ["skill_id"]
            }
        },
        {
            "name": "genui_generate",
            "description": "Generate UI components using GenUI",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Generation prompt"},
                    "template": {"type": "string", "description": "Template type", "default": "component"},
                    "constraints": {"type": "string", "description": "Additional constraints"}
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "afo_api_health",
            "description": "Check AFO API health status",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]
    send_response(request_id, {"tools": tools})


def _execute_tool_with_timeout(tool_name: str, args: Dict[str, Any], timeout_seconds: float = 5.0) -> Any:
    """Execute tool with timeout protection using threading (cross-platform)"""
    import threading

    result_container = {"result": None, "exception": None}

    def execute_tool():
        try:
            if tool_name == "skills_list":
                result = _http("GET", f"/api/skills/list?{urllib.parse.urlencode({k: v for k, v in args.items() if v is not None})}")
            elif tool_name == "skills_detail":
                if "skill_id" not in args:
                    raise ValueError("skill_id is required")
                safe_id = urllib.parse.quote(str(args["skill_id"]), safe="")
                result = _http("GET", f"/api/skills/detail/{safe_id}")
            elif tool_name == "skills_execute":
                if "skill_id" not in args:
                    raise ValueError("skill_id is required")
                result = _http("POST", "/api/skills/execute", {
                    "skill_id": args["skill_id"],
                    "inputs": args.get("inputs", {}),
                    "dry_run": args.get("dry_run", True)
                })
            elif tool_name == "genui_generate":
                if "prompt" not in args:
                    raise ValueError("prompt is required")
                result = _http("POST", "/api/genui/generate", {
                    "prompt": args["prompt"],
                    "template": args.get("template", "component"),
                    "constraints": args.get("constraints", "")
                })
            elif tool_name == "afo_api_health":
                result = _http("GET", "/api/skills/health")
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            result_container["result"] = result

        except Exception as e:
            result_container["exception"] = e

    # Start execution in a separate thread
    tool_thread = threading.Thread(target=execute_tool, daemon=True)
    tool_thread.start()
    tool_thread.join(timeout_seconds)

    # Check if thread is still alive (timed out)
    if tool_thread.is_alive():
        return {"ok": False, "error": f"Tool {tool_name} timed out after {timeout_seconds} seconds"}

    # Check for exceptions
    if result_container["exception"] is not None:
        exception = result_container["exception"]
        if isinstance(exception, ValueError):
            return {"ok": False, "error": f"Validation error: {str(exception)}"}
        else:
            return {"ok": False, "error": f"Tool execution failed: {str(exception)}"}

    return result_container["result"]


def handle_tools_call(request_id: Any, params: Dict[str, Any]) -> None:
    """Handle tools/call request with timeout protection"""
    tool_name = params.get("name")
    args = params.get("arguments", {})

    # Execute tool with timeout protection
    result = _execute_tool_with_timeout(tool_name, args, 5.0)

    # Format result for MCP
    content = [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}]
    send_response(request_id, {"content": content})


def handle_notifications(request: Dict[str, Any]) -> None:
    """Handle notification (no response needed)"""
    pass


def main():
    """Main MCP server loop with proper EOF handling"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:  # EOF reached
                break

            if not line.strip():
                continue

            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                handle_initialize(request_id, params)
            elif method == "tools/list":
                handle_tools_list(request_id, params)
            elif method == "tools/call":
                handle_tools_call(request_id, params)
            elif method == "shutdown":
                # Handle shutdown gracefully
                response = {"jsonrpc": "2.0", "id": request_id, "result": {"ok": True}}
                print(json.dumps(response), flush=True)
                sys.stdout.flush()
                break
            elif method == "exit":
                # Handle exit gracefully
                response = {"jsonrpc": "2.0", "id": request_id, "result": {"ok": True}}
                print(json.dumps(response), flush=True)
                sys.stdout.flush()
                break
            elif method.startswith("notifications/") or method == "$/cancelRequest":
                handle_notifications(request)
            else:
                # Unknown method - ignore silently for compatibility
                pass

        except json.JSONDecodeError:
            # Invalid JSON - ignore
            continue
        except Exception as e:
            # Unexpected error
            if "request_id" in locals() and request_id is not None:
                send_error(request_id, -32603, f"Internal error: {str(e)}")
            continue


if __name__ == "__main__":
    main()