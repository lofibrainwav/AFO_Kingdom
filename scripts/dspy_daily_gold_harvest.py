import os
import subprocess
import sys
from datetime import datetime, timedelta


def main():
    # Define Source Mines (SSOT)
    # We look in 'data' for manual gold examples and potential 'logs' for production traces
    search_dirs = ["data", "logs"]

    # Target Gold File
    today = datetime.now().strftime("%Y%m%d")
    target_gold_file = f"data/dspy/gold_commander_briefing_{today}.jsonl"

    # Check sources exist
    valid_inputs = [d for d in search_dirs if os.path.exists(d)]
    if not valid_inputs:
        print("❌ No valid input directories found.")
        sys.exit(1)

    print(f"🌾 Harvesting Gold from: {valid_inputs}")
    print(f"🎯 Target: {target_gold_file}")

    # Construct command to call the Builder (Ticket-003)
    # Use --min_score 0.90 as per Operation Rule A
    cmd = [
        "python",
        "scripts/dspy_build_gold.py",
        "--out",
        target_gold_file,
        "--min_score",
        "0.90",
        "--limit",
        "500",
    ]
    for d in valid_inputs:
        cmd.extend(["--in", d])

    try:
        subprocess.run(cmd, check=True)

        # Verify result
        if os.path.exists(target_gold_file):
            line_count = 0
            with open(target_gold_file) as f:
                line_count = sum(1 for _ in f)
            print(f"✅ Harvest Complete. Yield: {line_count} gold examples.")

            # Append to Master Gold File (Cumulative)
            master_file = "data/dspy/gold_commander_briefing.jsonl"
            # Deduplicate logic could be here, but for now simple append or cat
            # We use 'dspy_build_gold.py' again to merge if needed, or just append distinct lines
            # For Safety, let's keep daily files separate but also maintain a 'latest' link or merge

            # Simple append if not exists to avoid duplication in simplest form?
            # Better: The Builder script handles extraction.
            # Safe Promote will use the specific GOLD file or the master?
            # Let's verify yield count for the Gate.
        else:
            print("⚠️  No gold file created (no data met criteria?).")
    except subprocess.CalledProcessError as e:
        print(f"❌ Harvest Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
