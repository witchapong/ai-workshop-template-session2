# Gate 3 — Task list

Your agent drafts this. You correct it and approve it.

**The one rule that matters:** every task touches exactly ONE file that no
other task touches. You are working alone, so this is not about collisions —
it is about being able to finish something, run it, and know it works before
you start the next thing.

**The second rule:** every task has a **Done when** copied from
`aidlc/requirements.md` — and it must be one that could fail. A task owning a
file under `pages/` gets an EYES criterion, because no test opens a page. A
task with no Done when is a task that can never be wrong, and it will be.

| # | Task | The ONE file it touches | Done when |
|---|---|---|---|
| 1 | Get the rules right: load and save jobs, and work out which ones are active and which match a search | `core/board.py` | `pytest tests/test_board.py -q` — 10 passed |
| 2 | Build the form for posting a job | `pages/1_Post_a_Job.py` | `EYES: on Post a Job, submit a job and read the success message underneath the form — it names the current total number of jobs, one more than the board held before you posted` |
| 3 | Build the board people actually browse | `pages/2_Browse_Jobs.py` | `EYES: open Browse Jobs with no filters set — the number in "N jobs available" equals the number of cards you count below it; change the location or budget filter and count again, still equal` |

One row per task, and no more. **Lab 1 has exactly two.** Lab 2 has three.
Delete any row you do not use — a row naming a file nobody owns is worse than
no row at all.

**Approved by:**
**Date:**
