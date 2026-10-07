# ============================================================
# app.py
# Main entry point for the Streamlit dashboard.
# Run with: streamlit run app.py
# ============================================================

import streamlit as st

from config import (
    APP_TITLE,
    APP_ICON,
    APP_VERSION,
)
from src.data_loader import (
    load_data,
    find_missing_columns,
    preview_dataframe,
)
from src.validation import run_all_checks
from src.data_cleaning import clean_data
from src.kpi import get_all_kpis, format_number


# ------------------------------------------------------------
# 1. PAGE SETUP
# ------------------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
)

st.title(f"{APP_ICON} {APP_TITLE}")
st.caption(f"Version {APP_VERSION} | Running on localhost")


# ------------------------------------------------------------
# 2. SIDEBAR - Data Source
# ------------------------------------------------------------
with st.sidebar:
    st.header("📂 Data Source")

    uploaded_file = st.file_uploader(
        "Upload a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="If you don't upload a file, the default dataset will be used.",
    )

    st.divider()
    st.caption("Navigate using the pages above ☝️")


# ------------------------------------------------------------
# 3. LOAD DATA
# ------------------------------------------------------------
df_raw, source_label = load_data(uploaded_file)

if df_raw is None:
    st.error("Could not load data. Please upload a valid file.")
    st.stop()

st.success(f"Data loaded successfully — {source_label}")


# ------------------------------------------------------------
# 4. VALIDATE DATA
# ------------------------------------------------------------
missing_cols = find_missing_columns(df_raw)

if missing_cols:
    st.error("❌ Invalid dataset — required columns are missing.")
    st.write("Missing columns:")
    for col in missing_cols:
        st.write(f"- {col}")
    st.stop()

report = run_all_checks(df_raw)

if not report["valid"]:
    st.error(f"Validation failed: {report['message']}")
    st.stop()


# ------------------------------------------------------------
# 5. CLEAN DATA
# ------------------------------------------------------------
df = clean_data(df_raw, verbose=False)

st.session_state["df"] = df
st.session_state["source_label"] = source_label


# ------------------------------------------------------------
# 6. KPI CARDS
# ------------------------------------------------------------
st.subheader("📊 Key Performance Indicators")

kpis = get_all_kpis(df)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Sales", format_number(kpis["total_sales"]))
col2.metric("Orders", f"{kpis['total_orders']:,}")
col3.metric("Customers", f"{kpis['total_customers']:,}")
col4.metric("Units Sold", f"{kpis['total_units']:,}")
col5.metric("Avg Order Value", format_number(kpis["average_order_value"]))
col6.metric("Median Order", format_number(kpis["median_order_value"]))


# ------------------------------------------------------------
# 7. DATA QUALITY SUMMARY
# ------------------------------------------------------------
st.divider()
st.subheader("🔍 Data Quality Snapshot")

q1, q2, q3, q4, q5 = st.columns(5)

q1.metric("Rows", f"{report['total_rows']:,}")
q2.metric("Duplicate Orders", report["duplicate_orders"])
q3.metric("Invalid Quantity", report["invalid_quantity_count"])
q4.metric("Invalid Price", report["invalid_price_count"])
q5.metric("Invalid Discount", report["invalid_discount_count"])


# ------------------------------------------------------------
# 8. DATA PREVIEW
# ------------------------------------------------------------
st.divider()
st.subheader("📋 Data Preview")
st.caption(f"Showing the first 10 rows of {len(df):,} cleaned records.")

st.dataframe(
    preview_dataframe(df, 10),
    width="stretch",
)


# ------------------------------------------------------------
# 9. FOOTER
# ------------------------------------------------------------
st.divider()
st.caption(
    "💡 Use the sidebar pages to explore Sales, Customers, Products, "
    "Statistics, and Data Quality."
)