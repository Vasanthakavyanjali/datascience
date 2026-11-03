# ============================================================
# src/statistics.py
# Basic statistics: mean, median, mode, variance, quartiles,
# IQR, outliers, correlation, covariance.
# All simple pandas functions.
# ============================================================

import pandas as pd
import numpy as np

from config import OUTLIER_IQR_MULTIPLIER


# ------------------------------------------------------------
# BASIC STATISTICS (one column)
# ------------------------------------------------------------
def get_mean(series):
    """Average."""
    if series is None or len(series) == 0:
        return 0.0
    return round(float(series.mean()), 2)


def get_median(series):
    """Middle value."""
    if series is None or len(series) == 0:
        return 0.0
    return round(float(series.median()), 2)


def get_mode(series):
    """Most frequent value."""
    if series is None or len(series) == 0:
        return 0.0

    mode_result = series.mode()
    if len(mode_result) == 0:
        return 0.0

    return round(float(mode_result.iloc[0]), 2)


def get_variance(series):
    """Variance (spread of data)."""
    if series is None or len(series) < 2:
        return 0.0
    return round(float(series.var()), 2)


def get_std_dev(series):
    """Standard deviation (spread in same units as data)."""
    if series is None or len(series) < 2:
        return 0.0
    return round(float(series.std()), 2)


def get_min(series):
    """Smallest value."""
    if series is None or len(series) == 0:
        return 0.0
    return round(float(series.min()), 2)


def get_max(series):
    """Largest value."""
    if series is None or len(series) == 0:
        return 0.0
    return round(float(series.max()), 2)


# ------------------------------------------------------------
# QUARTILES AND IQR
# ------------------------------------------------------------
def get_quartiles(series):
    """
    Returns Q1, Q2, Q3.
    Q2 is the same as the median.
    """
    if series is None or len(series) == 0:
        return {"Q1": 0.0, "Q2": 0.0, "Q3": 0.0}

    q1 = float(series.quantile(0.25))
    q2 = float(series.quantile(0.50))
    q3 = float(series.quantile(0.75))

    return {
        "Q1": round(q1, 2),
        "Q2": round(q2, 2),
        "Q3": round(q3, 2),
    }


def get_iqr(series):
    """IQR = Q3 - Q1."""
    q = get_quartiles(series)
    return round(q["Q3"] - q["Q1"], 2)


def get_outlier_bounds(series, multiplier=OUTLIER_IQR_MULTIPLIER):
    """
    Returns lower and upper bounds for outliers.
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    """
    q = get_quartiles(series)
    iqr = q["Q3"] - q["Q1"]

    lower = q["Q1"] - multiplier * iqr
    upper = q["Q3"] + multiplier * iqr

    return round(lower, 2), round(upper, 2)


def count_outliers(series, multiplier=OUTLIER_IQR_MULTIPLIER):
    """How many values fall outside the outlier bounds."""
    if series is None or len(series) == 0:
        return 0

    lower, upper = get_outlier_bounds(series, multiplier)
    outliers = series[(series < lower) | (series > upper)]

    return int(len(outliers))


def get_outlier_rows(df, column, multiplier=OUTLIER_IQR_MULTIPLIER):
    """Return all rows where the column value is an outlier."""
    if df is None or column not in df.columns:
        return pd.DataFrame()

    lower, upper = get_outlier_bounds(df[column], multiplier)
    outliers = df[(df[column] < lower) | (df[column] > upper)]

    return outliers


# ------------------------------------------------------------
# CORRELATION AND COVARIANCE
# ------------------------------------------------------------
def get_correlation(df, col_x, col_y):
    """
    Pearson correlation between two columns.
    Value is between -1 and 1.
    """
    if df is None or col_x not in df.columns or col_y not in df.columns:
        return 0.0

    # Drop rows where either value is missing
    clean = df[[col_x, col_y]].dropna()

    if len(clean) < 2:
        return 0.0

    return round(float(clean[col_x].corr(clean[col_y])), 4)


def get_covariance(df, col_x, col_y):
    """
    Covariance between two columns.
    """
    if df is None or col_x not in df.columns or col_y not in df.columns:
        return 0.0

    clean = df[[col_x, col_y]].dropna()

    if len(clean) < 2:
        return 0.0

    return round(float(clean[col_x].cov(clean[col_y])), 2)


def interpret_correlation(value):
    """
    Returns a simple text explanation of a correlation value.
    """
    if value is None:
        return "Not enough data."

    value = abs(value)

    if value >= 0.80:
        return "Very strong relationship."
    elif value >= 0.60:
        return "Strong relationship."
    elif value >= 0.40:
        return "Moderate relationship."
    elif value >= 0.20:
        return "Weak relationship."
    else:
        return "Little or no relationship."


# ------------------------------------------------------------
# MASTER FUNCTION: Full statistics for one column
# ------------------------------------------------------------
def full_statistics(series):
    """
    Returns a dictionary with all main statistics for one column.
    """
    quartiles = get_quartiles(series)

    return {
        "mean": get_mean(series),
        "median": get_median(series),
        "mode": get_mode(series),
        "variance": get_variance(series),
        "std_dev": get_std_dev(series),
        "min": get_min(series),
        "max": get_max(series),
        "Q1": quartiles["Q1"],
        "Q2": quartiles["Q2"],
        "Q3": quartiles["Q3"],
        "IQR": get_iqr(series),
        "outlier_count": count_outliers(series),
    }


# ------------------------------------------------------------
# TEST BLOCK
# Run: python -m src.statistics
# ------------------------------------------------------------
if __name__ == "__main__":
    from src.data_loader import load_default_data
    from src.data_cleaning import clean_data

    print("Loading and cleaning data...")
    raw = load_default_data()
    df = clean_data(raw, verbose=False)

    if df is None:
        print("Could not load data.")
    else:
        print()
        print("=" * 50)
        print("STATISTICS FOR 'sales' COLUMN")
        print("=" * 50)

        stats = full_statistics(df["sales"])

        for key, value in stats.items():
            print(f"{key:15s}: {value}")

        print()
        print("=" * 50)
        print("CORRELATION (discount vs sales)")
        print("=" * 50)

        corr = get_correlation(df, "discount", "sales")
        print(f"Correlation : {corr}")
        print(f"Interpretation: {interpret_correlation(corr)}")

        cov = get_covariance(df, "discount", "sales")
        print(f"Covariance  : {cov}")