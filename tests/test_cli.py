from __future__ import annotations

import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

from hh_raiser.cli import build_parser


class CliTests(unittest.TestCase):
    def test_command_line_credentials_are_accepted(self) -> None:
        args = build_parser().parse_args(["--phone", "+79990000000", "--password", "secret"])
        self.assertEqual(args.phone, "+79990000000")
        self.assertEqual(args.password, "secret")

    def test_default_browser_profile_is_next_to_project(self) -> None:
        args = build_parser().parse_args([])
        self.assertEqual(
            args.profile_dir,
            Path(__file__).resolve().parents[1] / ".hh-resume-raiser" / "browser-profile",
        )

    def test_self_test_flag_is_preserved_for_compatibility(self) -> None:
        args = build_parser().parse_args(["--self-test"])
        self.assertTrue(args.self_test)

    def test_page_refresh_timeout_can_be_configured(self) -> None:
        args = build_parser().parse_args(["--page-refresh-seconds", "120"])

        self.assertEqual(args.page_refresh_seconds, 120)

    def test_page_refresh_timeout_must_be_positive(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            build_parser().parse_args(["--page-refresh-seconds", "0"])

    def test_legacy_mode_remains_default(self) -> None:
        args = build_parser().parse_args([])
        self.assertFalse(args.full_activity)

    def test_full_activity_options_are_parsed(self) -> None:
        args = build_parser().parse_args(
            [
                "--full-activity",
                "--vacancies-per-cycle",
                "3",
                "--search-scrolls",
                "4",
                "--vacancy-view-seconds",
                "8.5",
            ]
        )
        self.assertTrue(args.full_activity)
        self.assertEqual(args.vacancies_per_cycle, 3)
        self.assertEqual(args.search_scrolls, 4)
        self.assertEqual(args.vacancy_view_seconds, 8.5)

    def test_activity_limits_are_bounded(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            build_parser().parse_args(["--vacancies-per-cycle", "11"])
