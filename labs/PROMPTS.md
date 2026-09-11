# Prompts that work

One prompt per gate, in the order you need them. Copy them exactly on your
first run — every sentence in them fixes a failure somebody actually hit — and
start improvising next week, once you have seen what a good one looks like.

| Gate | Prompt below | What it writes |
|---|---|---|
| 1 — Intent | **none, you write this one** | `aidlc/intent.md` |
| 2 — Spec | Gate 2 | `aidlc/requirements.md` |
| 3 — Plan | Gate 3 | `aidlc/design.md`, `aidlc/tasks.md` |
| 4 — Build, task 1 | Gate 4, task 1 | `core/spectrum.py` |
| 4 — Build, task 2 | Gate 4, task 2 | `pages/2_Spectrum_Analyzer.py` |
| 5 — Ship | none — `git push`, then deploy | |

**Start a new Cline task for each one.** A long conversation makes an agent
worse, not better.

Round 1's single prompt is not here. It lives inline in `labs/LAB1.md`, on
purpose: it is the one you are meant to fire off without thinking, and it does
not belong on a page called "prompts that work".

Copy these. Improvise later, once you have seen what good looks like. On day
one, use these.

## Gate 2 — ask for the spec

```
Read aidlc/intent.md first. Then read tests/test_spectrum.py.

Now use your file-writing tool to WRITE the file aidlc/requirements.md. Keep
the explanation at the top of that file exactly as it is — replace the table
and everything after it. It must contain a markdown table with one numbered row
per requirement, and every row needs an acceptance criterion that could fail.

Exactly two kinds of criterion are allowed, and you must use both:

  pytest <test name>   for anything tests/test_spectrum.py already checks.
                       There are seven tests in that file. EVERY ONE of them
                       must appear as the criterion of some row, including
                       the one asserting that a tone entered at amplitude 1.0
                       reads back as 1.0, and the one about a constant offset
                       at zero hertz.
                       Word these rows as claims about the COMPUTATION, never
                       about the screen: "the spectrum of a 50 Hz tone peaks
                       at 50 Hz", not "the system accepts a frequency". If the
                       row describes what a person types or sees, it is not a
                       pytest row.

  EYES: <what a person opens, and what they must see>
                       for anything the tests do not reach. Everything about
                       what appears on the screen is this kind.

A pytest criterion may only back a claim about core/. If a row says what the
PAGE does, it needs an EYES criterion — a real test cited for a claim it
cannot decide is worse than no criterion at all, because it passes.

Two EYES rows are required:

  - One about the SPECTRUM chart that fails if an axis is drawn as a line:
    "the spectrum chart's legend names only the amplitude series; if
    'Frequency (Hz)' appears in it as a plotted line, this row has failed."
  - One that CHANGES a value and predicts the number that must change with
    it, e.g. "set tone 1 to amplitude 0.3 and the 50 Hz spike reads 0.3".

Every bullet under "What does done look like" in aidlc/intent.md must appear as
at least one row. A bullet with no test still gets a row, with an EYES
criterion naming the exact thing to look at and the exact value to read.

Write the file now. Do not ask permission first. Do not print the table in your
reply instead of writing it. Do not write any .py file.
```

## Gate 3 — ask for the plan

```
aidlc/requirements.md is approved. Read it.

Now use your file-writing tool to WRITE two files. In each one, keep THAT
FILE'S OWN explanation — the text already above its table — exactly as it is,
and replace only the table and what follows it. Do not copy the explanation
from one file into the other, and do not bring across anything from
aidlc/requirements.md; each file keeps the words it already had, because that
is what the student reads when they come back to it:

1. aidlc/design.md — what the app computes, and which screen shows it. It must
   include a function table with one row per function in core/spectrum.py,
   giving the exact name, what it takes and what it returns, matching how
   tests/test_spectrum.py calls them. Gate 4 implements that table, so it is
   the part of this document that has to be right.
2. aidlc/tasks.md — a markdown table of exactly two tasks. Task 1 owns
   core/spectrum.py and nothing else. Task 2 owns pages/2_Spectrum_Analyzer.py
   and nothing else. One file per row, and no file appears twice.

   Your table needs four columns, the last one headed "Done when". Fill that
   column in for BOTH tasks by copying an acceptance criterion from
   aidlc/requirements.md. Task 2's must be an EYES criterion: no test in this
   repository opens pages/, so a task that owns a page can never be finished
   by pytest.

   Copy the STRONGEST EYES row you wrote, not the easiest one. Task 2's Done
   when must name a number to read off the screen. "two spikes appear" can be
   ticked by someone who never read a spike height, and reading the height is
   the whole reason this app exists.

Write both files now. Do not ask permission first. Do not print them in your
reply instead of writing them. Do not write any .py file.
```

## Gate 4, task 1 — the maths

```
aidlc/design.md and aidlc/tasks.md are approved. Read aidlc/design.md first:
its function table is the contract you are implementing, and what you write
must match it. Implement task 1 only.

core/spectrum.py already exists as a stub whose functions raise
NotImplementedError. Use your file-writing tool to OVERWRITE that whole file in
one go — do not edit it line by line. It must end up with exactly these three
functions:

  make_signal(components, fs, duration) -> (times, signal)
      components is a list of (frequency_hz, amplitude) pairs
  spectrum(signal, fs) -> (freqs, magnitudes)
  peak_frequency(freqs, magnitudes) -> float

Write the whole file in one go rather than editing it repeatedly. Every test in
tests/test_spectrum.py must pass, including the one asserting that a tone at
amplitude 1.0 reads back as 1.0.

Write the file now.

Then run this exact command and paste its output verbatim into your reply:

    .venv\Scripts\python.exe -m pytest tests/test_spectrum.py -q

Do NOT write your own test script, and do NOT judge the implementation by one.
The file tests/test_spectrum.py is the only thing that decides whether this is
finished. If it reports any failure, fix the code and run it again.

Do not touch pages/.
```

## Gate 4, task 2 — the screen

```
Task 1 is done. Implement task 2 only.

Use your file-writing tool to CREATE pages/2_Spectrum_Analyzer.py: a Streamlit
page with number inputs for two tones, each with a frequency in hertz and an
amplitude, plus a sampling rate and a duration in seconds — six inputs in
total. Import make_signal, spectrum and
peak_frequency from core.spectrum. Show the strongest frequency, then two
charts: the combined waveform against time, and the amplitude of each frequency
present. Default the inputs to tone 1 at 50 Hz amplitude 1.0, tone 2 at 120 Hz
amplitude 0.5, sampling rate 1000 and duration 1.0 second, so the charts are
readable the moment the page opens.

Write the whole file in one go. Write it now, do not print it in your reply
instead. Do not modify core/spectrum.py.
```

## Why these are worded the way they are

Eight things in these prompts are deliberate. The last four were learned the
hard way — an earlier version of this file scored zero, and the agent replied
*"I don't have the capability to create files on your system."* That was not
true. It was the prompt.

1. **Each one is a separate task.** Start a new Cline task per gate. A long
   conversation makes the agent worse, not better.
2. **"Write the whole file in one go."** When an agent edits a file it has to
   match the existing text exactly, and it often fails. Writing a new file
   whole avoids that failure entirely.
3. **Exact function names and arguments are stated.** Anything you leave vague
   is a decision the agent makes for you, and it will not read your mind.
4. **Name the tool: "use your file-writing tool to WRITE …".** "Draft" and
   "create" both get satisfied by an agent that just talks at you. Naming the
   action leaves no room for that.
5. **Never write "wait for my approval" in a prompt.** `.clinerules` already
   makes the agent stop at each gate. Repeating it in the prompt makes the
   agent stop *instead of* doing the work.
6. **Forbid the near-miss.** "Do not print it in your reply instead of writing
   it" closes the one failure the other rules still allow.

7. **Gate 2 must cover intent.md, not just the test file.** An earlier
   version of this prompt said "those tests are the acceptance criteria". A
   student whose intent.md asked for plots that "correctly display values in
   both axes" got a spec of seven rows, every one of them a pytest test on
   `core/spectrum.py`, and not one word about the screen. The agent obeyed
   perfectly. Every test passed. The chart was unreadable. A spec that can
   only cite tests can only describe the half of the app that has tests.

8. **Short is a feature, not a saving.** These prompts used to be forty lines.
   Most of that was the same four instructions repeated in each one — use your
   file-writing tool, write the whole file, do not print it at me, do not ask
   first. Those now live in `.clinerules.gates`, which your agent reads every
   time. Nothing was dropped; it was moved somewhere it only had to be said
   once. What is left is the part that changes from gate to gate.

**The transferable lesson:** when an agent tells you it *cannot* do something
it plainly can, read your own prompt before you blame the model. Nine times in
ten you told it not to.

## If a gate goes wrong

Do not keep prompting a confused agent. Restore the reference version of that
gate and carry on — it costs you nothing:

**First, once, make the reference reachable.** Your repository was
made with "Use this template", and that copies only `main` — the solution
branches live on the template, not on your copy. Without this the commands
below fail with `invalid reference`:

```
git remote add reference https://github.com/witchapong/ai-workshop-template.git
git fetch reference
```

| Stuck at | Run this |
|---|---|
| Gate 2 | `git checkout reference/solution/lab1 -- aidlc/requirements.md` |
| Gate 3 | `git checkout reference/solution/lab1 -- aidlc/design.md aidlc/tasks.md` |
| Gate 4 task 1 | `git checkout reference/solution/lab1 -- core/spectrum.py` |
| Gate 4 task 2 | `git checkout reference/solution/lab1 -- pages/2_Spectrum_Analyzer.py` |


---

# Lab 2 prompts — the campus job board

Five prompts: one for each gate, and Gate 4 takes two. Each fits on a slide
because the rules that used to be repeated in all four now live in
`.clinerules.gates`, which your agent reads on every message whether you
mention it or not.

**Start a new Cline task for each gate.** A long conversation makes an agent
worse, not better.

## Gate 2 — ask for the spec

```
Read aidlc/intent.md, then tests/test_board.py.

Write aidlc/requirements.md: one numbered row per
requirement, each with a check that can fail. Only two
kinds are allowed:

  pytest <test name>   for what tests/test_board.py
  checks. Never cite a test for a claim about the
  screen: a passing test that cannot decide the claim
  is worse than none.
  EYES: <what to open, what to see>   for everything
  else.

All ten tests must appear. Every bullet in intent.md
needs a row. Two rows must be EYES: one where two
numbers must match, one naming a value to read.
```

## Gate 3 — ask for the plan

```
aidlc/requirements.md is approved. Read it.

Write two files, each keeping its own explanation.

aidlc/design.md: a function table, one row per function
in core/board.py - exact name, what it takes, what it
returns - matching how tests/test_board.py calls them.

aidlc/tasks.md: exactly three tasks. Task 1 owns
core/board.py, task 2 pages/1_Post_a_Job.py, task 3
pages/2_Browse_Jobs.py. Four columns, the last headed
"Done when", filled from requirements.md. Tasks 2 and 3
need EYES criteria naming a number: no test here opens a
page.
```

## Gate 4, task 1 — the rules

```
aidlc/design.md is approved. Its function table is the
contract. Implement task 1 only: overwrite core/board.py
with these five:

  load_jobs(path) -> list of jobs
  save_job(path, job) -> None
  is_active(job, today) -> True or False
  active_jobs(jobs, today) -> list of jobs
  search(jobs, location=None,
         min_budget=None) -> list of jobs

today is handed in, never read from the clock. Then run
.venv\Scripts\python.exe -m pytest `
    tests/test_board.py -q
and paste the output verbatim. Do not touch pages/.
```

## Gate 4, tasks 2 and 3 — the screens

```
Task 1 is done. Implement task 2, then stop.

Create pages/1_Post_a_Job.py: a Streamlit form with a
title, a location dropdown, a budget number, a date, and
a contact box. Saving calls save_job("data/jobs.json",
job). Store the date as text with str().

After saving, show a message naming how many jobs are
now on the board.

Do not modify core/board.py.
```

```
Task 2 is done. Implement task 3.

Create pages/2_Browse_Jobs.py: a location dropdown, a
minimum budget, and a date to view the board as of. Work
out the jobs to show ONCE, into one variable, then show
how many there are and list them from that same
variable.

Import load_jobs, active_jobs and search from
core.board. Do not filter the jobs yourself in this
file.

Do not modify core/board.py.
```

---

# Lab 3 prompts

Same rules as Lab 1: name the tool, ask for a whole file, forbid the reply that
talks instead of writing.

## Checkpoint 2 — the plain call

```
Read core/llm.py. It is a stub whose functions raise NotImplementedError.

Use your file-writing tool to OVERWRITE the whole file in one go, implementing
ask() so it sends a question to Gemini and returns the reply text. Read the
GEMINI_MODELS list at the top of check_setup.py and use the same
try-each-in-turn approach: pinned models get retired and busy ones return
"high demand".

Leave ask_structured() raising NotImplementedError for now. Write the file now;
do not print it in your reply instead.
```

## Checkpoint 3a — the schema call

```
Now implement ask_structured() in core/llm.py, overwriting the whole file
again. It takes a question and a JSON schema, asks the model to reply as JSON
matching that schema, and returns it as a Python dictionary. If the reply is
not valid JSON, raise ValueError saying so and showing what came back.

Keep ask() exactly as it is. Write the file now.
```

## Checkpoint 3b — the extractor

```
core/intake.py is a stub. Read session3/menu.md and session3/inbox.json first,
then overwrite core/intake.py in one go so that:

  load_menu and order_total are plain Python with no model call
  extract_one sends ONE message and returns the ORDER_SCHEMA shape
  extract_batch sends ALL messages in a SINGLE request and returns a list

Item names must come from the menu — pass the menu names into the prompt and
say they are the only permitted values. Do NOT ask the model to compute any
total; order_total does that in Python.

Then run: .venv\Scripts\python.exe -m pytest -m lab3 tests/test_intake.py -q
and paste the output verbatim. Do not write your own test script.
```

## Checkpoint 4 — the review queue

```
Implement needs_review() in core/intake.py: return the ids of records the model
flagged with needs_review true, plus any record with an empty required field or
a quantity of zero or less. Plain Python, no model call.

Then run: .venv\Scripts\python.exe -m pytest -m lab3 tests/test_intake.py -q
and paste the output verbatim.
```

## If it argues instead of writing

An agent that replies "I don't have the ability to create files" or hands you
the code in chat has been told to, somewhere in your wording. Say **"use your
file-writing tool to write the file now"** and it will.
