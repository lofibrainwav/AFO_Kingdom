from __future__ import annotations

import json
from pathlib import Path

from AFO.julie_cpa.csv_inbox_labeler import _load_rules, label_csv_file


def test_labeler_basic(tmp_path: Path) -> None:
    rules_path = Path("config/julie_cpa/label_rules.json")
    rules = _load_rules(rules_path)

    csv_path = tmp_path / "t.csv"
    csv_path.write_text(
        "date,description,amount\n"
        "2025-12-01,Costco,-10.00\n"
        "2025-12-02,Vanguard,-2000.00\n"
        "2025-12-03,Something,5.00\n",
        encoding="utf-8",
    )

    report = label_csv_file(csv_path, rules)
    assert report["labeled_rows"] == 3
    assert report["label_counts"]["groceries"] == 1
    assert report["label_counts"]["investment"] == 1
    assert report["label_counts"]["unknown"] == 1
    assert report["queue_size"] >= 2
    json.dumps(report)
