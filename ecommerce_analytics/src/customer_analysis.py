# ============================================================
# src/customer_analysis.py
# Customer spending and segmentation.
# ============================================================

import pandas as pd


def customer_summary(df):
    """
    Returns one row per customer with:
    - total_spend
    - order_count
    - average_order_value
    """
    if df is None or df.empty:
        return pd.DataFrame()

    needed = ["customer_id", "order_id", "sales"]
    if not all(c in df.columns for c in needed):
        return pd.DataFrame()

    result = (
        df.groupby("customer_id")
        .agg(
            total_spend=("sales", "sum"),
            order_count=("order_id", "nunique"),
        )
        .reset_index()
    )

    result["average_order_value"] = (
        result["total_spend"] / result["order_count"]
    ).round(2)

    result["total_spend"] = result["total_spend"].round(2)

    return result.sort_values("total_spend", ascending=False)


def segment_customers(customer_df):
    """
    Adds a 'segment' column based on total_spend quartiles.
    Low / Medium / High value.
    """
    if customer_df is None or customer_df.empty:
        return pd.DataFrame()

    if "total_spend" not in customer_df.columns:
        return customer_df

    df = customer_df.copy()

    q1 = df["total_spend"].quantile(0.25)
    q3 = df["total_spend"].quantile(0.75)

    def label(spend):
        if spend <= q1:
            return "Low Value"
        elif spend <= q3:
            return "Medium Value"
        else:
            return "High Value"

    df["segment"] = df["total_spend"].apply(label)

    return df


def segment_counts(segmented_df):
    """Count customers in each segment."""
    if segmented_df is None or segmented_df.empty:
        return pd.DataFrame()

    if "segment" not in segmented_df.columns:
        return pd.DataFrame()

    result = (
        segmented_df.groupby("segment")
        .agg(
            customers=("customer_id", "nunique"),
            total_spend=("total_spend", "sum"),
        )
        .reset_index()
    )

    return result.sort_values("total_spend", ascending=False)


def top_customers(customer_df, n=10):
    """Return top N customers by total_spend."""
    if customer_df is None or customer_df.empty:
        return pd.DataFrame()

    return customer_df.head(n)


# ------------------------------------------------------------
# TEST BLOCK
# ------------------------------------------------------------
if __name__ == "__main__":
    from src.data_loader import load_default_data
    from src.data_cleaning import clean_data

    print("Loading and cleaning data...")
    raw = load_default_data()
    df = clean_data(raw, verbose=False)

    if df is not None:
        summary = customer_summary(df)
        print()
        print("TOP 5 CUSTOMERS")
        print(top_customers(summary, 5).to_string(index=False))

        segmented = segment_customers(summary)
        print()
        print("CUSTOMER SEGMENTS")
        print(segment_counts(segmented).to_string(index=False))