# (Writes structured logs)
# Purpose:
# Ensures standardized event format for downstream phases.

import csv
from pathlib import Path

class LogWriter:
    def __init__(self):
        self.output_dir = Path("data/raw_logs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.file_path = self.output_dir / "event_logs.csv"
        self.headers = [
            "case_id", "step", "timestamp",
            "actor", "duration_minutes", "cost"
        ]

        if not self.file_path.exists():
            with open(self.file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    def write(self, event):
        with open(self.file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(event.values())
