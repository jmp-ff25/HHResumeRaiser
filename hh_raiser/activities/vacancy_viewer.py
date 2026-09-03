from __future__ import annotations

from typing import TYPE_CHECKING

from hh_raiser.domain.action import ActivityKind
from hh_raiser.domain.policies import ActivityPolicy
from hh_raiser.domain.result import ActivityResult, ActivityStatus
from hh_raiser.infrastructure.browser.page_state_reader import canonical_vacancy_url
from hh_raiser.infrastructure.hh.selectors import VACANCY_DESCRIPTION, VACANCY_HEADING

if TYPE_CHECKING:
    from playwright.sync_api import Page

from playwright.sync_api import Error as PlaywrightError


def view_vacancies(
    page: Page, vacancy_urls: list[str], policy: ActivityPolicy
) -> list[ActivityResult]:
    results: list[ActivityResult] = []
    for url in vacancy_urls[: policy.vacancies_per_cycle]:
        canonical = canonical_vacancy_url(url)
        if canonical is None:
            continue
        try:
            page.goto(canonical, wait_until="domcontentloaded")
            heading = page.locator(VACANCY_HEADING)
            if not heading.count():
                heading = page.get_by_role("heading", level=1)
            description = page.locator(VACANCY_DESCRIPTION)
            recognized = heading.count() > 0 and heading.first.is_visible()
            description_visible = description.count() > 0 and description.first.is_visible()
            if description_visible:
                page.locator("body").press("PageDown")
                page.wait_for_timeout(round(policy.scroll_pause_seconds * 1_000))
            page.wait_for_timeout(round(policy.vacancy_view_seconds * 1_000))
            results.append(
                ActivityResult(
                    action=ActivityKind.VIEW_VACANCY,
                    status=ActivityStatus.SUCCESS if recognized else ActivityStatus.UNKNOWN,
                    detail=(
                        "Страница вакансии содержательно просмотрена."
                        if recognized
                        else "Страница открыта, но заголовок вакансии не распознан."
                    ),
                    metadata={"description_visible": description_visible},
                )
            )
        except PlaywrightError as error:
            results.append(
                ActivityResult(
                    action=ActivityKind.VIEW_VACANCY,
                    status=ActivityStatus.ERROR,
                    detail=f"Не удалось просмотреть вакансию: {error.__class__.__name__}",
                )
            )
    if not results:
        results.append(
            ActivityResult(
                action=ActivityKind.VIEW_VACANCY,
                status=ActivityStatus.SKIPPED,
                detail="Подходящие ссылки на вакансии не найдены.",
            )
        )
    return results
