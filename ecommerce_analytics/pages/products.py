# ============================================================
# pages/products.py
# Top products, low performers, category performance.
# ============================================================

import streamlit as st
import plotly.express as px

from src.page_utils import get_data
from src.product_analysis import (
    product_summary,
    top_products,
    low_performing_products,
    category_summary,
)


st.title("📦 Product Analysis")
st.caption("Which products drive revenue — and which lag behind?")

df = get_data()

products = product_summary(df)

if products.empty:
    st.warning("Not enough product data.")
    st.stop()

# ---------- TOP PRODUCTS ----------
st.subheader("Top 10 Products by Sales")

top = top_products(products, 10)
fig = px.bar(
    top,
    x="total_sales",
    y="product_name",
    orientation="h",
    labels={"total_sales": "Sales (₹)", "product_name": "Product"},
)
fig.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, width="stretch")

st.divider()

# ---------- LOW PERFORMERS ----------
st.subheader("Low Performing Products")
st.caption("These products contribute the least to revenue.")

low = low_performing_products(products, 10)
fig = px.bar(
    low,
    x="total_sales",
    y="product_name",
    orientation="h",
    color_discrete_sequence=["#d62728"],
    labels={"total_sales": "Sales (₹)", "product_name": "Product"},
)
fig.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, width="stretch")

st.divider()

# ---------- CATEGORY SUMMARY ----------
st.subheader("Category Performance")

cat = category_summary(df)
if not cat.empty:
    left, right = st.columns(2)

    with left:
        fig = px.bar(cat, x="category", y="total_sales", color="category")
        st.plotly_chart(fig, width="stretch")

    with right:
        fig = px.pie(cat, names="category", values="total_sales", hole=0.4)
        st.plotly_chart(fig, width="stretch")

    st.dataframe(cat, width="stretch")
else:
    st.info("No category data.")

st.divider()

# ---------- DOWNLOAD ----------
st.subheader("⬇️ Download")
csv = products.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download product summary as CSV",
    data=csv,
    file_name="product_summary.csv",
    mime="text/csv",
)