# ============================================================
# pages/sales.py
# Sales analysis: trend, categories, regions, top months.
# ============================================================

import streamlit as st
import plotly.express as px

from src.page_utils import get_data
from src.sales_analysis import (
    sales_over_time,
    orders_over_time,
    sales_by_category,
    sales_by_region,
    monthly_sales,
)


st.title("📊 Sales Analysis")
st.caption("How are sales performing over time and across dimensions?")

df = get_data()

# ---------- FILTERS ----------
st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:
    period = st.selectbox(
        "Time grouping",
        options=["Daily", "Weekly", "Monthly"],
        index=2,
    )

with col2:
    if "category" in df.columns:
        categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
        selected_category = st.selectbox("Category", categories)
    else:
        selected_category = "All"

filtered = df.copy()
if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

period_map = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}
rule = period_map[period]

st.divider()

# ---------- SALES OVER TIME ----------
st.subheader(f"{period} Sales")
trend = sales_over_time(filtered, period=rule)
if not trend.empty:
    fig = px.line(trend, x="order_date", y="sales", markers=True)
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Not enough data.")

# ---------- ORDERS OVER TIME ----------
st.subheader(f"{period} Orders")
orders = orders_over_time(filtered, period=rule)
if not orders.empty:
    fig = px.bar(orders, x="order_date", y="orders")
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Not enough data.")

st.divider()

# ---------- CATEGORY + REGION ----------
left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    cat = sales_by_category(filtered)
    if not cat.empty:
        fig = px.bar(cat, x="category", y="sales", color="category")
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No data.")

with right:
    st.subheader("Sales by Region")
    reg = sales_by_region(filtered)
    if not reg.empty:
        fig = px.pie(reg, names="region", values="sales", hole=0.4)
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No data.")

st.divider()

# ---------- MONTHLY SUMMARY ----------
st.subheader("Sales by Month Name")
month = monthly_sales(filtered)
if not month.empty:
    fig = px.bar(month, x="order_month_name", y="sales")
    st.plotly_chart(fig, width="stretch")
else:
    st.info("No data.")

# ---------- DOWNLOAD ----------
st.divider()
st.subheader("⬇️ Download")

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data as CSV",
    data=csv,
    file_name="filtered_orders.csv",
    mime="text/csv",
)