r"""Start here. Run the app with:  .venv\Scripts\python.exe -m streamlit run app.py

Streamlit turns every file in the pages/ folder into a tab automatically.
That is why one feature = one file in pages/ = one person's work.
"""

import streamlit as st

st.set_page_config(page_title="My Project", page_icon="*", layout="wide")

st.title("My Project")
st.write(
    "Replace this text with what your project does. "
    "Use the sidebar to move between features."
)
st.info("Each feature lives in its own file in the pages/ folder.")
