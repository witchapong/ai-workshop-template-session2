"""The way this was done before language models.

Regular expressions, hand-written rules, and a long list of things it cannot
handle. Run it, read what it gets wrong, and keep the failures in mind - you
are about to replace it with five lines.

Nothing here is sabotaged. This is roughly what a careful person writes in
twenty minutes, and it is roughly how far twenty minutes gets you: it reads
"2 iced lattes" and "iced choc x2" fine, and falls over on "one green tea
latte", on "my friend wants a matcha", and on a name that arrives with no
label in front of it.
"""

import re

# Every spelling a customer might use, pointing at the one spelling the menu
# uses. Every new way of writing an item means another line in this dictionary.
# That is the whole problem with the rules approach, visible in one place.
ALIASES = {
    "espresso": "Espresso",
    "espressos": "Espresso",
    "americano": "Americano",
    "americanos": "Americano",
    "cappuccino": "Cappuccino",
    "cappuccinos": "Cappuccino",
    "iced latte": "Iced Latte",
    "iced lattes": "Iced Latte",
    "green tea latte": "Green Tea Latte",
    "green tea lattes": "Green Tea Latte",
    "matcha": "Matcha",
    "thai tea": "Thai Tea",
    "black coffee": "Black Coffee",
    "iced chocolate": "Iced Chocolate",
    "iced choc": "Iced Chocolate",
    "croissant": "Croissant",
    "croissants": "Croissant",
    "cheesecake": "Cheesecake",
    "cheesecakes": "Cheesecake",
    "brownie": "Brownie",
    "brownies": "Brownie",
}

# Longest alias first, so "iced chocolate" is matched before "iced choc" gets
# a chance, and "espressos" before "espresso".
_ITEM = re.compile(
    r"\b(" + "|".join(re.escape(a) for a in sorted(ALIASES, key=len, reverse=True)) + r")\b"
)

# "2 iced lattes" - a number sitting just before the item name.
_QTY_BEFORE = re.compile(r"(\d+)\s*$")
# "iced choc x2" and "croissant 3" - a number just after it.
_QTY_AFTER = re.compile(r"^\s*(?:x\s*)?(\d+)\b")

# "15:45", "2.30pm" - an hour, a separator, then minutes.
_TIME_WITH_MINUTES = re.compile(r"\b(\d{1,2})[:.](\d{2})\s*(am|pm)?", re.IGNORECASE)
# "3pm", "5 pm", "9am" - an hour with am or pm and nothing else.
_TIME_HOUR_ONLY = re.compile(r"\b(\d{1,2})\s*(am|pm)\b", re.IGNORECASE)

# "name is Beam", "name: Wan", "name Ryan".
_NAME_LABEL = re.compile(r"\bname\s*(?:is\b|[:=])?\s*([A-Za-z]+)", re.IGNORECASE)
# "-- Tim" or "— Ploy" at the very end of the message.
_NAME_AFTER_DASH = re.compile(r"[-–—]{1,2}\s*([A-Za-z]+)\s*[.!]?\s*$")


def _find_items(text: str) -> list[dict]:
    """Every menu item mentioned, with the number written next to it.

    An item only counts if a digit is sitting on one side of it. "one green
    tea latte" and "a matcha" are therefore invisible to this function, which
    is exactly the kind of hole rules leave behind.
    """
    found: dict[str, int] = {}
    for match in _ITEM.finditer(text):
        before = _QTY_BEFORE.search(text[: match.start()])
        after = _QTY_AFTER.match(text[match.end() :])
        if before:
            qty = int(before.group(1))
        elif after:
            qty = int(after.group(1))
        else:
            continue
        canonical = ALIASES[match.group(1)]
        found[canonical] = found.get(canonical, 0) + qty
    return [{"name": name, "qty": qty} for name, qty in found.items()]


def _to_24_hour(hour: int, minute: int, meridiem: str | None) -> str | None:
    """Turn 3 pm into "15:00". Returns None if the numbers are not a real time."""
    if meridiem:
        meridiem = meridiem.lower()
        if hour == 12:
            hour = 0
        if meridiem == "pm":
            hour += 12
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return f"{hour:02d}:{minute:02d}"


def _find_pickup(text: str) -> str:
    """The pickup time as "HH:MM" on a 24-hour clock, or "" if there is none."""
    match = _TIME_WITH_MINUTES.search(text)
    if match:
        found = _to_24_hour(int(match.group(1)), int(match.group(2)), match.group(3))
        if found:
            return found
    match = _TIME_HOUR_ONLY.search(text)
    if match:
        found = _to_24_hour(int(match.group(1)), 0, match.group(2))
        if found:
            return found
    return ""


def _find_customer(text: str) -> str:
    """The customer's name, or "" when it is not announced by a label or a dash."""
    match = _NAME_LABEL.search(text)
    if match:
        return match.group(1)
    match = _NAME_AFTER_DASH.search(text.strip())
    if match:
        return match.group(1)
    return ""


def parse(message: str) -> dict | None:
    """One chat message in, one order out - or None when the rules give up.

    The order has the same shape as a row in answer_key.json: a customer, a
    list of {name, qty} items, and a pickup time. Fields the rules could not
    find come back as empty strings, so you can see how far it got.
    """
    items = _find_items(message)
    if not items:
        return None
    return {
        "customer": _find_customer(message),
        "items": items,
        "pickup": _find_pickup(message),
    }


def parse_all(messages: list[dict]) -> list[dict]:
    """Run parse() over a whole inbox.

    messages is the list loaded from inbox.json - each one a dict with an
    "id" and a "text". Returns [{"id": ..., "parsed": <order or None>}].
    """
    return [{"id": m["id"], "parsed": parse(m["text"])} for m in messages]
