from __future__ import annotations

import unittest

from hh_raiser.infrastructure.browser.playwright_browser import maximize_browser_window


class PlaywrightBrowserTests(unittest.TestCase):
    def test_headless_mode_does_not_request_window_changes(self) -> None:
        class Context:
            def new_cdp_session(self, page: object) -> object:
                raise AssertionError("CDP must not be used in headless mode")

        self.assertFalse(maximize_browser_window(Context(), object(), headless=True))

    def test_headed_window_is_maximized_through_cdp(self) -> None:
        calls: list[tuple[str, object | None]] = []

        class Session:
            def send(self, method: str, payload: object | None = None) -> dict[str, int]:
                calls.append((method, payload))
                return {"windowId": 42}

            def detach(self) -> None:
                calls.append(("detach", None))

        class Context:
            def new_cdp_session(self, page: object) -> Session:
                return Session()

        class Page:
            def bring_to_front(self) -> None:
                calls.append(("bring_to_front", None))

        self.assertTrue(maximize_browser_window(Context(), Page(), headless=False))
        self.assertIn(
            (
                "Browser.setWindowBounds",
                {"windowId": 42, "bounds": {"windowState": "maximized"}},
            ),
            calls,
        )
