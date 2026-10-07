# ============================================================
# src/data_cleaning.py
#
# Purpose:
# Clean and transform the sales dataset after it has been
# loaded and validated.
#
# Important:
# This module contains cleaning logic.
# Dataset-specific column definitions are maintained in
# config.py.
# ============================================================

import pandas as pd
from config.config import (
    CRITICAL_COLUMNS, NUMERIC_COLUMNS, TEXT_COLUMNS, DATE_COLUMNS,
    MIN_QUANTITY, MIN_UNIT_PRICE, MIN_DISCOUNT, MAX_DISCOUNT,
)

# ============================================================
# 1. MAKE COPY
# ============================================================

def make_copy(df):
    """
    Create a copy of the original DataFrame.
    Why? Cleaning should not modify the original raw dataset.
    This allows us to keep:
        Raw Data
            |
            +----> Cleaned Data
    instead of permanently changing the raw data.
    """
    if df is None:
        return None
    return df.copy()

# ============================================================
# 2. REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):
    """
    Remove duplicate records based on order_id.
    The first occurrence is kept.
    Note: This rule is specific to this sales project because
    order_id is expected to uniquely identify an order.
    """
    if df is None:
        return df
    if "order_id" not in df.columns:
        return df
    before = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    after = len(df)
    removed = before - after
    if removed > 0:
        print(f"Removed {removed} duplicate order(s).")
    return df

# ============================================================
# 3. FILL MISSING TEXT VALUES
# ============================================================

def fill_missing_text(df):
    """
    Replace missing values in configured text columns with 'Unknown'.
    Example:
        category        category
        --------        --------
        Laptop          Laptop
        NaN       -->   Unknown
        Mobile          Mobile
    """
    if df is None:
        return df
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    return df

# ============================================================
# 4. REMOVE MISSING CRITICAL VALUES
# ============================================================

def remove_missing_critical(df):
    """
    Remove rows where critical business columns are missing.
    Critical columns are defined in config.py.
    Example: order_id, customer_id, order_date, sales
    These fields are important for this sales project.
    Important: We first check whether the expected columns
    actually exist. Missing schema columns should normally be
    handled by validation before cleaning.
    """
    if df is None:
        return df
    missing_columns = [col for col in CRITICAL_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "Dataset schema is invalid. "
            f"Missing critical columns: {missing_columns}"
        )
    before = len(df)
    df = df.dropna(subset=CRITICAL_COLUMNS)
    after = len(df)
    removed = before - after
    if removed > 0:
        print(f"Removed {removed} row(s) with missing critical values.")
    return df

# ============================================================
# 5. FIX DATA TYPES
# ============================================================

def fix_data_types(df):
    """
    Convert columns to their correct data types.
    Numeric columns: quantity, unit_price, discount, sales
    Date columns: order_date
    Invalid values are converted to NaN/NaT.
    Example:
        quantity        quantity
        --------        --------
        10              10
        5         -->   5
        "abc"           NaN
    """
    if df is None:
        return df
    # Convert numeric columns
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # Convert date columns
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

# ============================================================
# 6. REMOVE INVALID ROWS
# ============================================================

def remove_invalid_rows(df):
    """
    Remove rows that violate the business rules.
    Rules for this sales project:
        quantity >= MIN_QUANTITY
        unit_price >= MIN_UNIT_PRICE
        MIN_DISCOUNT <= discount <= MAX_DISCOUNT
        order_date must be valid
    """
    if df is None:
        return df
    before = len(df)
    # Quantity validation
    if "quantity" in df.columns:
        df = df[df["quantity"] >= MIN_QUANTITY]
    # Unit price validation
    if "unit_price" in df.columns:
        df = df[df["unit_price"] >= MIN_UNIT_PRICE]
    # Discount validation
    if "discount" in df.columns:
        df = df[(df["discount"] >= MIN_DISCOUNT) & (df["discount"] <= MAX_DISCOUNT)]
    # Date validation
    if "order_date" in df.columns:
        df = df[df["order_date"].notna()]
    after = len(df)
    removed = before - after
    if removed > 0:
        print(f"Removed {removed} invalid row(s).")
    return df

# ============================================================
# 7. ADD CALCULATED COLUMNS
# ============================================================

def add_new_columns(df):
    """
    Create derived business features.
    Calculations:
        gross_sales     = quantity * unit_price
        discount_amount = gross_sales * discount / 100
        net_sales       = gross_sales - discount_amount
    Date features: order_year, order_month, order_month_name
    """
    if df is None or df.empty:
        return df
    # Gross Sales
    if "quantity" in df.columns and "unit_price" in df.columns:
        df["gross_sales"] = df["quantity"] * df["unit_price"]
    # Discount Amount
    if "gross_sales" in df.columns and "discount" in df.columns:
        df["discount_amount"] = df["gross_sales"] * df["discount"] / 100
    # Net Sales
    if "gross_sales" in df.columns and "discount_amount" in df.columns:
        df["net_sales"] = df["gross_sales"] - df["discount_amount"]
    # Date Features
    if "order_date" in df.columns:
        df["order_year"] = df["order_date"].dt.year
        df["order_month"] = df["order_date"].dt.month
        df["order_month_name"] = df["order_date"].dt.strftime("%b")
    return df

# ============================================================
# 8. MAIN CLEANING PIPELINE
# ============================================================

def clean_data(df, verbose=True):
    """
    Run all data-cleaning steps in the correct order.
    Pipeline:
        Raw Data
            |
            v
        Make Copy
            |
            v
        Remove Duplicates
            |
            v
        Fill Missing Text
            |
            v
        Remove Missing Critical Values
            |
            v
        Fix Data Types
            |
            v
        Remove Invalid Rows
            |
            v
        Add New Columns
            |
            v
        Reset Index
            |
            v
        Clean Data
    """
    if df is None:
        if verbose:
            print("No data to clean.")
        return None
    # Start message
    if verbose:
        print("=" * 50)
        print("CLEANING DATA")
        print("=" * 50)
        print("Rows before cleaning:", len(df))
    # Step 1: Protect original data
    df = make_copy(df)
    # Step 2: Remove duplicate orders
    df = remove_duplicates(df)
    # Step 3: Fill missing text values
    df = fill_missing_text(df)
    # Step 4: Remove rows with missing critical values
    df = remove_missing_critical(df)
    # Step 5: Correct data types
    df = fix_data_types(df)
    # Step 6: Remove invalid business values
    df = remove_invalid_rows(df)
    # Step 7: Create calculated columns
    df = add_new_columns(df)
    # Step 8: Reset DataFrame index
    df = df.reset_index(drop=True)
    # End message
    if verbose:
        print()
        print("Rows after cleaning:", len(df))
        print("Cleaning finished.")
        print("=" * 50)
    return df

# ============================================================
# DIRECT TESTING
# ============================================================

if __name__ == "__main__":
    from src.data_loader import load_default_data
    print("=" * 50)
    print("DATA CLEANING TEST")
    print("=" * 50)
    print()
    print("Loading data...")
    raw = load_default_data()
    if raw is not None:
        print()
        print("Columns BEFORE cleaning:")
        print(list(raw.columns))
        print()
        cleaned = clean_data(raw)
        print()
        print("Columns AFTER cleaning:")
        print(list(cleaned.columns))
        print()
        print("First 5 rows of cleaned data:")
        print(cleaned.head().to_string())
    else:
        print("Could not load data.")