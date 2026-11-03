# ============================================================
# src/sales_analysis.py
# Groups and summarizes sales data.
# Compatible with pandas 2.1 AND 2.2+ (handles "M" -> "ME").
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# HELPER: translate old pandas period aliases to new ones
# ------------------------------------------------------------
def _normalize_period(period):
    """
    Pandas 2.2+ requires 'ME', 'QE', 'YE' instead of 'M', 'Q', 'Y'.
    Accepts both old and new, so callers don't have to worry.
    """
    mapping = {
        "M": "ME",
        "Q": "QE",
        "Y": "YE",
        "A": "YE",
    }
    return mapping.get(period, period)


# ------------------------------------------------------------
# SALES BY CATEGORY
# ------------------------------------------------------------
def sales_by_category(df):
    """Total sales per category."""
    if df is None or df.empty:
        return pd.DataFrame()

    if "category" not in df.columns or "sales" not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby("category")["sales"]
        .sum()
        .reset_index()
        .sort_values("sales", ascending=False)
    )
    return result


# ------------------------------------------------------------
# SALES BY REGION
# ------------------------------------------------------------
def sales_by_region(df):
    """Total sales per region."""
    if df is None or df.empty:
        return pd.DataFrame()

    if "region" not in df.columns or "sales" not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby("region")["sales"]
        .sum()
        .reset_index()
        .sort_values("sales", ascending=False)
    )
    return result


# ------------------------------------------------------------
# SALES OVER TIME
# ------------------------------------------------------------
def sales_over_time(df, period="ME"):
    """
    Sales over time.
    period = "D"  -> daily
           = "W"  -> weekly
           = "ME" -> monthly (default)
           = "M"  -> also works (auto-converted to "ME")
    """
    if df is None or df.empty:
        return pd.DataFrame()

    if "order_date" not in df.columns or "sales" not in df.columns:
        return pd.DataFrame()

    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])

    if df.empty:
        return pd.DataFrame()

    period = _normalize_period(period)

    result = (
        df.set_index("order_date")
        .resample(period)["sales"]
        .sum()
        .reset_index()
    )

    return result


# ------------------------------------------------------------
# ORDERS OVER TIME
# ------------------------------------------------------------
def orders_over_time(df, period="ME"):
    """
    Number of orders over time.
    Same period rules as sales_over_time.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    if "order_date" not in df.columns or "order_id" not in df.columns:
        return pd.DataFrame()

    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])

    if df.empty:
        return pd.DataFrame()

    period = _normalize_period(period)

    result = (
        df.set_index("order_date")
        .resample(period)["order_id"]
        .nunique()
        .reset_index()
        .rename(columns={"order_id": "orders"})
    )

    return result


# ------------------------------------------------------------
# MONTHLY SALES (by month name)
# ------------------------------------------------------------
def monthly_sales(df):
    """Sales grouped by month name (Jan, Feb, ...)."""
    if df is None or df.empty:
        return pd.DataFrame()

    if "order_month_name" not in df.columns or "sales" not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby("order_month_name")["sales"]
        .sum()
        .reset_index()
        .sort_values("sales", ascending=False)
    )
    return result


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
        print()
        print("SALES BY CATEGORY")
        print(sales_by_category(df).to_string(index=False))

        print()
        print("SALES BY REGION")
        print(sales_by_region(df).to_string(index=False))

        print()
        print("MONTHLY SALES OVER TIME")
        print(sales_over_time(df).to_string(index=False))

        print()
        print("MONTHLY SALES BY NAME")
        print(monthly_sales(df).to_string(index=False))