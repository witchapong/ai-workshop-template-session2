"""Lab 3 reference solution: ten messy chat orders, two ways of reading them."""

import json
from pathlib import Path

import streamlit as st

from core.intake import (
    extract_batch,
    extract_one,
    load_menu,
    needs_review,
    order_total,
    score,
)
from core.naive_parser import parse, parse_all

SESSION3 = Path(__file__).resolve().parent.parent / "session3"

st.set_page_config(page_title="Intake Desk", layout="wide")

st.title("Intake Desk")
st.caption("Ten messy messages in. Ten clean rows out.")

inbox = json.loads((SESSION3 / "inbox.json").read_text(encoding="utf-8"))
answer_key = json.loads((SESSION3 / "answer_key.json").read_text(encoding="utf-8"))
menu = load_menu(SESSION3 / "menu.md")


def price(order: dict) -> str:
    """The order's cost in baht, or a warning when an item is not on the menu."""
    try:
        return f"{order_total(order, menu):,.0f}"
    except ValueError:
        return "not on the menu"


def show(orders: list[dict], with_totals: bool) -> dict:
    """One row per message, a tick or a cross against the answer key, and the marks."""
    result = score(orders, answer_key)
    rows = []
    for message, order in zip(inbox, orders):
        items = order.get("items") or []
        row = {
            "": "✗" if message["id"] in result["wrong_ids"] else "✓",
            "id": message["id"],
            # The message sits beside what was read out of it, so the failures
            # are legible without cross-referencing a separate list.
            "the message": message["text"],
            "customer": order.get("customer", ""),
            "items": ", ".join(f"{i.get('qty')} x {i.get('name')}" for i in items),
            "pickup": order.get("pickup", ""),
        }
        if with_totals:
            row["total (baht)"] = price(order)
            # A flagged row used to look identical to a clean one here, with the
            # warning only in the section below. A twenty-cup substitution is
            # exactly the row you must not miss at a glance.
            row["?"] = "!" if order.get("needs_review") else ""
        rows.append(row)

    # Without explicit widths the message column eats the table and pushes the
    # extracted fields off the right edge - which hides the very comparison
    # this table exists to make.
    columns_config = {
        "": st.column_config.TextColumn(width="small"),
        "id": st.column_config.TextColumn(width="small"),
        "the message": st.column_config.TextColumn(width="large"),
        "customer": st.column_config.TextColumn(width="small"),
        "items": st.column_config.TextColumn(width="medium"),
        "pickup": st.column_config.TextColumn(width="small"),
    }
    if with_totals:
        columns_config["total (baht)"] = st.column_config.TextColumn(width="small")
        columns_config["?"] = st.column_config.TextColumn(
            "?", width="small", help="! means the model wants a human to look"
        )
    st.dataframe(rows, hide_index=True, width="stretch", column_config=columns_config)

    columns = st.columns(4)
    columns[0].metric("Fully correct", f"{result['exact']} / {result['total']}")
    for column, field in zip(columns[1:], ("customer", "items", "pickup")):
        column.metric(field.title(), f"{result['by_field'][field]} / {result['total']}")
    return result


way = st.radio(
    "How should the desk read the inbox?",
    ["The old way (rules)", "The new way (model)"],
    horizontal=True,
)

if way == "The old way (rules)":
    st.write(
        "Regular expressions and a hand-written alias list. Nothing here is "
        "sabotaged - this is what twenty careful minutes buys you."
    )
    show([row["parsed"] or {} for row in parse_all(inbox)], with_totals=False)
else:
    st.write("One request, every message. Five lines replace the whole rules file.")
    if st.button("Read the inbox", type="primary"):
        try:
            with st.spinner("Asking the model to read all ten messages..."):
                orders = extract_batch([m["text"] for m in inbox], sorted(menu))
            for order, message in zip(orders, inbox):
                order["id"] = message["id"]
            st.session_state["orders"] = orders
        except RuntimeError as error:
            # No key, or no key the app can see. Say so plainly - a traceback
            # here tells a student nothing they can act on.
            st.error(str(error))
        except Exception as error:  # noqa: BLE001 - students must see the real reason
            st.error(f"The model call failed: {error}")
            st.caption(
                "Rate limit? Wait a minute and try again. Anything else, check "
                "TROUBLESHOOTING.md."
            )

    orders = st.session_state.get("orders")
    if orders:
        show(orders, with_totals=True)
        st.divider()
        st.subheader("Needs a human")
        flagged = needs_review(orders)
        if not flagged:
            st.success("Nothing escalated. Every order went straight through.")
        else:
            st.warning(f"{len(flagged)} of {len(orders)} orders stopped here.")
            st.dataframe(
                [
                    {"id": o["id"], "why": o.get("note") or "a field came back empty"}
                    for o in orders
                    if o.get("id") in flagged
                ],
                hide_index=True,
                width="stretch",
            )

st.divider()

# --- Try your own -----------------------------------------------------------
# The ten messages in the inbox are fixed, and students quickly want to know
# what happens to a message the lab did not anticipate. Both readers run on it,
# so the comparison stays honest: whatever the model does, the rules are trying
# the same sentence.
st.subheader("Try your own message")
st.write(
    "Write an order the way a real customer would. Both readers get the same "
    "sentence."
)

SUGGESTIONS = {
    "A word instead of a number": "two flat whites and a brownie for Nok, 4pm",
    "A time nobody writes as a time": "one americano please, sometime before my 2pm lecture — Ton",
    "Something not on the menu": "3 bubble teas and a croissant, 1pm, Bee",
    "An order with a condition": "1 iced latte but oat milk if you have it, 3.30, May",
    "Ambiguous on purpose": "coffee for me and the same again for my friend, later this afternoon, Ploy",
}

pick = st.selectbox(
    "Start from an example, or write your own below",
    ["(write my own)"] + list(SUGGESTIONS),
)
default = "" if pick == "(write my own)" else SUGGESTIONS[pick]

# A form, not a bare text box and button. Streamlit commits a text_area when it
# loses focus, so with a plain button the first click after typing only commits
# the text and the button never fires - you have to click twice. Inside a form,
# submitting does both at once.
with st.form("custom-message"):
    message = st.text_area("The message", value=default, height=90, key=f"custom-{pick}")
    submitted = st.form_submit_button("Read this one")

if submitted and message.strip():
    left, right = st.columns(2)

    with left:
        st.markdown("**The old way (rules)**")
        rules_result = parse(message)
        if rules_result is None:
            st.warning("Could not parse it at all.")
        else:
            st.json(rules_result)

    with right:
        st.markdown("**The new way (model)**")
        try:
            with st.spinner("Asking the model..."):
                order = extract_one(message, sorted(menu))
            st.json(order)
            st.caption(f"Total: {price(order)} baht — computed in Python, not by the model")
            if needs_review([order]):
                st.warning(
                    f"Stopped for a human: {order.get('note') or 'a field came back empty'}"
                )
        except RuntimeError as error:
            st.error(str(error))
        except Exception as error:  # noqa: BLE001 - students must see the real reason
            st.error(f"The model call failed: {error}")

    st.caption(
        "Look for what the model had to drop. Anything your schema has no field "
        "for is gone, and the only warning you get is the note."
    )
