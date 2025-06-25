from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


def ensure_file(path: Path) -> None:
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "timestamp",
                    "prompt",
                    "commercial",
                    "local",
                    "diff_html",
                ]
            )


def log_test(
    path: str | Path,
    prompt: str,
    commercial: str,
    local: str,
    diff_html: str,
) -> None:
    path = Path(path)
    ensure_file(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [datetime.utcnow().isoformat(), prompt, commercial, local, diff_html]
        )
