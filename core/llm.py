"""Where your app talks to a language model. You build this in Lab 3.

Two ways to ask:
  ask()            - question in, plain text out. Good for explanations.
  ask_structured() - question in, a fixed shape out. Good for anything your
                     code has to read afterwards.

Prefer ask_structured whenever another part of your program uses the answer.
Reading prose with code is guesswork; reading a known shape is not.
"""

import json
import os
from pathlib import Path

# Model names go stale and busy models refuse to answer, so try several rather
# than pinning one. Both failure modes were seen within three days in August
# 2026: a pinned model was retired for new accounts, and a "latest" alias came
# back with "high demand" while a pinned version answered fine. A list survives
# both. The first name that answers wins.
GEMINI_MODELS = ["gemini-flash-latest", "gemini-3.6-flash", "gemini-3.5-flash"]


def _default_client():
    """Build a Gemini client from the key in your .env file.

    Every function here takes a `client` argument. Leave it as None and you
    get this one. Pass your own - a fake, in a test - and no network call
    happens at all.
    """
    import logging

    from dotenv import load_dotenv
    from google import genai

    # Same SDK advice-warning check_setup.py silences; it clutters the terminal
    # students watch while Streamlit runs.
    logging.getLogger("google_genai").setLevel(logging.ERROR)

    # Streamlit does not read .env by itself. Without this the app reports
    # "no key" while .env sits right there with the key in it - which is
    # exactly what happened the first time this page was run.
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "No GEMINI_API_KEY found. Copy .env.example to .env, paste your key "
            "into GEMINI_API_KEY, then restart the app. "
            "Get one free at https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=key)


def _generate(client, prompt: str, config: dict | None = None) -> str:
    """Send one prompt, trying each model in GEMINI_MODELS until one answers.

    If they all fail you get the last error, not a tidied-up version of it -
    "that model was retired" and "you are out of free calls" need different
    fixes, and hiding the difference wastes your afternoon.
    """
    last_error = None
    for model in GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model, contents=prompt, config=config
            )
            return response.text
        except Exception as error:  # noqa: BLE001 - try the next model, keep the reason
            last_error = error
    raise last_error


def ask(question: str, context: str = "", client=None) -> str:
    """Ask a question in plain language and get plain text back."""
    client = client or _default_client()
    prompt = (
        "You are a careful assistant. Answer using ONLY the reference text "
        "below. If the answer is not in it, say plainly that you do not know. "
        "Do not fill gaps with what you happen to remember.\n\n"
        f"Reference text:\n{context}\n\n"
        f"Question: {question}"
    )
    return _generate(client, prompt)


def ask_structured(question: str, schema: dict, context: str = "", client=None) -> dict | list:
    """Ask a question and get the answer in the shape described by schema.

    schema is a JSON schema - a description of the shape you want back. The
    model is held to it, so you can read the answer with ordinary dictionary
    code instead of guessing your way through a paragraph.

    You normally get a dictionary back. If your schema asks for an array at the
    top level you get a list instead, because that is what you asked for.
    """
    client = client or _default_client()
    prompt = (
        "Extract the requested information from the reference text below. "
        "Use ONLY what is in the text.\n\n"
        f"Reference text:\n{context}\n\n"
        f"Task: {question}"
    )
    config = {"response_mime_type": "application/json", "response_schema": schema}
    raw = _generate(client, prompt, config)
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError(
            f"The model did not return valid JSON. It said: {raw!r}"
        ) from error
