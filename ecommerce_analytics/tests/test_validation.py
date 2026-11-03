# ============================================================
# tests/test_validation.py
# Tests for the validation module.
# ============================================================

import pandas as pd

from src.validation import (
    check_required_columns,
    check_missing_values,
    check_duplicate_orders,
    check_invalid_quantity,
    check_invalid_price,
    check_invalid_discount,
    check_invalid_dates,
    run_all_checks,
)


# ------------------------------------------------------------
# Helper: good test data
# ------------------------------------------------------------
def good_data():
    return pd.DataFrame({
        "order_id":    ["ORD1", "ORD2"],
        "order_date":  ["2026-01-01", "2026-01-02"],
        "customer_id": ["C1", "C2"],
        "product_id":  ["P1", "P2"],
        "category":    ["Electronics", "Clothing"],
        "region":      ["North", "South"],
        "quantity":    [2, 3],
        "unit_price":  [100, 200],
        "discount":    [10, 20],
        "sales":       [180, 480],
    })


# ------------------------------------------------------------
# Test: All required columns present
# ------------------------------------------------------------
def test_required_columns_all_present():
    df = good_data()
    missing = check_required_columns(df)
    assert missing == []


# ------------------------------------------------------------
# Test: Detect missing column
# ------------------------------------------------------------
def test_required_columns_missing():
    df = good_data().drop(columns=["sales"])
    missing = check_required_columns(df)
    assert "sales" in missing


# ------------------------------------------------------------
# Test: Duplicate order detection
# ------------------------------------------------------------
def test_duplicate_orders():
    df = pd.DataFrame({
        "order_id": ["ORD1", "ORD1", "ORD2"],
    })
    assert check_duplicate_orders(df) == 1


# ------------------------------------------------------------
# Test: Invalid quantity
# ------------------------------------------------------------
def test_invalid_quantity():
    df = pd.DataFrame({
        "quantity": [2, -1, 3, 0],
    })
    invalid = check_invalid_quantity(df)
    assert len(invalid) == 2  # -1 and 0


# ------------------------------------------------------------
# Test: Invalid price
# ------------------------------------------------------------
def test_invalid_price():
    df = pd.DataFrame({
        "unit_price": [100, 0, 50, -10],
    })
    invalid = check_invalid_price(df)
    assert len(invalid) == 2  # 0 and -10


# ------------------------------------------------------------
# Test: Invalid discount (too high or negative)
# ------------------------------------------------------------
def test_invalid_discount():
    df = pd.DataFrame({
        "discount": [10, 150, -5, 50],
    })
    invalid = check_invalid_discount(df)
    assert len(invalid) == 2  # 150 and -5


# ------------------------------------------------------------
# Test: Invalid dates
# ------------------------------------------------------------
def test_invalid_dates():
    df = pd.DataFrame({
        "order_date": ["2026-01-01", "not-a-date", "2026-01-03"],
    })
    invalid = check_invalid_dates(df)
    assert len(invalid) == 1


# ------------------------------------------------------------
# Test: run_all_checks on good data
# ------------------------------------------------------------
def test_run_all_checks_good_data():
    df = good_data()
    report = run_all_checks(df)

    assert report["valid"] is True
    assert report["duplicate_orders"] == 0
    assert report["invalid_quantity_count"] == 0
    assert report["invalid_price_count"] == 0
    assert report["invalid_discount_count"] == 0
    assert report["invalid_date_count"] == 0


# ------------------------------------------------------------
# Test: run_all_checks with missing column
# ------------------------------------------------------------
def test_run_all_checks_missing_column():
    df = good_data().drop(columns=["sales"])
    report = run_all_checks(df)

    assert report["valid"] is False
    assert "sales" in report["missing_columns"]