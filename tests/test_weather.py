from datetime import datetime, timedelta, timezone

from cyborg_gardening.library import weather

TZ = timezone(timedelta(hours=10))
NOW = datetime(2026, 7, 10, 14, 0, tzinfo=TZ)


def hourly(temps, start=NOW, rain=0.0, chance=0):
    return [
        {
            "datetime": (start + timedelta(hours=i)).isoformat(),
            "temperature": t,
            "precipitation": rain,
            "precipitation_probability": chance,
        }
        for i, t in enumerate(temps)
    ]


def test_tonight_min_runs_until_nine_am():
    temps = [12, 10, 8, 6, 4, 3, 2, 1.5, 1, 1, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 3, -5]
    out = weather.outlook(hourly(temps), None, NOW)
    # entries run 14:00 today to 11:00 tomorrow; the -5 at 11:00 is after 9 am
    assert out.tonight_min == 0.5
    assert weather.frost_expected(out, 2)
    assert not weather.frost_expected(out, 0)


def test_daily_fallback_uses_next_mornings_low():
    daily = [
        {"datetime": "2026-07-10T00:00:00+10:00", "temperature": 13, "templow": 5},
        {"datetime": "2026-07-11T00:00:00+10:00", "temperature": 12, "templow": 1},
    ]
    out = weather.outlook(None, daily, NOW)
    assert out.tonight_min == 1
    assert out.today_max == 13
    assert out.tomorrow_max == 12


def test_heat_and_rain():
    out = weather.outlook(hourly([30, 36, 37], rain=2, chance=80), None, NOW)
    assert weather.heat_expected(out, 35)
    assert out.rain_mm == 6
    assert weather.rain_expected(out, 5)
    assert not weather.rain_expected(out, 10)


def test_unlikely_rain_is_ignored():
    out = weather.outlook(hourly([20, 20, 20], rain=3, chance=20), None, NOW)
    assert not weather.rain_expected(out, 5)


def test_bad_rows_are_skipped():
    out = weather.outlook([{"temperature": 1}, {"datetime": "nope"}], None, NOW)
    assert out.tonight_min is None
