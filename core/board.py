"""The campus job board: remember jobs, and decide which ones to show."""

from datetime import date


def load_jobs(path) -> list[dict]:
    """Read every job from the JSON file at path.

    Returns an empty list if the file does not exist yet - the first run on a
    fresh copy must not crash.
    """
    raise NotImplementedError


def save_job(path, job: dict) -> None:
    """Add one job to the JSON file at path, creating the file if needed."""
    raise NotImplementedError


def is_active(job: dict, today: date) -> bool:
    """True if this job has not expired.

    today is handed in, never read from the clock. A function that calls
    date.today() itself cannot be tested: any test you write against it stops
    being true tomorrow.

    A job expiring ON today is still open.
    """
    raise NotImplementedError


def active_jobs(jobs: list[dict], today: date) -> list[dict]:
    """The jobs that have not expired.

    Hides them. Never deletes them - the person who posted a job still wants
    to see it after it closes.
    """
    raise NotImplementedError


def search(jobs: list[dict], location=None, min_budget=None) -> list[dict]:
    """The jobs matching every filter given.

    An argument left as None means "do not filter on this".
    min_budget is inclusive: a job paying exactly that much is a match.
    """
    raise NotImplementedError
