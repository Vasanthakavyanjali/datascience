# ============================================================
# pages/dashboard.py
# Management overview: KPIs, trends, top categories/regions.
# ============================================================

import streamlit as st
import plotly.express as px

from src.page_utils import get_data
from src.kpi import get_all_kpis, format_number
from src.sales_analysis import (
    sales_over_time,
    sales_by_category,
    sales_by_region,
)
from src.statistics import count_outliers


st.title("📈 Dashboard")
st.caption("How is the business performing?")

df = get_data()

# ---------- KPI ROW ----------
kpis = get_all_kpis(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", format_number(kpis["total_sales"]))
c2.metric("Orders", f"{kpis['total_orders']:,}")
c3.metric("Customers", f"{kpis['total_customers']:,}")
c4.metric("Avg Order Value", format_number(kpis["average_order_value"]))

st.divider()

# ---------- SALES TREND ----------
st.subheader("Sales Trend")
trend = sales_over_time(df, period="ME")

if not trend.empty:
    fig = px.line(
        trend,
        x="order_date",
        y="sales",
        markers=True,
        title="Monthly Sales",
    )
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Not enough data to plot a trend.")

st.divider()

# ---------- CATEGORY + REGION ----------
left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    cat = sales_by_category(df)
    if not cat.empty:
        fig = px.bar(cat, x="category", y="sales", color="category")
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No category data.")

with right:
    st.subheader("Sales by Region")
    reg = sales_by_region(df)
    if not reg.empty:
        fig = px.bar(reg, x="region", y="sales", color="region")
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No region data.")

st.divider()

# ---------- OUTLIER NOTE ----------
outliers = count_outliers(df["sales"]) if "sales" in df.columns else 0

if outliers > 0:
    st.warning(f"⚠️ {outliers} potential outlier order(s) detected. "
               "See Statistics page for details.")
else:
    st.success("✅ No statistical outliers detected in order values.")