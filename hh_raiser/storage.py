from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from hh_raiser.models import MOSCOW


def _guard_path(profile_dir: Path) -> Path:
    return profile_dir / "resume-raise-last-attempt.json"


def _status_path(profile_dir: Path) -> Path:
    return profile_dir.parent / "status.json"


def _resume_refresh_attempt_path(profile_dir: Path) -> Path:
    return profile_dir / "resume-refresh-last-attempt.json"


def write_next_raise_time(profile_dir: Path, next_at: datetime) -> None:
    profile_dir.parent.mkdir(parents=True, exist_ok=True)
    path = _status_path(profile_dir)
    temporary_path = path.with_suffix(".tmp")
    temporary_path.write_text(
        json.dumps(
            {"next_raise_at": next_at.isoformat(), "updated_at": datetime.now(MOSCOW).isoformat()},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def read_next_raise_time(profile_dir: Path) -> datetime | None:
    try:
        payload = json.loads(_status_path(profile_dir).read_text(encoding="utf-8"))
        return datetime.fromisoformat(payload["next_raise_at"])
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None


def write_attempt_guard(profile_dir: Path, attempted_at: datetime) -> None:
    profile_dir.mkdir(parents=True, exist_ok=True)
    _guard_path(profile_dir).write_text(
        json.dumps({"attempted_at": attempted_at.isoformat()}, ensure_ascii=False),
        encoding="utf-8",
    )


def guarded_until(profile_dir: Path, minimum_cooldown: timedelta) -> datetime | None:
    path = _guard_path(profile_dir)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        last_attempt = datetime.fromisoformat(payload["attempted_at"])
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None
    guarded = last_attempt + minimum_cooldown
    return guarded if guarded > datetime.now(MOSCOW) else None


def write_resume_refresh_attempt(profile_dir: Path, attempted_at: datetime) -> None:
    profile_dir.mkdir(parents=True, exist_ok=True)
    _resume_refresh_attempt_path(profile_dir).write_text(
        json.dumps({"attempted_at": attempted_at.isoformat()}, ensure_ascii=False),
        encoding="utf-8",
    )


def resume_refresh_due_at(profile_dir: Path, interval: timedelta) -> datetime:
    try:
        payload = json.loads(_resume_refresh_attempt_path(profile_dir).read_text(encoding="utf-8"))
        last_attempt = datetime.fromisoformat(payload["attempted_at"])
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return datetime.now(MOSCOW)
    return max(last_attempt + interval, datetime.now(MOSCOW))
