
import pandas as pd

from src.validation import (
    REQUIRED_COLUMNS,
    validate_customers,
    validate_policies,
    validate_claims,
    validate_relationships,
)


def make_table(table_name, values):
    row = {column: None for column in REQUIRED_COLUMNS[table_name]}
    row.update(values)

    return pd.DataFrame([row])


def valid_data():
    return {
        "customers": make_table(
            "customers",
            {"customer_id": 1},
        ),
        "vehicles": make_table(
            "vehicles",
            {"vehicle_id": 10, "customer_id": 1},
        ),
        "policies": make_table(
            "policies",
            {
                "policy_id": 100,
                "customer_id": 1,
                "vehicle_id": 10,
            },
        ),
        "claims": make_table(
            "claims",
            {
                "claim_id": 1000,
                "policy_id": 100,
                "customer_id": 1,
            },
        ),
        "payments": make_table(
            "payments",
            {
                "payment_id": 5000,
                "claim_id": 1000,
                "policy_id": 100,
            },
        ),
    }


def test_validate_customers():
    customers = make_table(
        "customers",
        {"customer_id": 1},
    )

    errors = validate_customers(customers)

    assert errors == []


def test_validate_policies():
    policies = make_table(
        "policies",
        {
            "policy_id": 100,
            "customer_id": 1,
            "vehicle_id": 10,
        },
    )

    errors = validate_policies(policies)

    assert errors == []


def test_validate_claims():
    claims = make_table(
        "claims",
        {
            "claim_id": 1000,
            "policy_id": 100,
            "customer_id": 1,
        },
    )

    errors = validate_claims(claims)

    assert errors == []


def test_validate_relationships():
    data = valid_data()

    errors = validate_relationships(data)

    assert errors == []


def test_validate_relationships_with_invalid_claim():
    data = valid_data()

    data["payments"].loc[0, "claim_id"] = 9999

    errors = validate_relationships(data)

    assert len(errors) > 0