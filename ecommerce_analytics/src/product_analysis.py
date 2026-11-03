# ============================================================
# src/product_analysis.py
# Product and category performance.
# ============================================================

import pandas as pd


def product_summary(df):
    """
    One row per product with:
    - total_sales
    - total_quantity
    - order_count
    - average_price
    """
    if df is None or df.empty:
        return pd.DataFrame()

    needed = ["product_name", "order_id", "sales", "quantity"]
    if not all(c in df.columns for c in needed):
        return pd.DataFrame()

    result = (
        df.groupby("product_name")
        .agg(
            total_sales=("sales", "sum"),
            total_quantity=("quantity", "sum"),
            order_count=("order_id", "nunique"),
            average_price=("unit_price", "mean"),
        )
        .reset_index()
    )

    result["total_sales"] = result["total_sales"].round(2)
    result["average_price"] = result["average_price"].round(2)

    return result.sort_values("total_sales", ascending=False)


def top_products(product_df, n=10):
    """Top N products by total sales."""
    if product_df is None or product_df.empty:
        return pd.DataFrame()

    return product_df.head(n)


def low_performing_products(product_df, n=10):
    """Bottom N products by total sales."""
    if product_df is None or product_df.empty:
        return pd.DataFrame()

    return product_df.tail(n).sort_values("total_sales")


def category_summary(df):
    """
    One row per category with:
    - total_sales
    - total_quantity
    - order_count
    - product_count
    """
    if df is None or df.empty:
        return pd.DataFrame()

    needed = ["category", "sales", "quantity", "order_id", "product_name"]
    if not all(c in df.columns for c in needed):
        return pd.DataFrame()

    result = (
        df.groupby("category")
        .agg(
            total_sales=("sales", "sum"),
            total_quantity=("quantity", "sum"),
            order_count=("order_id", "nunique"),
            product_count=("product_name", "nunique"),
        )
        .reset_index()
    )

    result["total_sales"] = result["total_sales"].round(2)

    return result.sort_values("total_sales", ascending=False)


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
        products = product_summary(df)
        print()
        print("TOP 5 PRODUCTS")
        print(top_products(products, 5).to_string(index=False))

        print()
        print("LOW PERFORMING PRODUCTS")
        print(low_performing_products(products, 5).to_string(index=False))

        print()
        print("CATEGORY SUMMARY")
        print(category_summary(df).to_string(index=False))