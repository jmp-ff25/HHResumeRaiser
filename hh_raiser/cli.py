from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from hh_raiser.browser import (
    NetworkCapture,
    close_context_quietly,
    login_if_needed,
    wait_for_profile_content,
)
from hh_raiser.logging_config import LOGGER, configure_logging
from hh_raiser.models import PROFILE_URL
from hh_raiser.scheduling import format_wait_duration, seconds_until, wait_for_due_time
from hh_raiser.service import run_cycle


def positive_seconds(value: str) -> int:
    seconds = int(value)
    if seconds <= 0:
        raise argparse.ArgumentTypeError("Значение должно быть больше нуля")
    return seconds


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Поднимает одно резюме HH, когда действие доступно."
    )
    parser.add_argument(
        "--resume-title", default=os.environ.get("HH_RESUME_TITLE", "Python-разработчик")
    )
    parser.add_argument(
        "--profile-dir",
        type=Path,
        default=Path(
            os.environ.get(
                "HH_PROFILE_DIR",
                Path(__file__).resolve().parents[1] / ".hh-resume-raiser" / "browser-profile",
            )
        ).expanduser(),
    )
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--check-login", action="store_true")
    parser.add_argument("--phone")
    parser.add_argument("--password")
    parser.add_argument("--credentials-file", type=Path)
    parser.add_argument("--install-browser", action="store_true")
    parser.add_argument("--self-test", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--poll-seconds", type=int, default=600)
    parser.add_argument(
        "--page-refresh-seconds",
        type=positive_seconds,
        default=300,
        help="Перезагрузить страницу, если её состояние не меняется указанное число секунд.",
    )
    parser.add_argument("--buffer-seconds", type=int, default=30)
    parser.add_argument("--minimum-cooldown-hours", type=float, default=4.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging()
    if args.self_test:
        import unittest

        tests_dir = Path(__file__).resolve().parents[1] / "tests"
        suite = unittest.defaultTestLoader.discover(str(tests_dir))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        return 0 if result.wasSuccessful() else 1

    args.profile_dir = args.profile_dir.resolve()
    browser_dir = args.profile_dir.parent / "playwright-browsers"
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browser_dir)
    if args.install_browser:
        args.profile_dir.parent.mkdir(parents=True, exist_ok=True)
        return subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"], check=False
        ).returncode
    from playwright.sync_api import sync_playwright

    args.profile_dir.parent.mkdir(parents=True, exist_ok=True)
    if args.check_login:
        with (
            TemporaryDirectory(dir=args.profile_dir.parent, prefix="login-check-") as temporary_dir,
            sync_playwright() as playwright,
        ):
            context = playwright.chromium.launch_persistent_context(
                temporary_dir, headless=args.headless, viewport=None, args=["--start-maximized"]
            )
            page = context.pages[0] if context.pages else context.new_page()
            try:
                login_if_needed(page, args)
                page.goto(PROFILE_URL, wait_until="domcontentloaded")
                wait_for_profile_content(
                    page,
                    args.resume_title,
                    page_refresh_seconds=args.page_refresh_seconds,
                )
                LOGGER.info("Авторизация подтверждена. Временный профиль проверки удалён.")
            finally:
                close_context_quietly(context)
        return 0
    args.profile_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            str(args.profile_dir), headless=args.headless, viewport=None, args=["--start-maximized"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        capture = NetworkCapture()
        page.on("response", capture.observe)
        login_if_needed(page, args)
        minimum_cooldown = timedelta(hours=args.minimum_cooldown_hours)
        try:
            while True:
                next_at = run_cycle(
                    page,
                    resume_title=args.resume_title,
                    profile_dir=args.profile_dir,
                    dry_run=args.dry_run,
                    capture=capture,
                    minimum_cooldown=minimum_cooldown,
                    page_refresh_seconds=args.page_refresh_seconds,
                )
                if args.once:
                    break
                wait_seconds = (
                    seconds_until(next_at, buffer_seconds=args.buffer_seconds)
                    if next_at
                    else args.poll_seconds
                )
                LOGGER.info(
                    "Следующая проверка через %s; часы сверяются каждые %s.",
                    format_wait_duration(wait_seconds),
                    format_wait_duration(args.poll_seconds),
                )
                wait_for_due_time(
                    next_at, buffer_seconds=args.buffer_seconds, poll_seconds=args.poll_seconds
                )
        except KeyboardInterrupt:
            LOGGER.info("Остановлено пользователем.")
        finally:
            close_context_quietly(context)
    return 0
