from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchState:
    card_count: int
    collected_vacancies: int
    scrolls_completed: int


@dataclass(frozen=True)
class ResumeReviewState:
    has_experience: bool
    has_education: bool
    has_languages: bool
    has_platform_recommendation: bool
