"""Acceptance tests for the campus job board.

These are the specification for Lab 2. They ship failing; making them pass is
the lab. Every test hands `today` in rather than letting the code look at the
clock, which is the single most important habit in this file.
"""

from datetime import date

from core.board import active_jobs, is_active, load_jobs, save_job, search

TODAY = date(2026, 9, 8)


def a_job(**overrides):
    """A complete job, with whichever fields this test cares about changed."""
    job = {
        "title": "Design a poster for our club night",
        "location": "Ratchathewi",
        "budget": 500,
        "expires": "2026-09-20",
        "contact": "line: @annb",
    }
    job.update(overrides)
    return job


def test_load_returns_empty_when_no_file(tmp_path):
    # A string path into a directory that does not exist yet - both pages
    # call save_job/load_jobs with the string literal "data/jobs.json", and
    # data/ is not present on a fresh clone. A bare tmp_path (a Path, into a
    # directory pytest already created) is too forgiving: it passes an
    # implementation with neither Path() coercion nor mkdir. Do not "tidy"
    # this back to tmp_path / "jobs.json" - that is the bug this test exists
    # to catch.
    path = str(tmp_path / "data" / "jobs.json")
    assert load_jobs(path) == []


def test_save_then_load_round_trips(tmp_path):
    # String path into a directory that doesn't exist yet - see the comment
    # on test_load_returns_empty_when_no_file.
    path = str(tmp_path / "data" / "jobs.json")
    save_job(path, a_job(title="Tutor first-year calculus", budget=300))
    loaded = load_jobs(path)
    assert len(loaded) == 1
    assert loaded[0]["title"] == "Tutor first-year calculus"
    assert loaded[0]["budget"] == 300


def test_job_expiring_next_week_is_active():
    assert is_active(a_job(expires="2026-09-15"), TODAY)


def test_job_expiring_today_is_still_active():
    # The boundary. A job open "until the 8th" is open ON the 8th.
    # Writing > instead of >= closes every job a day early, and nobody
    # notices for a week.
    assert is_active(a_job(expires="2026-09-08"), TODAY)


def test_job_that_expired_yesterday_is_not_active():
    assert not is_active(a_job(expires="2026-09-07"), TODAY)


def test_active_jobs_hides_expired_without_deleting_them(tmp_path):
    # String path into a directory that doesn't exist yet - see the comment
    # on test_load_returns_empty_when_no_file.
    path = str(tmp_path / "data" / "jobs.json")
    # Expiring exactly today, so it is still open. active_jobs has its own
    # boundary and nothing forces it to call is_active - an independent > here
    # would slip past every other test in this file.
    save_job(path, a_job(title="still open", expires="2026-09-08"))
    save_job(path, a_job(title="closed", expires="2026-08-01"))

    jobs = load_jobs(path)
    assert [job["title"] for job in active_jobs(jobs, TODAY)] == ["still open"]
    # Hidden, not deleted: both are still on disk.
    assert len(load_jobs(path)) == 2


def test_search_by_location_returns_only_that_location():
    jobs = [a_job(location="Ratchathewi"), a_job(location="Bang Sue")]
    assert [job["location"] for job in search(jobs, location="Bang Sue")] == ["Bang Sue"]


def test_search_min_budget_includes_a_job_at_exactly_that_budget():
    # 500 asked for, 500 offered: a match. This is the best-paying job that
    # a > instead of a >= silently drops.
    jobs = [a_job(budget=500), a_job(budget=300)]
    assert [job["budget"] for job in search(jobs, min_budget=500)] == [500]


def test_search_with_no_filters_returns_everything():
    # The browse page opens with no filters set, so this is the first thing
    # anyone sees. An implementation that starts from an empty list and only
    # adds rows when a filter is given passes every other test in this file
    # and shows a blank board.
    jobs = [a_job(location="Ratchathewi"), a_job(location="Bang Sue")]
    assert len(search(jobs)) == 2


def test_search_applies_both_filters_together():
    # Both filters at once, which no other test does. An implementation that
    # combines them with "or" instead of "and" passes every single-filter test
    # and then offers people jobs they cannot take.
    jobs = [
        a_job(location="Bang Sue", budget=800),      # matches both
        a_job(location="Bang Sue", budget=200),      # right place, too cheap
        a_job(location="Ratchathewi", budget=900),   # pays enough, wrong place
    ]
    found = search(jobs, location="Bang Sue", min_budget=500)
    assert [job["budget"] for job in found] == [800]
