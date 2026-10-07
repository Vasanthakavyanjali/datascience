# ============================================================
# src/page_utils.py
# Small helpers used by every page.
# ============================================================

import streamlit as st


def get_data():
    """
    Get the cleaned DataFrame from session_state.
    If missing, show a warning and stop the page.
    """
    df = st.session_state.get("df")

    if df is None or df.empty:
        st.warning("⚠️ Please load data on the Home page first.")
        st.stop()

    return df