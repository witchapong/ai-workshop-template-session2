r"""The live checks: a real request to a real model, marked so they stay opt-in.

Run them on their own, when you have a key in .env and a minute to spare:

    .venv\Scripts\python.exe -m pytest -m live

Then run them again. The wording of the notes will have changed, and possibly
which orders got flagged - the model is not a function, and the same input
does not guarantee the same output. That is why the thresholds below are "at
least 8 out of 10" rather than "exactly this answer": you test the behaviour
you need, not the sentence you happened to get on Tuesday.

One request is made for the whole file, not one per test.
"""

import json
from pathlib import Path

import pytest
from dotenv import load_dotenv

from core.intake import extract_batch, load_menu, needs_review, score

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SESSION3 = Path(__file__).resolve().parent.parent / "session3"
INBOX = json.loads((SESSION3 / "inbox.json").read_text(encoding="utf-8"))
ANSWER_KEY = json.loads((SESSION3 / "answer_key.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def extracted():
    """One real extraction of the whole inbox, shared by every test here."""
    menu = load_menu(SESSION3 / "menu.md")
    orders = extract_batch([m["text"] for m in INBOX], sorted(menu), client=None)
    for order, message in zip(orders, INBOX):
        order["id"] = message["id"]
    return orders
# Hidden until Session 3: see pytest.ini. Run these with `pytest -m lab3`.
pytestmark = pytest.mark.lab3



@pytest.mark.live
def test_the_model_reads_at_least_eight_of_the_ten_messages_perfectly(extracted):
    result = score(extracted, ANSWER_KEY)
    # Run with `pytest -m live -s` to watch this line change between runs.
    print(f"\nscore: {result['exact']}/10 exact, by field {result['by_field']}")
    assert result["total"] == 10
    assert result["exact"] >= 8, (
        f"only {result['exact']}/10 exact. Wrong: {result['wrong_ids']}. "
        f"By field: {result['by_field']}"
    )


@pytest.mark.live
def test_the_orders_sent_to_a_human_are_a_small_and_explained_minority(extracted):
    """The flags have to be worth acting on, not noise.

    Two things make them worth acting on. Most of the inbox has to go through
    untouched, or there is no automation left. And every order that does stop
    has to say why, so the person picking it up knows what to look at.

    An order that was flagged and turned out to be right is a false alarm, not
    a bug: the model said "the second drink here is only implied" and it was
    correct to be uneasy about it. A false alarm costs one glance. A wrong
    order that sailed through costs a customer.
    """
    result = score(extracted, ANSWER_KEY)
    flagged = needs_review(extracted)
    print(f"\nescalated: {flagged}, actually wrong: {result['wrong_ids']}")

    assert len(flagged) <= 4, f"escalated {len(flagged)} of 10 - that is not automation"
    for order in extracted:
        if order["id"] in flagged and order.get("customer") and order.get("pickup"):
            assert order.get("note"), f"{order['id']} was escalated without saying why"
