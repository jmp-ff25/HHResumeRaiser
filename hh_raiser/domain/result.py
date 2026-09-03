from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from hh_raiser.models import MOSCOW

JsonScalar = str | int | float | bool | None


class ActivityStatus(StrEnum):
    SUCCESS = "success"
    SKIPPED = "skipped"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ActivityResult:
    action: str
    status: ActivityStatus
    detail: str
    metadata: dict[str, JsonScalar] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(MOSCOW))
