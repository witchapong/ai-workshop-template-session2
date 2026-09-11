"""The campus job board: remember jobs, and decide which ones to show."""

import json
from datetime import date
from pathlib import Path


def load_jobs(path) -> list[dict]:
    """Read every job from the JSON file at path.

    Returns an empty list if the file does not exist yet - the first run on a
    fresh copy must not crash.
    """
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_job(path, job: dict) -> None:
    """Add one job to the JSON file at path, creating the file if needed."""
    path = Path(path)
    jobs = load_jobs(path)
    jobs.append(job)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jobs, indent=2, ensure_ascii=False),
                    encoding="utf-8")


def is_active(job: dict, today: date) -> bool:
    """True if this job has not expired.

    today is handed in, never read from the clock. A function that calls
    date.today() itself cannot be tested: any test you write against it stops
    being true tomorrow.

    >= and not >, because a job open "until the 8th" is open ON the 8th.
    """
    return date.fromisoformat(job["expires"]) >= today


def active_jobs(jobs: list[dict], today: date) -> list[dict]:
    """The jobs that have not expired.

    Hides them. Never deletes them - the person who posted a job still wants
    to see it after it closes, which is why this filters a list rather than
    touching the file.
    """
    return [job for job in jobs if is_active(job, today)]


def search(jobs: list[dict], location=None, min_budget=None) -> list[dict]:
    """The jobs matching every filter given.

    An argument left as None means "do not filter on this".
    min_budget is inclusive: a job paying exactly that much is a match.
    """
    found = list(jobs)
    if location is not None:
        found = [job for job in found if job["location"] == location]
    if min_budget is not None:
        found = [job for job in found if job["budget"] >= min_budget]
    return found
