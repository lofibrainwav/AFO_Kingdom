import json
import os
import queue
import subprocess
import sys
import threading
import time
from typing import Any, Dict, Optional, Tuple

def now() -> float:
    return time.monotonic()

def spawn() -> subprocess.Popen:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    cmd = [os.path.join(os.getcwd(), ".venv-mcp/bin/python"), "-u", "-m", "AFO.mcp.afo_skills_mcp"]
    return subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
        bufsize=1,
    )

def reader_thread(proc: subprocess.Popen, q: "queue.Queue[str]") -> None:
    assert proc.stdout is not None
    for line in proc.stdout:
        q.put(line)

def send(proc: subprocess.Popen, obj: Dict[str, Any]) -> None:
    assert proc.stdin is not None
    proc.stdin.write(json.dumps(obj) + "\n")
    proc.stdin.flush()

def try_parse(line: str) -> Optional[Dict[str, Any]]:
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except Exception:
        return None

def recv_for_id(q: "queue.Queue[str]", want_id: int, timeout_s: float) -> Tuple[Optional[Dict[str, Any]], list]:
    deadline = now() + timeout_s
    junk: list = []
    while now() < deadline:
        remaining = max(0.0, deadline - now())
        try:
            line = q.get(timeout=min(0.2, remaining))
        except queue.Empty:
            continue
        obj = try_parse(line)
        if obj is None:
            junk.append(line.rstrip("\n"))
            continue
        if obj.get("id") == want_id:
            return obj, junk
        junk.append(line.rstrip("\n"))
    return None, junk

def main() -> int:
    os.chdir("/Users/brnestrm/AFO_Kingdom")

    base = os.environ.get("AFO_API_BASE_URL", "http://127.0.0.1:8010")
    py_path = os.environ.get("PYTHONPATH", "")
    if "/Users/brnestrm/AFO_Kingdom/packages/afo-core" not in py_path.split(":"):
        os.environ["PYTHONPATH"] = "/Users/brnestrm/AFO_Kingdom/packages/afo-core" + (":" + py_path if py_path else "")
    os.environ["AFO_API_BASE_URL"] = base

    proc = spawn()
    q: "queue.Queue[str]" = queue.Queue()
    t = threading.Thread(target=reader_thread, args=(proc, q), daemon=True)
    t.start()

    init_id = 1
    send(proc, {
        "jsonrpc": "2.0",
        "id": init_id,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": "afo-smoke", "version": "0.2"},
            "capabilities": {}
        }
    })
    init_resp, init_junk = recv_for_id(q, init_id, 10.0)
    if init_resp is None:
        print("FAIL: initialize timeout")
        for s in init_junk[-30:]:
            print(s)
        proc.terminate()
        return 1
    print("OK: initialize")

    tools_id = 2
    send(proc, {"jsonrpc": "2.0", "id": tools_id, "method": "tools/list", "params": {}})
    tools_resp, tools_junk = recv_for_id(q, tools_id, 10.0)
    if tools_resp is None:
        print("FAIL: tools/list timeout")
        for s in tools_junk[-30:]:
            print(s)
        proc.terminate()
        return 1

    tools = (((tools_resp.get("result") or {}).get("tools")) or [])
    names = [t.get("name") for t in tools if isinstance(t, dict)]
    print(f"OK: tools/list ({len(names)}): {', '.join([n for n in names if n])}")

    shutdown_id = 3
    send(proc, {"jsonrpc": "2.0", "id": shutdown_id, "method": "shutdown", "params": {}})
    _shutdown_resp, _ = recv_for_id(q, shutdown_id, 5.0)

    send(proc, {"jsonrpc": "2.0", "method": "exit", "params": {}})

    if proc.stdin:
        proc.stdin.close()

    try:
        proc.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3.0)

    code = proc.returncode
    if code == 0:
        print("PASS: clean exit (0)")
        return 0
    print(f"WARN: exit code {code}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
