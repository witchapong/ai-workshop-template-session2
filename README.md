# AI for Software Development — project template

This is the starting point for every lab and project in the workshop.

## Setup (about 10 minutes, at the start of every session)

Only one thing here survives from week to week. These are shared lab PCs, and
they get wiped between sessions, so everything after your GitHub account —
your clone, your `.env`, Cline's settings — has to be redone every time you
sit down at one, even if it is the same machine you used last week. Budget
the ten minutes for it each session. See "Leaving, and coming back" below for
what that means in practice, and message the class channel if any step fails
— do not wait until class, because sixty people cannot be unblocked at once.

1. **Create a GitHub account** at https://github.com/signup using a personal
   email address, if you do not already have one. This is the one step that
   only needs doing once, ever.
2. **Make your own copy of this project.** Click the green **Use this
   template** button at the top of this page, then **Create a new
   repository**. Give it any name. Set it to **Public**, and leave
   **"Include all branches"** switched **off** — you do not need the solution
   branches in your copy.
3. **Clone it and open it.** In VS Code's terminal:

   ```
   git clone <the URL of your new repository>
   ```

   then **File → Open Folder** on the folder it created.
4. **Create a virtual environment** — a private copy of Python and its
   packages just for this project, so it cannot clash with anything else
   already on the machine:

   ```
   py -3.14 -m venv .venv
   ```

   `py` is the Python launcher Windows installs alongside Python itself;
   `-3.14` pins exactly which version to use, even if the machine has others.
5. **Install the approved packages**, using the Python *inside* that new
   environment rather than activating it — activating can be blocked by this
   machine's security policy, and this form always works regardless:

   ```
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
6. **Copy in your key.**

   ```
   copy .env.example .env
   ```

   Open `.env`, replace the placeholder text after `ZAI_API_KEY=` with the
   key on the projector, save, and **close the tab** — a key on screen is a
   key shared, and you will be sharing this screen later.
7. **Seed the sample data**, so the app is not empty the first time you open
   it:

   ```
   New-Item -ItemType Directory -Force -Path data
   copy session2\jobs_seed.json data\jobs.json
   ```

   `data\` does not exist in a fresh clone — it is also where your own work
   will be saved later. `-Force` just means the first command will not
   complain if you ever run it again and the folder already exists.
8. **Check everything works.** In the terminal:

   ```
   .venv\Scripts\python.exe check_setup.py
   ```

   Keep fixing what it reports until it prints `ALL CHECKS PASSED`. Always
   name the interpreter like this inside a project — the venv you just built
   is never activated (see step 5), so a bare `python` either errors or
   silently runs some other Python with none of this project's packages.
9. **Point Cline at the model.** This is a *separate step* from `.env`, and
   skipping it is the most common way to arrive unable to work. `.env` is
   read by the *app* — `check_setup.py` today, and your own code later; Cline
   is a different program, with its own settings, that never looks at `.env`.

   - Click the **Cline icon** — the robot, near the bottom of the strip of
     icons down the far left. The icons are unlabelled; hover to check.
   - Cline opens on **"How will you use Cline?"**. It has already ticked
     **Absolutely Free** for you. **Do not take it.** Choose
     **Bring my own API key** — the free option signs you into Cline's own
     service and never touches the key you were just given.
   - API Provider **OpenAI Compatible** — **not "Z AI."** Cline's built-in Z
     AI provider has a fixed model dropdown that stops at `glm-5.2`; it does
     not offer `glm-5.3-flash`, even though the API genuinely serves it.
     OpenAI Compatible gives you a free-text Model ID field instead of a
     dropdown, and that is the only way to reach the model this course uses.
   - Base URL **`https://api.z.ai/api/coding/paas/v4`** — type this exactly.
     The similar-looking `/api/paas/v4` (no `coding`) is a different billing
     plan on the same key, and it rejects every request with an error that
     reads like a billing problem when it is really the wrong address.
   - Model ID **`glm-5.3-flash`**, typed into the free-text field — do not go
     looking for it in a dropdown, this provider does not have one.
   - Paste the same key from the projector as the API Key.
   - Type **hello** at it and check you get a reply.

   > **Cline says `429`?** That is the whole room landing on the model at
   > once, not a problem with your key — measured against the real key at a
   > full room, about one request in five gets this. **Wait about ten
   > seconds and send it again.** Do not change anything.

## Leaving, and coming back

**Push before you leave.** Nothing on this machine is yours to come back to
— it is a shared lab PC and it gets wiped between sessions.

```
git add -A
git commit -m "done for today"
git push
```

Anything not pushed by the time you stand up does not exist next week.

**Next session, you start again from Step 3.** Your GitHub account (Step 1)
is the only thing that carries over. Clone your repository again, rebuild the
virtual environment, re-paste the key into `.env`, re-seed the sample data,
and repoint Cline at the model. None of that is optional and none of it is
skippable because you did it last week.

Two things worth knowing:

- **`.env` never survives even though your code does.** It is git-ignored on
  purpose — a key belongs in nobody's repository, and never in a public one —
  so `git push` never carries it, and you paste it in fresh every session
  regardless of what else changed.
- **This is the tradeoff for a machine that needs no signup and no billing,
  and behaves identically for sixty people in a row.** Nothing personal
  persists on it, so nothing personal is at risk for whoever sits down after
  you.

## What is in here

| Folder | What it is for |
|---|---|
| `aidlc/` | The four planning documents you fill in before writing code |
| `pages/` | One file per feature. Streamlit turns each one into a tab |
| `core/` | Shared code: your data shapes, saving and loading, AI calls |
| `tests/` | Automated checks that your code still works |
| `labs/` | Instructions and prompts for each lab session |

## Running your app

```
.venv\Scripts\python.exe -m streamlit run app.py
```

A browser tab opens automatically at `http://localhost:8501`. If it does not,
copy that address out of the terminal yourself and paste it into a browser.

## Running your tests

```
.venv\Scripts\python.exe -m pytest
```

## Something is broken

See `TROUBLESHOOTING.md`. Give it a real try for ten minutes before asking.
