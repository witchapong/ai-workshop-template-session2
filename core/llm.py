"""Where your app talks to a language model.

YOU BUILD THIS. It is Lab 3.

The slot has been sitting here empty since Session 1 on purpose: when you add
an AI feature to your group project, it drops into a place that already exists
instead of needing the project rearranged around it.

Two ways to ask, and the difference is the whole lesson:

  ask()            question in, plain text out. Good for explaining to a human.
  ask_structured() question in, a shape you specified out. Good for anything
                   your code has to read afterwards.

Prefer ask_structured whenever another part of your program uses the answer.
Reading prose with code is guesswork; reading a known shape is not.
"""

TODO = "You build this in Lab 3. See labs/LAB3.md and labs/PROMPTS.md."

# Whatever you build here must call load_dotenv() before reading the key.
# check_setup.py does it for you; Streamlit does not, so an app that skips it
# reports "no key" even though .env is sitting right there. That exact bug hit
# us while writing this lab.

# Model names go stale and busy models refuse. Both happened within three days
# in August 2026: one model was retired for new accounts, and the alias adopted
# to survive that returned "high demand" while a pinned version answered fine.
# A list survives both. Try them in order.
GEMINI_MODELS = ["gemini-flash-latest", "gemini-3.6-flash", "gemini-3.5-flash"]


def ask(question: str, context: str = "", client=None) -> str:
    """Ask a question in plain language and get plain text back."""
    raise NotImplementedError(TODO)


def ask_structured(question: str, schema: dict, context: str = "", client=None) -> dict | list:
    """Ask a question and get the answer in the shape described by schema.

    A schema asking for an object gives you a dict; one asking for an array
    gives you a list. Lab 3 uses both.
    """
    raise NotImplementedError(TODO)
