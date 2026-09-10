# Lab 3 — The Intake Desk

A café near campus takes orders by chat message. Nobody writes them the same
way. Somebody has to read all of them and type them into the till.

You are going to replace that somebody — twice. Once the way it was done before
language models, and once the way it is done now. The comparison is the lab.

Work in a **fresh copy of the template** — click "Use this template" again and
call it `lab3-practice`. Not in your own project: a failed experiment here
must not touch the app you demo in two hours.

**Two notes before you start.** Lab 3's tests have been hidden since Session 1
so that each lab shows you only its own red. Switch them on with `-m lab3`,
which every command below already does. And in a fresh copy, running
`.venv\Scripts\python.exe -m pytest` also reports Lab 1's spectrum tests
failing — you never built that module in *this* copy. Ignore those; every
command below names the tests that matter.

**Leave the gates off here.** A fresh copy of the template ships without the
Four Gates rules, and for this lab that is what you want: today is four short
checkpoints against code that already exists, not a project being designed
from nothing. Do not copy `.clinerules.gates` into place — your own project
is where the gates belong.

## Checkpoint 1 — The way it used to be (10 minutes)

`core/naive_parser.py` is already written for you. It is regular expressions and
hand-written rules — a reasonable twenty minutes of work by a competent
programmer. Run it against the ten real messages:

```
.venv\Scripts\python.exe -m pytest tests/test_naive_parser.py -v
```

Read the failures. Not the error messages — the **messages themselves**, in
`session3/inbox.json`. For each one it missed, work out what tripped it: a
quantity written as a word, a time written a way the pattern did not expect, a
second item hiding in a clause like "and my friend wants a matcha".

Now ask yourself the question the whole lab turns on: **how many more rules
would you need to get all ten?** And when the eleventh message arrives next
week, in a format nobody predicted, how many then?

That is why software like this mostly did not get built. It was not worth it.

## Checkpoint 2 — Ask a model, get a paragraph (15 minutes)

Implement `ask()` in `core/llm.py` — a plain question in, plain text out. The
prompt is in `labs/PROMPTS.md`.

Then ask it to read message 1 and tell you the order.

It will answer, and the answer will be **correct and completely useless**. You
get a sentence. Your till needs a customer, a list of items with quantities, and
a pickup time. There is no reliable way to get those out of a sentence — you are
back to writing a parser, only now for text that changes every time.

Write in your log what the model actually returned. You are about to fix it with
one argument.

## Checkpoint 3 — Ask for a shape, get data (25 minutes)

Implement `ask_structured()` in `core/llm.py`, then `extract_one()` in
`core/intake.py`. The difference is one thing: you hand the model a **schema** —
a description of the shape you want back — and it fills it in.

Run it on message 1. You get a dictionary. Your code can use it immediately.

Then two more things, and both matter:

**Constrain the vocabulary.** The schema says item names must come from
`session3/menu.md`. Without that, one message gives you "iced choc" and another
gives you "Iced Chocolate" and your till has two products. Production systems do
this constantly: give the model your list, and make it choose from it.

**Do the arithmetic yourself.** `order_total()` is plain Python, and it stays
that way. The model is superb at reading a message and hopeless at being trusted
with a sum. Extract with the model; calculate with code. That division is most
of the skill.

Now do all ten in a single request with `extract_batch()` and put them in a
table with totals.

**You are done when** ten messy messages have become ten rows you could hand to
a till, and you did not write a single regular expression.

## Checkpoint 4 — Now prove it, and plan for being wrong (15 minutes)

You have a machine that reads messages. You do not yet know how good it is.

`session3/answer_key.json` holds the ten correct answers. Run `score()`:

```
.venv\Scripts\python.exe -m pytest -m live -v
```

Expect nine or ten of ten. When we measured it while building this lab it
scored ten out of ten on three runs in a row — which is a better result than
the rules parser managed on any message it had not been written for.

If it missed one, look at it and decide honestly: is that a bug, or is that
message genuinely ambiguous — the kind a human would also have to ask about?

Then wire up the last piece. The schema has a `needs_review` field, and the
model fills it when it is unsure. `needs_review()` collects those, plus anything
with a missing field or an impossible quantity, into a **queue for a human**.

That is the shape of every serious system built on a model: most of the work
automated, a minority escalated, and a person who only sees the hard ones. Not
"the AI does it". Not "the AI is unreliable so we do it by hand". Both, on
purpose.

**Your queue may come back empty, and that is worth noticing.** Running this
while building the lab, one run flagged the "my friend wants a matcha" message
and the next flagged nothing at all — same code, same messages. The model
decides how sure it feels, and that decision moves between runs. A flagged
order that turns out fine costs somebody one glance. A wrong order that sails
through costs a customer. Which error would you rather your queue made?

**Read the reasons, not just the count.** When we ran this while writing the
lab, the model scored ten out of ten and still stopped three orders:

| order | why it stopped |
|---|---|
| msg-04 | "Assumed *iced choc* refers to Iced Chocolate" |
| msg-06 | "Customer requested **no sugar** for the cappuccino" |
| msg-07 | "Customer specified **hot** for Americano" |

Look at what those last two actually are. Nothing was got wrong — "no sugar"
and "hot" are real things the customer asked for, and **your schema has nowhere
to put them.** They were silently dropped, and the only reason you know is that
the model said so.

And the note does not catch everything. Ask it for *"two flat whites and a
brownie for Nok, 4pm, oat milk if you have it"* and it correctly refuses to
invent a menu item — `needs_review: true`, *"Flat white is not on the menu"* —
but says nothing at all about the oat milk. Two things were dropped and one was
reported. **The flag is a courtesy, not a guarantee.**

That is the sharpest thing in this lab, so sit with it: **your schema decides
what your business is able to remember.** Anything outside it disappears
without a trace. Add a `notes` field for the customer's own words and you keep
it; leave it out and every "no sugar" in your inbox is lost, quietly, forever.
Real intake systems are mostly arguments about exactly this.

**Run the live tests twice.** The wording moves between runs though your code
did not change. That is why you assert on the customer and the quantities, never
on the sentence.

## Part 2 — Transfer it to your project (20 minutes)

Optional, and strongly encouraged. Every brief has an AI feature waiting, and
every one of them is this lab wearing different clothes:

| Your brief | The messy input | The shape you want back |
|---|---|---|
| Carpool | "anyone driving to the remote campus Friday morning?" | date, time window |
| Sessions | "physics cramming thurs after lab, maybe 5ish, library 3rd floor" | subject, date, start, end, place |
| Tutoring | "im ok at calc 2 and circuits, terrible at EM" | offers[], requests[] |
| Roommates | "night owl, pretty tidy, headphones always on, freezing AC" | sleep_hour, tidiness, noise, ac |
| Bills | a pasted delivery receipt | items[], amounts, who shares |

Copy `core/llm.py` into your project — the slot has been sitting empty since
Session 1 for exactly this — write your own schema, and wire it to one page.

**If time runs out, stop and demo what works.** A working project without an AI
feature beats a broken one with it, and it always will.

## You are done when

- [ ] You can say what the naive parser got wrong, and why
- [ ] Ten messages become ten rows with totals your code computed
- [ ] You have scored yourself against the answer key
- [ ] Records the model was unsure about are separated for a human
- [ ] You ran the live tests twice and saw the wording change

## If a checkpoint defeats you

Fifteen minutes, then take the reference and move on — the later checkpoints are
the more interesting ones:

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
| 2 or 3 | `git checkout reference/solution/lab3 -- core/llm.py` |
| 3 | `git checkout reference/solution/lab3 -- core/intake.py` |
| The page | `git checkout reference/solution/lab3 -- pages/9_Intake_Desk.py` |

Then read what you took. Reading working code you did not write is the same
skill you practised in Lab 1, and it is most of the job.

## If you finish early

- **Give it a price list it has not memorised.** Ask "how much for two lattes
  and a brownie?" — the model does not know your prices. Retrieve `menu.md`,
  put it in the prompt, and answer with the real number. That is retrieval, and
  it is how models are made to answer about things they were never trained on.
- **Order in Thai.** The messages in the inbox are English, and the model was
  never told to expect anything else. Try `ลาเต้ร้อน 20 แก้ว, มิค, 1pm` and see
  how far it gets - name, quantity and time included.
- **Order something the menu nearly has.** When we first wrote this lab the
  menu had Iced Latte but no hot Latte, so a hot latte came back as `Iced
  Latte` - the right word, the wrong drink, twenty times over. The model did
  flag it, but the row in the table looked like any other. Two lessons in one
  bug: your vocabulary list is a product decision, and a warning nobody sees is
  not a warning.
- **Break it on purpose.** Write a message so ambiguous that a human would have
  to ask. Does the model flag it, or guess confidently? Which would you rather
  ship?
- **Fix the dropped information.** The system currently drops anything it
  cannot match and mentions it only in `note`, as a sentence. Add an
  `unmatched` field to `ORDER_SCHEMA` - a list of the customer's own words for
  whatever did not make it - and instruct the model to fill it. Now ask for a
  flat white with oat milk and read the row. Two things change: staff can ring
  the customer back and offer a Latte, and you can count how often people ask
  for mocha, which is the number that tells you what to add to the menu. You
  have just had the argument every real intake system has, and it cost you one
  field.
- **Count the cost.** Ten messages in one request: how many tokens? What would
  ten thousand messages cost? That number is why businesses care.
