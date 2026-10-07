# ============================================================
# tests/test_statistics.py
# Tests for statistics module.
# ============================================================

import pandas as pd

from src.statistics import (
    get_mean,
    get_median,
    get_mode,
    get_variance,
    get_std_dev,
    get_quartiles,
    get_iqr,
    get_outlier_bounds,
    count_outliers,
    get_correlation,
    get_covariance,
    interpret_correlation,
    full_statistics,
)


# ------------------------------------------------------------
# Small fixed dataset
# ------------------------------------------------------------
def make_series():
    # Values: 10, 20, 20, 30, 40
    return pd.Series([10, 20, 20, 30, 40])


# ------------------------------------------------------------
# Test: Mean
# ------------------------------------------------------------
def test_mean():
    s = make_series()
    # (10 + 20 + 20 + 30 + 40) / 5 = 24
    assert get_mean(s) == 24.0


# ------------------------------------------------------------
# Test: Median
# ------------------------------------------------------------
def test_median():
    s = make_series()
    # Middle value = 20
    assert get_median(s) == 20.0


# ------------------------------------------------------------
# Test: Mode (most frequent)
# ------------------------------------------------------------
def test_mode():
    s = make_series()
    # 20 appears twice, others once
    assert get_mode(s) == 20.0


# ------------------------------------------------------------
# Test: Variance (sample)
# ------------------------------------------------------------
def test_variance():
    s = make_series()
    # Sample variance = 130
    assert get_variance(s) == 130.0


# ------------------------------------------------------------
# Test: Standard deviation
# ------------------------------------------------------------
def test_std_dev():
    s = make_series()
    # sqrt(130) ≈ 11.4018 -> rounded to 11.4
    assert abs(get_std_dev(s) - 11.4) < 0.1


# ------------------------------------------------------------
# Test: Quartiles
# ------------------------------------------------------------
def test_quartiles():
    s = make_series()
    q = get_quartiles(s)
    # Q1 = 20, Q2 = 20, Q3 = 30
    assert q["Q1"] == 20.0
    assert q["Q2"] == 20.0
    assert q["Q3"] == 30.0


# ------------------------------------------------------------
# Test: IQR
# ------------------------------------------------------------
def test_iqr():
    s = make_series()
    # Q3 - Q1 = 30 - 20 = 10
    assert get_iqr(s) == 10.0


# ------------------------------------------------------------
# Test: Outlier bounds
# ------------------------------------------------------------
def test_outlier_bounds():
    s = make_series()
    # Q1 = 20, Q3 = 30, IQR = 10
    # Lower = 20 - 15 = 5
    # Upper = 30 + 15 = 45
    lower, upper = get_outlier_bounds(s)
    assert lower == 5.0
    assert upper == 45.0


# ------------------------------------------------------------
# Test: Count outliers (this data has none)
# ------------------------------------------------------------
def test_count_outliers_none():
    s = make_series()
    assert count_outliers(s) == 0


# ------------------------------------------------------------
# Test: Count outliers (with a value outside bounds)
# ------------------------------------------------------------
def test_count_outliers_with_outlier():
    s = pd.Series([10, 20, 20, 30, 40, 1000])
    assert count_outliers(s) >= 1


# ------------------------------------------------------------
# Test: Correlation (perfect positive)
# ------------------------------------------------------------
def test_correlation_perfect_positive():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 6, 8, 10],
    })
    assert get_correlation(df, "x", "y") == 1.0


# ------------------------------------------------------------
# Test: Correlation (perfect negative)
# ------------------------------------------------------------
def test_correlation_perfect_negative():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [10, 8, 6, 4, 2],
    })
    assert get_correlation(df, "x", "y") == -1.0


# ------------------------------------------------------------
# Test: Covariance
# ------------------------------------------------------------
def test_covariance_positive():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 6, 8, 10],
    })
    assert get_covariance(df, "x", "y") > 0


# ------------------------------------------------------------
# Test: interpret_correlation text
# ------------------------------------------------------------
def test_interpret_correlation():
    assert "Very strong" in interpret_correlation(0.9)
    assert "Strong" in interpret_correlation(0.7)
    assert "Moderate" in interpret_correlation(0.5)
    assert "Weak" in interpret_correlation(0.3)
    assert "no relationship" in interpret_correlation(0.05)


# ------------------------------------------------------------
# Test: full_statistics returns all keys
# ------------------------------------------------------------
def test_full_statistics():
    s = make_series()
    stats = full_statistics(s)

    required_keys = ["mean", "median", "mode", "variance", "std_dev",
                     "min", "max", "Q1", "Q2", "Q3", "IQR", "outlier_count"]

    for key in required_keys:
        assert key in stats