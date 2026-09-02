from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

MOSCOW = timezone(timedelta(hours=3), "MSK")
PROFILE_URL = "https://hh.ru/applicant/profile/me"
RAISE_BUTTON_SELECTOR = '[data-qa~="resume-update-button"]'
RUSSIAN_MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


@dataclass(frozen=True)
class PageState:
    kind: str
    next_at: datetime | None = None


@dataclass(frozen=True)
class LoginEvidence:
    landing_button: bool = False
    phone_input: bool = False
    password_input: bool = False


@dataclass(frozen=True)
class Credentials:
    phone: str
    password: str
