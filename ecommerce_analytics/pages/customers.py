# ============================================================
# pages/customers.py
# Customer spending, top spenders, segmentation.
# ============================================================

import streamlit as st
import plotly.express as px

from src.page_utils import get_data
from src.customer_analysis import (
    customer_summary,
    segment_customers,
    segment_counts,
    top_customers,
)
from src.statistics import full_statistics


st.title("👥 Customer Analysis")
st.caption("Who are our customers and how much do they spend?")

df = get_data()

summary = customer_summary(df)

if summary.empty:
    st.warning("Not enough customer data.")
    st.stop()

# ---------- STATISTICS ----------
st.subheader("Customer Spending Statistics")
stats = full_statistics(summary["total_spend"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mean", f"₹{stats['mean']:,.0f}")
c2.metric("Median", f"₹{stats['median']:,.0f}")
c3.metric("Std Dev", f"₹{stats['std_dev']:,.0f}")
c4.metric("IQR", f"₹{stats['IQR']:,.0f}")

st.divider()

# ---------- TOP CUSTOMERS ----------
st.subheader("Top 10 Customers by Total Spend")

top = top_customers(summary, 10)
fig = px.bar(
    top,
    x="total_spend",
    y="customer_id",
    orientation="h",
    labels={"total_spend": "Total Spend (₹)", "customer_id": "Customer"},
)
fig.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, width="stretch")

st.divider()

# ---------- SEGMENTATION ----------
st.subheader("Customer Segments")
st.caption("Low = bottom 25% spenders · Medium = middle 50% · High = top 25%")

segmented = segment_customers(summary)
seg_counts = segment_counts(segmented)

if not seg_counts.empty:
    left, right = st.columns(2)

    with left:
        fig = px.pie(
            seg_counts,
            names="segment",
            values="customers",
            hole=0.4,
            title="Customers per Segment",
        )
        st.plotly_chart(fig, width="stretch")

    with right:
        fig = px.bar(
            seg_counts,
            x="segment",
            y="total_spend",
            color="segment",
            title="Spend per Segment",
        )
        st.plotly_chart(fig, width="stretch")

    st.dataframe(seg_counts, width="stretch")
else:
    st.info("Not enough customers to segment.")

st.divider()

# ---------- DOWNLOAD ----------
st.subheader("⬇️ Download")
csv = segmented.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download customer summary as CSV",
    data=csv,
    file_name="customer_summary.csv",
    mime="text/csv",
)