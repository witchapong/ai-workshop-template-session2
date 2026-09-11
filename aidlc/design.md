# Gate 3 — Design

Your agent drafts this. You correct it and approve it.

## What does it compute, or store?

Some apps work out an answer from what you type. Some keep rows and hand them
back later. Plenty do both — a job board keeps the jobs, and works out which
of them are still open. Fill in whichever tables describe yours.

**If it computes** — name each function, what goes in, and what comes out:

| Function | Takes | Returns |
|---|---|---|
| `load_jobs(path)` | the file path to `data/jobs.json` | every job in that file, as a list of dicts — `[]` if the file doesn't exist yet |
| `save_job(path, job)` | the file path, and one job (a dict with title, location, budget, expires, contact) | nothing — it appends the job to the file |
| `is_active(job, today)` | one job, and `today` as a `date` (never read from the clock) | `True` if `job["expires"]` is today or later, `False` if it's already passed |
| `active_jobs(jobs, today)` | a list of jobs, and `today` as a `date` | just the ones that are still active — the rest stay on disk, they're just not in this list |
| `search(jobs, location=None, min_budget=None)` | a list of jobs, plus an optional location and an optional minimum budget | the jobs matching every filter that was actually given — leaving an argument as `None` means don't filter on it |

**If it stores** — one row per job:

| Column | Meaning | Example |
|---|---|---|
| title | what the job is | "Design a poster for our club night" |
| location | where the job is, one of five campus areas | "Ratchathewi" |
| budget | what it pays, in baht | 500 |
| expires | the last day the post is open, as an ISO date string | "2026-09-20" |
| contact | how to reach the person who posted it | "line: @annb" |

## What are the screens?

One row per page. Lab 1 has one page; Lab 2 has two.

| Page file | What the user does here | What they see |
|---|---|---|
| `pages/1_Post_a_Job.py` | Types a title, picks a location, sets a budget and an "open until" date, and gives a way to be contacted, then submits | A success message once it's posted, naming how many jobs are now on the board — or an error if the title or contact is left blank |
| `pages/2_Browse_Jobs.py` | Picks a location (or "Anywhere"), a minimum budget, and a date to view the board "as of" | A count — "N jobs available" — and one card per matching job showing its title, location, budget, open-until date and contact, or a message that nothing matches |

## How does it move?

Three sentences: what the user types, what is computed or saved, and what
appears on the screen as a result.

On Post a Job, the user types a title, picks a location and a date, sets a
budget, and gives their contact info; submitting calls `save_job` and the job
is appended straight to `data/jobs.json`. On Browse Jobs nothing is saved —
`load_jobs` reads every job off disk, `active_jobs` drops anything past the
"as of" date, and `search` applies whichever filters are set, all worked out
once into a single variable. That same variable then feeds both the "N jobs
available" count and the list of cards underneath it, which is the only way
they're guaranteed to agree.

**Approved by:** (your name — this gate is not finished while this is blank)
**Date:**
