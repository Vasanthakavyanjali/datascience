# ============================================================
# src/validation.py
# ============================================================

'''
What is Validation?
---------------------
Before we trust the data, we ask simple questions:

Are all the columns there?

Are there missing values?

Are there duplicate orders?

Are quantities positive?

Are prices positive?

Are discounts between 0 and 100?

Important: We do NOT fix the data here. We only check and report. Fixing .



'''
import pandas as pd

from config import (
    REQUIRED_COLUMNS,
    MIN_QUANTITY,
    MIN_UNIT_PRICE,
    MIN_DISCOUNT,
    MAX_DISCOUNT,
)


# ------------------------------------------------------------
# CHECK 1: Are all required columns present?
# ------------------------------------------------------------
def check_required_columns(df):
    """
    Returns a list of required columns that are missing.
    If empty list -> all good.
    """
    if df is None:
        return list(REQUIRED_COLUMNS)

    missing = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)

    return missing


# ------------------------------------------------------------
# CHECK 2: Missing values in each column
# ------------------------------------------------------------
def check_missing_values(df):
    """
    Returns a DataFrame showing how many values are missing
    in each column.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    result = pd.DataFrame({
        "column": df.columns,
        "missing": [df[col].isna().sum() for col in df.columns],
    })

    # Add percentage
    total = len(df)
    result["missing_%"] = (result["missing"] / total * 100).round(2)

    # Show only columns that have missing values
    result = result[result["missing"] > 0]

    return result


# ------------------------------------------------------------
# CHECK 3: Duplicate order IDs
# ------------------------------------------------------------
def check_duplicate_orders(df):
    """
    Returns the number of duplicate order_id values.
    """
    if df is None or "order_id" not in df.columns:
        return 0

    duplicates = df["order_id"].duplicated().sum()
    return int(duplicates)


# ------------------------------------------------------------
# CHECK 4: Invalid quantity
# ------------------------------------------------------------
def check_invalid_quantity(df):
    """
    Returns rows where quantity is less than the minimum.
    """
    if df is None or "quantity" not in df.columns:
        return pd.DataFrame()

    # Make sure it's a number
    quantity = pd.to_numeric(df["quantity"], errors="coerce")

    invalid = df[quantity < MIN_QUANTITY]
    return invalid


# ------------------------------------------------------------
# CHECK 5: Invalid unit price
# ------------------------------------------------------------
def check_invalid_price(df):
    """
    Returns rows where unit_price is less than the minimum.
    """
    if df is None or "unit_price" not in df.columns:
        return pd.DataFrame()

    price = pd.to_numeric(df["unit_price"], errors="coerce")

    invalid = df[price < MIN_UNIT_PRICE]
    return invalid


# ------------------------------------------------------------
# CHECK 6: Invalid discount
# ------------------------------------------------------------
def check_invalid_discount(df):
    """
    Returns rows where discount is below 0 or above 100.
    """
    if df is None or "discount" not in df.columns:
        return pd.DataFrame()

    discount = pd.to_numeric(df["discount"], errors="coerce")

    invalid = df[(discount < MIN_DISCOUNT) | (discount > MAX_DISCOUNT)]
    return invalid


# ------------------------------------------------------------
# CHECK 7: Invalid or missing dates
# ------------------------------------------------------------
def check_invalid_dates(df):
    """
    Returns rows where order_date cannot be converted to a date.
    """
    if df is None or "order_date" not in df.columns:
        return pd.DataFrame()

    # Try to convert to date
    dates = pd.to_datetime(df["order_date"], errors="coerce")

    # Rows where conversion failed
    invalid = df[dates.isna()]
    return invalid


# ------------------------------------------------------------
# MASTER FUNCTION: Run all checks and return a report
# ------------------------------------------------------------
def run_all_checks(df):
    """
    Runs all validation checks and returns a dictionary
    with the results.
    """
    if df is None:
        return {
            "valid": False,
            "message": "No data to validate.",
            "missing_columns": list(REQUIRED_COLUMNS),
        }

    # Check 1: Missing columns
    missing_cols = check_required_columns(df)

    # If required columns are missing, stop early
    if missing_cols:
        return {
            "valid": False,
            "message": "Required columns are missing.",
            "missing_columns": missing_cols,
        }

    # Run the other checks
    report = {
        "valid": True,
        "message": "All required columns are present.",
        "missing_columns": [],

        "total_rows": len(df),

        "missing_values": check_missing_values(df),
        "duplicate_orders": check_duplicate_orders(df),

        "invalid_quantity_count": len(check_invalid_quantity(df)),
        "invalid_price_count": len(check_invalid_price(df)),
        "invalid_discount_count": len(check_invalid_discount(df)),
        "invalid_date_count": len(check_invalid_dates(df)),
    }

    return report


# ------------------------------------------------------------
# HELPER: Print the report nicely (for testing)
# ------------------------------------------------------------
def print_report(report):
    """
    Print the validation report in a readable way.
    """
    print("=" * 50)
    print("DATA VALIDATION REPORT")
    print("=" * 50)

    if not report["valid"]:
        print("STATUS: INVALID")
        print("Message:", report["message"])
        print("Missing columns:", report["missing_columns"])
        return

    print("STATUS: VALID")
    print("Message:", report["message"])
    print("Total rows:", report["total_rows"])
    print()

    print("Duplicate order IDs:", report["duplicate_orders"])
    print("Invalid quantity rows:", report["invalid_quantity_count"])
    print("Invalid price rows:", report["invalid_price_count"])
    print("Invalid discount rows:", report["invalid_discount_count"])
    print("Invalid date rows:", report["invalid_date_count"])
    print()

    missing = report["missing_values"]
    if missing.empty:
        print("No missing values.")
    else:
        print("Missing values:")
        print(missing.to_string(index=False))


# ------------------------------------------------------------
# TEST BLOCK
# Run: python -m src.validation
# ------------------------------------------------------------
if __name__ == "__main__":
    from src.data_loader import load_default_data

    print("Loading data...")
    df = load_default_data()

    if df is not None:
        report = run_all_checks(df)
        print_report(report)
    else:
        print("Could not load data.")