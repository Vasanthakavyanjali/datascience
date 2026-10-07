# ============================================================
# tests/test_kpi.py
# Tests for KPI calculations using a small fake dataset.
# ============================================================

import pandas as pd

from src.kpi import (
    total_sales,
    total_orders,
    total_customers,
    total_units,
    average_order_value,
    median_order_value,
    get_all_kpis,
    format_number,
)


# ------------------------------------------------------------
# Small fake data for testing (2 orders, 2 customers)
# ------------------------------------------------------------
def make_test_data():
    return pd.DataFrame({
        "order_id":    ["ORD1", "ORD2", "ORD2"],
        "customer_id": ["C1",   "C2",   "C2"],
        "quantity":    [2,      3,      1],
        "unit_price":  [100,    200,    200],
        "discount":    [0,      10,     10],
        "sales":       [200,    540,    180],
    })


# ------------------------------------------------------------
# Test: Total sales
# ------------------------------------------------------------
def test_total_sales():
    df = make_test_data()
    # 200 + 540 + 180 = 920
    assert total_sales(df) == 920


# ------------------------------------------------------------
# Test: Total orders (unique)
# ------------------------------------------------------------
def test_total_orders():
    df = make_test_data()
    # ORD1, ORD2 -> 2 unique
    assert total_orders(df) == 2


# ------------------------------------------------------------
# Test: Total customers (unique)
# ------------------------------------------------------------
def test_total_customers():
    df = make_test_data()
    # C1, C2 -> 2 unique
    assert total_customers(df) == 2


# ------------------------------------------------------------
# Test: Total units
# ------------------------------------------------------------
def test_total_units():
    df = make_test_data()
    # 2 + 3 + 1 = 6
    assert total_units(df) == 6


# ------------------------------------------------------------
# Test: Average order value
# ------------------------------------------------------------
def test_average_order_value():
    df = make_test_data()
    # 920 / 2 = 460
    assert average_order_value(df) == 460.0


# ------------------------------------------------------------
# Test: Median order value
# ------------------------------------------------------------
def test_median_order_value():
    df = make_test_data()
    # Order ORD1 total = 200
    # Order ORD2 total = 540 + 180 = 720
    # Median of [200, 720] = (200 + 720) / 2 = 460
    assert median_order_value(df) == 460.0


# ------------------------------------------------------------
# Test: get_all_kpis returns dict
# ------------------------------------------------------------
def test_get_all_kpis():
    df = make_test_data()
    kpis = get_all_kpis(df)

    assert isinstance(kpis, dict)
    assert "total_sales" in kpis
    assert "total_orders" in kpis
    assert "total_customers" in kpis
    assert "total_units" in kpis
    assert "average_order_value" in kpis
    assert "median_order_value" in kpis


# ------------------------------------------------------------
# Test: Empty DataFrame returns 0
# ------------------------------------------------------------
def test_empty_dataframe():
    empty = pd.DataFrame()
    assert total_sales(empty) == 0.0
    assert total_orders(empty) == 0
    assert total_customers(empty) == 0


# ------------------------------------------------------------
# Test: format_number works for Lakhs
# ------------------------------------------------------------
def test_format_number_lakhs():
    # 250000 -> ₹2.50 L
    assert "L" in format_number(250000)


# ------------------------------------------------------------
# Test: format_number for small values
# ------------------------------------------------------------
def test_format_number_small():
    result = format_number(1500)
    assert "1,500" in result