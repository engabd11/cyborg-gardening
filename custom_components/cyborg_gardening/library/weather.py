"""Frost, heat and rain outlook from Home Assistant forecast lists (pure).

Forecast items are the dicts ``weather.get_forecasts`` returns: ``datetime``
(ISO text), ``temperature``, and optionally ``templow``, ``precipitation``
and ``precipitation_probability``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Any

MORNING = time(9, 0)  # a frost night runs until 9 am the next morning


@dataclass
class Outlook:
    """What the next day looks like, for the garden."""

    tonight_min: float | None = None
    tomorrow_max: float | None = None
    today_max: float | None = None
    rain_mm: float | None = None  # expected over the next 24 hours
    rain_chance: float | None = None

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON friendly dict."""
        return dict(self.__dict__)


def _when(item: dict[str, Any], tz) -> datetime | None:
    try:
        value = datetime.fromisoformat(str(item["datetime"]))
    except (KeyError, ValueError):
        return None
    return value.astimezone(tz) if value.tzinfo else value.replace(tzinfo=tz)


def _num(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def outlook(hourly: list[dict] | None, daily: list[dict] | None, now: datetime) -> Outlook:
    """Summarise tonight's low, today's and tomorrow's highs and rain."""
    tz = now.tzinfo
    out = Outlook()
    night_end = datetime.combine(now.date(), MORNING, tz)
    if now >= night_end:
        night_end += timedelta(days=1)
    tomorrow = now.date() + timedelta(days=1)
    if hourly:
        rows = [(w, item) for item in hourly if (w := _when(item, tz)) is not None]
        lows = [_num(i.get("temperature")) for w, i in rows if now <= w <= night_end]
        highs_today = [_num(i.get("temperature")) for w, i in rows if w.date() == now.date()]
        highs_tomorrow = [_num(i.get("temperature")) for w, i in rows if w.date() == tomorrow]
        rain = [
            (_num(i.get("precipitation")), _num(i.get("precipitation_probability")))
            for w, i in rows
            if now <= w < now + timedelta(hours=24)
        ]
        out.tonight_min = min((v for v in lows if v is not None), default=None)
        out.today_max = max((v for v in highs_today if v is not None), default=None)
        out.tomorrow_max = max((v for v in highs_tomorrow if v is not None), default=None)
        if any(mm is not None for mm, _ in rain):
            out.rain_mm = round(sum(mm or 0 for mm, _ in rain), 1)
        if any(p is not None for _, p in rain):
            out.rain_chance = max(p or 0 for _, p in rain)
    if daily:
        by_date = {w.date(): i for i in daily if (w := _when(i, tz)) is not None}
        night_day = night_end.date()
        if out.tonight_min is None and night_day in by_date:
            out.tonight_min = _num(by_date[night_day].get("templow"))
        if out.today_max is None and now.date() in by_date:
            out.today_max = _num(by_date[now.date()].get("temperature"))
        if out.tomorrow_max is None and tomorrow in by_date:
            out.tomorrow_max = _num(by_date[tomorrow].get("temperature"))
        if out.rain_mm is None and now.date() in by_date:
            out.rain_mm = _num(by_date[now.date()].get("precipitation"))
            out.rain_chance = _num(by_date[now.date()].get("precipitation_probability"))
    return out


def frost_expected(out: Outlook, threshold: float) -> bool:
    """Return True when tonight's low is at or below the frost threshold."""
    return out.tonight_min is not None and out.tonight_min <= threshold


def heat_expected(out: Outlook, threshold: float) -> bool:
    """Return True when today or tomorrow reaches the heat threshold."""
    return any(t is not None and t >= threshold for t in (out.today_max, out.tomorrow_max))


def rain_expected(out: Outlook, mm: float, chance: float = 60) -> bool:
    """Return True when enough rain is likely in the next day to skip watering."""
    if out.rain_mm is None or out.rain_mm < mm:
        return False
    return out.rain_chance is None or out.rain_chance >= chance
