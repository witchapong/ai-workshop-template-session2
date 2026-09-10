# Lab 1 — Build a spectrum analyser, twice

You will build the same app two ways, and the comparison between them is the
whole point of the lab. Round 1 you just ask for it. Round 2 you go through
four checkpoints where a person decides before the agent is allowed to carry
on. Same app, same agent, same model.

Everything below is written so you can follow it on your own. If you get
stuck for more than ten minutes on any step, ask a neighbour before you ask
the instructor — there are sixty of you and one of them.

---

## What you are building

A **spectrum analyser** takes a signal and tells you which frequencies it is
made of.

**What you type in:**

| Input | Meaning | Use this |
|---|---|---|
| Frequency 1 | how fast the first tone oscillates, in hertz | **50** |
| Amplitude 1 | how tall that tone is | **1.0** |
| Frequency 2 | the second tone, in hertz | **120** |
| Amplitude 2 | how tall the second tone is | **0.5** |
| Sampling rate | samples taken per second | **1000** |
| Duration | how many seconds of signal | **1.0** |

**What must come out:** two charts.

1. **Time domain** — the two sine waves added together. A messy wiggle. This
   is what an oscilloscope would show you.
2. **Frequency domain** — the spectrum. Two spikes: one **at 50 Hz reaching
   1.0**, one **at 120 Hz reaching 0.5**.

Those spike heights are not decoration. They are the numbers you typed in,
handed back to you — which is what makes this app checkable at all.

---

## What is in this repository

Before you build anything, spend three minutes looking at what you already
have. Open the file explorer on the left and follow along.

```
your-repo/
├── app.py                  the front page. Run this to start the app.
├── pages/                  ONE FILE PER FEATURE. This matters in Session 2:
│   └── 1_Example.py        one task owns one file, so nothing collides.
├── core/                   shared code the pages import.
│   ├── spectrum.py         <- YOU BUILD THIS in Lab 1. Currently every
│   │                          function raises NotImplementedError.
│   ├── llm.py              the AI slot. Empty until Session 3, on purpose.
│   ├── models.py           the shapes your data takes.
│   └── storage.py          saving and loading.
├── tests/                  automated checks.
│   └── test_spectrum.py    <- YOUR SPECIFICATION. Seven checks. The app is
│                              finished when all seven pass.
├── aidlc/                  the four planning documents. You fill these in
│   ├── intent.md           before any code exists. This is Round 2.
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
├── labs/                   these instructions, and the prompts to paste.
├── .clinerules             the rules your agent obeys on EVERY request.
├── .clinerules.gates       the stricter version. Round 2 switches to it.
├── .env                    YOUR API KEYS. Never commit this file.
└── requirements.txt        the approved library list. It is closed.
```

One of these deserves a proper look right now.

**Open `.clinerules`.** Plain English, in a plain file. Your agent reads it
before every single request. Right now it contains safety rules only — no
process, no approvals, no one telling it to stop and check. That is
deliberate, and Round 1 is why.

Leave `tests/` alone for now. You will open it in Round 2, at the point where
it does the most good.

---

## Before you start: point Cline at a model

Your key in `.env` is for the **app**. Cline is a separate extension with
its own settings and its own copy of the key. Passing `check_setup.py` tells
you nothing about whether your agent can talk to anything.

**"Why the same key in two places?"** Because they are two different
programs. `.env` is read by *your app* — `check_setup.py` today, and
`core/llm.py` in Session 3 when your app starts calling a model itself. Cline
is not your app; it is the tool building it, and it carries its own
credentials. Lab 1's app never calls a model at all, so today `.env` is doing
one job: proving your key is real before you depend on it.

That split — the tool that does things, and the model that decides what to
say — is the mental model this whole course runs on. You just met it as an
annoyance.

1. Click the **Cline icon** — the robot, near the bottom of the strip of icons
   down the far left. They are unlabelled; hover to check.
2. Cline opens on **"How will you use Cline?"** with **Absolutely Free**
   already ticked. **Do not take it** — that signs you into Cline's own service
   and never uses your key. Choose **Bring my own API key**.
3. Provider: **Mistral** (or **Google Gemini** if that is the key you have).
   Paste the matching key.
4. Choose a **model**. Cline's list is its own and does not match the names in
   `.env` or in Mistral's documentation: the entries carry a date, like
   `devstral-2512`. Some entries do say "latest", but the dated coding models
   are the ones you want. Pick one starting with **`devstral`** if you see one,
   otherwise **`mistral-medium`**.
5. **If you have a second key, add that provider too.** Cline runs one provider
   at a time; switching means changing it in the model selector, not having two
   set up side by side.
6. Type **hello** into Cline and check that you get a reply.

> **Check the model name after any window reload.** It is the small grey text
> at the bottom of the Cline box, and Cline can quietly reset it.
>
> Judge it by **whose** model it is, not by the price. Cline shows a price per
> million tokens for everything; on a free key you are rate-limited, not
> billed. But if the name stops looking like a Mistral one — anything with
> `zai`, `anthropic`, `openai`, `claude` or `gpt` in it — it has jumped to a
> provider you have no key for, and nothing will work. Set it back. If
> `devstral` has disappeared from the list, which happens after a reload,
> take `mistral-medium`.

**Then close the `.env` tab.** Your keys are passwords and they are sitting
on screen. Get in the habit now — you will be sharing this screen later.

### Switching providers is a two-minute skill you need today

Do it once now, deliberately, while nothing is at stake: open the model
selector, change the model, ask "hello", change it back. That way when it
happens under pressure you already know where the button is.

**Only got one key?** You cannot practise the switch, so read the table below
instead and know it is there.

You will hit one of two failures today, and they need opposite responses:

| What you see | What it means | What to do |
|---|---|---|
| `429` / "rate limit exceeded" | You are asking too fast. Your quota is fine. | **Wait.** About a minute. Switching wastes your other key. |
| `503` / "high demand" / "unavailable" | That model is refusing everyone. | **Switch provider.** Waiting will not help. |

**One honest warning about the second key.** Mistral's free tier is about three
requests a minute, and one instruction to an agent is four to ten requests. It
is a rescue for a stuck step, not a second full allowance — it will not carry a
whole 70-minute round on its own. If your main provider dies for good, pair up
with a neighbour whose quota is alive: one drives, one reads the diff. Then
take the reference version for whatever you cannot finish, which is what it is
there for.

Free tiers are genuinely flaky. Both of these happened repeatedly while this
lab was being written, on an ordinary weekday, with one user.

---

## Round 1: just ask for it (25 minutes)

### Where each step leaves you

Round 1 happens on a branch called `round1`. Nothing you build here reaches
`main` — that is deliberate, and it is what makes the comparison at the end
honest.

| After | You are on | Your files | `pytest` |
|---|---|---|---|
| Step 1 | `round1` | nothing changed yet | not run |
| Step 3 | `round1` | whatever the agent chose to write | `7 failed` |
| Step 6 | `main` | Round 1's files vanish from the explorer — safe on `round1` | `7 failed` |

**One file decides how this round goes: `.clinerules`.** Right now it holds
the ungated version — safety rules only, no approval stops. That is why your
agent will go straight to code without asking you anything.
`.clinerules.gates` is sitting next to it, unused, until Round 2 Step 1.

**Round 1 is not expected to make a single test pass, and it is not supposed
to.** Your agent was never told the tests exist, so it is not aiming at them.
Seven failures at the start, almost certainly seven at the end — that is the
honest measure of what "just ask for it" bought you.

### Step 1 — Put Round 1 on its own branch

**Start on `main`, with nothing uncommitted.** Check both:

```
git branch --show-current     # must print: main
git status --short            # must print nothing at all
```

If `git status --short` lists any file, commit it before you go on. A branch
switch carries uncommitted changes with you, and they resurface in the middle
of Round 1 looking like something your agent did.

You are going to throw this work away, but keeping it lets you compare the
two rounds at the end.

```
git checkout -b round1
```

**You are now on `round1`, and not one file has changed.** You have only made
a place to put them.

### Step 2 — Ask for the app

**You are on `round1`.** The agent has no spec, no plan, and no rule telling
it to stop and ask. It will decide by itself which files to create — and
where it puts them is one of the things you compare at the end.

Open Cline, start a **new task**, and paste exactly this:

```
Build me a spectrum analyser in Streamlit. I set two sine waves - a frequency
and an amplitude for each - and it adds them together and plots the
time-domain waveform and the frequency spectrum.
```

### Step 3 — Accept whatever it does

Expect two or three `429 rate limit exceeded` messages per task on a free tier.
Cline retries by itself and each costs twenty to forty seconds — that is the
limit working, not a fault.

Sometimes it gives up: **"Auto-retry failed after 3 attempts. Manual
intervention required."** That is not broken either. Wait about a minute and
click **Retry**.

No spec. No plan. No corrections beyond getting it to run. When it asks to
create or edit a file, click **Save**. If it crashes, paste the error back to
it and let it try again. Your only goal is something on screen.

### Step 4 — Run it

```
.venv\Scripts\python.exe -m streamlit run app.py
```

A browser tab opens automatically at `http://localhost:8501`. If it does not,
copy that address out of the terminal yourself and paste it into a browser.

**Your new page may not be in the sidebar.** Nothing told the agent about the
`pages/` convention, so it has probably written a standalone script at the top
level instead. If the sidebar only shows *app* and *Example*, look at what it
actually created and run that file by name:

```
.venv\Scripts\python.exe -m streamlit run whatever_it_made.py
```

That is not a mistake to fix — it is Round 1 being Round 1, and it is one of
the things you will compare at the end.

> **Run it yourself — do not ask your agent to.** "Run my app" looks like a
> reasonable request and it wedges Cline completely: a web server never exits,
> so the agent sits waiting for a command that will never finish and stops
> responding to anything else. If you have already done it, press `Ctrl+C` in
> the terminal to stop the server and the agent comes back.

### Step 5 — Interrogate it

Set **tone 1 to 50 Hz at amplitude 1.0** and **tone 2 to 120 Hz at amplitude
0.5**. Then answer these in `LOG.md` (your AI collaboration log — it is in your repository, with the questions already written out). Answer whichever set
applies:

**If it never ran:**
- What was the error, in full?
- How many attempts did it take, and how many minutes?
- Did the agent understand its own error, or did it guess?

**If it ran:**
- **Does the 50 Hz spike reach 1.0?** Read the number off the chart.
- Does the 120 Hz spike reach 0.5?
- If a classmate asked "is this correct?", could you show them why? Not
  "it looks right" — *show* them.

Whatever you find, write down the number you actually saw. It is the most
useful line in your log.

Then, with the app still running, open a second terminal and run:

```
.venv\Scripts\python.exe -m pytest -q
```

Look at the last line. Expect `7 failed, 21 passed, 25 deselected`. **A working app and seven failing
tests at the same time** — that is Round 1 in one line, and it is worth a
sentence in your log. (If your agent happened to edit `core/spectrum.py` you
may see fewer failures. Note whichever number you actually get.)

### Step 6 — Put it away

**You are on `round1`, the server is running, and your work is uncommitted.**
All three change here.

```
Ctrl+C                                    # stop the app first
git add -A
git commit -m "Round 1 - just asked for it"
git checkout main
```

Stop the server before you switch. Leave it running and it keeps serving a file
that no longer exists on this branch, your next `streamlit run` quietly lands on
port 8502 instead of 8501, and you spend ten minutes looking at a stale tab
wondering why nothing changes.

**Everything the agent wrote will disappear from the file explorer**, and
that is what is supposed to happen. Those files exist on the `round1` branch,
not on this one. `git checkout round1` brings them all back whenever you want
them.

**You end on `main`: tree clean, `pytest` back to `7 failed, 21 passed`,
`core/spectrum.py` still an untouched stub.** Confirm it if you like:

```
git branch --show-current     # main
git status --short            # nothing
```

Your `.env` survives the switch — it is git-ignored, so it belongs to no
branch and is never committed.

---

## Round 2: the Four Gates (70 minutes)

Gate 1 five, Gate 2 ten, Gate 3 ten, Gate 4 forty. That is sixty-five, and it
leaves nothing spare — Gate 5 (ship) happens in the ten minutes after this
block, not inside it. If you are behind, Gate 4 task 2 is the one to shorten.

Same app. Different route. Every prompt you need is in `labs/PROMPTS.md` —
copy them exactly on your first run.

### Where each gate leaves you

**Everything from here to the end of the lab happens on `main`.** You do not
change branch again. What changes is which files exist, and what `pytest` says.

| After | Files that now exist | `pytest` |
|---|---|---|
| Step 0 | none of yours yet | `7 failed, 21 passed` |
| Step 1 | `.clinerules` swapped for the gated one | `7 failed, 21 passed` |
| Gate 1 | `aidlc/intent.md`, filled in by you | `7 failed, 21 passed` |
| Gate 2 | `+ aidlc/requirements.md` | `7 failed, 21 passed` |
| Gate 3 | `+ aidlc/design.md`, `aidlc/tasks.md` | `7 failed, 21 passed` |
| Gate 4 task 1 | `core/spectrum.py` written | **`28 passed`** |
| Gate 4 task 2 | `+ pages/2_Spectrum_Analyzer.py` | `28 passed` |
| Gate 5 | same files, now live on the internet | `28 passed` |

**Nothing turns green until Gate 4.** Gates 1, 2 and 3 produce documents, not
code. If you are three gates in and still staring at seven failures, you are
exactly where you should be — the count does not move until the maths gets
written.

> **Lost at any point?** These three lines tell you where you are. Match them
> against the table above.
>
> ```
> git branch --show-current                        # which branch you are on
> git status --short                                # what you have changed but not committed
> .venv\Scripts\python.exe -m pytest -q             # how far the code has got (read the last line)
> ```

### Step 0 — Check you are on `main`, and see where you start from

Round 2 belongs on `main`. If you are still on the `round1` branch, everything
below happens in the wrong place: the gate swap, every commit, and the Round 1
files are still sitting there for your agent to find.

```
git branch --show-current
git status --short
```

**The first must say `main`, and the second must print nothing.** If it says
`round1`, you have not finished Round 1 — go back and do Step 6:

```
git add -A
git commit -m "Round 1 - just asked for it"
git checkout main
```

Now look at where you are starting from:

```
.venv\Scripts\python.exe -m pytest
```

```
7 failed, 21 passed, 25 deselected
```

**That is correct, not broken.** The 21 passing are the template's own checks.
The 25 deselected belong to Session 3 and stay hidden until you get there. The
7 failing are your specification, and watching those seven turn green is the
whole of Round 2.

**You get exactly this number because you are on `main`.** Round 1's code is
on `round1` and cannot affect anything here. Everyone in the room sees the
same seven failures at this point, no matter how Round 1 went for them.

### Step 1 — Turn the gates on

In Round 1 your agent had no process rules, which is why it went straight to
code. The rules that change that are already in your repository — this copies
one file over another:

```
copy .clinerules.gates .clinerules
git add .clinerules
git commit -m "turn the gates on"
```

**`.clinerules` now holds the gated rules; `.clinerules.gates` is unchanged
and still sits beside it** as the copy you took it from. Nothing else in the
repository moved.

**Commit it.** Otherwise the next `git checkout -- .` you run quietly puts
the old file back, your agent stops asking for approval, and you will not
know why.

Open `.clinerules` and read it again — it has changed. Then **start a new Cline task** — it reads
the rules when a task begins, so the one already open is still using the old
set.

Nothing else has changed. Same agent, same model, same request. Only this
file.

> ### ⚠ Two things that will cost you work if you skip them
>
> **1. Click Save before starting a new task.** When Cline writes a file it
> shows you a diff with **Save** and **Reject** buttons. Until you click
> Save, that work exists only in the preview. **If you start a new task
> while a diff is open, the edit is silently thrown away** — the code you
> just watched it write disappears and your tests go back to failing. This is
> the single easiest way to lose twenty minutes today.
>
> **2. `git checkout -- <file>` is your undo.** Pasted into the wrong pane?
> Agent mangled a file? One command puts that file back to your last commit:
> ```
> git checkout -- core/spectrum.py
> ```
> This is why you commit every time the tests pass.

### Gate 1 — Intent (5 minutes). You write this one.

| | |
|---|---|
| **Paste** | nothing — this is the gate a person writes |
| **You edit** | `aidlc/intent.md` |
| **Check** | open `aidlc/intent.md`, `Ctrl+F` for `PLACEHOLDER` — 0 matches |
| **Then** | move to Gate 2 |
| **You end with** | `aidlc/intent.md` filled in · no code yet · still `7 failed` |


Open `aidlc/intent.md`. Replace every `PLACEHOLDER` line with your own
answer. Four questions:

- **Who is this for?** One real person, one sentence.
- **What problem does it solve?** What is slow or annoying for them today?
- **What does "done" look like?** Be concrete. If you enter 1.0, say that the
  chart must show 1.0.
- **What is deliberately NOT included?** This is the one that saves you.
  No file loading, no saving, no more than two tones.

Your agent will refuse to write code while the placeholder text is still
there. That refusal is the file working.

### Gate 2 — Spec (10 minutes). The agent drafts, you approve.

| | |
|---|---|
| **Paste** | the **Gate 2** prompt from `labs/PROMPTS.md`, into a new Cline task |
| **You get** | `aidlc/requirements.md` — a numbered table |
| **Check** | every "done" bullet has a row; **all seven tests are cited**; a `pytest` criterion only ever backs a claim about `core/`; and every name it cites really exists |
| **Then** | reply `approved` in that same task |
| **You end with** | `+ aidlc/requirements.md` · still `7 failed` |


**Before you prompt anything**, write down in your own words how you would
*check* that the spectrum your app draws is correct. Do it now, on paper.

Now paste the **Gate 2** prompt from `labs/PROMPTS.md`. The agent writes
`aidlc/requirements.md` — a numbered table where every requirement carries an
acceptance criterion you can run.

Read every line. Compare it to what you wrote on paper.

Most people write "the peaks should be in the right places". The tests check
that too — but they also check that **a tone entered at 1.0 reads back as
1.0**. The gap between those two sentences is the entire skill this lab is
teaching. Note it in your log.

**Check that each criterion can decide its own row.** This is the subtle one,
and it is the mistake that actually gets made. A row saying *"the page reports
the strongest frequency"* backed by `pytest test_a_50_hz_sine_peaks_at_50_hz`
looks impeccable — but that test calls a function in `core/`, and it passes
happily while the page shows nothing at all. **If the row says what the page
does, it needs an `EYES:` criterion.** A real test cited for a claim it cannot
decide is worse than no criterion, because it passes.

**Check the test names are real.** An agent that writes
`pytest test_the_chart_is_correct` has invented a test that does not exist, and
a criterion citing a test nobody wrote can never fail. One check settles it:
open `tests/test_spectrum.py`, `Ctrl+F` for `def test_` — the match count
should read 7.

Every `pytest` name in your table must appear in that file — and every test in
that file must appear in your table. Those seven tests are what Gate 4 is
aiming at, so a test with no requirement is work nobody asked for.

Now open `aidlc/requirements.md` and `Ctrl+F` for `pytest test_`. That match
count must be at least 7. A weaker model will happily write you a spec of nine
EYES rows and one test, because the EYES half of the prompt is longer.

**Then count the rows against your `intent.md`.** Every bullet you wrote under
*what does done look like* must appear. The ones about the screen cannot point
at a test — no test in this repository opens a page — so they get an `EYES:`
criterion instead, naming what to open, what to set, and what number to read.

A real spec from this course had seven rows, every one of them a passing test
on `core/spectrum.py`, and nothing at all about the chart. Every test passed.
The chart plotted the time axis as a line and was unreadable. **A spec that
only cites tests can only describe the half of the app that has tests.**

Reply `approved` **in the same Cline task**. Then start a **new** task for
Gate 3 — one task per gate, because a long conversation makes an agent worse.

### Gate 3 — Plan (10 minutes). The agent drafts, you approve.

| | |
|---|---|
| **Paste** | the **Gate 3** prompt from `labs/PROMPTS.md`, into a **new** task |
| **You get** | `aidlc/design.md` and `aidlc/tasks.md` |
| **Check** | `design.md`'s function table matches what `tests/test_spectrum.py` calls; two tasks, one file each; and **task 2's Done when names a number to read**, not just something to look at |
| **Then** | reply `approved`, then commit: `git add -A`, then `git commit -m "gates 1-3"` |
| **You end with** | `+ aidlc/design.md`, `aidlc/tasks.md` · committed · still `7 failed` |


Paste the **Gate 3** prompt from `labs/PROMPTS.md`. You get two files:

- `aidlc/design.md` — what the app computes and which screen shows it.
- `aidlc/tasks.md` — a table of exactly two tasks. Task 1 owns
  `core/spectrum.py`. Task 2 owns `pages/2_Spectrum_Analyzer.py`. One task,
  one file.

That looks like bookkeeping right now. In Session 2 it is the whole trick,
aimed at a different target: it is not there to stop two people colliding,
it is there to stop *you* moving on to task 2 before task 1 actually works —
each file gets built, tested, and committed on its own, one thing at a time.

**Read `design.md` against the tests before you approve it.** The task table
is easy to check and it will almost always be right, because the Gate 3 prompt
dictated it — so checking it proves very little. `design.md` is the part
nobody dictated. Open it beside `tests/test_spectrum.py` and confirm the
function names and their arguments match what the tests actually call: open
`tests/test_spectrum.py`, turn on regex search in `Ctrl+F` (the `.*` icon),
and search for `def test_|make_signal\(|spectrum\(|peak_frequency\(`.

Gate 4 implements the contract in `design.md`. An error you approve here comes
back as broken code twenty minutes later.

Then check the task table. Two tasks, one file each — and read task 2's **Done
when** carefully, because this is where a good spec quietly goes soft. *"Two
spikes appear in the spectrum chart"* can be ticked by someone who never read a
spike height, and the height is the whole reason this app exists. Task 2 owns
the entire screen, so its Done when has to name a number: *"the 50 Hz spike
reads 1.0"*. Send it back if it does not.

Then approve.

### The one piece of maths you need

Gate 4 is where the agent gets the scaling wrong, and you cannot judge its fix
unless you know what right looks like. It is two lines.

An FFT of a signal with **N** samples splits each tone's energy between a
positive and a negative frequency. A one-sided spectrum only shows you the
positive half, so a tone you entered at amplitude 1.0 arrives holding **N/2**.
To get your 1.0 back you scale every bin by **2/N**.

The 0 Hz bin is the exception. A constant offset has no negative-frequency
twin to share with, so it was never halved — doubling it makes it twice as big
as it should be. It takes **1/N**.

```python
magnitudes = 2.0 * np.abs(coefficients) / n
magnitudes[0] = np.abs(coefficients[0]) / n     # DC has no twin
```

That asymmetry is requirement 5 in your spec, and it is the single thing the
agent is most likely to get wrong.

### Gate 4 — Build (40 minutes). One task at a time.

| | |
|---|---|
| **Paste** | **Gate 4, task 1** from `labs/PROMPTS.md`, into a **new** task |
| **You get** | `core/spectrum.py` |
| **Check** | `.venv\Scripts\python.exe -m pytest tests/test_spectrum.py -q` says `7 passed` |
| **Then** | `git add -A`, then `git commit -m "task 1: the maths"` |
| **You end with** | `core/spectrum.py` written · **`pytest` now `28 passed`** · committed |

| | |
|---|---|
| **Paste** | **Gate 4, task 2**, into another **new** task |
| **You get** | `pages/2_Spectrum_Analyzer.py` |
| **Check** | the page opens at 50 Hz / 1.0 — **that spike reaches 1.0**. Then change it to 0.3 and watch the spike follow |
| **Then** | commit again |
| **You end with** | `+ pages/2_Spectrum_Analyzer.py` · `28 passed` · committed |


**Task 1, the maths.** Paste the **Gate 4, task 1** prompt from
`labs/PROMPTS.md`. Then run:

```
.venv\Scripts\python.exe -m pytest tests/test_spectrum.py -q
```

You are aiming for `7 passed`. Some of you will get it first time and some
will not — the failure to expect is
`test_a_constant_offset_appears_at_zero_hz`, because a constant offset must not
be doubled the way the tones are. Whether it fires depends on how much of the
scaling rule reached `design.md` at Gate 3, so a clean first run is a sign your
spec was good, not a sign you skipped something. If a test does fail, paste the
failure back to the agent and let it fix that one thing.

**You will not all get the same result.** The same prompt on the same model
gives different answers on different runs. That is normal and it is worth
noting in your log.

When it is green:

```
git add -A
git commit -m "task 1: the maths"
```

**Task 2, the screen.** Paste the **Gate 4, task 2** prompt from
`labs/PROMPTS.md`. Then run the app
and check it with your own eyes:

```
.venv\Scripts\python.exe -m streamlit run app.py
```

The page opens with tone 1 at 50 Hz and amplitude 1.0 already filled in, so
there is nothing to type: **that spike must reach 1.0.** Compare it with what
you wrote down in Round 1, Step 5.

**Then change tone 1's amplitude to 0.3 and watch the spike drop to 0.3.** A
chart that is quietly wrong can still look right at one setting; it rarely
survives being moved. This is the `EYES:` perturbation row from your own spec.

**First, look for a legend.** A correct chart here has **no legend at all** —
one line needs no key. If you see one listing `Time` or `Frequency (Hz)` beside
`Signal` or `Amplitude`, your chart is drawing the axis as a line instead of
using it as an axis, and there is no amplitude scale left to read.
`TROUBLESHOOTING.md` has the one-line fix. Every test still passes while this
is wrong, which is exactly why your spec had to carry an `EYES:` row.

**To read a value off the chart, hover over the spike.** These charts have no
printed data labels; the number appears in a tooltip under the pointer.

Commit again.

### If a gate is not working after 15 minutes, stop

Do not keep prompting. A long conversation makes an agent worse, not better.
Restore the reference version of whatever gate you are stuck at, read it, and
carry on:

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

Those files are a reference run — one time the agent did the job well, saved
so you can pick it up rather than start again. **This is not cheating and it
does not cost you marks.** Recognising a dead end and recovering from it is
the skill being assessed. Write down what the agent was doing wrong and what
you tried.

### Gate 5 — Ship (10 minutes)

| | |
|---|---|
| **Paste** | nothing — no prompt, no agent. This gate is all yours |
| **You need** | branch `main`, `git status --short` printing nothing, `28 passed` |
| **Check** | the public URL loads for someone who is not you |
| **You end with** | the same files, pushed to GitHub and live on the internet |

**Push first.** Streamlit Cloud builds from GitHub, not from wherever you are
working — anything you have not pushed does not exist as far as it is
concerned, and the most common failure here is deploying an empty repository.

```
git status --short     # must print nothing — anything listed is not going anywhere
git push
```

Then go to **https://share.streamlit.io**:

1. **Continue to sign-in** → sign in with GitHub.
2. **First time only:** you are creating a Streamlit Community Cloud account
   and granting it access to your repositories. Read the screen, then accept.
   This is the only account you make today.
3. **Create app** → **Deploy a public app from GitHub**.
4. Fill in three things and nothing else:
   - **Repository:** `your-username/your-repo`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. **Deploy**, then wait. Two to five minutes is normal, and sixty of us are
   building at the same time. The log scrolls while it installs; that is fine.
6. Post the public URL to the class channel.

Nothing in Lab 1 needs an API key, so this is as simple as deployment gets.
Your `requirements.txt` is at the top of the repository, which is where the
cloud looks, and the pinned versions install on every Python it offers.

**If it is not live by the end of the session, stop.** Push your code and
deploy at home. The code and your four `aidlc/` documents are the deliverable;
the URL is a bonus and nobody is marked down for someone else's build queue.

---

## Part 3 — Compare the two rounds, and read the reference (15 minutes)

**Everyone does this**, whether your own version worked or not.

First, put your two rounds side by side:

```
git diff round1 main -- core/ pages/
```

Look for two things specifically:

- **Where does the maths live?** Round 1 usually puts it inside the page
  file. Round 2's plan forced it into `core/spectrum.py`, where a test can
  reach it.
- **How many tones can it handle?** Round 1 often hardcodes exactly two.

Then study the reference implementation with your agent, following
`labs/EXPLAIN.md`.

If your app works: find one thing each version does better.

If it does not: this is where you get the content. Understanding code you did
not write, with an AI explaining it, is a real skill and the most common way
these tools are used at work.

Either way, put one thing you learned into your log.

---

## You are done when

- [ ] Two tones at 50 Hz and 120 Hz produce exactly two spikes, in those places
- [ ] A tone you set to amplitude 1.0 produces a spike that reaches **1.0**
- [ ] `.venv\Scripts\python.exe -m pytest tests/test_spectrum.py` reports **7 passed**
- [ ] Your app is live at a public URL
- [ ] You have run `git diff round1 main` and looked at it
- [ ] You have worked through `labs/EXPLAIN.md`
- [ ] Your log has the Round 1 number and the Round 2 number in it — and if
      Round 1 never drew a chart, "no number, it crashed" is the answer, and it
      counts

## If you finish early

- Add a third tone. Notice whether your Round 2 code makes that easy.
- Add random noise to the signal and watch a noise floor appear underneath
  the spikes. How much noise before you can no longer see the smaller tone?
- **Aliasing:** allow tone 1 above half the sampling rate. Set the sampling
  rate to 500 and tone 1 to 300 Hz. The spike appears at 200 Hz, not 300 —
  the frequency has "folded back". This is why sampling rate matters, and it
  is the single most important idea in digital signal processing.
- Export the spectrum as a CSV file.
