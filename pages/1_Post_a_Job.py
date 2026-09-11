"""Post a job. One form, five fields, one button."""

from datetime import date

import streamlit as st

from core.board import load_jobs, save_job

DATA = "data/jobs.json"
LOCATIONS = ["Ratchathewi", "Phaya Thai", "Chatuchak", "Bang Sue", "Online"]

st.title("Post a job")
st.caption("Say what you need doing, what it pays, and how long the offer stands.")

with st.form("post"):
    title = st.text_input("What needs doing?")
    location = st.selectbox("Where?", LOCATIONS)
    budget = st.number_input("Budget (baht)", min_value=0, step=50, value=500)
    expires = st.date_input("Open until", value=date.today())
    contact = st.text_input("How should people reach you?")
    submitted = st.form_submit_button("Post it")

if submitted:
    if not title.strip() or not contact.strip():
        st.error("A job needs a title and a way to contact you.")
    else:
        save_job(DATA, {
            "title": title.strip(),
            "location": location,
            "budget": int(budget),
            # str() turns a date into "2026-09-20" for storage. JSON has no
            # date type, so something has to do this, and here is the one
            # place that knows a date came from a date picker.
            "expires": str(expires),
            "contact": contact.strip(),
        })
        st.success(f"Posted. The board now holds {len(load_jobs(DATA))} jobs.")
