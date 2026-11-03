# ============================================================
# src/insights.py
# Generates plain-English business insights from the data.
# Every insight is calculated - nothing is hard-coded.
# ============================================================

import pandas as pd

from src.kpi import (
    total_sales,
    total_orders,
    total_customers,
    average_order_value,
    median_order_value,
)
from src.statistics import (
    get_correlation,
    interpret_correlation,
    count_outliers,
)


# ------------------------------------------------------------
# HELPER: Format money in Lakhs
# ------------------------------------------------------------
def money(value):
    """Turns 2540000 into ₹25.40 L."""
    if value is None:
        return "₹0"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)

    if abs(value) >= 100000:
        return f"₹{value / 100000:.2f} L"
    return f"₹{value:,.0f}"


# ------------------------------------------------------------
# INSIGHT 1: Overall business snapshot
# ------------------------------------------------------------
def insight_overall(df):
    """One sentence summarizing the business."""
    if df is None or df.empty:
        return "No data available."

    sales = total_sales(df)
    orders = total_orders(df)
    customers = total_customers(df)

    return (
        f"The business recorded {money(sales)} in total sales "
        f"across {orders:,} orders from {customers:,} unique customers."
    )


# ------------------------------------------------------------
# INSIGHT 2: Top category
# ------------------------------------------------------------
def insight_top_category(df):
    """Which category brings the most sales."""
    if df is None or df.empty or "category" not in df.columns:
        return None

    grouped = df.groupby("category")["sales"].sum().sort_values(ascending=False)

    if grouped.empty:
        return None

    top_name = grouped.index[0]
    top_sales = grouped.iloc[0]
    total = grouped.sum()

    share = (top_sales / total * 100) if total > 0 else 0

    return (
        f"**{top_name}** is the top category with {money(top_sales)} in sales, "
        f"contributing {share:.1f}% of total revenue."
    )


# ------------------------------------------------------------
# INSIGHT 3: Top region
# ------------------------------------------------------------
def insight_top_region(df):
    """Which region brings the most sales."""
    if df is None or df.empty or "region" not in df.columns:
        return None

    grouped = df.groupby("region")["sales"].sum().sort_values(ascending=False)

    if grouped.empty:
        return None

    top_name = grouped.index[0]
    top_sales = grouped.iloc[0]

    return f"**{top_name}** region leads with {money(top_sales)} in sales."


# ------------------------------------------------------------
# INSIGHT 4: Weakest region
# ------------------------------------------------------------
def insight_weak_region(df):
    """Which region is underperforming."""
    if df is None or df.empty or "region" not in df.columns:
        return None

    grouped = df.groupby("region")["sales"].sum().sort_values()

    if grouped.empty or len(grouped) < 2:
        return None

    low_name = grouped.index[0]
    low_sales = grouped.iloc[0]

    return (
        f"**{low_name}** region shows the lowest sales at {money(low_sales)}. "
        f"Consider reviewing demand and distribution there."
    )


# ------------------------------------------------------------
# INSIGHT 5: Top product
# ------------------------------------------------------------
def insight_top_product(df):
    """Best-selling product by revenue."""
    if df is None or df.empty or "product_name" not in df.columns:
        return None

    grouped = df.groupby("product_name")["sales"].sum().sort_values(ascending=False)

    if grouped.empty:
        return None

    top_name = grouped.index[0]
    top_sales = grouped.iloc[0]

    return f"Top product by revenue is **{top_name}** ({money(top_sales)})."


# ------------------------------------------------------------
# INSIGHT 6: Outliers in sales
# ------------------------------------------------------------
def insight_outliers(df):
    """How many unusual transactions exist."""
    if df is None or df.empty or "sales" not in df.columns:
        return None

    count = count_outliers(df["sales"])
    total = len(df)

    if count == 0:
        return "No statistical outliers detected in order values."

    percent = (count / total * 100) if total > 0 else 0

    return (
        f"**{count} transaction(s)** ({percent:.1f}%) fall outside the normal "
        f"order-value range and may require investigation."
    )


# ------------------------------------------------------------
# INSIGHT 7: Discount vs Sales correlation
# ------------------------------------------------------------
def insight_discount_sales(df):
    """Relationship between discount and sales."""
    if df is None or df.empty:
        return None

    if "discount" not in df.columns or "sales" not in df.columns:
        return None

    corr = get_correlation(df, "discount", "sales")
    explanation = interpret_correlation(corr)

    return (
        f"Discount and sales show a correlation of **{corr}** "
        f"({explanation.lower()}) This does not prove that discount causes sales."
    )


# ------------------------------------------------------------
# INSIGHT 8: Average vs Median comparison
# ------------------------------------------------------------
def insight_avg_vs_median(df):
    """
    Compares average to median. A big gap means outliers exist.
    """
    if df is None or df.empty:
        return None

    avg = average_order_value(df)
    med = median_order_value(df)

    if med == 0:
        return None

    ratio = avg / med

    if ratio > 1.3:
        return (
            f"Average order value ({money(avg)}) is much higher than the median "
            f"({money(med)}). A few very large orders are pulling the average up."
        )
    elif ratio < 0.8:
        return (
            f"Average order value ({money(avg)}) is lower than the median "
            f"({money(med)}). Small orders are more common."
        )
    else:
        return (
            f"Average and median order values are close "
            f"({money(avg)} vs {money(med)}), suggesting consistent spending."
        )


# ------------------------------------------------------------
# MASTER FUNCTION: Collect all insights
# ------------------------------------------------------------
def generate_insights(df):
    """
    Runs all insight functions and returns a list of strings.
    Only includes insights that are not None.
    """
    if df is None or df.empty:
        return ["No data available to generate insights."]

    insights = [
        insight_overall(df),
        insight_top_category(df),
        insight_top_region(df),
        insight_weak_region(df),
        insight_top_product(df),
        insight_avg_vs_median(df),
        insight_outliers(df),
        insight_discount_sales(df),
    ]

    # Remove any None values
    return [i for i in insights if i]


# ------------------------------------------------------------
# RECOMMENDATIONS (simple, safe wording)
# ------------------------------------------------------------
def generate_recommendations(df):
    """
    Suggests next steps based on the data.
    Wording is careful - no absolute claims.
    """
    if df is None or df.empty:
        return ["No data available."]

    recommendations = []

    # 1. Category check
    if "category" in df.columns:
        grouped = df.groupby("category")["sales"].sum().sort_values(ascending=False)
        if len(grouped) >= 2:
            top = grouped.index[0]
            recommendations.append(
                f"Review inventory levels for **{top}** to ensure top-selling "
                f"products stay in stock."
            )

    # 2. Region check
    if "region" in df.columns:
        grouped = df.groupby("region")["sales"].sum().sort_values()
        if len(grouped) >= 2:
            low = grouped.index[0]
            recommendations.append(
                f"Investigate the low sales in **{low}** region — could be pricing, "
                f"distribution, or local demand."
            )

    # 3. Outlier check
    if "sales" in df.columns:
        count = count_outliers(df["sales"])
        if count > 0:
            recommendations.append(
                f"Review the **{count} outlier transaction(s)** to confirm they are "
                f"genuine bulk or corporate orders, not data-entry issues."
            )

    # 4. Customer check
    if "customer_id" in df.columns:
        unique_customers = df["customer_id"].nunique()
        total_orders = df["order_id"].nunique()
        if total_orders > 0 and unique_customers > 0:
            repeat = total_orders / unique_customers
            if repeat < 1.2:
                recommendations.append(
                    "Most customers order only once. Consider loyalty programs "
                    "or follow-up campaigns to encourage repeat purchases."
                )

    if not recommendations:
        recommendations.append("No specific action suggested — data looks normal.")

    return recommendations


# ------------------------------------------------------------
# TEST BLOCK
# Run: python -m src.insights
# ------------------------------------------------------------
if __name__ == "__main__":
    from src.data_loader import load_default_data
    from src.data_cleaning import clean_data

    print("Loading and cleaning data...")
    raw = load_default_data()
    df = clean_data(raw, verbose=False)

    if df is None:
        print("Could not load data.")
    else:
        print()
        print("=" * 60)
        print("BUSINESS INSIGHTS")
        print("=" * 60)
        for i, line in enumerate(generate_insights(df), 1):
            print(f"{i}. {line}")
            print()

        print("=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)
        for i, line in enumerate(generate_recommendations(df), 1):
            print(f"{i}. {line}")
            print()