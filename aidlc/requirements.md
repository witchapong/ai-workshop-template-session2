# Gate 2 — Requirements

Your agent drafts this. You correct it and approve it.

A requirement is only finished when its acceptance criterion **could fail**.
"The app should be user friendly" could never fail. "Booking a taken slot shows
the message 'already booked'" could.

There are exactly two kinds of criterion, and a good spec has both:

| Kind | Write it like this | Use it for |
|---|---|---|
| A test | `pytest test_a_50_hz_sine_peaks_at_50_hz` | anything the test suite already checks |
| A person | `EYES: with 50 Hz at 1.0, the tallest spike sits at 50 on the x-axis and reaches 1.0 on the y-axis` | anything on the screen |

**No test in this repository opens a page.** So every requirement about what
the app *looks like* is an EYES criterion, and if you have none, your spec
cannot see the half of the app your user actually uses.

An EYES criterion names what to open, what to set, and what number to read. If
it says "the chart looks right", it could never fail, so it is not a criterion.

**The strongest ones change something.** "Open it and look" passes for a chart
that is quietly wrong. "Set tone 1 to amplitude 0.3, and the 50 Hz spike reads
0.3" cannot. Write at least one row that moves a value and predicts the number
that must move with it.

**Keep each criterion in its own half.** A `pytest` row may only back a claim
about `core/`. Backing *"the page shows the strongest frequency"* with a test
that calls `peak_frequency()` is the trap — that test passes perfectly while
the page is blank.

| # | Requirement | Acceptance criterion (how we check it) |
|---|---|---|
| 1 | A job I post is still there the next time the app starts | `pytest test_save_then_load_round_trips` |
| 2 | A board nobody has posted to yet doesn't crash — it's just empty | `pytest test_load_returns_empty_when_no_file` |
| 3 | A job that hasn't reached its open-until date yet is still active | `pytest test_job_expiring_next_week_is_active` |
| 4 | A job open "until the 8th" is still open ON the 8th, not the day before | `pytest test_job_expiring_today_is_still_active` |
| 5 | A job stops being active the day after its open-until date | `pytest test_job_that_expired_yesterday_is_not_active` |
| 6 | `active_jobs` leaves out a job whose open-until date has passed, without removing it from the file | `pytest test_active_jobs_hides_expired_without_deleting_them` |
| 7 | On Browse Jobs, a job disappears once its open-until date is behind the "Board as of" date, and the count drops with it | `EYES: open Browse Jobs with no filters set and note the count — then find the card with the earliest open-until date (with the seed data as shipped, that's "Photograph a graduation shoot," open until 2026-11-30) and set "Board as of" to the day after that date. That job's card is gone and the count is exactly one lower` |
| 8 | Filtering by location only returns jobs in that location | `pytest test_search_by_location_returns_only_that_location` |
| 9 | A job paying exactly the minimum budget typed in still counts as a match | `pytest test_search_min_budget_includes_a_job_at_exactly_that_budget` |
| 10 | With no filters set, browsing returns every job handed to it, not zero | `pytest test_search_with_no_filters_returns_everything` |
| 11 | Both filters applied together only match a job that satisfies both at once, not either one alone | `pytest test_search_applies_both_filters_together` |
| 12 | Filling in the Post a Job form and submitting puts that exact job on the board | `EYES: open Post a Job, fill in a title, a location, a budget, an open-until date and a contact, click "Post it" — open Browse Jobs and the job is listed with the same title, location, budget and date you typed` |
| 13 | Posting a job tells you how many jobs are now on the board | `EYES: on Post a Job, submit a job and read the success message underneath the form — it names the current total number of jobs, one more than the board held before you posted` |
| 14 | The heading on Browse Jobs never disagrees with the cards underneath it | `EYES: open Browse Jobs with no filters set — the number in "N jobs available" equals the number of cards you count below it; change the location or budget filter and count again, still equal` |

**Approved by:** (your name)
**Date:**
