import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class JSONLLogger:
    """
    Writes structured events to a .jsonl file (one JSON object per line).
    This is useful for traceability and debugging agent runs.
    """

    def __init__(self, log_path: Path):
        self.log_path = log_path

    def log(self, phase: str, status: str, details: Dict[str, Any]) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": phase,
            "status": status,
            "details": details,
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")