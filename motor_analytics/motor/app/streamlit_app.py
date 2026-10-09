import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_all_data
from src.data_cleaner import clean_data
from src.insurance_analysis import calculate_kpis

from src.insights import (
    generate_portfolio_insights,
    generate_claim_insights,
    generate_premium_insights,
    generate_customer_insights,
    generate_vehicle_insights,
    generate_risk_patterns,
)

from src.visualization import (
    plot_policy_status,
    plot_policy_type_distribution,
    plot_premium_by_policy_type,
    plot_monthly_claims,
    plot_claim_status,
    plot_claim_type_distribution,
    plot_claim_amount_distribution,
    plot_claim_amount_by_vehicle_type,
    plot_claims_by_region,
    plot_claim_severity_by_region,
    plot_average_settlement_time,
    plot_claim_to_premium_by_policy_type,
    plot_vehicle_age_vs_claim_amount,
    plot_customer_age_vs_claim_amount,
    plot_vehicle_type_claim_performance,
    plot_damage_severity_distribution,
    plot_payment_status,
    plot_monthly_premium_trend,
)


st.set_page_config(
    page_title="Motor Insurance Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_dashboard_data():
    raw_data = load_all_data()
    return clean_data(raw_data)


def format_number(value):
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)


def filter_values(df, column):
    if column not in df.columns:
        return []

    return sorted(
        df[column].dropna().astype(str).unique().tolist()
    )


def filter_dataframe(df, column, selected_values):
    """Apply a multiselect only when values are selected."""
    if selected_values and column in df.columns:
        return df[df[column].astype(str).isin(selected_values)].copy()

    return df.copy()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

def apply_filters(data):
    filtered = {
        name: df.copy()
        for name, df in data.items()
    }

    st.sidebar.markdown("## 🔎 Dashboard Filters")
    st.sidebar.caption(
        "Select your criteria and apply them to the dashboard."
    )

    filter_keys = [
        "motor_policy_types",
        "motor_policy_statuses",
        "motor_vehicle_types",
        "motor_vehicle_makes",
        "motor_states",
        "motor_cities",
        "motor_claim_statuses",
        "motor_claim_types",
        "motor_severities",
        "motor_date_type",
        "motor_date_range",
    ]

    if st.sidebar.button(
        "↺ Reset Filters",
        use_container_width=True,
    ):
        for key in filter_keys:
            st.session_state.pop(key, None)

    customers_all = filtered["customers"]
    vehicles_all = filtered["vehicles"]
    policies_all = filtered["policies"]
    claims_all = filtered["claims"]

    with st.sidebar.form("motor_insurance_filters"):

        with st.expander("📄 Policy Filters", expanded=True):
            policy_types = st.multiselect(
                "Policy Type",
                filter_values(policies_all, "policy_type"),
                key="motor_policy_types",
                placeholder="All policy types",
            )

            policy_statuses = st.multiselect(
                "Policy Status",
                filter_values(policies_all, "policy_status"),
                key="motor_policy_statuses",
                placeholder="All policy statuses",
            )

        with st.expander("🚘 Vehicle Filters", expanded=False):
            vehicle_types = st.multiselect(
                "Vehicle Type",
                filter_values(vehicles_all, "vehicle_type"),
                key="motor_vehicle_types",
                placeholder="All vehicle types",
            )

            vehicle_makes = st.multiselect(
                "Vehicle Make",
                filter_values(vehicles_all, "vehicle_make"),
                key="motor_vehicle_makes",
                placeholder="All vehicle makes",
            )

        with st.expander("📍 Customer Location", expanded=False):
            states = st.multiselect(
                "State",
                filter_values(customers_all, "state"),
                key="motor_states",
                placeholder="All states",
            )

            cities = st.multiselect(
                "City",
                filter_values(customers_all, "city"),
                key="motor_cities",
                placeholder="All cities",
            )

        with st.expander("📝 Claim Filters", expanded=False):
            claim_statuses = st.multiselect(
                "Claim Status",
                filter_values(claims_all, "claim_status"),
                key="motor_claim_statuses",
                placeholder="All claim statuses",
            )

            claim_types = st.multiselect(
                "Claim Type",
                filter_values(claims_all, "claim_type"),
                key="motor_claim_types",
                placeholder="All claim types",
            )

            severities = st.multiselect(
                "Damage Severity",
                filter_values(claims_all, "damage_severity"),
                key="motor_severities",
                placeholder="All damage severities",
            )

        with st.expander("📅 Date Filter", expanded=False):
            date_options = [
                ("Policy Start Date", "policies", "policy_start_date"),
                ("Claim Date", "claims", "claim_date"),
            ]

            date_labels = [item[0] for item in date_options]

            date_choice = st.selectbox(
                "Filter date by",
                date_labels,
                key="motor_date_type",
            )

            _, date_table, date_column = next(
                item for item in date_options
                if item[0] == date_choice
            )

            date_df = filtered[date_table]
            date_range = None

            if date_column in date_df.columns and not date_df.empty:
                valid_dates = pd.to_datetime(
                    date_df[date_column],
                    errors="coerce",
                ).dropna()

                if not valid_dates.empty:
                    min_date = valid_dates.min().date()
                    max_date = valid_dates.max().date()

                    date_range = st.date_input(
                        "Date range",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date,
                        key="motor_date_range",
                    )

        st.form_submit_button(
            "✓ Apply Filters",
            type="primary",
            use_container_width=True,
        )

    # --------------------------------------------------
    # FILTER CUSTOMERS
    # --------------------------------------------------

    customers = filter_dataframe(
        customers_all, "state", states
    )

    customers = filter_dataframe(
        customers, "city", cities
    )

    # --------------------------------------------------
    # FILTER VEHICLES
    # --------------------------------------------------

    vehicles = filter_dataframe(
        vehicles_all, "vehicle_type", vehicle_types
    )

    vehicles = filter_dataframe(
        vehicles, "vehicle_make", vehicle_makes
    )

    # --------------------------------------------------
    # FILTER POLICIES
    # --------------------------------------------------

    policies = filter_dataframe(
        policies_all, "policy_type", policy_types
    )

    policies = filter_dataframe(
        policies, "policy_status", policy_statuses
    )

    if "customer_id" in policies.columns:
        policies = policies[
            policies["customer_id"].isin(customers["customer_id"])
        ]

    if "vehicle_id" in policies.columns:
        policies = policies[
            policies["vehicle_id"].isin(vehicles["vehicle_id"])
        ]

    # --------------------------------------------------
    # FILTER BY DATE
    # --------------------------------------------------

    if (
        isinstance(date_range, (tuple, list))
        and len(date_range) == 2
        and date_range[0] is not None
        and date_range[1] is not None
    ):
        start_date, end_date = date_range

        if start_date <= end_date:
            if date_table == "policies":
                if date_column in policies.columns:
                    dates = pd.to_datetime(
                        policies[date_column],
                        errors="coerce",
                    ).dt.date

                    policies = policies[
                        dates.notna()
                        & dates.between(start_date, end_date)
                    ]

            elif date_table == "claims":
                if date_column in claims_all.columns:
                    dates = pd.to_datetime(
                        claims_all[date_column],
                        errors="coerce",
                    ).dt.date

                    claims_all = claims_all[
                        dates.notna()
                        & dates.between(start_date, end_date)
                    ]

    # --------------------------------------------------
    # FILTER CLAIMS
    # --------------------------------------------------

    claims = claims_all.copy()

    if "policy_id" in claims.columns:
        claims = claims[
            claims["policy_id"].isin(policies["policy_id"])
        ]

    claims = filter_dataframe(
        claims, "claim_status", claim_statuses
    )

    claims = filter_dataframe(
        claims, "claim_type", claim_types
    )

    claims = filter_dataframe(
        claims, "damage_severity", severities
    )

    # --------------------------------------------------
    # FILTER RELATED TABLES
    # --------------------------------------------------

    if "vehicle_id" in policies.columns:
        vehicles = vehicles[
            vehicles["vehicle_id"].isin(policies["vehicle_id"])
        ]

    payments = filtered["payments"].copy()

    if "claim_id" in payments.columns:
        payments = payments[
            payments["claim_id"].isin(claims["claim_id"])
        ]

    filtered["customers"] = customers
    filtered["vehicles"] = vehicles
    filtered["policies"] = policies
    filtered["claims"] = claims
    filtered["payments"] = payments

    st.sidebar.divider()
    st.sidebar.markdown("### 📊 Filtered Records")

    st.sidebar.metric("Customers", f"{len(customers):,}")
    st.sidebar.metric("Policies", f"{len(policies):,}")
    st.sidebar.metric("Claims", f"{len(claims):,}")

    return filtered


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

def show_kpis(data):
    kpis = calculate_kpis(data)

    rows = [
        ("Total Customers", "total_customers"),
        ("Total Policies", "total_policies"),
        ("Active Policies", "active_policies"),
        ("Total Premium", "total_premium"),
        ("Total Claims", "total_claims"),
        ("Total Claim Amount", "total_claim_amount"),
        ("Approval Rate (%)", "claim_approval_rate"),
        ("Average Settlement Days", "average_settlement_days"),
    ]

    columns = st.columns(4)

    for index, (label, key) in enumerate(rows):
        value = kpis.get(key, 0)

        with columns[index % 4]:
            st.metric(label, format_number(value))


# --------------------------------------------------
# CHART HELPER
# --------------------------------------------------

def show_chart(fig, caption=None, table=None):
    if fig is not None:
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    if caption:
        st.caption(caption)

    if table is not None and not table.empty:
        with st.expander("View chart data"):
            st.dataframe(
                table,
                use_container_width=True,
            )


# --------------------------------------------------
# EXECUTIVE OVERVIEW
# --------------------------------------------------

def executive_overview(data):
    st.header("Executive Overview")

    show_kpis(data)

    left, right = st.columns(2)

    with left:
        show_chart(
            plot_policy_status(data["policies"]),
            "Distribution of recorded policy statuses.",
        )

    with right:
        show_chart(
            plot_claim_status(data["claims"]),
            "Distribution of recorded claim statuses.",
        )

    st.subheader("Portfolio Insights")

    for insight in generate_portfolio_insights(data):
        st.write(insight)

    st.subheader("Claim Insights")

    for insight in generate_claim_insights(data):
        st.write(insight)


# --------------------------------------------------
# POLICY ANALYSIS
# --------------------------------------------------

def policy_analysis(data):
    st.header("Policy Analysis")

    col1, col2 = st.columns(2)

    with col1:
        show_chart(
            plot_policy_type_distribution(data["policies"])
        )

    with col2:
        show_chart(
            plot_premium_by_policy_type(data["policies"])
        )

    show_chart(
        plot_monthly_premium_trend(data["policies"])
    )

    if not data["policies"].empty:
        summary = data["policies"].groupby(
            "policy_type",
            dropna=False,
        ).agg(
            policy_count=("policy_id", "nunique"),
            total_premium=("premium_amount", "sum"),
            average_premium=("premium_amount", "mean"),
        ).reset_index()

        st.subheader("Policy Summary")
        st.dataframe(summary, use_container_width=True)

    st.subheader("Premium Insights")

    for insight in generate_premium_insights(data):
        st.write(insight)


# --------------------------------------------------
# CLAIMS ANALYSIS
# --------------------------------------------------

def claims_analysis(data):
    st.header("Claims Analysis")

    col1, col2 = st.columns(2)

    with col1:
        show_chart(
            plot_claim_type_distribution(data["claims"])
        )

    with col2:
        show_chart(
            plot_claim_amount_distribution(data["claims"])
        )

    col3, col4 = st.columns(2)

    with col3:
        show_chart(
            plot_claim_amount_by_vehicle_type(data)
        )

    with col4:
        show_chart(
            plot_claims_by_region(data["claims"])
        )

    col5, col6 = st.columns(2)

    with col5:
        show_chart(
            plot_claim_severity_by_region(data["claims"])
        )

    with col6:
        show_chart(
            plot_average_settlement_time(data["claims"])
        )

    show_chart(
        plot_monthly_claims(data["claims"])
    )

    if not data["claims"].empty:
        summary = data["claims"].groupby(
            "claim_status",
            dropna=False,
        ).agg(
            claim_count=("claim_id", "nunique"),
            total_claim_amount=("claim_amount", "sum"),
            average_claim_amount=("claim_amount", "mean"),
        ).reset_index()

        st.subheader("Claim Summary")
        st.dataframe(summary, use_container_width=True)


# --------------------------------------------------
# CUSTOMER ANALYSIS
# --------------------------------------------------

def customer_analysis(data):
    st.header("Customer Analysis")

    customers = data["customers"].copy()
    claims = data["claims"].copy()

    if (
        "customer_age" not in customers.columns
        and "date_of_birth" in customers.columns
    ):
        dob = pd.to_datetime(
            customers["date_of_birth"],
            errors="coerce",
        )

        customers["customer_age"] = (
            pd.Timestamp.today().year - dob.dt.year
        )

    if not customers.empty:
        st.subheader("Customer Demographics")

        if "gender" in customers.columns:
            gender_summary = (
                customers["gender"]
                .value_counts(dropna=False)
                .rename_axis("gender")
                .reset_index(name="customer_count")
            )

            st.dataframe(
                gender_summary,
                use_container_width=True,
            )

        if "customer_age" in customers.columns:
            age_data = customers.dropna(
                subset=["customer_age"]
            )

            if not age_data.empty:
                fig = px.histogram(
                    age_data,
                    x="customer_age",
                    title="Customer Age Distribution",
                    labels={
                        "customer_age": "Customer Age",
                        "count": "Number of Customers",
                    },
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

    show_chart(
        plot_customer_age_vs_claim_amount(data)
    )

    st.subheader("Customer Claim Summary")

    if not claims.empty:
        customer_claims = claims.groupby(
            "customer_id"
        ).agg(
            claim_count=("claim_id", "nunique"),
            total_claim_amount=("claim_amount", "sum"),
            average_claim_amount=("claim_amount", "mean"),
        ).reset_index()

        st.dataframe(
            customer_claims,
            use_container_width=True,
        )

    for insight in generate_customer_insights(data):
        st.write(insight)


# --------------------------------------------------
# VEHICLE ANALYSIS
# --------------------------------------------------

def vehicle_analysis(data):
    st.header("Vehicle Analysis")

    col1, col2 = st.columns(2)

    with col1:
        show_chart(
            plot_vehicle_age_vs_claim_amount(data)
        )

    with col2:
        show_chart(
            plot_vehicle_type_claim_performance(data)
        )

    vehicles = data["vehicles"]

    if not vehicles.empty:
        st.subheader("Vehicle Summary")

        required_columns = {
            "vehicle_type",
            "vehicle_id",
            "vehicle_value",
            "vehicle_year",
        }

        if required_columns.issubset(vehicles.columns):
            vehicle_summary = vehicles.groupby(
                "vehicle_type",
                dropna=False,
            ).agg(
                vehicle_count=("vehicle_id", "nunique"),
                average_vehicle_value=("vehicle_value", "mean"),
                average_vehicle_year=("vehicle_year", "mean"),
            ).reset_index()

            st.dataframe(
                vehicle_summary,
                use_container_width=True,
            )

    for insight in generate_vehicle_insights(data):
        st.write(insight)


# --------------------------------------------------
# PREMIUM AND RISK ANALYSIS
# --------------------------------------------------

def premium_risk_analysis(data):
    st.header("Premium & Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:
        show_chart(
            plot_claim_to_premium_by_policy_type(data)
        )

    with col2:
        show_chart(
            plot_damage_severity_distribution(data["claims"])
        )

    kpis = calculate_kpis(data)

    st.subheader("Premium and Risk Metrics")

    metrics = [
        ("Total Premium", "total_premium"),
        ("Total Claim Amount", "total_claim_amount"),
        ("Average Premium", "average_premium"),
        ("Average Claim Amount", "average_claim_amount"),
        ("Claim-to-Premium Ratio", "claim_to_premium_ratio"),
        ("Claim-to-Coverage Ratio", "claim_to_coverage_ratio"),
        ("Paid Claim Ratio", "paid_claim_ratio"),
    ]

    for start in range(0, len(metrics), 3):
        columns = st.columns(3)

        for column, (label, key) in zip(
            columns,
            metrics[start:start + 3],
        ):
            column.metric(
                label,
                format_number(kpis.get(key, 0)),
            )

    st.subheader("Risk Patterns")

    for insight in generate_risk_patterns(data):
        st.write(insight)


# --------------------------------------------------
# INSIGHTS AND RECOMMENDATIONS
# --------------------------------------------------

def insights_recommendations(data):
    st.header("Insights & Recommendations")

    insight_functions = [
        ("Portfolio Insights", generate_portfolio_insights),
        ("Claim Insights", generate_claim_insights),
        ("Premium Insights", generate_premium_insights),
        ("Customer Insights", generate_customer_insights),
        ("Vehicle Insights", generate_vehicle_insights),
        ("Risk Patterns", generate_risk_patterns),
    ]

    for title, function in insight_functions:
        st.subheader(title)

        for insight in function(data):
            st.write(insight)


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

def main():
    st.title("🚗 Motor Insurance Claims & Policy Analytics")

    st.caption(
        "Interactive analytics for policies, customers, "
        "vehicles, claims, payments and business performance."
    )

    try:
        raw_data = load_dashboard_data()

    except FileNotFoundError as exc:
        st.warning(
            "The required CSV files could not be found. Add "
            "customers.csv, vehicles.csv, policies.csv, claims.csv "
            "and payments.csv to data/raw/."
        )

        st.code(str(exc))
        st.stop()

    except Exception as exc:
        st.error(f"Unable to load dashboard data: {exc}")
        st.stop()

    pages = {
        "Executive Overview": executive_overview,
        "Policy Analysis": policy_analysis,
        "Claims Analysis": claims_analysis,
        "Customer Analysis": customer_analysis,
        "Vehicle Analysis": vehicle_analysis,
        "Premium & Risk": premium_risk_analysis,
        "Insights & Recommendations": insights_recommendations,
    }

    selected_page = st.sidebar.radio(
        "📑 Navigate Dashboard",
        list(pages.keys()),
    )

    data = apply_filters(raw_data)

    if all(
        dataframe.empty
        for dataframe in data.values()
        if isinstance(dataframe, pd.DataFrame)
    ):
        st.warning(
            "No records match the selected filters. "
            "Use Reset Filters and try again."
        )
        st.stop()

    pages[selected_page](data)


if __name__ == "__main__":
    main()