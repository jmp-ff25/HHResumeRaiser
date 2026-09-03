from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from hh_raiser.domain.result import ActivityResult


def append_activity_results(path: Path, results: list[ActivityResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        for result in results:
            payload = asdict(result)
            payload["occurred_at"] = result.occurred_at.isoformat()
            stream.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")
