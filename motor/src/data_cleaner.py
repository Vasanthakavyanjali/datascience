
from pathlib import Path

import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


DATE_COLUMNS = {
    "customers": ["date_of_birth"],
    "vehicles": [],
    "policies": ["policy_start_date", "policy_end_date"],
    "claims": [
        "claim_date",
        "accident_date",
        "approval_date",
        "settlement_date",
    ],
    "payments": ["payment_date"],
}


def clean_text_columns(df):
    """Remove unnecessary spaces from text columns."""
    df = df.copy()

    for column in df.select_dtypes(include=["object", "string"]).columns:
        df[column] = df[column].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    return df


def remove_duplicates(df, key=None):
    """Remove duplicate records using a key or complete-row comparison."""
    df = df.copy()

    if key and key in df.columns:
        return df.drop_duplicates(subset=[key], keep="last").reset_index(
            drop=True
        )

    return df.drop_duplicates().reset_index(drop=True)


def convert_data_types(data):
    """Convert date and numeric columns to suitable data types."""
    data = {name: df.copy() for name, df in data.items()}

    for table_name, columns in DATE_COLUMNS.items():
        if table_name not in data:
            continue

        for column in columns:
            if column in data[table_name].columns:
                data[table_name][column] = pd.to_datetime(
                    data[table_name][column],
                    errors="coerce",
                )

    numeric_columns = {
        "customers": ["age"],
        "vehicles": ["vehicle_year", "vehicle_value"],
        "policies": ["premium_amount", "coverage_amount"],
        "claims": ["claim_amount"],
        "payments": ["payment_amount"],
    }

    for table_name, columns in numeric_columns.items():
        if table_name not in data:
            continue

        for column in columns:
            if column in data[table_name].columns:
                data[table_name][column] = pd.to_numeric(
                    data[table_name][column],
                    errors="coerce",
                )

    return data


def create_derived_columns(data, analysis_date=None):
    """Create useful age, duration, and insurance ratio columns."""
    data = {name: df.copy() for name, df in data.items()}

    # Convert date columns before performing date calculations.
    for table_name, columns in DATE_COLUMNS.items():
        if table_name not in data:
            continue

        for column in columns:
            if column in data[table_name].columns:
                data[table_name][column] = pd.to_datetime(
                    data[table_name][column],
                    errors="coerce",
                )

    reference_date = (
        pd.Timestamp(analysis_date)
        if analysis_date is not None
        else pd.Timestamp.today().normalize()
    )

    # Customer age
    customers = data["customers"]

    if "date_of_birth" in customers.columns:
        dob = customers["date_of_birth"]

        customers["customer_age"] = (
            reference_date.year
            - dob.dt.year
            - (
                (reference_date.month < dob.dt.month)
                | (
                    (reference_date.month == dob.dt.month)
                    & (reference_date.day < dob.dt.day)
                )
            ).astype("Int64")
        )

        customers.loc[
            dob.isna() | (customers["customer_age"] < 0),
            "customer_age",
        ] = pd.NA

    # Vehicle age
    vehicles = data["vehicles"]

    if "vehicle_year" in vehicles.columns:
        vehicles["vehicle_year"] = pd.to_numeric(
            vehicles["vehicle_year"],
            errors="coerce",
        )

        vehicles["vehicle_age"] = (
            reference_date.year - vehicles["vehicle_year"]
        )

        vehicles.loc[
            vehicles["vehicle_year"].isna()
            | (vehicles["vehicle_age"] < 0),
            "vehicle_age",
        ] = pd.NA

    # Policy duration and status flag
    policies = data["policies"]

    if (
        "policy_start_date" in policies.columns
        and "policy_end_date" in policies.columns
    ):
        policies["policy_duration_days"] = (
            policies["policy_end_date"]
            - policies["policy_start_date"]
        ).dt.days

    if "policy_status" in policies.columns:
        policies["is_active_policy"] = (
            policies["policy_status"]
            .astype("string")
            .str.strip()
            .str.lower()
            .eq("active")
        )

    # Claim processing and settlement durations
    claims = data["claims"]

    if "claim_date" in claims.columns and "approval_date" in claims.columns:
        claims["claim_processing_days"] = (
            claims["approval_date"] - claims["claim_date"]
        ).dt.days

    if (
        "approval_date" in claims.columns
        and "settlement_date" in claims.columns
    ):
        claims["claim_settlement_days"] = (
            claims["settlement_date"] - claims["approval_date"]
        ).dt.days

    if (
        "claim_date" in claims.columns
        and "settlement_date" in claims.columns
    ):
        claims["total_claim_resolution_days"] = (
            claims["settlement_date"] - claims["claim_date"]
        ).dt.days

    # Claim amount relative to policy coverage
    if (
        "policy_id" in claims.columns
        and "policy_id" in policies.columns
        and "claim_amount" in claims.columns
        and "coverage_amount" in policies.columns
    ):
        coverage_lookup = policies.drop_duplicates(
            subset=["policy_id"]
        ).set_index("policy_id")["coverage_amount"]

        claims["coverage_amount"] = claims["policy_id"].map(
            coverage_lookup
        )

        claims["claim_to_coverage_ratio"] = (
            claims["claim_amount"]
            / claims["coverage_amount"].replace(0, pd.NA)
        )

    # Claim amount relative to premium
    if (
        "policy_id" in claims.columns
        and "policy_id" in policies.columns
        and "claim_amount" in claims.columns
        and "premium_amount" in policies.columns
    ):
        premium_lookup = policies.drop_duplicates(
            subset=["policy_id"]
        ).set_index("policy_id")["premium_amount"]

        claims["premium_amount"] = claims["policy_id"].map(
            premium_lookup
        )

        claims["claim_to_premium_ratio"] = (
            claims["claim_amount"]
            / claims["premium_amount"].replace(0, pd.NA)
        )

    # Payment amount relative to claim amount
    payments = data["payments"]

    if (
        "claim_id" in payments.columns
        and "claim_id" in claims.columns
        and "payment_amount" in payments.columns
        and "claim_amount" in claims.columns
    ):
        claim_amount_lookup = claims.drop_duplicates(
            subset=["claim_id"]
        ).set_index("claim_id")["claim_amount"]

        payments["claim_amount"] = payments["claim_id"].map(
            claim_amount_lookup
        )

        payments["paid_claim_ratio"] = (
            payments["payment_amount"]
            / payments["claim_amount"].replace(0, pd.NA)
        )

    return data


def clean_data(data, analysis_date=None):
    """Clean all datasets and create derived analytical columns."""
    logger.info("Starting data cleaning.")

    cleaned_data = {}

    for table_name, df in data.items():
        cleaned_df = clean_text_columns(df)

        key_columns = {
            "customers": "customer_id",
            "vehicles": "vehicle_id",
            "policies": "policy_id",
            "claims": "claim_id",
            "payments": "payment_id",
        }

        cleaned_df = remove_duplicates(
            cleaned_df,
            key=key_columns.get(table_name),
        )

        cleaned_data[table_name] = cleaned_df

    cleaned_data = convert_data_types(cleaned_data)

    cleaned_data = create_derived_columns(
        cleaned_data,
        analysis_date=analysis_date,
    )

    logger.info("Data cleaning completed.")

    return cleaned_data


def save_cleaned_data(data, output_dir):
    """Save cleaned datasets as CSV files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for table_name, df in data.items():
        output_file = output_path / f"{table_name}_cleaned.csv"

        df.to_csv(output_file, index=False)

        logger.info("Saved cleaned dataset: %s", output_file)

    return output_path