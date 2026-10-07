'''
What is a KPI?
-------------------------
KPI = Key Performance Indicator.

These are the numbers a manager wants to see at a glance:

How much did we sell?

How many orders?

How many customers?

What is the average order value?

Simple, one-line calculations. No charts. Just numbers.

'''


# ============================================================
# src/kpi.py
# Calculates the main business KPIs.
# Each function returns one number.
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# KPI 1: Total Sales
# ------------------------------------------------------------
def total_sales(df):
    """
    Sum of all sales.
    """
    if df is None or df.empty or "sales" not in df.columns:
        return 0.0

    return float(df["sales"].sum())


# ------------------------------------------------------------
# KPI 2: Total Orders
# ------------------------------------------------------------
def total_orders(df):
    """
    Number of unique orders.
    """
    if df is None or df.empty or "order_id" not in df.columns:
        return 0

    return int(df["order_id"].nunique())


# ------------------------------------------------------------
# KPI 3: Total Customers
# ------------------------------------------------------------
def total_customers(df):
    """
    Number of unique customers.
    """
    if df is None or df.empty or "customer_id" not in df.columns:
        return 0

    return int(df["customer_id"].nunique())


# ------------------------------------------------------------
# KPI 4: Total Units Sold
# ------------------------------------------------------------
def total_units(df):
    """
    Sum of all quantities.
    """
    if df is None or df.empty or "quantity" not in df.columns:
        return 0

    return int(df["quantity"].sum())


# ------------------------------------------------------------
# KPI 5: Average Order Value (AOV)
# ------------------------------------------------------------
def average_order_value(df):
    """
    Total sales divided by number of unique orders.
    """
    orders = total_orders(df)
    if orders == 0:
        return 0.0

    return round(total_sales(df) / orders, 2)


# ------------------------------------------------------------
# KPI 6: Median Order Value
# ------------------------------------------------------------
def median_order_value(df):
    """
    Median of sales per order.
    We group by order_id, sum the sales, then take the median.
    """
    if df is None or df.empty:
        return 0.0

    if "order_id" not in df.columns or "sales" not in df.columns:
        return 0.0

    # One sales value per order
    order_totals = df.groupby("order_id")["sales"].sum()

    return round(float(order_totals.median()), 2)


# ------------------------------------------------------------
# MASTER FUNCTION: Get all KPIs at once
# ------------------------------------------------------------
def get_all_kpis(df):
    """
    Returns a dictionary with all KPIs.
    Useful for the dashboard.
    """
    return {
        "total_sales": total_sales(df),
        "total_orders": total_orders(df),
        "total_customers": total_customers(df),
        "total_units": total_units(df),
        "average_order_value": average_order_value(df),
        "median_order_value": median_order_value(df),
    }


# ------------------------------------------------------------
# HELPER: Format a number for display
# ------------------------------------------------------------
def format_number(value):
    """
    Turns a big number like 2540000 into 25.40 L (Lakhs).
    If smaller than 1 Lakh, shows as-is.
    """
    if value is None:
        return "0"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)

    # 1 Lakh = 100,000
    if abs(value) >= 100000:
        lakhs = value / 100000
        return f"₹{lakhs:.2f} L"

    return f"₹{value:,.0f}"


# ------------------------------------------------------------
# TEST BLOCK
# Run: python -m src.kpi
# ------------------------------------------------------------
if __name__ == "__main__":
    from src.data_loader import load_default_data
    from src.data_cleaning import clean_data

    print("Loading and cleaning data...")
    raw = load_default_data()
    df = clean_data(raw, verbose=False)

    if df is not None:
        print()
        print("=" * 50)
        print("KPI REPORT")
        print("=" * 50)

        kpis = get_all_kpis(df)

        print(f"Total Sales        : {format_number(kpis['total_sales'])}")
        print(f"Total Orders       : {kpis['total_orders']:,}")
        print(f"Total Customers    : {kpis['total_customers']:,}")
        print(f"Total Units Sold   : {kpis['total_units']:,}")
        print(f"Avg Order Value    : {format_number(kpis['average_order_value'])}")
        print(f"Median Order Value : {format_number(kpis['median_order_value'])}")
    else:
        print("Could not load data.")