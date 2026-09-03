from __future__ import annotations

import re
from urllib.parse import urljoin, urlsplit, urlunsplit

from hh_raiser.infrastructure.hh.selectors import SEARCH_URL


def redact_url(url: str) -> str:
    """Remove query/fragment data and opaque numeric path identifiers."""
    parts = urlsplit(url)
    safe_path = re.sub(r"/\d{6,}(?=/|$)", "/<id>", parts.path)
    return urlunsplit((parts.scheme, parts.netloc, safe_path, "", ""))


def is_public_vacancy_url(url: str) -> bool:
    parts = urlsplit(url)
    return (
        parts.scheme == "https"
        and parts.netloc == "hh.ru"
        and bool(re.fullmatch(r"/vacancy/\d+", parts.path))
    )


def canonical_vacancy_url(url: str) -> str | None:
    absolute = urljoin(SEARCH_URL, url)
    if not is_public_vacancy_url(absolute):
        return None
    parts = urlsplit(absolute)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
