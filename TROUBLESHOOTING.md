# If something breaks

Work down this list. Each fix takes under two minutes. If you are still stuck
after ten minutes, ask a neighbour before asking the instructor — the person
next to you has probably hit the same thing.

## Setup

**`python : The term 'python' is not recognized as the name of a cmdlet,
function, script file, or operable program`**
Two different moments produce this, and they need different fixes.

- **Outside any project** — for example, typing `python --version` to check
  what is installed, or before a `.venv` exists at all — Windows registered
  the `py` launcher, not a bare `python` command. Use `py -3.14` instead.
- **Inside this project**, once a `.venv` already exists: the virtual
  environment is real, but it is never activated, on purpose (see the next
  entry). A bare `python` typed here either errors exactly like this, or —
  worse — silently runs some *other* Python that has none of this project's
  packages installed. Always name the interpreter directly instead:
  `.venv\Scripts\python.exe check_setup.py`.

**`.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is
disabled on this system`**
Do not activate the virtual environment — this machine's security policy
blocks the script that does it, and there is nothing you did wrong. Skip
activation entirely and call the interpreter directly instead:
`.venv\Scripts\python.exe -m pip install -r requirements.txt`,
`.venv\Scripts\python.exe check_setup.py`, and so on. This always works,
policy or no policy.

**`pytest : The term 'pytest' is not recognized...`**
The same cause as the second case above — the venv is never activated, so
bare `pytest` is not on `PATH` either. Use
`.venv\Scripts\python.exe -m pytest` for the whole suite, or name one file:
`.venv\Scripts\python.exe -m pytest tests\test_board.py -q`.

**`The token '&&' is not a valid statement separator in this version`**
This machine's PowerShell (5.1, the version Windows ships with) does not
support chaining two commands with `&&` the way a Mac terminal does. Run
them on two separate lines instead:

```
git add -A
git commit -m "what you did"
```

**`grep`, `tail`, or `pkill` is not recognized as the name of a cmdlet...**
These are Linux commands, and this is a Windows machine, so none of them
exist here. If you were following an old note or a video that used one: to
search inside a file, open it in VS Code and press `Ctrl+F` instead of
hunting for a command-line equivalent; to stop a stuck process, `Ctrl+C` in
its terminal or the trash-can icon on that terminal's tab does the job (see
"Cline has stopped responding," below).

**`check_setup.py` says a package is missing**
Run `.venv\Scripts\python.exe -m pip install -r requirements.txt`, then run
`.venv\Scripts\python.exe check_setup.py` again.

**`ModuleNotFoundError: streamlit`, even though `check_setup.py` said
packages were fine a minute ago**
The packages were installed into a *different* Python than the one now
running your code — usually because a plain `python` on this machine points
somewhere other than your `.venv`. Reinstall using the interpreter inside
your own environment: `.venv\Scripts\python.exe -m pip install -r
requirements.txt`.

**`check_setup.py` says your key was rejected, is busy, or could not be
reached**
Read the `[FAIL]` line itself first — it already names what to try:
reopening `.env` to check the whole key was pasted, waiting ten seconds and
running the check again, or trying a phone hotspot if campus wifi is the
problem. One thing it cannot tell you: this is the department's one key for
the whole class, not a personal one, so if it is genuinely rejected — not
just busy — you cannot fix it by making yourself a new one. Tell the
instructor.

**There is no `.env` file**
Run `copy .env.example .env` in the terminal, then paste your key in.

**Setup is failing and you can't tell why**
This only helps if Cline itself still responds. The provider, base URL, key,
and model have to already be working — Cline cannot fix Cline. If typing to
it does nothing, that is a different problem; see "The agent," below, first.

Otherwise, paste this whole block into Cline once and let it run every
remaining setup step for you:

```
Set up this project on Windows. Run these in PowerShell,
in order. Stop at the first failure and paste it.

  py -3.14 -m venv .venv
  .venv\Scripts\python.exe -m pip install `
      -r requirements.txt
  New-Item -ItemType Directory -Force -Path data
  copy session2\jobs_seed.json data\jobs.json
  .venv\Scripts\python.exe -m pytest -q

Do not touch .env — that one is mine. Do not edit any
file. Report pytest's last line.
```

It skips two steps on purpose. `.env` is untouched because `copy
.env.example .env` overwrites silently — if you already pasted your key,
Plan B would wipe it, and Plan B is exactly what you reach for after
something has already gone wrong. `check_setup.py` is skipped too: it makes
a live call to the model, and a Cline that is still responding already
proves the key works, so `pytest` — which proves the packages installed —
is the better signal here.

A correct run ends `10 failed, 28 passed, 25 deselected`. That is Lab 2's
normal starting point, not a broken install.

**`pytest` collects nothing, or says "no tests ran"**
You are in the wrong folder. `cd` to the folder that contains `app.py` —
usually the one your clone created — and run
`.venv\Scripts\python.exe -m pytest` again.

**`pytest` says some tests were "deselected"**
Deliberate, not broken. Later sessions' tests are hidden until you reach them,
so each lab shows you only its own failures. Session 3 switches its own on
with `.venv\Scripts\python.exe -m pytest -m lab3`.

**Browse Jobs is empty the first time I open it**
`session2/jobs_seed.json` has fixed dates, and by the time you run this some
or all of them may already have passed — a job past its own date reads as
closed and disappears from everyone's search but its poster's. Open
`session2/jobs_seed.json`, move each `expires` date forward past today, then
repeat the seed step from setup:

```
copy session2\jobs_seed.json data\jobs.json
```

This is aging sample data, not your code — nothing in `tests/test_board.py`
depends on this file at all.

**My chart has "Time" or "Frequency (Hz)" in its legend, and looks nothing
like a waveform**
Your chart is plotting the axis as data. `st.line_chart` given a dict of two
columns draws *both* of them as lines against the row number — so the axis you
meant becomes a diagonal line and there is no scale left to read a value off.
Name the axes explicitly:

```python
st.line_chart({"Time": times, "Signal": signal}, x="Time", y="Signal")
st.line_chart({"Frequency (Hz)": freqs, "Amplitude": mags},
              x="Frequency (Hz)", y="Amplitude")
```

Every test still passes while this is wrong, because no test opens a page.
The legend is the tell: a correct chart here has no legend at all.

`df.set_index("Frequency (Hz)")` also works, but it leaves the horizontal axis
with **no label** — numbers with no name or unit. Prefer `x=` and `y=`.

**Do I need to do all of this setup again next session?**
Yes, all of it, every time. These are shared lab machines, and they get
wiped between sessions — nothing survives that: not your clone, not `.env`,
not Cline's settings. Your code is not lost, though — it is on GitHub,
because you pushed it, and that is the one thing that actually is safe.

**I sat down today and none of yesterday's files are here**
That is expected on this machine, not broken — see the entry above.
`git clone` your repository again and repeat the setup steps in `README.md`.
Anything you pushed is exactly as you left it; anything you did not push is
gone, which is why committing and pushing before you stand up matters more
here than on a computer that remembers you.

**"Do you trust the authors of the files in this folder?"**
VS Code asks this the first time it opens any folder it has not seen before.
It is your own repository, made from the template. Click **Trust Folder &
Continue** — nothing works until you do.

**A popup about `python.terminal.useEnvFile` or "environment injection"**
Ignore it. It sounds like your key will not be read; it will. `check_setup.py`
and the app load `.env` themselves.

**I typed a message to Cline and it vanished**
If the panel is showing **Resume Task**, or a command still marked *Pending*,
Cline is not listening — anything you type is silently discarded. Resume or
cancel the pending thing first, then type. If it will not clear, reload the
window (see the next entry).

**Cline asks me to click Save more than once for one file**
Normal. Creating a file, then showing you the diff, then confirming, can each
want a click. Keep clicking Save until the panel moves on.

**My typing goes into the wrong pane**
The editor, the terminal and the app preview all take focus, and VS Code
hands it around between them. Close the preview tab when you are working in
the terminal, click into the terminal, and check the cursor is blinking there
before you type a command.

**The icons on the left strip moved**
They reorder between reloads and none of them are labelled. Hover before you
click — Cline is the robot.

**"Start New Task" does nothing and the old task stays on screen**
Cline will not start a new task while the old one has a command waiting for
approval or still marked *Running*. Approve or cancel whatever is pending
first. If that does not free it, reload the editor: **Ctrl+Shift+P** →
**Developer: Reload Window**. Your files are safe; check the model name at the
bottom of the Cline box afterwards, because a reload can reset it.

**`error: remote reference already exists`**
You already added it, earlier in this same lab — skip that line and run
`git fetch reference` on its own.

**`error: Your local changes would be overwritten by checkout`**
You have edits you have not committed, and git will not throw them away
silently. Commit them first:

```
git add -A
git commit -m "wip"
```

Then run your checkout again.

**My changes are not showing in the app**
Three things, in order. Is the browser tab pointing at the port the terminal
actually printed? Running the app a second time while the first is still
going lands on 8502, and your old tab is still watching 8501. Press
`Ctrl+C`, start it once, and open the URL it prints. If the port is right,
hit **R** in the app to rerun. If it is still wrong, you saved the file in a
different folder than the one you are running.

**My deployed app says it cannot find an API key, but it works on my
computer**
`.env` is git-ignored, so it was never pushed and the cloud has never seen it.
Open your app on Streamlit Cloud, go to **Settings → Secrets**, and paste the
same key lines that are in your `.env` (as `NAME = "value"`). Save; the app
restarts. This only affects apps that call a model — Lab 1's and Lab 2's do
not.

**Deploying to Streamlit Community Cloud failed, or is still building**
Builds take two to five minutes and everyone in the room is deploying at once,
so slow is normal. Check that you have **pushed** — the cloud builds from
GitHub, not from your PC — and that the main file is set to `app.py`.
If it has not finished by the end of the session, push your code and deploy
at home. The code and your four `aidlc/` documents are the deliverable; the
URL is a bonus.

## The agent

**glm-5.3-flash is not in Cline's model list**
Cline's built-in **Z AI** provider ships a fixed model dropdown that stops
at `glm-5.2` — it does not offer `glm-5.3-flash`, even though the API
genuinely serves it (it is right there in `/models`; Cline's UI just does
not show it). Do not pick "Z AI" from Cline's provider list. Use **OpenAI
Compatible** instead: it gives you a free-text Model ID field, so you type
`glm-5.3-flash` rather than choosing it from a list. The base URL and key
stay the same either way: `https://api.z.ai/api/coding/paas/v4` and the key
on the projector.

**Cline says the key is invalid, or that there is "insufficient balance"**
The base URL is almost certainly the pay-as-you-go one. It must be
`https://api.z.ai/api/coding/paas/v4` — note **`coding`** in the path. The
similar `/api/paas/v4` (no `coding`) accepts the same key and then refuses
every request with a message that reads like a billing problem; it is really
just the wrong address. Fix it in Cline's provider settings and try again.

**Cline says `429` or "rate limit exceeded"**
You are not doing anything wrong, and nothing about your key is broken. Fifty
of you are sharing one key, and Z.ai briefly bounces requests when a burst of
you type at once — measured against the real key at a full room, this happens
to roughly one request in five. **Wait about ten seconds and send it again.**

**Cline says `503`, "high demand", or "unavailable"**
Different from a `429`: the model itself is refusing everyone, and waiting ten
seconds will not help this one. You do not hold a spare key to switch to —
tell the instructor. They hold a backup for exactly this and will announce it
to the room if it is needed.

**Cline has stopped responding and one command says "Running" forever**
You asked it to run the app. A web server never exits, so the agent is
waiting for a command that will never finish. Click into that terminal and
press `Ctrl+C`; if that does not free it, click the trash-can icon on the
terminal's own tab to kill it outright. Start servers yourself; agents are
for changing files.

**I clicked "Start New Task" and my code vanished**
When Cline writes a file it shows a diff with **Save** and **Reject** buttons.
Until you click Save, that work only exists in the preview — and starting a new
task throws it away silently. Your tests will go back to failing with no
explanation. Always click **Save** first. If you lost work this way, the agent
has to redo it; there is no undo.

**I pasted into the wrong pane and wrecked a file**
`git checkout -- path/to/the/file.py` puts that one file back to your last
commit. This works for anything: your mistakes, the agent's, a bad paste. It
is why you commit every time the tests pass.

**Cline refuses to write code and keeps asking for `requirements.md`**
In Round 2 of Lab 1, and in Lab 2, that is correct behaviour and not a bug.
Fill in `aidlc/intent.md`, let it draft `aidlc/requirements.md`, read it, then
reply "approved".

If it happens in **Round 1** of Lab 1, the gates are on when they should be
off. Run `Move-Item .clinerules .clinerules.off` and start a new task.

**Cline writes code immediately and never asks me to approve anything**
The gates are off. You either skipped `copy .clinerules.gates .clinerules`, or
you ran it and a later `git checkout -- .` undid it because you did not
commit. Copy it again, commit it, and start a NEW Cline task — the rules are
read when a task begins, so the one already open is still using the old set.

**Cline rewrote a file and broke everything**
Do not panic and do not try to fix it by prompting. In the terminal:
`git checkout -- path/to/the/file.py` puts that file back to the last commit.
This is why you commit after every working step.

**The agent is going in circles on the same error**
Stop it. Start a NEW task instead of continuing the conversation — a long
conversation makes the agent worse, not better. Tell it what you already
tried.

**"Diff Edit Failed" keeps repeating**
The agent is trying to edit a file and cannot match the text it is looking
for. Stop it, start a new task, and ask it to rewrite the whole file in one
go rather than editing it.

## The app

**Running the app says "command not found", or `streamlit` is not recognized**
Three causes, roughly in order of how often they happen.

1. **Check the spelling.** It is `streamlit`, not `steamlit`. The missing "r"
   is the single most frequent typo in this workshop.
2. **Check you named the interpreter.** The venv is never activated (see
   Setup, above), so a bare `streamlit` is not on `PATH` either. Use
   `.venv\Scripts\python.exe -m streamlit run app.py` — always, not just
   when this happens.
3. If both of those are right, the packages did not install. Run
   `.venv\Scripts\python.exe -m pip install -r requirements.txt`, watch for
   errors, and if it fails, tell your instructor what the error said.

**The preview is blank, or a tab never opens**
Copy `http://localhost:8501` from the terminal yourself and paste it into a
browser — the automatic tab does not always appear.

**The page loads but spins forever and never finishes connecting**
A different problem from the one above: this is the network, not your code.
Streamlit's page needs a WebSocket connection to stay alive, and some campus
proxies allow the page to load while quietly blocking that connection —
which looks identical to a hang from where you are sitting. Report it to the
instructor rather than debugging your own files; there is nothing in `app.py`
that causes this.

**`ModuleNotFoundError: No module named 'core'`**
You are running from the wrong folder. Run `pwd`. You must be in the folder
that contains `app.py`.

**My page does not appear in the sidebar**
The file must be inside `pages/` and end in `.py`. Restart Streamlit.

**`TypeError: is_active() takes 1 positional argument but 2 were given`**
This is Lab 2's first trap: the agent wrote a version of `is_active` that
reads today's date itself instead of accepting it as an argument. Tell it
that `today` is a required second argument, always passed in, never read
from `date.today()`. `labs/LAB2.md` covers this one in full, as Trap 1.

## Git

**`git pull` says "no tracking information for the current branch"**
Your copy has lost track of where it came from. Fix it once with:
`git branch --set-upstream-to=origin/main main`

**I accidentally committed my `.env` file**
Tell the instructor immediately. This key is shared by the entire class, so
you cannot fix it yourself by generating a replacement — only the instructor
can rotate it, and they need to know it may be exposed as soon as possible.
Do not push again until they tell you to.
