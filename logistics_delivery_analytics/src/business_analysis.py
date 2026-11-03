import pandas as pd

# --- Basic KPIs ---
def calculate_total_orders(df: pd.DataFrame) -> int:
    """Return total count of unique orders."""
    return int(df['order_id'].nunique()) if 'order_id' in df.columns else len(df)

def calculate_total_delivered(df: pd.DataFrame) -> int:
    """Return total count of delivered orders."""
    if 'delivery_status' in df.columns:
        return int((df['delivery_status'].str.lower() == 'delivered').sum())
    return 0

def calculate_total_delayed(df: pd.DataFrame) -> int:
    """Return total count of delayed orders."""
    if 'delay_days' in df.columns:
        return int((df['delay_days'] > 0).sum())
    return 0

import pandas as pd

def calculate_on_time_percentage(df: pd.DataFrame) -> float:
    """Calculate percentage of shipments delivered on time."""
    if df is None or len(df) == 0:
        return 0.0

    # Work on a shallow copy to prevent side effects
    working_df = df.copy()

    # Prioritize on_time_flag if available in dataset
    if 'on_time_flag' in working_df.columns:
        return float(pd.to_numeric(working_df['on_time_flag'], errors='coerce').fillna(0).mean() * 100)

    # Filter by delivery_status safely if present
    if 'delivery_status' in working_df.columns:
        # Convert status column safely to string
        status_series = working_df['delivery_status'].astype(str).str.strip().str.lower()
        
        # Include delivered / on-time shipments
        delivered_mask = status_series.isin(['delivered', 'on-time', 'on time'])
        
        if delivered_mask.any():
            working_df = working_df[delivered_mask]

    if len(working_df) == 0:
        return 0.0

    # Ensure delay_days is numeric and calculate on-time percentage
    if 'delay_days' in working_df.columns:
        delay_days = pd.to_numeric(working_df['delay_days'], errors='coerce').fillna(0)
        return float((delay_days <= 0).sum() / len(working_df) * 100)

    return 0.0
def calculate_average_delivery_days(df: pd.DataFrame) -> float:
    """Calculate mean delivery duration in days."""
    return float(df['delivery_days'].mean()) if 'delivery_days' in df.columns else 0.0

def calculate_average_delay_days(df: pd.DataFrame) -> float:
    """Calculate mean delay duration for delayed orders."""
    delayed = df[df['delay_days'] > 0] if 'delay_days' in df.columns else pd.DataFrame()
    return float(delayed['delay_days'].mean()) if len(delayed) > 0 else 0.0

# --- Cost KPIs ---
def calculate_total_shipping_cost(df: pd.DataFrame) -> float:
    """Calculate total shipping cost expenditure."""
    return float(df['shipping_cost'].sum()) if 'shipping_cost' in df.columns else 0.0

def calculate_average_shipping_cost(df: pd.DataFrame) -> float:
    """Calculate mean shipping cost per order."""
    return float(df['shipping_cost'].mean()) if 'shipping_cost' in df.columns else 0.0

def calculate_total_fuel_cost(df: pd.DataFrame) -> float:
    """Calculate total fuel expenditure."""
    return float(df['fuel_cost'].sum()) if 'fuel_cost' in df.columns else 0.0

def calculate_total_logistics_cost(df: pd.DataFrame) -> float:
    """Calculate total logistics cost (shipping + fuel)."""
    return float(df['total_logistics_cost'].sum()) if 'total_logistics_cost' in df.columns else 0.0

def calculate_average_logistics_cost(df: pd.DataFrame) -> float:
    """Calculate mean total logistics cost per order."""
    return float(df['total_logistics_cost'].mean()) if 'total_logistics_cost' in df.columns else 0.0

def calculate_average_cost_per_km(df: pd.DataFrame) -> float:
    """Calculate average cost per kilometer."""
    return float(df['cost_per_km'].mean()) if 'cost_per_km' in df.columns else 0.0

# --- Route Analysis ---
def analyze_route_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate volume and performance by origin-destination route."""
    df['route'] = df['origin_city'] + " -> " + df['destination_city']
    return df.groupby('route').agg(
        total_orders=('order_id', 'count'),
        avg_delivery_days=('delivery_days', 'mean'),
        avg_delay_days=('delay_days', 'mean')
    ).reset_index()

def analyze_route_cost(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate logistics costs by route."""
    df['route'] = df['origin_city'] + " -> " + df['destination_city']
    return df.groupby('route').agg(
        total_cost=('total_logistics_cost', 'sum'),
        avg_cost=('total_logistics_cost', 'mean'),
        avg_cost_per_km=('cost_per_km', 'mean')
    ).reset_index()

def analyze_route_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze delay metrics and delay rates by route."""
    df['route'] = df['origin_city'] + " -> " + df['destination_city']
    return df.groupby('route').agg(
        total_orders=('order_id', 'count'),
        delayed_orders=('delay_days', lambda x: (x > 0).sum()),
        avg_delay=('delay_days', 'mean')
    ).assign(delay_rate=lambda x: (x['delayed_orders'] / x['total_orders']) * 100).reset_index()

# --- Warehouse Analysis ---
def analyze_warehouse_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total orders and average processing hours per warehouse."""
    return df.groupby('warehouse').agg(
        total_orders=('order_id', 'count'),
        avg_processing_hours=('warehouse_processing_hours', 'mean')
    ).reset_index()

def analyze_warehouse_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate delay ratios per warehouse."""
    return df.groupby('warehouse').agg(
        total_orders=('order_id', 'count'),
        delayed_orders=('delay_days', lambda x: (x > 0).sum())
    ).assign(delay_percentage=lambda x: (x['delayed_orders'] / x['total_orders']) * 100).reset_index()

def analyze_warehouse_processing_time(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze mean warehouse processing time."""
    return df.groupby('warehouse')['warehouse_processing_hours'].mean().reset_index()

# --- Shipping Mode Analysis ---
def analyze_shipping_mode(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze order distributions per shipping mode."""
    return df.groupby('shipping_mode').size().reset_index(name='order_count')

def analyze_shipping_mode_cost(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate mean shipping and total costs per shipping mode."""
    return df.groupby('shipping_mode').agg(
        avg_shipping_cost=('shipping_cost', 'mean'),
        avg_total_cost=('total_logistics_cost', 'mean')
    ).reset_index()

def analyze_shipping_mode_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Evaluate delay percentages across shipping modes."""
    return df.groupby('shipping_mode').agg(
        total=('order_id', 'count'),
        delayed=('delay_days', lambda x: (x > 0).sum())
    ).assign(delay_rate=lambda x: (x['delayed'] / x['total']) * 100).reset_index()

# --- Delivery Partner Analysis ---
def analyze_delivery_partner(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze volume metrics across delivery partners."""
    return df.groupby('delivery_partner').agg(total_orders=('order_id', 'count')).reset_index()

def analyze_partner_cost(df: pd.DataFrame) -> pd.DataFrame:
    """Compare logistics costs across delivery partners."""
    return df.groupby('delivery_partner').agg(
        avg_shipping_cost=('shipping_cost', 'mean'),
        avg_total_cost=('total_logistics_cost', 'mean')
    ).reset_index()

def analyze_partner_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate on-time delivery percentages by partner."""
    return df.groupby('delivery_partner').agg(
        total=('order_id', 'count'),
        on_time=('on_time_flag', 'sum')
    ).assign(on_time_percentage=lambda x: (x['on_time'] / x['total']) * 100).reset_index()

def analyze_partner_damage_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate package damage percentages by partner."""
    return df.groupby('delivery_partner').agg(
        total=('order_id', 'count'),
        damaged=('damage_flag', 'sum')
    ).assign(damage_rate=lambda x: (x['damaged'] / x['total']) * 100).reset_index()

# --- Customer Analysis ---
def calculate_average_customer_rating(df: pd.DataFrame) -> float:
    """Calculate overall average customer satisfaction score."""
    return float(df['customer_rating'].mean()) if 'customer_rating' in df.columns else 0.0

def calculate_return_rate(df: pd.DataFrame) -> float:
    """Calculate return rate percentage."""
    return float((df['return_flag'].sum() / len(df)) * 100) if 'return_flag' in df.columns and len(df) > 0 else 0.0

def calculate_damage_rate(df: pd.DataFrame) -> float:
    """Calculate damage rate percentage."""
    return float((df['damage_flag'].sum() / len(df)) * 100) if 'damage_flag' in df.columns and len(df) > 0 else 0.0