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
| 1 | | `core/....py` | `pytest test_...` |
| 2 | | `pages/N_....py` | `EYES: ...` |

One row per task, and no more. **Lab 1 has exactly two.** Lab 2 has three.
Delete any row you do not use — a row naming a file nobody owns is worse than
no row at all.

**Approved by:**
**Date:**
