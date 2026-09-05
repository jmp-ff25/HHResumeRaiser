from __future__ import annotations

from typing import TYPE_CHECKING

from hh_raiser.activities.resume_review import review_resume
from hh_raiser.activities.search_page_viewer import view_search_page
from hh_raiser.activities.vacancy_viewer import view_vacancies
from hh_raiser.application.vacancy_rotation import VacancyRotation
from hh_raiser.domain.policies import ActivityPolicy
from hh_raiser.domain.result import ActivityResult

if TYPE_CHECKING:
    from playwright.sync_api import Page


def run_permitted_activities(
    page: Page, policy: ActivityPolicy, rotation: VacancyRotation
) -> list[ActivityResult]:
    query, search_page = rotation.next_search()
    search_result, vacancy_urls = view_search_page(
        page, policy, query=query, search_page=search_page
    )
    selected_urls = rotation.select(vacancy_urls, policy.vacancies_per_cycle)
    if not vacancy_urls and search_page:
        rotation.reset_pages()
    results = [search_result]
    results.extend(view_vacancies(page, selected_urls, policy))
    results.append(review_resume(page))
    return results
