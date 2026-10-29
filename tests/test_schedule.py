from datetime import date

from cyborg_gardening.library import schedule


def task(lib, task_id):
    return next(t for t in lib.plants["lemon"]["tasks"] if t["id"] == task_id)


def due(lib, task_id, today, **kw):
    kw.setdefault("stage", "established")
    kw.setdefault("setting", "pot")
    return schedule.due_date(lib, task(lib, task_id), today=today, **kw)


def test_never_done_in_season_is_due_today(lib):
    assert due(lib, "feed", date(2026, 10, 29)) == date(2026, 10, 29)


def test_never_done_out_of_season_waits_for_window(lib):
    # feed runs spring, summer and early autumn: in June it waits for 1 September
    assert due(lib, "feed", date(2026, 6, 10)) == date(2026, 9, 1)


def test_repeat_interval_from_last_done(lib):
    assert due(lib, "feed", date(2026, 10, 29), last_done=date(2026, 10, 1)) == date(2026, 12, 30)


def test_interval_landing_out_of_season_moves_to_next_window(lib):
    # done 1 March, +90 days is 30 May (late autumn, out of season) so next is 1 September
    assert due(lib, "feed", date(2026, 3, 2), last_done=date(2026, 3, 1)) == date(2026, 9, 1)


def test_interval_by_setting_and_season(lib):
    assert due(lib, "water", date(2026, 1, 10), last_done=date(2026, 1, 10)) == date(2026, 1, 12)
    ground = due(lib, "water", date(2026, 1, 10), last_done=date(2026, 1, 10), setting="ground")
    assert ground == date(2026, 1, 17)


def test_season_without_interval_rests(lib):
    # ground watering only has a summer interval: done in late February, next is 1 December
    got = due(lib, "water", date(2026, 2, 27), last_done=date(2026, 2, 27), setting="ground")
    assert got == date(2026, 12, 1)


def test_soil_factor_applies_to_ground_watering_only(lib):
    kw = {"last_done": date(2026, 1, 1), "factor": 1.3}
    assert due(lib, "water", date(2026, 1, 1), setting="ground", **kw) == date(2026, 1, 10)
    assert due(lib, "water", date(2026, 1, 1), setting="pot", **kw) == date(2026, 1, 3)


def test_stage_filter(lib):
    assert due(lib, "feed", date(2026, 10, 29), stage="young") is None


def test_once_job_due_from_window_start_then_next_year(lib):
    assert due(lib, "prune", date(2026, 8, 20)) == date(2026, 8, 1)
    assert due(lib, "prune", date(2026, 8, 20), last_done=date(2026, 8, 15)) == date(2027, 8, 1)
    assert due(lib, "prune", date(2026, 10, 1)) == date(2027, 8, 1)


def test_snooze_pushes_due_date(lib):
    got = due(lib, "feed", date(2026, 10, 29), snoozed_until=date(2026, 11, 2))
    assert got == date(2026, 11, 2)


def test_moisture_sensor_decides_watering(lib):
    assert due(lib, "water", date(2026, 1, 5), soil_dry=True) == date(2026, 1, 5)
    assert due(lib, "water", date(2026, 1, 5), soil_dry=False) is None


def test_year_wrap_window(lib):
    # summer spans December to February
    w = task(lib, "water")
    assert schedule.window_start(lib, w, "ground", date(2027, 2, 10)) == date(2026, 12, 1)


def test_status():
    today = date(2026, 10, 29)
    assert schedule.status(None, today) == "resting"
    assert schedule.status(date(2026, 10, 20), today) == "overdue"
    assert schedule.status(date(2026, 10, 20), today, once=True) == "due"
    assert schedule.status(today, today) == "due"
    assert schedule.status(date(2026, 10, 31), today) == "soon"
    assert schedule.status(date(2026, 11, 20), today) == "ok"


def test_once_job_without_seasons_runs_once_per_plant(lib):
    job = {"id": "stake", "kind": "other", "title": "Stake", "once": True, "sources": []}
    kw = {"today": date(2026, 10, 30), "stage": "young", "setting": "pot"}
    assert schedule.due_date(lib, job, **kw) == date(2026, 10, 30)
    assert schedule.due_date(lib, job, last_done=date(2026, 10, 1), **kw) is None
