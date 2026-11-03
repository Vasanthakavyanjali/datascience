# ============================================================
# tests/test_data.py
# Tests for data loading and cleaning.
# ============================================================

import pandas as pd

from src.data_loader import (
    load_default_data,
    find_missing_columns,
    preview_dataframe,
)
from src.data_cleaning import clean_data


# ------------------------------------------------------------
# Test 1: Default data loads without error
# ------------------------------------------------------------
def test_default_data_loads():
    df = load_default_data()
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


# ------------------------------------------------------------
# Test 2: All required columns are present
# ------------------------------------------------------------
def test_required_columns_present():
    df = load_default_data()
    missing = find_missing_columns(df)
    assert missing == [], f"Missing columns: {missing}"


# ------------------------------------------------------------
# Test 3: Cleaning returns a DataFrame
# ------------------------------------------------------------
def test_cleaning_returns_dataframe():
    raw = load_default_data()
    cleaned = clean_data(raw, verbose=False)
    assert cleaned is not None
    assert isinstance(cleaned, pd.DataFrame)
    assert len(cleaned) > 0


# ------------------------------------------------------------
# Test 4: Cleaning adds new columns
# ------------------------------------------------------------
def test_cleaning_adds_columns():
    raw = load_default_data()
    cleaned = clean_data(raw, verbose=False)

    expected_new = ["gross_sales", "discount_amount", "net_sales",
                    "order_year", "order_month", "order_month_name"]

    for col in expected_new:
        assert col in cleaned.columns, f"Missing new column: {col}"


# ------------------------------------------------------------
# Test 5: Cleaned data has no negative quantities
# ------------------------------------------------------------
def test_cleaned_no_negative_quantity():
    raw = load_default_data()
    cleaned = clean_data(raw, verbose=False)

    if "quantity" in cleaned.columns:
        assert (cleaned["quantity"] >= 1).all()


# ------------------------------------------------------------
# Test 6: Cleaned discount is between 0 and 100
# ------------------------------------------------------------
def test_cleaned_discount_range():
    raw = load_default_data()
    cleaned = clean_data(raw, verbose=False)

    if "discount" in cleaned.columns:
        assert (cleaned["discount"] >= 0).all()
        assert (cleaned["discount"] <= 100).all()


# ------------------------------------------------------------
# Test 7: preview_dataframe returns requested rows
# ------------------------------------------------------------
def test_preview_dataframe():
    df = load_default_data()
    preview = preview_dataframe(df, 5)

    assert isinstance(preview, pd.DataFrame)
    assert len(preview) <= 5