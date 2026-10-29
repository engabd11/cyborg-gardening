"""When each plant job is due (pure).

A job runs in the months its seasons cover. Repeating jobs come back
``every_days`` after they were last done; ``once`` jobs come back at the start
of their next season window. A job never done is due today when it is in
season, otherwise at the start of its next window.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .loader import SETTINGS, Library

GRACE_DAYS = 2  # a repeating job turns overdue this many days after its due date
SOON_DAYS = 3


def applies(task: dict[str, Any], stage: str, setting: str) -> bool:
    """Return True when a job fits the plant's stage and setting."""
    stages = task.get("stages")
    settings = task.get("settings")
    return (not stages or stage in stages) and (not settings or setting in settings)


def interval(task: dict[str, Any], setting: str, season: str, factor: float = 1.0) -> int | None:
    """Return the repeat interval in days for a setting and base season, or None to rest."""
    value = task.get("every_days")
    if isinstance(value, dict) and set(value) & set(SETTINGS):
        value = value.get(setting)
    if isinstance(value, dict):
        value = value.get(season)
    if value is None:
        return None
    if task.get("kind") == "water" and setting != "pot":
        value = round(value * factor)  # soil type: rule of thumb, pots use potting mix
    return max(1, int(value))


def _next_month(day: date) -> date:
    return date(day.year + (day.month == 12), day.month % 12 + 1, 1)


def _active(lib: Library, task: dict, setting: str, day: date) -> bool:
    if day.month not in lib.season_months(task.get("seasons")):
        return False
    return task.get("once") or interval(task, setting, lib.season_of(day.month)) is not None


def first_active(lib: Library, task: dict, setting: str, start: date) -> date | None:
    """Return the first day on or after ``start`` when the job is in season."""
    day = start
    for _ in range(13):
        if _active(lib, task, setting, day):
            return day
        day = _next_month(day)
    return None


def window_start(lib: Library, task: dict, setting: str, day: date) -> date:
    """Return the first day of the run of active months holding ``day``."""
    start = date(day.year, day.month, 1)
    for _ in range(12):
        prev = (start - timedelta(days=1)).replace(day=1)
        if not _active(lib, task, setting, prev):
            break
        start = prev
    return start


def due_date(
    lib: Library,
    task: dict[str, Any],
    *,
    today: date,
    stage: str,
    setting: str,
    last_done: date | None = None,
    snoozed_until: date | None = None,
    factor: float = 1.0,
    soil_dry: bool | None = None,
) -> date | None:
    """Return when a job is next due, or None when it does not apply to this plant."""
    if not applies(task, stage, setting):
        return None
    if task.get("kind") == "water" and soil_dry is not None:
        # A linked moisture sensor decides watering, within the job's seasons.
        if not _active(lib, task, setting, today):
            return first_active(lib, task, setting, _next_month(today))
        due = today if soil_dry else None
    elif task.get("once"):
        if _active(lib, task, setting, today):
            start = window_start(lib, task, setting, today)
            if last_done is None or last_done < start:
                due = start
            else:  # done this window: next window after this one ends
                day = _next_month(today)
                while _active(lib, task, setting, day) and day.year <= today.year + 1:
                    day = _next_month(day)
                due = first_active(lib, task, setting, day)
        else:
            due = first_active(lib, task, setting, today)
    elif last_done is None:
        due = first_active(lib, task, setting, today)
    else:
        days = interval(task, setting, lib.season_of(last_done.month), factor)
        due = first_active(lib, task, setting, last_done + timedelta(days=days or 1))
    if due and snoozed_until and snoozed_until > due:
        due = snoozed_until
    return due


def status(due: date | None, today: date, *, once: bool = False) -> str:
    """Return overdue, due, soon, ok or resting."""
    if due is None:
        return "resting"
    days = (due - today).days
    if days < -GRACE_DAYS and not once:
        return "overdue"
    if days <= 0:
        return "due"
    if days <= SOON_DAYS:
        return "soon"
    return "ok"
