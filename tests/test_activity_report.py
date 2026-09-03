from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hh_raiser.domain.result import ActivityResult, ActivityStatus
from hh_raiser.reporting.activity_report import append_activity_results


class ActivityReportTests(unittest.TestCase):
    def test_appends_json_lines_without_urls(self) -> None:
        result = ActivityResult(
            action="review_search",
            status=ActivityStatus.SUCCESS,
            detail="ok",
            metadata={"card_count": 12},
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            append_activity_results(path, [result])
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["metadata"], {"card_count": 12})
        self.assertNotIn("url", payload)
