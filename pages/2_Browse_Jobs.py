"""Browse the board. The count and the list must always agree."""

from datetime import date

import streamlit as st

from core.board import active_jobs, load_jobs, search

DATA = "data/jobs.json"
LOCATIONS = ["Anywhere", "Ratchathewi", "Phaya Thai", "Chatuchak", "Bang Sue", "Online"]

st.title("Browse jobs")

where = st.selectbox("Where?", LOCATIONS)
least = st.number_input("Paying at least (baht)", min_value=0, step=50, value=0)
# The board as of a date you choose. Set it forward and watch jobs close:
# that is the expiry rule working, and it is why is_active takes today as an
# argument instead of reading the clock.
viewing = st.date_input("Board as of", value=date.today())

# Worked out ONCE. The heading below and the list below it read this same
# variable, so they cannot disagree. Filter twice and they will: the heading
# says twelve, the list shows nine, and neither one looks wrong on its own.
showing = search(
    active_jobs(load_jobs(DATA), viewing),
    location=None if where == "Anywhere" else where,
    min_budget=least or None,
)

st.subheader(f"{len(showing)} jobs available")

for job in showing:
    with st.container(border=True):
        st.markdown(f"**{job['title']}**")
        st.caption(
            f"{job['location']} · {job['budget']} baht · open until {job['expires']}"
        )
        st.write(job["contact"])

if not showing:
    st.info("Nothing matches. Widen the search, or move the date back.")
