"""What the rules-and-regular-expressions parser actually manages on the real inbox.

These tests do not check that the parser is good. They pin down how good it
is, so that the number stops being an opinion. It is deliberately not compared
against core.intake here - the rules parser ships finished, and its tests
should pass on day one whether or not the model half has been built yet.
"""

import json
from pathlib import Path

from core.naive_parser import parse, parse_all

SESSION3 = Path(__file__).resolve().parent.parent / "session3"
INBOX = json.loads((SESSION3 / "inbox.json").read_text(encoding="utf-8"))
ANSWER_KEY = json.loads((SESSION3 / "answer_key.json").read_text(encoding="utf-8"))


def _matches(parsed: dict | None, expected: dict) -> bool:
    """True when the parsed order has the right customer, items and pickup."""
    if parsed is None:
        return False
    same_items = sorted(
        (i["name"], i["qty"]) for i in parsed["items"]
    ) == sorted((i["name"], i["qty"]) for i in expected["items"])
    return (
        parsed["customer"].strip().lower() == expected["customer"].strip().lower()
        and same_items
        and parsed["pickup"] == expected["pickup"]
    )


def test_the_rules_get_four_of_the_ten_messages_fully_right():
    # Four. That number is the point of Lab 3: this is a genuine, careful
    # regular-expression parser, and on ten ordinary café messages it is
    # wrong more often than it is right. The model version scores 8 or more
    # and took five lines to write.
    results = parse_all(INBOX)
    correct = [
        row["id"]
        for row, expected in zip(results, ANSWER_KEY)
        if _matches(row["parsed"], expected)
    ]
    assert len(correct) == 4
    assert correct == ["msg-01", "msg-02", "msg-05", "msg-10"]


def test_it_gives_up_completely_when_the_quantity_is_a_word():
    # "one green tea latte" - the rules look for a digit next to an item name,
    # and "one" is not a digit. No items found means nothing to return at all.
    assert parse("Nong here. one green tea latte pls. i'll come by after 4") is None


def test_it_misses_an_item_whose_quantity_is_only_implied():
    # "my friend wants a matcha" is an order for one matcha to any human
    # reader. There is no number in it, so the rules never see it. The
    # cappuccino, which does have a number, comes through fine.
    parsed = parse(
        "hey! 1 cappuccino no sugar, and my friend wants a matcha. "
        "pickup around noon. this is Mint"
    )
    assert parsed["items"] == [{"name": "Cappuccino", "qty": 1}]
    assert parsed["pickup"] == ""  # "noon" is a word, not a time


def test_it_loses_a_name_that_arrives_without_a_label():
    # "iced choc x2, cheesecake x1, 15:45, Fai" - everything is right except
    # the name, because Fai did not write "name:" or a dash in front of it.
    parsed = parse("iced choc x2, cheesecake x1, 15:45, Fai")
    assert parsed["pickup"] == "15:45"
    assert parsed["customer"] == ""


def test_it_reads_the_easy_message_perfectly_well():
    # It is not useless. Digits in front of items, a plain time, a name after
    # a dash: this is the shape the rules were written for.
    assert parse("2 iced lattes and 1 croissant, pickup 3pm — Ploy") == {
        "customer": "Ploy",
        "items": [{"name": "Iced Latte", "qty": 2}, {"name": "Croissant", "qty": 1}],
        "pickup": "15:00",
    }


def test_parse_all_returns_one_row_per_message_keeping_the_ids():
    results = parse_all(INBOX)
    assert [row["id"] for row in results] == [m["id"] for m in INBOX]
    assert all("parsed" in row for row in results)
