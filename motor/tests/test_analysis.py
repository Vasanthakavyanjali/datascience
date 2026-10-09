
import pandas as pd

from src.insurance_analysis import (
    calculate_total_policies,
    calculate_active_policies,
    calculate_total_claims,
    calculate_total_premium,
    calculate_claim_approval_rate,
    calculate_average_claim_amount,
)


def sample_analysis_data():
    return {
        "customers": pd.DataFrame({
            "customer_id": [1, 2, 3],
        }),
        "policies": pd.DataFrame({
            "policy_id": [101, 102, 103],
            "policy_status": ["Active", "Expired", "Active"],
            "premium_amount": [10000, 15000, 20000],
        }),
        "claims": pd.DataFrame({
            "claim_id": [1, 2, 3],
            "claim_amount": [10000, 20000, 30000],
            "claim_status": ["Approved", "Rejected", "Approved"],
        }),
        "payments": pd.DataFrame({
            "payment_id": [1, 2],
            "payment_amount": [10000, 30000],
        }),
    }


def test_calculate_total_policies():
    data = sample_analysis_data()

    result = calculate_total_policies(data["policies"])

    assert result == 3


def test_calculate_active_policies():
    data = sample_analysis_data()

    result = calculate_active_policies(data["policies"])

    assert result == 2


def test_calculate_total_claims():
    data = sample_analysis_data()

    result = calculate_total_claims(data["claims"])

    assert result == 3


def test_calculate_total_premium():
    data = sample_analysis_data()

    result = calculate_total_premium(data["policies"])

    assert result == 45000


def test_calculate_claim_approval_rate():
    data = sample_analysis_data()

    result = calculate_claim_approval_rate(data["claims"])

    assert result == 2 / 3 * 100


def test_calculate_average_claim_amount():
    data = sample_analysis_data()

    result = calculate_average_claim_amount(data["claims"])

    assert result == 20000