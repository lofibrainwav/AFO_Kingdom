# Language: ko-KR (AFO SSOT)
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from typing import List


# Configuration
# Configuration
GOLD_PATH = os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_factcard_graphrag.jsonl")
GATE_THRESHOLD = 200
DASHBOARD_PATH = "data/dspy/gate_dashboard.html"
STATUS_PATH = "data/dspy/gate_monitor.json"

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>AFO Kingdom - Intelligence Gate</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {{ font-family: sans-serif; background: #111; color: #eee; padding: 20px; }}
    .card {{ background: #222; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; }}
    h1, h2 {{ color: #a8d1ff; }}
    .status-locked {{ color: #ff6b6b; font-weight: bold; }}
    .status-open {{ color: #51cf66; font-weight: bold; }}
    .metric {{ font-size: 24px; font-weight: bold; }}
    canvas {{ max-height: 400px; }}
  </style>
</head>
<body>
  <h1>🏰 AFO Intelligence Gate Monitor</h1>
  
  <div class="card">
    <h2>Gate Status: <span class="{status_class}">{status_text}</span></h2>
    <p>Target: <strong>{threshold}</strong> Gold Samples</p>
    <p>Current: <strong class="metric">{current}</strong> Gold Samples</p>
    <p>Progress: {progress}%</p>
  </div>

  <div class="card">
    <canvas id="goldChart"></canvas>
  </div>

  <div class="card">
    <canvas id="trinityRadar"></canvas>
  </div>

  <script>
    // Gold Count Gauge
    const goldCtx = document.getElementById('goldChart').getContext('2d');
    new Chart(goldCtx, {{
      type: 'doughnut',
      data: {{
        labels: ['Collected', 'Remaining'],
        datasets: [{{
          data: [{current}, {remaining}],
          backgroundColor: ['#ffd700', '#333'],
          borderWidth: 0
        }}]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ position: 'bottom' }},
          title: {{ display: true, text: 'Gold Harvest Progress' }}
        }}
      }}
    }});

    // Trinity Score Sim (Placeholder until real avg calc)
    // 眞=0.35, 善=0.35, 美=0.20, 孝=0.08, 永=0.02
    new Chart(document.getElementById('trinityRadar'), {{
      type: 'radar',
      data: {{
        labels: ['Truth (眞)', 'Goodness (善)', 'Beauty (美)', 'Serenity (孝)', 'Eternity (永)'],
        datasets: [{{
          label: 'Current Avg Trinity',
          data: [0.85, 0.90, 0.80, 0.95, 0.99], // Mock/Placeholder avg
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        }}]
      }},
      options: {{
        scales: {{ r: {{ suggestedMin: 0, suggestedMax: 1 }} }}
      }}
    }});
  </script>
</body>
</html>
"""


def read_jsonl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except:
                pass
    return rows


def main():
    gold_rows = read_jsonl(GOLD_PATH)
    count = len(gold_rows)

    is_open = count >= GATE_THRESHOLD
    status_text = "OPEN" if is_open else "LOCKED (Gathering Data)"
    status_class = "status-open" if is_open else "status-locked"
    remaining = max(0, GATE_THRESHOLD - count)
    progress = round((count / GATE_THRESHOLD) * 100, 1) if GATE_THRESHOLD > 0 else 100

    # Generate Dashboard
    html = HTML_TEMPLATE.format(
        status_text=status_text,
        status_class=status_class,
        threshold=GATE_THRESHOLD,
        current=count,
        remaining=remaining,
        progress=progress,
    )

    os.makedirs(os.path.dirname(DASHBOARD_PATH), exist_ok=True)
    pathlib.Path(DASHBOARD_PATH).write_text(html, encoding="utf-8")

    status_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "OPEN" if is_open else "LOCKED",
        "gold_count": count,
        "threshold": GATE_THRESHOLD,
        "dashboard": DASHBOARD_PATH,
    }
    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(status_data, f, indent=2)

    print(f"[{status_text}] Gold: {count}/{GATE_THRESHOLD}")
    print(f"- Dashboard: {DASHBOARD_PATH}")

    if is_open:
        print(">> GATE OPEN! Initiating MIPROv2 Optimization Sequence...")
        try:
            # Run the optimization script
            cmd = [sys.executable, "scripts/dspy_optimize_commander_briefing.py"]
            print(f">> Executing: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)

            # Update Dashboard to reflect new optimized status if needed (optional)
            # For now, just logging completion
            print(">> MIPROv2 Optimization COMPLETE (See output above).")

        except subprocess.CalledProcessError as e:
            print(f"!! MIPROv2 Optimization FAILED: {e}", file=sys.stderr)
            print(f"!! STDERR: {e.stderr}", file=sys.stderr)
    else:
        print(f">> GATE LOCKED. Waiting for {remaining} more gold samples.")
        print(">> System Sleeping (Safe Mode)")


if __name__ == "__main__":
    main()
