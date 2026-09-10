"""Everything about the intake desk that can be checked without a network.

No API key, no waiting, no cost, and the same answer every time. The parts
that talk to the model are exercised with a fake client that hands back a
canned reply, so these tests still fail loudly if the schema stops being sent
or the reply stops being parsed. The live checks live in test_intake_eval.py.
"""

import copy
import json
from pathlib import Path

import pytest

from core.intake import (
    ORDER_SCHEMA,
    extract_batch,
    extract_one,
    load_menu,
    needs_review,
    order_total,
    score,
)

SESSION3 = Path(__file__).resolve().parent.parent / "session3"
MENU_PATH = SESSION3 / "menu.md"
ANSWER_KEY = json.loads((SESSION3 / "answer_key.json").read_text(encoding="utf-8"))

ONE_ORDER = {
    "customer": "Ploy",
    "items": [{"name": "Iced Latte", "qty": 2}, {"name": "Croissant", "qty": 1}],
    "pickup": "15:00",
    "needs_review": False,
    "note": "",
}


class FakeResponse:
    """Stands in for the object the real client returns."""

    def __init__(self, text: str):
        self.text = text


class FakeModels:
    def __init__(self, text: str):
        self._text = text
        self.calls = []

    def generate_content(self, model=None, contents=None, config=None):
        self.calls.append({"model": model, "contents": contents, "config": config})
        return FakeResponse(self._text)


class FakeClient:
    """Anything with .models.generate_content(...).text works. No network."""

    def __init__(self, text: str):
        self.models = FakeModels(text)
# Hidden until Session 3: see pytest.ini. Run these with `pytest -m lab3`.
pytestmark = pytest.mark.lab3



# --- the menu, read with plain Python ---------------------------------------


def test_the_menu_has_thirteen_items():
    menu = load_menu(MENU_PATH)
    assert len(menu) == 13


def test_an_iced_latte_costs_sixty_five_baht():
    menu = load_menu(MENU_PATH)
    assert menu["Iced Latte"] == 65.0
    # Hot and iced are different products at different prices. A cafe that
    # sells one sells the other, and a menu missing the hot one forces the
    # model to substitute.
    assert menu["Latte"] == 60.0


# --- the arithmetic, which the model never touches --------------------------


def test_a_known_order_adds_up():
    # 2 Iced Latte at 65 = 130, plus 1 Croissant at 55, is 185 baht.
    menu = load_menu(MENU_PATH)
    assert order_total(ONE_ORDER, menu) == 185.0


def test_an_item_that_is_not_on_the_menu_is_named_in_the_error():
    menu = load_menu(MENU_PATH)
    order = {"items": [{"name": "Unicorn Frappe", "qty": 1}]}
    with pytest.raises(ValueError, match="Unicorn Frappe"):
        order_total(order, menu)


# --- the scoring ------------------------------------------------------------


def test_the_answer_key_scores_ten_out_of_ten_against_itself():
    result = score(ANSWER_KEY, ANSWER_KEY)
    assert result["total"] == 10
    assert result["exact"] == 10
    assert result["by_field"] == {"customer": 10, "items": 10, "pickup": 10}
    assert result["wrong_ids"] == []


def test_a_wrong_quantity_is_caught():
    extracted = copy.deepcopy(ANSWER_KEY)
    extracted[0]["items"][0]["qty"] = 3  # Ploy ordered 2 iced lattes, not 3
    result = score(extracted, ANSWER_KEY)
    assert result["exact"] == 9
    assert result["by_field"]["items"] == 9
    assert result["wrong_ids"] == ["msg-01"]


def test_a_wrong_item_name_is_caught():
    extracted = copy.deepcopy(ANSWER_KEY)
    extracted[1]["items"][0]["name"] = "Espresso"  # Beam ordered Americano
    result = score(extracted, ANSWER_KEY)
    assert result["exact"] == 9
    assert result["by_field"]["items"] == 9
    assert result["wrong_ids"] == ["msg-02"]


def test_a_wrong_pickup_time_is_caught():
    extracted = copy.deepcopy(ANSWER_KEY)
    extracted[2]["pickup"] = "4:00"  # not the same string as "16:00"
    result = score(extracted, ANSWER_KEY)
    assert result["exact"] == 9
    assert result["by_field"]["pickup"] == 9
    assert result["wrong_ids"] == ["msg-03"]


def test_the_order_the_items_are_listed_in_does_not_matter():
    extracted = copy.deepcopy(ANSWER_KEY)
    extracted[0]["items"].reverse()  # croissant first, iced latte second
    result = score(extracted, ANSWER_KEY)
    assert result["exact"] == 10
    assert result["wrong_ids"] == []


def test_the_customer_name_is_compared_ignoring_case_and_spaces():
    extracted = copy.deepcopy(ANSWER_KEY)
    extracted[0]["customer"] = "  ploy "
    assert score(extracted, ANSWER_KEY)["exact"] == 10


def test_a_missing_record_counts_as_wrong_rather_than_crashing():
    result = score(ANSWER_KEY[:9], ANSWER_KEY)
    assert result["total"] == 10
    assert result["exact"] == 9
    assert result["wrong_ids"] == ["msg-10"]


# --- deciding what a human has to look at -----------------------------------


def test_a_record_the_model_flagged_itself_is_escalated():
    flagged = dict(ONE_ORDER, id="msg-01", needs_review=True, note="two possible times")
    assert needs_review([flagged]) == ["msg-01"]


def test_a_record_with_no_customer_is_escalated_even_if_the_model_was_happy():
    empty_name = dict(ONE_ORDER, id="msg-04", customer="")
    assert needs_review([empty_name]) == ["msg-04"]


def test_a_quantity_of_zero_is_escalated():
    zero = dict(ONE_ORDER, id="msg-07", items=[{"name": "Croissant", "qty": 0}])
    assert needs_review([zero]) == ["msg-07"]


def test_a_clean_record_is_left_alone_and_ids_fall_back_to_position():
    # No "id" key on these, so needs_review numbers them the way inbox.json
    # does: the second record is msg-02.
    broken = dict(ONE_ORDER, pickup="")
    assert needs_review([ONE_ORDER, broken]) == ["msg-02"]


# --- the two calls that would talk to a model -------------------------------


def test_extract_one_sends_the_schema_and_parses_the_reply():
    client = FakeClient(json.dumps(ONE_ORDER))
    order = extract_one("2 iced lattes and 1 croissant, 3pm — Ploy", ["Iced Latte"], client)

    assert isinstance(order, dict)
    assert order["customer"] == "Ploy"
    assert order["items"][0]["qty"] == 2

    call = client.models.calls[0]
    assert call["config"]["response_schema"] == ORDER_SCHEMA
    assert call["config"]["response_mime_type"] == "application/json"
    assert "Iced Latte" in call["contents"]  # the menu names went with the question


def test_extract_batch_asks_once_for_all_the_messages():
    client = FakeClient(json.dumps([ONE_ORDER, dict(ONE_ORDER, customer="Beam")]))
    orders = extract_batch(["first message", "second message"], ["Iced Latte"], client)

    assert [o["customer"] for o in orders] == ["Ploy", "Beam"]
    assert len(client.models.calls) == 1  # one request, not one per message

    call = client.models.calls[0]
    assert call["config"]["response_schema"] == {"type": "array", "items": ORDER_SCHEMA}
    assert "first message" in call["contents"]
    assert "second message" in call["contents"]


def test_a_reply_that_is_not_json_gives_a_readable_error():
    client = FakeClient("Sorry, I cannot help with that.")
    with pytest.raises(ValueError, match="did not return valid JSON"):
        extract_one("anything", ["Iced Latte"], client)
