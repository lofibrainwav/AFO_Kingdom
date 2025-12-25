#!/usr/bin/env python3
"""
AFO Kingdom - Dynamic Status Generator
Generates kingdom_status.html with real-time data from git, ruff, and Trinity Score.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_cmd(cmd: str) -> str:
    """Run shell command and return output."""
    result = subprocess.run(
        cmd,
        check=False,
        shell=True,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    return result.stdout.strip()


def get_git_stats() -> dict:
    """Get git statistics."""
    total_commits = run_cmd("git rev-list --count HEAD")
    head_sha = run_cmd("git rev-parse --short HEAD")
    branch = run_cmd("git branch --show-current")
    today_commits = run_cmd("git log --oneline --since='midnight' | wc -l").strip()
    status = run_cmd("git status --porcelain")
    synced = "✅ Synced" if not status else "⚠️ Uncommitted"

    # Get timeline milestones
    first_commit = run_cmd("git log --oneline --reverse | head -1")
    latest_commit = run_cmd("git log --oneline -1")

    return {
        "total": total_commits,
        "today": today_commits,
        "head": head_sha,
        "branch": branch,
        "synced": synced,
        "first": first_commit,
        "latest": latest_commit,
    }


def get_ruff_stats() -> dict:
    """Get ruff error count."""
    output = run_cmd("ruff check packages/ 2>&1 | tail -1")
    # Parse "Found X errors."
    count = output.split()[1] if "Found" in output else "0"
    return {"errors": count}


def get_trinity_score() -> dict:
    """Get Trinity Score from trinity_score.json if exists."""
    try:
        with Path(Path(__file__).parent / "trinity_score.json").open(
            encoding="utf-8"
        ) as f:
            data = json.load(f)
            scores = data.get("trinity", {}).get("scores", {})
            total = data.get("trinity", {}).get("total", 1.0)
            return {
                "total": round(total * 100, 1),
                "truth": scores.get("truth", 1.0),
                "goodness": scores.get("goodness", 1.0),
                "beauty": scores.get("beauty", 1.0),
                "serenity": scores.get("serenity", 1.0),
                "eternity": scores.get("eternity", 1.0),
            }
    except Exception:
        return {
            "total": 100.0,
            "truth": 1.0,
            "goodness": 1.0,
            "beauty": 1.0,
            "serenity": 1.0,
            "eternity": 1.0,
        }


def get_package_stats() -> dict:
    """Get file counts per package."""
    packages = {}
    for pkg in ["afo-core", "trinity-os", "dashboard", "aicpa-core", "sixXon"]:
        count = run_cmd(f"find packages/{pkg} -type f 2>/dev/null | wc -l").strip()
        packages[pkg] = count
    return packages


def get_timeline() -> list:
    """Get key timeline milestones."""
    output = run_cmd("git log --oneline --reverse")
    lines = output.split("\n")
    milestones = []
    key_indices = [0, 4, 42, 44, 62, 70, 90, 103, len(lines) - 1]

    for i in key_indices:
        if i < len(lines) and lines[i]:
            parts = lines[i].split(" ", 1)
            if len(parts) == 2:
                milestones.append(
                    {"num": i + 1, "hash": parts[0], "msg": parts[1][:50]}
                )

    return milestones


def generate_html():
    """Generate the HTML dashboard."""
    git = get_git_stats()
    ruff = get_ruff_stats()
    trinity = get_trinity_score()
    packages = get_package_stats()
    timeline = get_timeline()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calculate file count
    total_files = run_cmd("git ls-tree -r HEAD --name-only | wc -l").strip()

    timeline_html = "\n".join(
        [
            f'<div class="timeline-item"><span class="timeline-num">#{m["num"]}</span>'
            f'<span class="timeline-hash">{m["hash"]}</span>'
            f'<span class="timeline-msg">{m["msg"]}</span></div>'
            for m in timeline
        ]
    )

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFO Kingdom - Status Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: #fff;
            padding: 40px;
        }}
        h1 {{
            text-align: center;
            font-size: 3rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{ text-align: center; color: #888; margin-bottom: 40px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .card h2 {{ font-size: 1.2rem; margin-bottom: 15px; color: #FFD700; }}
        .stat {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .stat:last-child {{ border: none; }}
        .stat-value {{ font-weight: bold; color: #4ade80; }}
        .stat-value.warning {{ color: #fbbf24; }}
        .timeline {{ margin-top: 40px; }}
        .timeline h2 {{ text-align: center; margin-bottom: 30px; font-size: 1.5rem; }}
        .timeline-item {{
            display: flex; gap: 20px; padding: 15px;
            background: rgba(255,255,255,0.03); border-radius: 10px;
            margin-bottom: 10px; border-left: 4px solid #FFD700;
        }}
        .timeline-num {{ font-weight: bold; color: #FFD700; min-width: 40px; }}
        .timeline-hash {{ color: #60a5fa; font-family: monospace; min-width: 80px; }}
        .timeline-msg {{ color: #e5e5e5; }}
        .trinity-score {{
            text-align: center; padding: 40px;
            background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,165,0,0.1));
            border-radius: 30px; margin-bottom: 30px;
        }}
        .trinity-number {{ font-size: 5rem; font-weight: bold; color: #FFD700; }}
        .trinity-label {{ color: #888; font-size: 1.2rem; }}
        .pillars {{ display: flex; justify-content: center; gap: 30px; margin-top: 20px; flex-wrap: wrap; }}
        .pillar {{ text-align: center; }}
        .pillar-name {{ font-size: 1.5rem; }}
        .pillar-weight {{ color: #888; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>👑 AFO Kingdom Status</h1>
    <p class="subtitle">Generated: {now} | {git["total"]} Commits</p>

    <div class="trinity-score">
        <div class="trinity-number">{trinity["total"]}</div>
        <div class="trinity-label">Trinity Score (眞善美孝永)</div>
        <div class="pillars">
            <div class="pillar"><div class="pillar-name">眞 {trinity["truth"]}</div><div class="pillar-weight">Truth 35%</div></div>
            <div class="pillar"><div class="pillar-name">善 {trinity["goodness"]}</div><div class="pillar-weight">Goodness 35%</div></div>
            <div class="pillar"><div class="pillar-name">美 {trinity["beauty"]}</div><div class="pillar-weight">Beauty 20%</div></div>
            <div class="pillar"><div class="pillar-name">孝 {trinity["serenity"]}</div><div class="pillar-weight">Serenity 8%</div></div>
            <div class="pillar"><div class="pillar-name">永 {trinity["eternity"]}</div><div class="pillar-weight">Eternity 2%</div></div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>📊 Git Status</h2>
            <div class="stat"><span>Total Commits</span><span class="stat-value">{git["total"]}</span></div>
            <div class="stat"><span>Today's Commits</span><span class="stat-value">{git["today"]}</span></div>
            <div class="stat"><span>HEAD</span><span class="stat-value">{git["head"]}</span></div>
            <div class="stat"><span>Branch</span><span class="stat-value">{git["branch"]}</span></div>
            <div class="stat"><span>Sync Status</span><span class="stat-value">{git["synced"]}</span></div>
        </div>
        <div class="card">
            <h2>🔧 Code Quality</h2>
            <div class="stat"><span>Ruff Errors</span><span class="stat-value warning">{ruff["errors"]}</span></div>
            <div class="stat"><span>Tracked Files</span><span class="stat-value">{total_files}</span></div>
        </div>
        <div class="card">
            <h2>📦 Packages</h2>
            <div class="stat"><span>afo-core</span><span class="stat-value">{packages.get("afo-core", "?")} files</span></div>
            <div class="stat"><span>trinity-os</span><span class="stat-value">{packages.get("trinity-os", "?")} files</span></div>
            <div class="stat"><span>dashboard</span><span class="stat-value">{packages.get("dashboard", "?")} files</span></div>
            <div class="stat"><span>aicpa-core</span><span class="stat-value">{packages.get("aicpa-core", "?")} files</span></div>
            <div class="stat"><span>sixXon</span><span class="stat-value">{packages.get("sixXon", "?")} files</span></div>
        </div>
    </div>

    <div class="timeline">
        <h2>🌳 Kingdom Timeline</h2>
        {timeline_html}
    </div>

    <p style="text-align: center; margin-top: 40px; color: #666;">
        Dynamic Generator by 승상 (Seungsang) | AFO Kingdom | 眞善美孝永
    </p>
</body>
</html>"""

    output_path = Path(__file__).parent / "kingdom_status.html"
    output_path.write_text(html)
    print(f"✅ Generated: {output_path}")
    print(
        f"📊 Commits: {git["total"]}, Trinity: {trinity["total"]}, Ruff: {ruff["errors"]}"
    )


if __name__ == "__main__":
    generate_html()
