
import pandas as pd

REQUIRED_COLUMNS = {
    "customers": [
        "customer_id", "customer_name", "gender",
        "date_of_birth", "age", "city", "state",
        "occupation",
    ],
    "vehicles": [
        "vehicle_id", "customer_id", "vehicle_type",
        "vehicle_make", "vehicle_model", "vehicle_year",
        "fuel_type", "vehicle_value",
    ],
    "policies": [
        "policy_id", "customer_id", "vehicle_id",
        "policy_start_date", "policy_end_date",
        "policy_type", "premium_amount", "coverage_amount",
        "policy_status", "payment_frequency",
    ],
    "claims": [
        "claim_id", "policy_id", "customer_id",
        "claim_date", "accident_date", "claim_type",
        "accident_location", "claim_amount", "claim_status",
        "approval_date", "settlement_date", "damage_severity",
    ],
    "payments": [
        "payment_id", "claim_id", "policy_id",
        "payment_date", "payment_amount",
        "payment_status", "payment_method",
    ],
}

PRIMARY_KEYS = {
    "customers": "customer_id",
    "vehicles": "vehicle_id",
    "policies": "policy_id",
    "claims": "claim_id",
    "payments": "payment_id",
}


def validate_table(df, table_name):
    if table_name not in REQUIRED_COLUMNS:
        raise ValueError(f"Unknown table: {table_name}")

    errors = []
    missing = [
        col for col in REQUIRED_COLUMNS[table_name]
        if col not in df.columns
    ]

    if missing:
        errors.append(f"Missing columns: {missing}")
        return errors

    key = PRIMARY_KEYS[table_name]

    if df[key].isna().any():
        errors.append(f"{key} contains missing values")

    if df[key].duplicated().any():
        errors.append(f"{key} contains duplicate values")

    return errors


def validate_customers(df):
    return validate_table(df, "customers")


def validate_policies(df):
    return validate_table(df, "policies")


def validate_claims(df):
    return validate_table(df, "claims")


def validate_vehicles(df):
    return validate_table(df, "vehicles")


def validate_payments(df):
    return validate_table(df, "payments")


def validate_relationships(data):
    errors = []

    required_tables = set(REQUIRED_COLUMNS)
    missing_tables = required_tables - set(data)

    if missing_tables:
        return [
            f"Missing tables: {sorted(missing_tables)}"
        ]

    relationships = [
        ("vehicles", "customer_id", "customers", "customer_id"),
        ("policies", "customer_id", "customers", "customer_id"),
        ("policies", "vehicle_id", "vehicles", "vehicle_id"),
        ("claims", "policy_id", "policies", "policy_id"),
        ("claims", "customer_id", "customers", "customer_id"),
        ("payments", "claim_id", "claims", "claim_id"),
        ("payments", "policy_id", "policies", "policy_id"),
    ]

    for child, child_col, parent, parent_col in relationships:
        child_df = data[child]
        parent_df = data[parent]

        if child_col not in child_df.columns:
            errors.append(
                f"{child}: missing relationship column {child_col}"
            )
            continue

        if parent_col not in parent_df.columns:
            errors.append(
                f"{parent}: missing relationship column {parent_col}"
            )
            continue

        parent_ids = set(parent_df[parent_col].dropna())
        child_ids = set(child_df[child_col].dropna())
        orphan_ids = child_ids - parent_ids

        if orphan_ids:
            errors.append(
                f"{child}.{child_col} has "
                f"{len(orphan_ids)} unmatched identifiers"
            )

    return errors


def validate_all_data(data):
    errors = []

    for table_name in REQUIRED_COLUMNS:
        if table_name not in data:
            errors.append(f"Missing table: {table_name}")
            continue

        errors.extend(
            f"{table_name}: {error}"
            for error in validate_table(
                data[table_name], table_name
            )
        )

    if not errors:
        errors.extend(validate_relationships(data))

    return errors