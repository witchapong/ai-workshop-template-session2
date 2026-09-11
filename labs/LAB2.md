# Lab 2 — Build a campus job board

Today you build one application from four short checkpoints — the same
**gates** from Lab 1's Round 2, where a person has to read and approve what
the agent drafted before it is allowed to write the next thing. There is no
Round 1 this week: you already felt what "no gates" is like last time, so
the gates are on from the start.

The deck carries the steps and the prompts in the room. This document is
what stands behind it: the reasoning for each check, what a wrong answer
looks like, and what to do when one of the four ways this particular app
quietly breaks happens to you. If you missed the session, everything you
need to finish is here.

Ten minutes to set up, forty for the first three gates, fifty-five to build,
ten to ship — about two hours end to end, and it leaves nothing spare. If you
are stuck on anything for more than ten minutes, ask a neighbour before the
instructor; there is one instructor and dozens of you.

---

## What you are building

A **campus job board** is two pages sharing one set of rules underneath.

In three sentences: someone posts a small job — what needs doing, where,
what it pays, how long the offer is open, and how to reach them — and anyone
else can search the board by location and minimum pay. A post stays on the
board until its own "open until" date passes, at which point it stops
appearing in *anyone else's* search, except the person who posted it, who can
still see it — closed does not mean thrown away. Every post is written to a
small file on disk, so it survives you closing the app and reopening it —
which is new: Lab 1 computed an answer and forgot it the moment you closed
the tab; this week's app remembers.

**A screenshot in words**, for the page you spend most of Gate 4 on. Open
**Browse Jobs** and this is what is there: a dropdown labelled "Where?"
(five campus areas, or "Anywhere"), a number box labelled "Paying at least
(baht)", and a date picker labelled "Board as of" — set to today, but you
can move it to see the board as it will look on any date. Under those three
controls sits one line of text, "*N* jobs available," and below that, one
card per job: its title in bold, then "*location* · *budget* baht · open
until *date*," then how to reach the poster. If nothing matches, the cards
vanish and one sentence takes their place: "Nothing matches. Widen the
search, or move the date back."

Hold onto one fact from that paragraph: **the number in the heading and the
number of cards underneath it are the same number, always.** Most of what
Gate 4 is actually testing is whether that stays true.

---

## What is different today

Three things changed since last week, and one thing changed since a plan for
this lab you may have heard about before today.

- **Your own machine, not a browser tab.** Session 1 ran inside a temporary
  computer GitHub lent you for free, reached through the browser. That is
  gone for good. Everything today happens locally, in VS Code on the PC in
  front of you, typing into **PowerShell**, Windows' own command line.
  `copy` replaces `cp`, `py -3.14` replaces `python3`, and paths use
  backslashes.
- **Working alone.** There is no team, no five briefs to choose between, and
  no pull request — a request to merge one person's branch into everyone
  else's shared copy, which only existed because several people shared a
  repository. You are the only person who will ever touch this one. The
  one-task-one-file rule in `aidlc/tasks.md` survives anyway, for a
  different reason: not to stop two people colliding, but to stop *you*
  starting task two before task one actually works.
- **One app, not a choice of five.** Everyone in the room is building the
  same Campus Job Board today, from the same ten tests. An app that is
  really yours — your own idea, your own scope — is Session 3, not this one.
- **No Round 1.** Last week you spent 25 minutes with an agent that had no
  rules at all, specifically so you could feel what "no gates" is like.
  You already know, so this week skips straight to Gate 1. The very first
  time you open Cline today — at Gate 2, since Gate 1 is yours alone to
  write — `.clinerules.gates` is already active, and your agent already
  refuses to write code before you approve a spec. Nothing switches it on
  partway through, the way it did in Lab 1.

---

## Set up (10 minutes)

Today's repository is not last week's. Your Session 1 app is untouched and
still deployed; this is a second, separate repository, seeded with last
week's *finished* spectrum analyser plus this week's job board, which fails
every test until you build it.

1. **Use this template** to make your own repository for this session. Click
   the green **Use this template** button on `ai-workshop-template-session2`,
   then **Create a new repository**, set to **Public**.
2. **Clone it and open it.** In VS Code's terminal:
   ```
   git clone <the URL of your new repository>
   ```
   then **File → Open Folder** on the folder it created.
3. **Create a virtual environment** — a private copy of Python and its
   packages just for this project, so it cannot clash with anything else on
   the machine:
   ```
   py -3.14 -m venv .venv
   ```
   `py` is the Python launcher Windows installs; `-3.14` pins exactly which
   version to use, even if others are on the machine.
4. **Install the approved packages**, using the Python *inside* that new
   environment rather than activating it — activating can be blocked by this
   machine's security policy, and this form always works regardless:
   ```
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
5. **Copy in your key.**
   ```
   copy .env.example .env
   ```
   Open `.env`, replace the placeholder text after `ZAI_API_KEY=` with the
   key on the projector, save, and **close the tab** — it is a password
   sitting on your screen.
6. **Seed the board**, so Browse Jobs is not empty on your very first run:
   ```
   New-Item -ItemType Directory -Force -Path data
   copy session2\jobs_seed.json data\jobs.json
   ```
   `data\` does not exist in a fresh clone — it is also where your own posts
   will land later. `-Force` means the first command does not complain if you
   ever run it a second time and the folder is already there.
7. **Point Cline at the model.** This is a separate step from `.env`, and
   skipping it is the most common way to arrive unable to work: `.env` is
   read by the *app*; Cline is a different program, with its own settings,
   that never looks at `.env`.
   - Click the **Cline icon** — the robot in the strip of icons down the far
     left.
   - **Bring my own API key** (not "Absolutely Free" — that signs you into
     Cline's own service and ignores the key you were just given).
   - API Provider **OpenAI Compatible** — **not "Z AI."** Cline's built-in Z
     AI provider has a fixed model dropdown that stops at `glm-5.2`; it does
     not offer `glm-5.3-flash`, even though the API genuinely serves it.
     OpenAI Compatible gives you a free-text Model ID field instead of a
     dropdown, and that is the only way to reach the model this course uses.
   - Base URL **`https://api.z.ai/api/coding/paas/v4`** — typing this
     exactly matters. The similar-looking `/api/paas/v4` (no `coding`) is a
     different billing plan on the same key, and it rejects every request
     with an error that reads like a billing problem when it is really the
     wrong address.
   - Model ID **`glm-5.3-flash`**, typed into the free-text field — do not go
     looking for it in a dropdown, this provider does not have one.
   - Paste the same key from the projector as the API Key.
   - Type **hello** and check you get a reply.
   > If Cline reports `429`, that is the whole room's requests landing on the
   > model at once, not a problem with your key. Wait about ten seconds and
   > send it again.
8. **Check your setup.**
   ```
   .venv\Scripts\python.exe check_setup.py
   ```
   Fix anything marked `FAIL` — the message tells you exactly what to do —
   and run it again until it prints `ALL CHECKS PASSED`. This uses the
   Python *inside* `.venv` for the same reason step 4 did: the environment is
   never activated, so a bare `python` can silently run the wrong one.
9. **See where you start.**
   ```
   .venv\Scripts\python.exe -m pytest
   ```
   The last line is your specification failing, on purpose. The next
   section says exactly what it should say, and why.

**Stuck on the venv, `pip`, or PowerShell itself?** `TROUBLESHOOTING.md`'s
"Setup is failing and you can't tell why" hands the rest of this section to
Cline — but only once step 7 above is already working.

---

## The state you start in

Before you touch anything, here is exactly what exists in your new
repository and what does not.

| File | State |
|---|---|
| `core/board.py` | a **stub** — code that exists only so the app imports without crashing; all five functions currently just `raise NotImplementedError` |
| `tests/test_board.py` | ships complete, ten checks — this is your specification, not something you write |
| `pages/1_Post_a_Job.py` | does not exist yet — you create it at Gate 4, task 2 |
| `pages/2_Browse_Jobs.py` | does not exist yet — you create it at Gate 4, task 3 |
| `core/spectrum.py`, `pages/2_Spectrum_Analyzer.py` | already finished — last week's app, carried over so it keeps working while you build this week's |
| `data/jobs.json` | eight seeded jobs, from the setup step above — **five of them still open**, three already past their date. A correct Browse page shows five, not eight: the other three are hidden, not deleted. If you see five, nothing is wrong |
| `aidlc/intent.md`, `requirements.md`, `design.md`, `tasks.md` | the same four gate documents as Lab 1, as blank **placeholder** templates — text marked `PLACEHOLDER` that your agent refuses to build past |

Run `.venv\Scripts\python.exe -m pytest` and you get, on Python 3.14:

```
10 failed, 28 passed, 25 deselected
```

That is measured, not estimated, and it is worth knowing what each number is
made of, because you will watch it change all afternoon.

- **10 failed** is `tests/test_board.py`, entirely — every one of the ten
  checks the stub cannot pass yet.
- **28 passed** is everything already correct and none of it yours to write
  today: `check_setup.py`'s own five checks (including the one that only
  passes on Python 3.14 itself — which is the whole reason this number is 28
  and not 27 on an older interpreter), the app's shared data shapes, a
  keyword parser Session 3 reuses, last week's finished spectrum analyser,
  and saving-and-loading.
- **25 deselected** means "skipped on purpose, not broken" — Session 3's
  tests, hidden until `pytest -m lab3` turns them on.

By the end of today, the ten failures become ten passes and nothing else
moves: `38 passed, 25 deselected`.

---

## Gate 1 — Intent (5 minutes). You write this one.

| | |
|---|---|
| **Paste** | nothing — this is the gate a person writes |
| **You edit** | `aidlc/intent.md` |
| **Check** | open `aidlc\intent.md` and press Ctrl+F for `PLACEHOLDER` — zero results |
| **Then** | move to Gate 2 |
| **You end with** | `aidlc/intent.md` filled in · no code yet · still `10 failed` |

Open `aidlc/intent.md`. It asks the same four questions Lab 1's did, but two
of them are largely already answered for you this week, because everyone in
the room is building the same app: who it is for, and what "done" looks
like, are pinned down by `tests/test_board.py` and the four traps later in
this document. Answer them anyway, in your own words — an agent reading a
vague intent file behaves like one that read none — but spend your real
thinking on the two questions that are genuinely yours to decide:

- **What problem does it solve?** Not "the tests require it." Say, in one
  sentence, what is actually slow or annoying today about finding or
  advertising a small paid job on campus, for one real or realistic person.
- **What is deliberately NOT included?** This is the one that saves you at
  Gate 2. Editing a posted job? Messaging inside the app? A login? Name at
  least two things you are choosing not to build, or your agent will invent
  them for you later, and you will pay for that at Gate 4.

Your agent will refuse to write code while placeholder text remains — that
refusal is the file working, exactly as it was in Lab 1.

---

## Gate 2 — Spec (15 minutes). The agent drafts, you approve.

| | |
|---|---|
| **Paste** | the **Gate 2** prompt from `labs/PROMPTS.md`, into a new Cline task |
| **You get** | `aidlc/requirements.md` — a numbered table |
| **Check** | all ten tests cited · every `pytest` row backs a claim about `core/` only · at least two `EYES:` rows · every `intent.md` bullet has a row |
| **Then** | reply `approved` in that same task |
| **You end with** | `+ aidlc/requirements.md` · still `10 failed` |

`labs/PROMPTS.md` has one section per lab — Lab 1's spectrum analyser has its
own Gate 2, and so does Lab 3. Copy the one under the heading **"Lab 2
prompts — the campus job board."**

**Why the prompt says what it says.** It tells the agent to read
`aidlc/intent.md` and `tests/test_board.py` before writing anything, because
a spec invented without looking at either is fiction. It allows exactly two
kinds of check: a `pytest` name, for anything the ten shipped tests already
decide, or an `EYES:` line — a check nobody but you can run, naming
something you open, something you set, and a value you read off the screen.
"Should work correctly" is neither of those, so it is not allowed. It
demands **all ten tests** appear somewhere, because a test with no
requirement pointing at it is work nobody asked for. And it demands **two
`EYES:` rows**, because no test in this repository opens a page — one of the
two is where your defence against the count-and-the-list trap below belongs.

**Check it like this**, before you approve anything:

Open `tests\test_board.py`, press Ctrl+F, and search for `def test_`. VS
Code's search box shows how many matches it found — confirm it says 10, then
confirm all ten of those exact test names show up somewhere in
`aidlc/requirements.md`.

Then check every `pytest` row with a second Ctrl+F pass — not judgement,
because "does this test really decide this claim?" has been gotten wrong
twice already: once by a real agent in a live run of this lab, and once in
the reference spec used to write this lab's answer key. Read the sentence
each `pytest` row is attached to and search it for **Browse, Post, page,
card, count, shows, sees,** or **screen**. No test in this repository opens a
page, so no `pytest` citation can ever decide a claim about one.

A hit is a flag, not a verdict. Ask one question about it: **what is this row
actually claiming?**

- If the claim is about what you'd *see on a page* — a count, a card, a
  message — the row is in the wrong column. Move it to `EYES:`.
- If the claim is about a function in `core/` and the page word is only
  scene-setting, the citation is fine and the **sentence** is what needs
  fixing. Reword it to say what the function does, and leave the row where
  it is.

The second case is real. A clean run of this lab produced:

> Expiry hides a job without deleting it: the active list **the Browse page
> displays** drops it, while both records remain in the data file.

attached to `pytest test_active_jobs_hides_expired_without_deleting_them`.
That test *does* decide that claim — the page words are describing why it
matters. Moving that row would have thrown away a good citation. Deleting
four words fixes it.

**A worked example, so you have seen the mistake once before you have to
catch it yourself.** This exact row reached an *approved* spec, in a live
run of this lab:

| # | Requirement | Acceptance criterion |
|---|---|---|
| 6 | Browsing is built from the open jobs only — every open job in, every expired one out | `pytest test_active_jobs_hides_expired_without_deleting_them` |

Ctrl+F catches it immediately — the sentence contains "Browsing." The test
named is real, and it does pass: `test_active_jobs_hides_expired_without_deleting_them`
calls `active_jobs()` on a list already sitting in memory and checks which
jobs come back. It never opens a page. So this one row is actually two
requirements wearing a single acceptance criterion — a `core/` claim the
test genuinely decides, and a page claim it cannot touch at all. Split it:

| # | Requirement | Acceptance criterion |
|---|---|---|
| 6a | `active_jobs` leaves out a job whose open-until date has passed, without deleting it from the list it was given | `pytest test_active_jobs_hides_expired_without_deleting_them` |
| 6b | Browsing is built from the open jobs only — every open job on screen, every expired one gone from it | `EYES: open Browse Jobs, note which of the seeded jobs are open today, and confirm the board shows exactly those and no others` |

A page that forgets to call `active_jobs` at all — one that lists every job
ever posted, expired or not — still passes 6a, because 6a never looks at the
page. Only 6b can catch that page. This is the whole reason the check above
is Ctrl-F and not a principle to remember: the wrong version of row 6 reads
exactly as thorough as the right one, right up until someone actually opens
the page.

Reply `approved` in the same task. Then start a **new** task for Gate 3 — a
long conversation makes an agent worse, not better.

---

## Gate 3 — Plan (20 minutes). The agent drafts, you approve.

| | |
|---|---|
| **Paste** | the **Gate 3** prompt from `labs/PROMPTS.md` (same "campus job board" section), into a **new** task |
| **You get** | `aidlc/design.md` and `aidlc/tasks.md` |
| **Check** | `design.md`'s function table matches `core/board.py` exactly as `tests/test_board.py` calls it · exactly three tasks, one file each · tasks 2 and 3's **Done when** each name a number |
| **Then** | reply `approved`, then commit (see below) |
| **You end with** | `+ aidlc/design.md`, `aidlc/tasks.md` · committed · still `10 failed` |

The task table is easy to check and it will almost always be right, because
the prompt already dictates its shape: task 1 owns `core/board.py`, task 2
owns `pages/1_Post_a_Job.py`, task 3 owns `pages/2_Browse_Jobs.py`. Checking
it proves very little.

`design.md`'s function table is the part nobody dictated, and it is the part
Gate 4 actually implements against. Read it beside the tests: open
`tests\test_board.py` — it is short, ten tests — and check, function by
function, that every call to `load_jobs`, `save_job`, `is_active`,
`active_jobs` and `search` in that file matches the arguments `design.md`
says each one takes.

Five functions, five names, and their arguments — in particular, `is_active`
and `active_jobs` both take a `today` argument in every test that calls
them. If `design.md`'s table drops it, or leaves room for a version that
reads the clock itself, you are about to approve trap 1 below before you
have even reached Gate 4.

Then check `tasks.md`. Three tasks, one file each, and read the **Done
when** column for tasks 2 and 3 carefully — this is where a plan quietly
goes soft. "The board displays correctly" can be signed off by someone who
never counted anything, and counting is the whole reason task 3 exists. A
**Done when** for a page has to name an actual number: task 3's, especially,
should say that the number in the heading and the number of cards must be
the *same* number — because no test can check that for you, and this is the
sentence that will save you an hour at Gate 4.

Then approve, and commit:

```
git add -A
git commit -m "gates 1-3"
```

---

## Gate 4 — Build (55 minutes). One task at a time.

Three tasks, one file each, run in order — task 2 needs task 1 finished, and
task 3 needs task 2's page to exist beside it. Start a **new** Cline task for
every one of them.

### Task 1 — the rules (`core/board.py`)

| | |
|---|---|
| **Paste** | **Gate 4, task 1** from `labs/PROMPTS.md`, into a new task |
| **You get** | `core/board.py`, all five functions filled in |
| **Check** | `.venv\Scripts\python.exe -m pytest tests/test_board.py -q` says `10 passed` |
| **Then** | `git add -A`, then `git commit -m "task 1: the rules"` |
| **You end with** | `core/board.py` written · **`pytest` now `38 passed, 25 deselected`** · committed |

If you see `TypeError: is_active() takes 1 positional argument but 2 were
given` the instant you run the tests, that is trap 1, and it is meant to
happen this fast — see below. For anything else, paste the failure back into
the same task and let the agent fix that one thing; do not start over.

### Task 2 — Post a Job (`pages/1_Post_a_Job.py`)

| | |
|---|---|
| **Paste** | the first **Gate 4, tasks 2 and 3** prompt from `labs/PROMPTS.md`, into a **new** task |
| **You get** | `pages/1_Post_a_Job.py` |
| **Check** | `.venv\Scripts\python.exe -m streamlit run app.py`, open **Post a Job**, submit one, and read the success message — it names how many jobs are now on the board |
| **Then** | `git add -A`, then `git commit -m "task 2: post a job"` |
| **You end with** | `+ pages/1_Post_a_Job.py` · `pytest` unchanged — nothing in `tests/` opens a page |

### Task 3 — Browse Jobs (`pages/2_Browse_Jobs.py`)

| | |
|---|---|
| **Paste** | the second **Gate 4, tasks 2 and 3** prompt, into **another new** task |
| **You get** | `pages/2_Browse_Jobs.py` |
| **Check** | open **Browse Jobs**. **Count the cards. Read the number in the heading. They must be the same number.** Then change the location, the minimum budget, and the date, one at a time, and check again after each |
| **Then** | commit |
| **You end with** | `+ pages/2_Browse_Jobs.py` · same `pytest` number · the app is functionally finished |

That last check is the one no test in the repository can do for you — it is
trap 4 below. Do it by eye, every time you change a filter, not just once.

---

## The four traps

Four specific ways this exact app goes wrong quietly, found by actually
building it and watching what real agents did. If you hit one of these, you
are not behind — you are exactly on schedule.

### Trap 1 — `TypeError: is_active() takes 1 positional argument but 2 were given`

**If you see this:** the agent wrote a version of `is_active` that reads
today's date itself, instead of accepting it as an argument. Every test in
`tests/test_board.py` hands a fixed `today` in — a `TypeError` is the
loudest, fastest possible feedback that the two disagree, and it fires on
the very first test that runs. A function that reads the clock cannot be
tested at all: whatever you wrote against it stops being true the day after
you wrote it, and nobody notices until it does. **Fix:** tell the agent
`today` is a required second argument, always passed in, never read from
`date.today()`.

### Trap 2 — a job vanishes a day early

**If you see this:** you set a job's "open until" date, and it disappears
from Browse Jobs the day before that date arrives. Somewhere, a comparison
used `>` where it needed `>=`. A job open "until the 8th" is open **on** the
8th — the closing day is included, not excluded — and `>` throws it out a
full day early. This is the same shape of bug as Lab 1's doubled zero-hertz
bin: an edge case nobody types by hand while testing casually, because
casual testing never lands exactly on the boundary. **Fix:** point the agent
at `test_job_expiring_today_is_still_active` and say the comparison is
inclusive.

### Trap 3 — a job you posted is gone for good

**If you see this:** a job expires, or you move "Board as of" past its date,
and then it is nowhere — not on the board, and not if you move the date back
either. Something deleted it, or filtered it out of the *file* instead of
out of what is displayed. Expired means **hidden, not deleted**: the person
who posted a job still wants to see it after it closes. **Check it
directly** — open `data/jobs.json` itself in the editor. A job you posted
must still be sitting in that file even when the board no longer shows it.
If it is missing from the file, `active_jobs` (or something upstream of it)
is rewriting storage instead of only filtering a list in memory — tell the
agent so.

### Trap 4 — the count and the list disagree

**If you see this:** the heading says "12 jobs available" and you count nine
cards below it. The heading and the list were worked out **separately** —
most likely the heading counted every job ever posted while the list below
applied the expiry and search filters, or the other way round. **No test in
this repository can catch this one**, because no test opens a page — which
is exactly why your Gate 2 spec had to carry an `EYES:` row for it, and
exactly why this is checked by eye here and nowhere else. The fix is the
lesson the whole session is built on: work out which jobs to show **once**,
into one variable, and have both the heading and the loop underneath it read
that same variable. Two separate filters will drift apart eventually, even
if they agree today.

---

## A fifth kind of gap — a requirement nobody wrote

This one is not a coding mistake, and none of the four traps above cover
it. It happened in a live run of this exact lab, and it is worth reading
even though nothing here asks you to go fix it.

A student posted a job with the **title field left blank**. It saved. The
confirmation message said success. Browse Jobs showed a card with a
location, a budget, a date and a contact — and no name.

Nothing caught it, at any gate:

- **All ten tests still passed.** None of them opens a page, and none of
  them says a job needs a title — there was nothing written down for any of
  them to fail against.
- **The `EYES:` row for posting a job passed too.** It only checked that
  the confirmation counted to the right number of jobs, never what was
  actually saved.
- **The `EYES:` row for the count-and-the-list agreement passed as well.**
  The heading and the cards agreed perfectly — about a board with a nameless
  job sitting on it.

The cause sits upstream of all four gates, not inside any of them.
`aidlc/intent.md` said the student posts "a job with a title, a place, a
budget…" and never said what should happen if she leaves one of those
blank. `requirements.md` inherited that silence — there was no bullet to
write a row against. `design.md` and `tasks.md` inherited it from
`requirements.md`. The build inherited it from the plan. Every document
downstream of the gap is honest about what it was actually given; the gap
itself was never given to any of them.

**The lesson is not "add validation to your form."** It is this: a missing
requirement is not caught downstream — it is *implemented* downstream, as
an absence, and every check you wrote along the way still goes green. The
gates catch what you asked them to check. They cannot catch a question
nobody thought to ask.

---

## Ship (10 minutes)

| | |
|---|---|
| **Paste** | nothing — no prompt, no agent, this one is all yours |
| **You need** | `git status --short` printing nothing, and `pytest` at `38 passed, 25 deselected` |
| **Check** | the public URL loads for someone who is not you |
| **You end with** | the same files, pushed to GitHub and live on the internet |

Push first. Streamlit Cloud builds from GitHub, not from your laptop —
anything you have not pushed does not exist as far as it is concerned:

```
git status --short     # anything listed here is not committed yet
```

If that printed anything, commit it before you go on:

```
git add -A
git commit -m "gate 4: the campus job board"
```

Then:

```
git push
```

Then go to **https://share.streamlit.io**:

1. **Continue to sign-in** → sign in with GitHub. If you already made this
   account for Lab 1, it remembers you.
2. **Create app** → **Deploy a public app from GitHub**.
3. Fill in three things and nothing else:
   - **Repository:** `your-username/your-new-repository`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. **Deploy**, then wait. Two to five minutes is normal while everyone in the
   room deploys at once.
5. Open the URL. Look for last week's **Spectrum Analyzer** and this week's
   **Post a Job** and **Browse Jobs** in the sidebar — those are the pages
   this app is built from.

Nothing you built today calls a model, so there is no key to add under
Streamlit's **Settings → Secrets** — that step is still ahead of you, in
Session 3.

**If it is not live by the end of the session, stop.** Push your code and
deploy at home. The code and your four `aidlc/` documents are the
deliverable; the URL is a bonus, and nobody is marked down for someone
else's build queue.

---

## Lost?

These three commands tell you exactly where you are. Run them and compare
the answer against the **You end with** line of whichever gate you last
completed, above.

```
git branch --show-current      # should say: main
git status --short             # what you have changed but not committed
.venv\Scripts\python.exe -m pytest -q
```

Ignore all of pytest's output except the very last line it prints — that
line is the count that matters.

You never leave `main` today — there is no branch switch this week, only
more files and a `pytest` count moving toward `38 passed, 25 deselected`. If
`git status --short` lists a file you do not recognise, an earlier attempt
left something behind; if `pytest` shows a number that matches none of the
gate rows above, work out which of the four traps you are in before you
touch anything else.

---

## If a gate goes wrong

If a gate is not working after fifteen minutes, stop prompting — a long
conversation makes an agent worse, not better. Restore the reference version
of whatever you are stuck at, read it, and carry on from there.

**First, once, make the reference reachable.** Your repository was made with
"Use this template," which copies only `main` — the worked solution lives on
the template itself, on branches your copy never received:

```
git remote add reference https://github.com/witchapong/ai-workshop-template-session2.git
git fetch reference
```

Then:

| Stuck at | Run this |
|---|---|
| Gate 2 | `git checkout reference/solution/lab2 -- aidlc/requirements.md` |
| Gate 3 | `git checkout reference/solution/lab2 -- aidlc/design.md aidlc/tasks.md` |
| Gate 4 task 1 | `git checkout reference/solution/lab2 -- core/board.py` |
| Gate 4 task 2 | `git checkout reference/solution/lab2 -- pages/1_Post_a_Job.py` |
| Gate 4 task 3 | `git checkout reference/solution/lab2 -- pages/2_Browse_Jobs.py` |

These files are a reference run — one time an agent did the job well, saved
so you can pick it up rather than start again. **This is not cheating and it
does not cost you marks.** Recognising a dead end and recovering from it is
the skill this lab is teaching. Read what you took before moving on — it is
one defensible answer, not the only one.
