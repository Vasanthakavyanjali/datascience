import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")

def plot_delivery_status(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='delivery_status', ax=ax, palette='Set2')
    ax.set_title('Delivery Status Distribution')
    ax.set_xlabel('Delivery Status')
    ax.set_ylabel('Order Count')
    plt.tight_layout()
    return fig

def plot_monthly_orders(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    df_temp = df.copy()
    df_temp['month'] = df_temp['order_date'].dt.to_period('M').astype(str)
    monthly = df_temp.groupby('month').size().reset_index(name='count')
    sns.lineplot(data=monthly, x='month', y='count', marker='o', ax=ax, color='b')
    ax.set_title('Monthly Order Volume Trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Orders')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_monthly_delivery_performance(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    df_temp = df.copy()
    df_temp['month'] = df_temp['order_date'].dt.to_period('M').astype(str)
    perf = df_temp.groupby('month')['on_time_flag'].mean().reset_index()
    perf['on_time_pct'] = perf['on_time_flag'] * 100
    sns.lineplot(data=perf, x='month', y='on_time_pct', marker='s', ax=ax, color='g')
    ax.set_title('Monthly On-Time Delivery %')
    ax.set_xlabel('Month')
    ax.set_ylabel('On-Time Delivery Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_delay_by_warehouse(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x='warehouse', y='delay_days', ax=ax, palette='Blues_r', ci=None)
    ax.set_title('Average Delay Days by Warehouse')
    ax.set_xlabel('Warehouse')
    ax.set_ylabel('Avg Delay (Days)')
    plt.tight_layout()
    return fig

def plot_delay_by_shipping_mode(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x='shipping_mode', y='delay_days', ax=ax, palette='Oranges_r', ci=None)
    ax.set_title('Average Delay Days by Shipping Mode')
    ax.set_xlabel('Shipping Mode')
    ax.set_ylabel('Avg Delay (Days)')
    plt.tight_layout()
    return fig

def plot_delay_by_route(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 5))
    df_temp = df.copy()
    df_temp['route'] = df_temp['origin_city'] + " -> " + df_temp['destination_city']
    route_delays = df_temp.groupby('route')['delay_days'].mean().reset_index().sort_values(by='delay_days', ascending=False)
    sns.barplot(data=route_delays, x='delay_days', y='route', ax=ax, palette='Reds_r')
    ax.set_title('Average Delay Days by Route')
    ax.set_xlabel('Avg Delay (Days)')
    ax.set_ylabel('Route')
    plt.tight_layout()
    return fig

def plot_delay_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df['delay_days'], kde=True, bins=15, ax=ax, color='purple')
    ax.set_title('Distribution of Delay Days')
    ax.set_xlabel('Delay (Days)')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    return fig

def plot_cost_by_shipping_mode(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x='shipping_mode', y='total_logistics_cost', ax=ax, palette='Purples_r', ci=None)
    ax.set_title('Average Total Logistics Cost by Shipping Mode')
    ax.set_xlabel('Shipping Mode')
    ax.set_ylabel('Avg Cost ($)')
    plt.tight_layout()
    return fig

def plot_cost_by_route(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 5))
    df_temp = df.copy()
    df_temp['route'] = df_temp['origin_city'] + " -> " + df_temp['destination_city']
    route_cost = df_temp.groupby('route')['total_logistics_cost'].mean().reset_index().sort_values(by='total_logistics_cost', ascending=False)
    sns.barplot(data=route_cost, x='total_logistics_cost', y='route', ax=ax, palette='Greens_r')
    ax.set_title('Average Logistics Cost by Route')
    ax.set_xlabel('Avg Total Logistics Cost ($)')
    ax.set_ylabel('Route')
    plt.tight_layout()
    return fig

def plot_cost_trend(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    df_temp = df.copy()
    df_temp['month'] = df_temp['order_date'].dt.to_period('M').astype(str)
    cost_monthly = df_temp.groupby('month')['total_logistics_cost'].sum().reset_index()
    sns.lineplot(data=cost_monthly, x='month', y='total_logistics_cost', marker='o', ax=ax, color='red')
    ax.set_title('Monthly Total Logistics Cost Trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Cost ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_orders_by_warehouse(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='warehouse', ax=ax, palette='Blues')
    ax.set_title('Order Volume by Warehouse')
    ax.set_xlabel('Warehouse')
    ax.set_ylabel('Total Orders')
    plt.tight_layout()
    return fig

def plot_processing_time_by_warehouse(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x='warehouse', y='warehouse_processing_hours', ax=ax, palette='YlOrRd', ci=None)
    ax.set_title('Average Processing Hours by Warehouse')
    ax.set_xlabel('Warehouse')
    ax.set_ylabel('Processing Time (Hours)')
    plt.tight_layout()
    return fig

def plot_shipments_by_partner(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.countplot(data=df, x='delivery_partner', ax=ax, palette='Dark2')
    ax.set_title('Shipments handled by Delivery Partner')
    ax.set_xlabel('Delivery Partner')
    ax.set_ylabel('Order Count')
    plt.tight_layout()
    return fig

def plot_partner_delivery_performance(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    partner_perf = df.groupby('delivery_partner')['on_time_flag'].mean().reset_index()
    partner_perf['on_time_pct'] = partner_perf['on_time_flag'] * 100
    sns.barplot(data=partner_perf, x='delivery_partner', y='on_time_pct', ax=ax, palette='Greens')
    ax.set_title('On-Time Delivery % by Partner')
    ax.set_xlabel('Delivery Partner')
    ax.set_ylabel('On-Time Delivery Rate (%)')
    plt.tight_layout()
    return fig

def plot_partner_cost(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x='delivery_partner', y='shipping_cost', ax=ax, palette='Spectral', ci=None)
    ax.set_title('Average Shipping Cost by Partner')
    ax.set_xlabel('Delivery Partner')
    ax.set_ylabel('Avg Shipping Cost ($)')
    plt.tight_layout()
    return fig

def plot_customer_rating_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df['customer_rating'], discrete=True, ax=ax, color='teal')
    ax.set_title('Customer Rating Distribution')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    plt.tight_layout()
    return fig

def plot_rating_by_delivery_status(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x='delivery_status', y='customer_rating', ax=ax, palette='Set3')
    ax.set_title('Customer Rating by Delivery Status')
    ax.set_xlabel('Delivery Status')
    ax.set_ylabel('Rating')
    plt.tight_layout()
    return fig