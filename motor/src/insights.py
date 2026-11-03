
import pandas as pd


def _format_amount(value):
    return f"{value:,.2f}"


def generate_portfolio_insights(data):
    policies = data["policies"]

    if policies.empty:
        return ["No policy data is available for analysis."]

    premium = pd.to_numeric(
        policies["premium_amount"], errors="coerce"
    ).sum()

    status_counts = policies["policy_status"].value_counts()
    highest_status = status_counts.idxmax()

    return [
        (
            f"PATTERN: {highest_status} is the most common policy status. "
            f"EVIDENCE: {int(status_counts.max())} policies have this status. "
            f"BUSINESS MEANING: This describes the current policy portfolio. "
            f"RECOMMENDATION: Review policy status distribution and "
            f"renewal opportunities."
        ),
        (
            f"PATTERN: Premium totals are available for the portfolio. "
            f"EVIDENCE: Total recorded premium is {_format_amount(premium)}. "
            f"BUSINESS MEANING: Premium totals indicate the recorded "
            f"premium volume, not necessarily cash collected. "
            f"RECOMMENDATION: Compare premium totals across policy types "
            f"and reporting periods."
        ),
    ]


def generate_claim_insights(data):
    claims = data["claims"]

    if claims.empty:
        return ["No claim data is available for analysis."]

    amounts = pd.to_numeric(
        claims["claim_amount"], errors="coerce"
    )
    total = amounts.sum()
    average = amounts.mean()

    status_counts = claims["claim_status"].value_counts()
    most_common_status = status_counts.idxmax()

    return [
        (
            f"PATTERN: Claim amounts vary across recorded claims. "
            f"EVIDENCE: Total claim amount is {_format_amount(total)} "
            f"and average claim amount is {_format_amount(average)}. "
            f"BUSINESS MEANING: These measures describe recorded claim "
            f"costs. RECOMMENDATION: Examine claim amounts by claim type, "
            f"vehicle type and damage severity."
        ),
        (
            f"PATTERN: {most_common_status} is the most common claim status. "
            f"EVIDENCE: {int(status_counts.max())} claims have this status. "
            f"BUSINESS MEANING: Claim status distribution describes the "
            f"recorded claim workflow. "
            f"RECOMMENDATION: Investigate pending and delayed claims "
            f"using their actual processing times."
        ),
    ]


def generate_premium_insights(data):
    policies = data["policies"]

    if policies.empty:
        return ["No policy premium data is available."]

    grouped = policies.groupby(
        "policy_type", dropna=False
    )["premium_amount"].sum()

    if grouped.empty:
        return ["No valid policy type premium totals are available."]

    highest_type = grouped.idxmax()
    highest_value = grouped.max()

    return [
        (
            f"PATTERN: {highest_type} has the highest recorded total "
            f"premium among policy types. "
            f"EVIDENCE: Its total is {_format_amount(highest_value)}. "
            f"BUSINESS MEANING: This type contributes the most recorded "
            f"premium in the current data. "
            f"RECOMMENDATION: Compare its claim costs and policy counts "
            f"before drawing conclusions about profitability."
        )
    ]


def generate_customer_insights(data):
    customers = data["customers"]
    claims = data["claims"]

    if customers.empty or claims.empty:
        return ["Customer and claim data are both required for this analysis."]

    customer_claims = claims.groupby("customer_id").agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum")
    )

    merged = customers.merge(
        customer_claims,
        on="customer_id",
        how="left",
        validate="one_to_one"
    )

    merged["claim_count"] = merged["claim_count"].fillna(0)
    merged["total_claim_amount"] = (
        merged["total_claim_amount"].fillna(0)
    )

    highest = merged.loc[merged["claim_count"].idxmax()]

    return [
        (
            f"PATTERN: The customer with the highest observed claim count "
            f"has {int(highest['claim_count'])} claims. "
            f"EVIDENCE: The customer's recorded total claim amount is "
            f"{_format_amount(highest['total_claim_amount'])}. "
            f"BUSINESS MEANING: Claim frequency varies between customers. "
            f"RECOMMENDATION: Review claim histories and exposure before "
            f"assessing customer risk."
        )
    ]


def generate_vehicle_insights(data):
    claims = data["claims"]
    policies = data["policies"]
    vehicles = data["vehicles"]

    merged = claims.merge(
        policies[["policy_id", "vehicle_id"]],
        on="policy_id",
        how="left",
        validate="many_to_one"
    ).merge(
        vehicles[["vehicle_id", "vehicle_type"]],
        on="vehicle_id",
        how="left",
        validate="many_to_one"
    )

    if merged.empty:
        return ["No linked vehicle claim data is available."]

    grouped = merged.groupby(
        "vehicle_type", dropna=False
    ).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum")
    )

    highest = grouped["total_claim_amount"].idxmax()
    row = grouped.loc[highest]

    return [
        (
            f"PATTERN: {highest} has the highest recorded total claim "
            f"amount among vehicle types. "
            f"EVIDENCE: {int(row['claim_count'])} claims total "
            f"{_format_amount(row['total_claim_amount'])}. "
            f"BUSINESS MEANING: Total claim cost may reflect claim "
            f"frequency, claim severity or the number of insured vehicles. "
            f"RECOMMENDATION: Compare per-policy claim costs and vehicle "
            f"exposure before changing underwriting decisions."
        )
    ]


def generate_risk_patterns(data):
    claims = data["claims"]

    if claims.empty:
        return ["No claims are available for risk pattern analysis."]

    amounts = pd.to_numeric(
        claims["claim_amount"], errors="coerce"
    ).dropna()

    if amounts.empty:
        return ["No valid claim amounts are available for risk analysis."]

    median_amount = amounts.median()
    high_amount_count = int((amounts > median_amount).sum())

    return [
        (
            f"PATTERN: Claim amounts can be compared against the median. "
            f"EVIDENCE: Median claim amount is "
            f"{_format_amount(median_amount)}; "
            f"{high_amount_count} claims are above the median. "
            f"BUSINESS MEANING: The median provides a reference point "
            f"for examining claim severity. "
            f"RECOMMENDATION: Investigate unusually large claims alongside "
            f"damage severity, claim type and supporting records."
        )
    ]


def generate_business_recommendations(data):
    recommendations = []

    recommendations.extend(generate_portfolio_insights(data))
    recommendations.extend(generate_claim_insights(data))
    recommendations.extend(generate_premium_insights(data))
    recommendations.extend(generate_customer_insights(data))
    recommendations.extend(generate_vehicle_insights(data))
    recommendations.extend(generate_risk_patterns(data))

    return recommendations