
import pandas as pd
import numpy as np


def _number(series):
    return pd.to_numeric(series, errors="coerce")


def _sum(df, column):
    return float(_number(df[column]).sum()) if column in df else 0.0


def _mean(df, column):
    return float(_number(df[column]).mean()) if column in df else 0.0


def _unique_count(df, column):
    return int(df[column].nunique()) if column in df else 0


def _status_count(df, column, status):
    if column not in df:
        return 0
    return int(
        df[column].astype("string").str.strip()
        .str.casefold().eq(status.casefold()).sum()
    )


def calculate_total_customers(customers):
    return _unique_count(customers, "customer_id")


def calculate_total_policies(policies):
    return _unique_count(policies, "policy_id")


def calculate_active_policies(policies):
    return _status_count(policies, "policy_status", "Active")


def calculate_expired_policies(policies):
    return _status_count(policies, "policy_status", "Expired")


def calculate_cancelled_policies(policies):
    return _status_count(policies, "policy_status", "Cancelled")


def calculate_renewed_policies(policies):
    return _status_count(policies, "policy_status", "Renewed")


def calculate_total_premium(policies):
    return _sum(policies, "premium_amount")


def calculate_average_premium(policies):
    return _mean(policies, "premium_amount")


def calculate_average_coverage(policies):
    return _mean(policies, "coverage_amount")


def calculate_total_claims(claims):
    return _unique_count(claims, "claim_id")


def calculate_total_claim_amount(claims):
    return _sum(claims, "claim_amount")


def calculate_average_claim_amount(claims):
    return _mean(claims, "claim_amount")


def calculate_claim_approval_rate(claims):
    if claims.empty or "claim_status" not in claims:
        return 0.0

    approved = _status_count(claims, "claim_status", "Approved")
    return approved / len(claims) * 100


def calculate_claim_rejection_rate(claims):
    if claims.empty or "claim_status" not in claims:
        return 0.0

    rejected = _status_count(claims, "claim_status", "Rejected")
    return rejected / len(claims) * 100


def calculate_average_processing_days(claims):
    if "claim_processing_days" in claims:
        values = _number(claims["claim_processing_days"])
    elif {"claim_date", "approval_date"}.issubset(claims.columns):
        values = (
            pd.to_datetime(claims["approval_date"], errors="coerce")
            - pd.to_datetime(claims["claim_date"], errors="coerce")
        ).dt.days
    else:
        return 0.0

    valid = values[values >= 0]
    return float(valid.mean()) if not valid.empty else 0.0


def calculate_average_settlement_days(claims):
    if "claim_settlement_days" in claims:
        values = _number(claims["claim_settlement_days"])
    elif {"claim_date", "settlement_date"}.issubset(claims.columns):
        values = (
            pd.to_datetime(claims["settlement_date"], errors="coerce")
            - pd.to_datetime(claims["claim_date"], errors="coerce")
        ).dt.days
    else:
        return 0.0

    valid = values[values >= 0]
    return float(valid.mean()) if not valid.empty else 0.0


def calculate_total_payment_amount(payments):
    return _sum(payments, "payment_amount")


def calculate_average_payment_amount(payments):
    return _mean(payments, "payment_amount")


def calculate_claim_to_premium_ratio(claims, policies):
    premium = calculate_total_premium(policies)
    return (
        calculate_total_claim_amount(claims) / premium
        if premium > 0 else 0.0
    )


def calculate_claim_to_coverage_ratio(claims, policies):
    coverage = _sum(policies, "coverage_amount")
    return (
        calculate_total_claim_amount(claims) / coverage
        if coverage > 0 else 0.0
    )


def calculate_paid_claim_ratio(claims, payments):
    total_claims = calculate_total_claim_amount(claims)
    return (
        calculate_total_payment_amount(payments) / total_claims
        if total_claims > 0 else 0.0
    )


def calculate_kpis(data):
    customers = data["customers"]
    policies = data["policies"]
    claims = data["claims"]
    payments = data["payments"]

    return {
        "total_customers": calculate_total_customers(customers),
        "total_policies": calculate_total_policies(policies),
        "active_policies": calculate_active_policies(policies),
        "expired_policies": calculate_expired_policies(policies),
        "cancelled_policies": calculate_cancelled_policies(policies),
        "renewed_policies": calculate_renewed_policies(policies),
        "total_premium": calculate_total_premium(policies),
        "average_premium": calculate_average_premium(policies),
        "average_coverage": calculate_average_coverage(policies),
        "total_claims": calculate_total_claims(claims),
        "total_claim_amount": calculate_total_claim_amount(claims),
        "average_claim_amount": calculate_average_claim_amount(claims),
        "claim_approval_rate": calculate_claim_approval_rate(claims),
        "claim_rejection_rate": calculate_claim_rejection_rate(claims),
        "average_processing_days": calculate_average_processing_days(claims),
        "average_settlement_days": calculate_average_settlement_days(claims),
        "total_payment_amount": calculate_total_payment_amount(payments),
        "average_payment_amount": calculate_average_payment_amount(payments),
        "claim_to_premium_ratio": calculate_claim_to_premium_ratio(claims, policies),
        "claim_to_coverage_ratio": calculate_claim_to_coverage_ratio(claims, policies),
        "paid_claim_ratio": calculate_paid_claim_ratio(claims, payments),
    }


def analyze_claims_by_type(claims):
    return claims.groupby("claim_type", dropna=False).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index()


def analyze_claims_by_status(claims):
    return claims.groupby("claim_status", dropna=False).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum"),
    ).reset_index()


def analyze_policies_by_type(policies):
    return policies.groupby("policy_type", dropna=False).agg(
        policy_count=("policy_id", "nunique"),
        total_premium=("premium_amount", "sum"),
        average_premium=("premium_amount", "mean"),
        average_coverage=("coverage_amount", "mean"),
    ).reset_index()


def analyze_claims_by_region(claims):
    region = (
        "accident_location"
        if "accident_location" in claims.columns else None
    )
    if region is None:
        return pd.DataFrame()

    return claims.groupby(region, dropna=False).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index()


def analyze_claims_by_vehicle_type(data):
    merged = data["claims"].merge(
        data["policies"][["policy_id", "vehicle_id"]],
        on="policy_id", how="left", validate="many_to_one"
    ).merge(
        data["vehicles"][["vehicle_id", "vehicle_type"]],
        on="vehicle_id", how="left", validate="many_to_one"
    )

    return merged.groupby("vehicle_type", dropna=False).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index()


def analyze_customer_claims(data):
    return data["claims"].groupby(
        "customer_id", dropna=False
    ).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index()


def analyze_customer_premiums(data):
    return data["policies"].groupby(
        "customer_id", dropna=False
    ).agg(
        policy_count=("policy_id", "nunique"),
        total_premium=("premium_amount", "sum"),
        average_premium=("premium_amount", "mean"),
    ).reset_index()


def analyze_vehicle_claims(data):
    claims = data["claims"].merge(
        data["policies"][["policy_id", "vehicle_id"]],
        on="policy_id", how="left", validate="many_to_one"
    )
    return claims.groupby("vehicle_id", dropna=False).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index()


def analyze_damage_severity(claims):
    return claims.groupby("damage_severity", dropna=False).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum"),
        average_claim_amount=("claim_amount", "mean"),
    ).reset_index()