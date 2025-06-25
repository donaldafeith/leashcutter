from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class TestRecord:
    timestamp: str
    prompt: str
    commercial_response: str
    local_response: str
    diff_html: str


def log_record(path: str, record: TestRecord) -> None:
    p = Path(path)
    exists = p.exists()
    with p.open("a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(TestRecord.__dataclass_fields__.keys())
        writer.writerow(
            [
                record.timestamp,
                record.prompt,
                record.commercial_response,
                record.local_response,
                record.diff_html,
            ]
        )


def create_record(
    prompt: str, commercial: str, local: str, diff_html: str
) -> TestRecord:
    return TestRecord(
        timestamp=datetime.utcnow().isoformat(),
        prompt=prompt,
        commercial_response=commercial,
        local_response=local,
        diff_html=diff_html,
    )
