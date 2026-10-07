# ============================================================
# pages/data_quality.py
# Full validation report of the raw dataset.
# ============================================================

import streamlit as st

from src.data_loader import load_data
from src.validation import run_all_checks


st.title("🔍 Data Quality")
st.caption("Validation report on the raw dataset.")

uploaded = st.session_state.get("uploaded_file", None)
df_raw, source = load_data(uploaded)

if df_raw is None:
    st.error("Could not load data.")
    st.stop()

st.write(f"**Source:** {source}")

report = run_all_checks(df_raw)

st.divider()

# ---------- STATUS ----------
if report["valid"]:
    st.success(f"✅ {report['message']}")
else:
    st.error(f"❌ {report['message']}")
    st.write("Missing columns:", report["missing_columns"])
    st.stop()

# ---------- SUMMARY CARDS ----------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Rows", f"{report['total_rows']:,}")
c2.metric("Duplicate Orders", report["duplicate_orders"])
c3.metric("Invalid Quantity", report["invalid_quantity_count"])
c4.metric("Invalid Price", report["invalid_price_count"])
c5.metric("Invalid Discount", report["invalid_discount_count"])

st.divider()

# ---------- MISSING VALUES ----------
st.subheader("Missing Values")

missing = report["missing_values"]

if missing.empty:
    st.success("No missing values found.")
else:
    st.dataframe(missing, width="stretch")

st.divider()

# ---------- INVALID DATES ----------
st.subheader("Invalid Date Rows")
st.write(f"Count: **{report['invalid_date_count']}**")

if report["invalid_date_count"] > 0:
    st.warning(
        "These rows have an order_date that could not be parsed. "
        "They are excluded from the cleaned dataset."
    )

st.divider()
st.caption("Note: The cleaned dataset used elsewhere in the app has already "
           "handled most of these issues.")