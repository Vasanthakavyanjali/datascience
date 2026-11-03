
import pandas as pd

from src.data_loader import load_all_data
from src.data_cleaner import (
    remove_duplicates,
    create_derived_columns,
    clean_data,
    save_cleaned_data,
)


def sample_data():
    return {
        "customers": pd.DataFrame({
            "customer_id": [1],
            "date_of_birth": ["1995-05-10"],
        }),
        "vehicles": pd.DataFrame({
            "vehicle_id": [10],
            "vehicle_year": [2020],
        }),
        "policies": pd.DataFrame({
            "policy_id": [100],
            "policy_start_date": ["2024-01-01"],
            "policy_end_date": ["2025-01-01"],
            "policy_status": ["Active"],
            "premium_amount": [12000],
            "coverage_amount": [500000],
        }),
        "claims": pd.DataFrame({
            "claim_id": [1000],
            "policy_id": [100],
            "claim_amount": [25000],
            "claim_date": ["2024-06-01"],
            "approval_date": ["2024-06-05"],
            "settlement_date": ["2024-06-10"],
        }),
        "payments": pd.DataFrame({
            "payment_id": [5000],
            "claim_id": [1000],
            "payment_amount": [25000],
        }),
    }


def test_load_all_data(tmp_path):
    from src.validation import REQUIRED_COLUMNS

    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    for table, columns in REQUIRED_COLUMNS.items():
        pd.DataFrame(columns=columns).to_csv(
            raw_dir / f"{table}.csv", index=False
        )

    loaded_data = load_all_data(data_dir=raw_dir)

    assert set(loaded_data.keys()) == {
        "customers",
        "vehicles",
        "policies",
        "claims",
        "payments",
    }


def test_remove_duplicates():
    df = pd.DataFrame({
        "customer_id": [1, 1, 2],
        "customer_name": ["A", "B", "C"],
    })

    result = remove_duplicates(df, key="customer_id")

    assert len(result) == 2
    assert result["customer_id"].is_unique


def test_create_derived_columns():
    data = sample_data()

    result = create_derived_columns(
        data,
        analysis_date="2025-01-01",
    )

    assert "customer_age" in result["customers"].columns
    assert "vehicle_age" in result["vehicles"].columns
    assert "policy_duration_days" in result["policies"].columns
    assert "claim_processing_days" in result["claims"].columns


def test_clean_data():
    data = sample_data()

    result = clean_data(
        data,
        analysis_date="2025-01-01",
    )

    assert len(result) == 5
    assert "customers" in result
    assert "claims" in result


def test_save_cleaned_data(tmp_path):
    data = {
        "customers": pd.DataFrame({
            "customer_id": [1],
            "customer_name": ["Test Customer"],
        })
    }

    save_cleaned_data(data, output_dir=tmp_path)

    output_file = tmp_path / "customers_cleaned.csv"

    assert output_file.exists()

    saved_data = pd.read_csv(output_file)

    assert saved_data.loc[0, "customer_id"] == 1