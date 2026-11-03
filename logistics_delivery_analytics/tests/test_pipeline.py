import os
import pandas as pd
import pytest
from src.data_loader import load_data
from src.data_cleaner import remove_duplicates, create_derived_columns, clean_data, save_cleaned_data
from src.business_analysis import calculate_total_orders, calculate_on_time_percentage

@pytest.fixture
def sample_df():
    data = {
        'order_id': ['ORD100', 'ORD100', 'ORD101'],
        'customer_id': ['CUST1', 'CUST1', 'CUST2'],
        'order_date': ['2026-01-01', '2026-01-01', '2026-01-02'],
        'warehouse': ['Wh_A', 'Wh_A', 'Wh_B'],
        'origin_city': ['CityA', 'CityA', 'CityB'],
        'destination_city': ['CityC', 'CityC', 'CityD'],
        'distance_km': [100, 100, 200],
        'product_category': ['Electronics', 'Electronics', 'Apparel'],
        'quantity': [1, 1, 2],
        'weight_kg': [2.5, 2.5, 1.0],
        'shipping_mode': ['Express', 'Express', 'Standard'],
        'delivery_partner': ['PartnerA', 'PartnerA', 'PartnerB'],
        'shipping_cost': [50.0, 50.0, 30.0],
        'fuel_cost': [10.0, 10.0, 5.0],
        'warehouse_processing_hours': [12, 12, 24],
        'dispatch_date': ['2026-01-02', '2026-01-02', '2026-01-03'],
        'expected_delivery_date': ['2026-01-05', '2026-01-05', '2026-01-06'],
        'actual_delivery_date': ['2026-01-04', '2026-01-04', '2026-01-07'],
        'delivery_status': ['Delivered', 'Delivered', 'Delayed'],
        'customer_rating': [5.0, 5.0, 3.0],
        'damage_flag': [0, 0, 0],
        'return_flag': [0, 0, 0]
    }
    return pd.DataFrame(data)

def test_load_data(tmp_path):
    p = tmp_path / "test.csv"
    p.write_text("order_id\nORD1")
    df = load_data(str(p))
    assert len(df) == 1

def test_remove_duplicates(sample_df):
    cleaned = remove_duplicates(sample_df)
    assert len(cleaned) == 2

def test_create_derived_columns(sample_df):
    cleaned = clean_data(sample_df)
    assert 'delivery_days' in cleaned.columns
    assert 'delay_days' in cleaned.columns
    assert 'cost_per_km' in cleaned.columns
    assert 'total_logistics_cost' in cleaned.columns
    assert 'on_time_flag' in cleaned.columns

def test_clean_data(sample_df):
    cleaned = clean_data(sample_df)
    assert len(cleaned) == 2
    assert cleaned['total_logistics_cost'].iloc[0] == 60.0

def test_calculate_total_orders(sample_df):
    cleaned = clean_data(sample_df)
    assert calculate_total_orders(cleaned) == 2

def test_calculate_on_time_percentage(sample_df):
    cleaned = clean_data(sample_df)
    # ORD100: delay_days = -1 (On-time), ORD101: delay_days = +1 (Delayed) -> 50%
    assert calculate_on_time_percentage(cleaned) == 50.0

def test_save_cleaned_data(tmp_path, sample_df):
    out = tmp_path / "cleaned.csv"
    save_cleaned_data(sample_df, str(out))
    assert os.path.exists(out)