from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityPolicy:
    vacancies_per_cycle: int = 2
    search_scrolls: int = 3
    scroll_pause_seconds: float = 1.5
    vacancy_view_seconds: float = 12.0

    def __post_init__(self) -> None:
        if not 0 <= self.vacancies_per_cycle <= 10:
            raise ValueError("vacancies_per_cycle must be between 0 and 10")
        if not 0 <= self.search_scrolls <= 20:
            raise ValueError("search_scrolls must be between 0 and 20")
        if not 0 <= self.scroll_pause_seconds <= 60:
            raise ValueError("scroll_pause_seconds must be between 0 and 60")
        if not 0 <= self.vacancy_view_seconds <= 300:
            raise ValueError("vacancy_view_seconds must be between 0 and 300")
