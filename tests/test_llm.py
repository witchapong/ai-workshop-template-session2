"""The two ways to talk to a model, checked without talking to one.

Both functions take a `client`. Pass a fake and the whole thing runs offline,
instantly, for free - which is why every function in core/llm.py has that
argument in the first place.
"""

import json

import pytest

from core.llm import GEMINI_MODELS, ask, ask_structured


class FakeResponse:
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
    def __init__(self, text: str):
        self.models = FakeModels(text)
# Hidden until Session 3: see pytest.ini. Run these with `pytest -m lab3`.
pytestmark = pytest.mark.lab3



def test_ask_returns_the_plain_text_the_model_sent():
    client = FakeClient("A resistor limits current.")
    assert ask("What is a resistor?", client=client) == "A resistor limits current."


def test_ask_puts_the_context_and_the_question_in_the_prompt():
    client = FakeClient("ok")
    ask("What is the price?", context="An espresso costs 45 baht.", client=client)
    prompt = client.models.calls[0]["contents"]
    assert "An espresso costs 45 baht." in prompt
    assert "What is the price?" in prompt


def test_ask_uses_the_first_model_in_the_list():
    client = FakeClient("ok")
    ask("anything", client=client)
    assert client.models.calls[0]["model"] == GEMINI_MODELS[0]


def test_ask_structured_asks_for_json_in_the_shape_you_gave():
    schema = {"type": "object", "properties": {"answer": {"type": "string"}}}
    client = FakeClient(json.dumps({"answer": "45 baht"}))
    result = ask_structured("How much?", schema, context="45 baht", client=client)

    assert result == {"answer": "45 baht"}
    config = client.models.calls[0]["config"]
    assert config["response_mime_type"] == "application/json"
    assert config["response_schema"] == schema


def test_a_reply_that_is_not_json_raises_a_readable_error():
    client = FakeClient("I am afraid I cannot do that.")
    with pytest.raises(ValueError, match="did not return valid JSON"):
        ask_structured("How much?", {"type": "object"}, client=client)
