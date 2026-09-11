"""The intake desk: messy chat messages in, clean order rows out.

The division of labour is the lesson. The model reads the language - it is the
only thing here that knows "iced choc" is an Iced Chocolate and that "after 4"
means 16:00. Everything you would be embarrassed to get wrong stays in plain
Python: the menu, the arithmetic, the scoring, and the decision about which
orders a human has to look at.
"""

from pathlib import Path

from core.llm import ask_structured

# The shape every extracted order comes back in. `name` must be one of the
# menu items, spelled exactly as menu.md spells it - that is what lets
# order_total() price the order without any guessing.
# What to do with something that is not on the menu is a policy decision, and
# this is ours: drop the line we cannot fulfil, keep the rest of the order, and
# flag it. We do NOT substitute a different product - twenty hot lattes turning
# into twenty iced ones is the kind of "helpful" a business cannot afford - and
# we do NOT reject the whole order, because "one flat white and one croissant"
# should still sell a croissant.
#
# It has a cost, and Lab 3 asks you to find it: the customer's own words are
# kept only in `note`, as prose. Nothing structured survives, so nobody can
# ring them back to offer a Latte, and nobody can count how often people ask
# for mocha - which is exactly the number that tells you what to put on the
# menu. The fix is a field, not a better prompt.
ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "customer": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "qty": {"type": "integer"},
                },
                "required": ["name", "qty"],
            },
        },
        "pickup": {"type": "string"},
        "needs_review": {"type": "boolean"},
        "note": {"type": "string"},
    },
    "required": ["customer", "items", "pickup", "needs_review", "note"],
}

REQUIRED_FIELDS = ("customer", "items", "pickup")


def load_menu(path) -> dict[str, float]:
    """Read menu.md and return {item name: price in baht}.

    No language model involved. The menu is a table, tables are easy, and
    every call you do not make is a call that cannot go wrong.
    """
    menu: dict[str, float] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        name, price = cells[0], cells[1]
        try:
            menu[name] = float(price)
        except ValueError:
            continue  # the header row and the ---- row land here
    return menu


def order_total(order: dict, menu: dict) -> float:
    """What the order costs, in baht.

    The model extracted the items; your code does the arithmetic. Models are
    good at reading and merely adequate at sums, and a café that is adequate
    at sums does not stay open.
    """
    total = 0.0
    for item in order.get("items") or []:
        name = item.get("name", "")
        if name not in menu:
            raise ValueError(f"{name!r} is not on the menu")
        total += menu[name] * int(item.get("qty", 0))
    return total


def _rules(menu_names: list[str]) -> str:
    """The instructions that go with every extraction request."""
    return (
        "You are the order desk of a small café. Turn each chat message into "
        "one order.\n"
        f"- name must be copied EXACTLY from this menu: {', '.join(menu_names)}. "
        "Never invent an item name.\n"
        "- qty is a whole number. Use 1 when the customer names an item without "
        "a number.\n"
        "- pickup is a 24-hour clock time written as HH:MM. 3pm is 15:00, "
        "noon is 12:00, 'after 4' in the afternoon is 16:00.\n"
        "- customer is the person's first name only, spelled as they wrote it.\n"
        "- needs_review is true when you had to guess, when something asked for "
        "is not on the menu, or when a time or a name is missing. Otherwise false.\n"
        "- note is one short sentence saying what you were unsure about, or an "
        "empty string when you were sure."
    )


def extract_one(message: str, menu_names: list[str], client=None) -> dict:
    """One message in, one order out.

    Returns {"customer", "items", "pickup", "needs_review", "note"}.
    """
    return ask_structured(
        _rules(menu_names) + "\n\nRead the message and fill in one order.",
        ORDER_SCHEMA,
        context=message,
        client=client,
    )


def extract_batch(messages: list[str], menu_names: list[str], client=None) -> list[dict]:
    """Every message in ONE request, in the order you gave them.

    Ten messages in one request instead of ten requests: one round trip
    instead of ten, one set of instructions paid for once instead of ten
    times. It is cheaper and it is faster, and the answers are no worse.
    """
    numbered = "\n".join(f"{i}. {text}" for i, text in enumerate(messages, start=1))
    orders = ask_structured(
        _rules(menu_names)
        + f"\n\nThere are {len(messages)} numbered messages. Return one order "
        "for each of them, in the same order as the numbering. Return exactly "
        f"{len(messages)} orders, even if a message is hard to read.",
        {"type": "array", "items": ORDER_SCHEMA},
        context=numbered,
        client=client,
    )
    if not isinstance(orders, list):
        raise ValueError(f"Expected a list of orders, got {type(orders).__name__}")
    return orders


def _same_items(left, right) -> bool:
    """True when two item lists hold the same things, in any order."""
    def bag(items):
        return sorted(
            (str(i.get("name", "")).strip(), int(i.get("qty", 0)))
            for i in (items or [])
        )

    return bag(left) == bag(right)


def score(extracted: list[dict], answer_key: list[dict]) -> dict:
    """Mark the extraction against the answer key. Plain Python, no model.

    Records are paired by position: the first extracted order is marked
    against the first row of the key. A field counts as right when

      customer  matches ignoring case and surrounding spaces,
      items     hold the same (name, qty) pairs in any order,
      pickup    matches exactly, character for character.

    Returns {"total", "exact", "by_field", "wrong_ids"} where "exact" is the
    number of records with all three fields right, and "wrong_ids" lists the
    ids where anything at all was wrong.
    """
    by_field = {"customer": 0, "items": 0, "pickup": 0}
    exact = 0
    wrong_ids = []
    for position, expected in enumerate(answer_key):
        got = extracted[position] if position < len(extracted) else None
        got = got or {}
        checks = {
            "customer": str(got.get("customer", "")).strip().lower()
            == str(expected.get("customer", "")).strip().lower(),
            "items": _same_items(got.get("items"), expected.get("items")),
            "pickup": str(got.get("pickup", "")) == str(expected.get("pickup", "")),
        }
        for field, correct in checks.items():
            by_field[field] += int(correct)
        if all(checks.values()):
            exact += 1
        else:
            wrong_ids.append(expected.get("id", f"msg-{position + 1:02d}"))
    return {
        "total": len(answer_key),
        "exact": exact,
        "by_field": by_field,
        "wrong_ids": wrong_ids,
    }


def needs_review(extracted: list[dict]) -> list[str]:
    """The ids a human has to look at before the café makes anything.

    Three reasons to escalate: the model said so itself, a field the kitchen
    needs came back empty, or a quantity that makes no sense. Ninety per cent
    handled automatically and ten per cent handed to a person is not a
    failure - that is what shipping looks like.

    Uses each record's "id" when it has one, otherwise its position in the
    list (msg-01, msg-02, ...), which is how inbox.json numbers them.
    """
    flagged = []
    for position, record in enumerate(extracted):
        record = record or {}
        record_id = record.get("id") or f"msg-{position + 1:02d}"
        if record.get("needs_review"):
            flagged.append(record_id)
            continue
        if any(not record.get(field) for field in REQUIRED_FIELDS):
            flagged.append(record_id)
            continue
        if any(int(item.get("qty", 0)) <= 0 for item in record["items"]):
            flagged.append(record_id)
    return flagged
