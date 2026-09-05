from __future__ import annotations

import unittest
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from hh_raiser.models import MOSCOW
from hh_raiser.storage import (
    read_next_raise_time,
    resume_refresh_due_at,
    write_next_raise_time,
    write_resume_refresh_attempt,
)


class StorageTests(unittest.TestCase):
    def test_next_raise_time_is_persisted(self) -> None:
        next_at = datetime(2026, 8, 27, 4, 34, tzinfo=MOSCOW)
        with TemporaryDirectory() as directory:
            profile_dir = Path(directory) / "browser-profile"
            write_next_raise_time(profile_dir, next_at)
            self.assertEqual(read_next_raise_time(profile_dir), next_at)
            self.assertTrue((profile_dir.parent / "status.json").exists())

    def test_resume_refresh_due_time_uses_persisted_attempt(self) -> None:
        attempted_at = datetime.now(MOSCOW)
        with TemporaryDirectory() as directory:
            profile_dir = Path(directory) / "browser-profile"
            write_resume_refresh_attempt(profile_dir, attempted_at)

            due_at = resume_refresh_due_at(profile_dir, timedelta(minutes=30))

            self.assertEqual(due_at, attempted_at + timedelta(minutes=30))
