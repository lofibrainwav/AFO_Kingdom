import json
import os
import re
from pathlib import Path


ROOT = Path(os.environ.get("AFO_ROOT", Path.cwd()))
LATEST = ROOT / "artifacts" / "recon" / "latest"


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def exit_code(name: str) -> int:
    c = read_text(LATEST / f"{name}.code").strip()
    try:
        return int(c)
    except Exception:
        return 999


def pick_log(name: str) -> str:
    return read_text(LATEST / f"{name}.log")


def has_listen(port: int, ports_log: str) -> bool:
    return f":{port}" in ports_log and "LISTEN" in ports_log


def summarize_health(body: str):
    body = body.strip()
    if not body:
        return None
    try:
        j = json.loads(body)
        hp = j.get("health_percentage", None)
        st = j.get("status", None)
        svc = j.get("service", None)
        return {"service": svc, "status": st, "health_percentage": hp}
    except Exception:
        return {"raw_head": body[:200]}


def md_facts(md: str):
    ports = sorted(set(int(x) for x in re.findall(r"\b(\d{3,5})\b", md) if 0 < int(x) < 65536))
    fp = re.findall(r"\bAFO-[A-Z0-9]{4}(?:-[A-Z0-9]{4}){3}\b", md)
    return {"ports_in_md": ports, "fingerprints_in_md": fp[:5]}


def crash_signals(text: str):
    pats = [
        r"Traceback",
        r"ModuleNotFoundError",
        r"AuthenticationError",
        r"ECONNREFUSED",
        r"EADDRINUSE",
        r"address already in use",
        r"FATAL",
        r"panic",
        r"TypeError",
        r"ReferenceError",
        r"Unhandled",
        r"SIGKILL|SIGSEGV",
    ]
    hits = []
    for pat in pats:
        if re.search(pat, text, re.IGNORECASE):
            hits.append(pat)
    return hits


def main():
    ts = read_text(LATEST / "_ts.txt").strip()
    ports_log = pick_log("ports_listen")
    docker_ps = pick_log("docker_ps")
    compose_ps = pick_log("docker_compose_ps")

    health = summarize_health(pick_log("curl_8010_health"))
    dash = pick_log("curl_3000")

    state_md_paths = pick_log("find_state_md").splitlines()
    md_path = None
    for line in state_md_paths:
        line = line.strip()
        if line.endswith("AFO_STATE_OF_KINGDOM.md") and Path(line).exists():
            md_path = Path(line)
            break
    md_text = read_text(md_path) if md_path else ""
    md_info = md_facts(md_text) if md_text else None

    log_files = {
        "api_server.log": pick_log("tail_api_server.log"),
        "server.log": pick_log("tail_server.log"),
        "dashboard_reboot.log": pick_log("tail_dashboard_reboot.log"),
        "dashboard_final.log": pick_log("tail_dashboard_final.log"),
    }
    log_hits = {
        k: crash_signals(v)
        for k, v in log_files.items()
        if v and v.strip() and v.strip() != "NOT_FOUND"
    }

    print("=== AFO Kingdom Recon Report (Ji-Pi-Ji-Gi) ===")
    print(f"As-of: {ts}")
    print()

    print("[Ports]")
    for p in [8010, 3000, 15432, 6379, 3001, 3002]:
        up = has_listen(p, ports_log)
        print(f"- :{p} LISTEN = {up!s}")
    print()

    print("[Docker]")
    print("- docker ps exit =", exit_code("docker_ps"))
    print("- compose ps exit =", exit_code("docker_compose_ps"))
    if docker_ps.strip():
        lines = docker_ps.splitlines()[:15]
        for ln in lines:
            print("  " + ln)
    if compose_ps.strip():
        lines = compose_ps.splitlines()[:15]
        for ln in lines:
            print("  " + ln)
    print()

    print("[Health Endpoints]")
    print("- 8010 /health =", health)
    print("- 8010 /metrics exit =", exit_code("curl_8010_metrics"))
    print("- 3000 HTTP head:")
    for ln in dash.splitlines()[:12]:
        print("  " + ln)
    print()

    print("[AFO_STATE_OF_KINGDOM.md]")
    if md_info is None:
        print("- NOT_FOUND")
    else:
        print("- ports_in_md:", md_info["ports_in_md"][:20])
        print("- fingerprints_in_md:", md_info["fingerprints_in_md"])
    print()

    print("[Crash Signals]")
    if not log_hits:
        print("- No known log files found or no crash signals detected in tails.")
    else:
        for k, hits in log_hits.items():
            print(f"- {k}: {hits}")
    print()

    print("[Git]")
    print(pick_log("git_status").strip())
    print()

    print("[Next Decision]")
    if exit_code("curl_8010_health") == 0:
        print("- Soul Engine: UP (health reachable)")
    else:
        print("- Soul Engine: DOWN or not reachable (run docker logs + port conflict check first)")
    if "EADDRINUSE" in (log_hits.get("api_server.log") or []) or "address already in use" in (
        log_hits.get("api_server.log") or []
    ):
        print("- Likely: Port conflict (EADDRINUSE)")
    if "TypeError" in (log_hits.get("dashboard_final.log") or []) or "ReferenceError" in (
        log_hits.get("dashboard_final.log") or []
    ):
        print("- Likely: Dashboard build/runtime crash (TS/JS)")
if __name__ == "__main__":
    main()
