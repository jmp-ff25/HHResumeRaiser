from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from hh_raiser.models import MOSCOW
from hh_raiser.storage import read_next_raise_time, write_next_raise_time


class StorageTests(unittest.TestCase):
    def test_next_raise_time_is_persisted(self) -> None:
        next_at = datetime(2026, 8, 27, 4, 34, tzinfo=MOSCOW)
        with TemporaryDirectory() as directory:
            profile_dir = Path(directory) / "browser-profile"
            write_next_raise_time(profile_dir, next_at)
            self.assertEqual(read_next_raise_time(profile_dir), next_at)
            self.assertTrue((profile_dir.parent / "status.json").exists())
