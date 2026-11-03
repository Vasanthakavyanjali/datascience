
import pandas as pd
import plotly.express as px


def _empty_figure(title):
    fig = px.scatter(title=title)
    fig.add_annotation(
        text="No data available for this chart",
        x=0.5, y=0.5, xref="paper", yref="paper",
        showarrow=False
    )
    return fig


def _bar(df, x, y, title, color=None, labels=None):
    if df.empty or x not in df or y not in df:
        return _empty_figure(title)

    fig = px.bar(
        df, x=x, y=y, color=color,
        title=title, labels=labels
    )
    fig.update_layout(template="plotly_white")
    return fig


def _donut(df, names, title):
    if df.empty or names not in df:
        return _empty_figure(title)

    fig = px.pie(df, names=names, title=title, hole=0.45)
    fig.update_layout(template="plotly_white")
    return fig


def _monthly(df, date_col, value_col, title, aggregation="sum"):
    if not {date_col, value_col}.issubset(df.columns):
        return _empty_figure(title)

    temp = df[[date_col, value_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp[value_col] = pd.to_numeric(temp[value_col], errors="coerce")
    temp = temp.dropna()

    if temp.empty:
        return _empty_figure(title)

    temp["month"] = temp[date_col].dt.to_period("M").astype(str)

    if aggregation == "count":
        grouped = temp.groupby("month").size().reset_index(name="value")
    else:
        grouped = temp.groupby("month")[value_col].sum().reset_index(name="value")

    fig = px.line(
        grouped, x="month", y="value",
        markers=True, title=title
    )
    fig.update_layout(template="plotly_white")
    return fig


def plot_policy_status(policies):
    counts = policies["policy_status"].value_counts(
        dropna=False
    ).rename_axis("status").reset_index(name="count")
    return _donut(counts, "status", "Policy Status Distribution")


def plot_policy_type_distribution(policies):
    counts = policies.groupby(
        "policy_type", dropna=False
    ).size().reset_index(name="policy_count")
    return _bar(
        counts, "policy_type", "policy_count",
        "Policy Type Distribution"
    )


def plot_premium_by_policy_type(policies):
    grouped = policies.groupby(
        "policy_type", dropna=False
    )["premium_amount"].sum().reset_index()
    return _bar(
        grouped, "policy_type", "premium_amount",
        "Total Premium by Policy Type"
    )


def plot_monthly_claims(claims):
    return _monthly(
        claims, "claim_date", "claim_id",
        "Monthly Claim Volume", aggregation="count"
    )


def plot_claim_status(claims):
    counts = claims["claim_status"].value_counts(
        dropna=False
    ).rename_axis("status").reset_index(name="count")
    return _donut(counts, "status", "Claim Status Distribution")


def plot_claim_type_distribution(claims):
    counts = claims.groupby(
        "claim_type", dropna=False
    ).size().reset_index(name="claim_count")
    return _bar(
        counts, "claim_type", "claim_count",
        "Claim Type Distribution"
    )


def plot_claim_amount_distribution(claims):
    if "claim_amount" not in claims:
        return _empty_figure("Claim Amount Distribution")

    values = pd.to_numeric(
        claims["claim_amount"], errors="coerce"
    ).dropna()

    if values.empty:
        return _empty_figure("Claim Amount Distribution")

    fig = px.histogram(
        values.to_frame(name="claim_amount"),
        x="claim_amount", nbins=30,
        title="Claim Amount Distribution"
    )
    fig.update_layout(template="plotly_white")
    return fig


def plot_claim_amount_by_vehicle_type(data):
    if isinstance(data, dict):
        claims = data["claims"].merge(
            data["policies"][["policy_id", "vehicle_id"]],
            on="policy_id", how="left", validate="many_to_one"
        ).merge(
            data["vehicles"][["vehicle_id", "vehicle_type"]],
            on="vehicle_id", how="left", validate="many_to_one"
        )
    else:
        claims = data

    if "vehicle_type" not in claims:
        return _empty_figure("Claim Amount by Vehicle Type")

    grouped = claims.groupby(
        "vehicle_type", dropna=False
    )["claim_amount"].sum().reset_index()

    return _bar(
        grouped, "vehicle_type", "claim_amount",
        "Total Claim Amount by Vehicle Type"
    )


def plot_claims_by_region(claims):
    if "accident_location" not in claims:
        return _empty_figure("Claims by Region")

    grouped = claims.groupby(
        "accident_location", dropna=False
    ).size().reset_index(name="claim_count")

    return _bar(
        grouped, "accident_location", "claim_count",
        "Claims by Accident Location"
    )


def plot_claim_severity_by_region(claims):
    if not {"accident_location", "damage_severity"}.issubset(claims.columns):
        return _empty_figure("Claim Severity by Region")

    grouped = claims.groupby(
        ["accident_location", "damage_severity"],
        dropna=False
    ).size().reset_index(name="claim_count")

    fig = px.bar(
        grouped, x="accident_location", y="claim_count",
        color="damage_severity", barmode="group",
        title="Claim Severity by Region"
    )
    fig.update_layout(template="plotly_white")
    return fig


def plot_average_settlement_time(claims):
    if "claim_settlement_days" in claims:
        temp = claims.copy()
    elif {"claim_date", "settlement_date"}.issubset(claims.columns):
        temp = claims.copy()
        temp["claim_settlement_days"] = (
            pd.to_datetime(temp["settlement_date"], errors="coerce")
            - pd.to_datetime(temp["claim_date"], errors="coerce")
        ).dt.days
    else:
        return _empty_figure("Average Settlement Time")

    temp["claim_settlement_days"] = pd.to_numeric(
        temp["claim_settlement_days"], errors="coerce"
    )
    temp = temp[temp["claim_settlement_days"] >= 0]

    if "claim_type" in temp:
        grouped = temp.groupby(
            "claim_type", dropna=False
        )["claim_settlement_days"].mean().reset_index()
        return _bar(
            grouped, "claim_type", "claim_settlement_days",
            "Average Settlement Days by Claim Type"
        )

    grouped = pd.DataFrame({
        "group": ["All Settled Claims"],
        "average_days": [temp["claim_settlement_days"].mean()]
    })
    return _bar(
        grouped, "group", "average_days",
        "Average Settlement Time"
    )


def plot_claim_to_premium_by_policy_type(data):
    claims = data["claims"]
    policies = data["policies"]

    if not {"policy_id", "claim_amount"}.issubset(claims.columns):
        return _empty_figure("Claim-to-Premium Ratio")

    claim_totals = claims.groupby("policy_id")[
        "claim_amount"
    ].sum().reset_index()

    grouped = policies.merge(
        claim_totals, on="policy_id", how="left",
        validate="one_to_one"
    )
    grouped["claim_amount"] = grouped["claim_amount"].fillna(0)
    grouped["ratio"] = (
        grouped["claim_amount"]
        / grouped["premium_amount"].where(
            pd.to_numeric(grouped["premium_amount"], errors="coerce") != 0
        )
    )

    result = grouped.groupby(
        "policy_type", dropna=False
    ).agg(
        claim_amount=("claim_amount", "sum"),
        premium_amount=("premium_amount", "sum")
    ).reset_index()

    result["ratio"] = (
        result["claim_amount"]
        / result["premium_amount"].where(
            result["premium_amount"] != 0
        )
    )

    return _bar(
        result, "policy_type", "ratio",
        "Aggregate Claim-to-Premium Ratio by Policy Type"
    )


def plot_vehicle_age_vs_claim_amount(data):
    merged = data["claims"].merge(
        data["policies"][["policy_id", "vehicle_id"]],
        on="policy_id", how="left", validate="many_to_one"
    ).merge(
        data["vehicles"][["vehicle_id", "vehicle_year"]],
        on="vehicle_id", how="left", validate="many_to_one"
    )

    current_year = pd.Timestamp.today().year
    merged["vehicle_age"] = current_year - pd.to_numeric(
        merged["vehicle_year"], errors="coerce"
    )

    fig = px.scatter(
        merged, x="vehicle_age", y="claim_amount",
        title="Vehicle Age vs Claim Amount",
        hover_data=["claim_id"]
    )
    fig.update_layout(template="plotly_white")
    return fig


def plot_customer_age_vs_claim_amount(data):
    merged = data["claims"].merge(
        data["customers"][["customer_id", "date_of_birth"]],
        on="customer_id", how="left", validate="many_to_one"
    )

    dob = pd.to_datetime(merged["date_of_birth"], errors="coerce")
    today = pd.Timestamp.today()
    merged["customer_age"] = (
        today.year - dob.dt.year
        - (
            (today.month < dob.dt.month)
            | (
                (today.month == dob.dt.month)
                & (today.day < dob.dt.day)
            )
        )
    )

    fig = px.scatter(
        merged, x="customer_age", y="claim_amount",
        title="Customer Age vs Claim Amount",
        hover_data=["claim_id"]
    )
    fig.update_layout(template="plotly_white")
    return fig


def plot_vehicle_type_claim_performance(data):
    grouped = data["claims"].merge(
        data["policies"][["policy_id", "vehicle_id"]],
        on="policy_id", how="left", validate="many_to_one"
    ).merge(
        data["vehicles"][["vehicle_id", "vehicle_type"]],
        on="vehicle_id", how="left", validate="many_to_one"
    ).groupby("vehicle_type", dropna=False).agg(
        claim_count=("claim_id", "nunique"),
        total_claim_amount=("claim_amount", "sum")
    ).reset_index()

    fig = px.bar(
        grouped, x="vehicle_type",
        y=["claim_count", "total_claim_amount"],
        barmode="group",
        title="Vehicle Type Claim Performance"
    )
    fig.update_layout(template="plotly_white")
    return fig


def plot_damage_severity_distribution(claims):
    counts = claims["damage_severity"].value_counts(
        dropna=False
    ).rename_axis("severity").reset_index(name="claim_count")
    return _bar(
        counts, "severity", "claim_count",
        "Damage Severity Distribution"
    )


def plot_payment_status(payments):
    counts = payments["payment_status"].value_counts(
        dropna=False
    ).rename_axis("status").reset_index(name="count")
    return _donut(counts, "status", "Payment Status Distribution")


def plot_monthly_premium_trend(policies):
    return _monthly(
        policies, "policy_start_date", "premium_amount",
        "Monthly Premium by Policy Start Date"
    )