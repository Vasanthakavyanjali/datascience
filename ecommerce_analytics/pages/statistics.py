# ============================================================
# pages/statistics.py
# Descriptive stats, IQR outliers, correlation, covariance.
# ============================================================

import pandas as pd
import streamlit as st
import plotly.express as px

from src.page_utils import get_data
from src.statistics import (
    full_statistics,
    get_outlier_bounds,
    get_outlier_rows,
    get_correlation,
    get_covariance,
    interpret_correlation,
)


st.title("📐 Statistical Analysis")
st.caption("Descriptive statistics, outliers, and relationships.")

df = get_data()

# ---------- STATS TABLE ----------
st.subheader("Descriptive Statistics")

numeric_options = [c for c in ["sales", "quantity", "unit_price", "discount"]
                   if c in df.columns]

if not numeric_options:
    st.warning("No numeric columns found.")
    st.stop()

column = st.selectbox("Choose a column", numeric_options)
stats = full_statistics(df[column])

left, right = st.columns(2)

with left:
    st.write("**Basic**")
    st.write(f"Mean: {stats['mean']:,}")
    st.write(f"Median: {stats['median']:,}")
    st.write(f"Mode: {stats['mode']:,}")
    st.write(f"Min: {stats['min']:,}")
    st.write(f"Max: {stats['max']:,}")

with right:
    st.write("**Spread**")
    st.write(f"Variance: {stats['variance']:,}")
    st.write(f"Std Dev: {stats['std_dev']:,}")
    st.write(f"Q1: {stats['Q1']:,}")
    st.write(f"Q2 (median): {stats['Q2']:,}")
    st.write(f"Q3: {stats['Q3']:,}")
    st.write(f"IQR: {stats['IQR']:,}")

st.divider()

# ---------- HISTOGRAM ----------
st.subheader(f"Distribution of {column}")
fig = px.histogram(df, x=column, nbins=30)
st.plotly_chart(fig, width="stretch")

st.divider()

# ---------- OUTLIERS ----------
st.subheader("IQR Outlier Analysis")

lower, upper = get_outlier_bounds(df[column])
st.write(f"Lower bound: **{lower:,}**")
st.write(f"Upper bound: **{upper:,}**")
st.write(f"Outliers detected: **{stats['outlier_count']}**")

if stats["outlier_count"] > 0:
    st.warning(
        "⚠️ These are potential statistical outliers. "
        "They may be genuine bulk orders — investigate before deleting."
    )
    outliers = get_outlier_rows(df, column)
    st.dataframe(outliers.head(20), width="stretch")
else:
    st.success("No outliers detected.")

st.divider()

# ---------- CORRELATION ----------
st.subheader("Correlation & Covariance")

if len(numeric_options) >= 2:
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        x_var = st.selectbox("X variable", numeric_options, index=0)

    with col_b:
        y_var = st.selectbox(
            "Y variable",
            [c for c in numeric_options if c != x_var],
            index=0,
        )

    corr = get_correlation(df, x_var, y_var)
    cov = get_covariance(df, x_var, y_var)

    with col_c:
        st.metric("Correlation", f"{corr}")

    st.write(f"**Interpretation:** {interpret_correlation(corr)}")
    st.write(f"**Covariance:** {cov}")
    st.caption(
        "Correlation is a value between -1 and +1 that measures linear "
        "association. Covariance depends on units and is harder to compare."
    )

    # Try trendline if statsmodels is installed; otherwise plain scatter.
    try:
        fig = px.scatter(df, x=x_var, y=y_var, trendline="ols")
    except Exception:
        fig = px.scatter(df, x=x_var, y=y_var)
        st.info(
            "ℹ️ Trendline not shown because 'statsmodels' is not installed. "
            "Install it with: pip install statsmodels"
        )

    st.plotly_chart(fig, width="stretch")
else:
    st.info("Need at least two numeric columns for correlation.")

st.divider()

# ---------- DOWNLOAD ----------
st.subheader("⬇️ Download")

stats_df = pd.DataFrame({
    "metric": list(stats.keys()),
    "value": list(stats.values()),
})

csv_bytes = stats_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download statistical summary as CSV",
    data=csv_bytes,
    file_name="statistical_summary.csv",
    mime="text/csv",
)