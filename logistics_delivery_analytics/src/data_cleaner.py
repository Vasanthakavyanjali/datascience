import os
import numpy as np
import pandas as pd

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values according to business domain rules."""
    df = df.copy()
    
    # Text/categorical defaults
    str_cols = ['warehouse', 'origin_city', 'destination_city', 'product_category', 
                'shipping_mode', 'delivery_partner', 'delivery_status']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
            
    # Numerical defaults
    num_cols_zero = ['distance_km', 'quantity', 'weight_kg', 'shipping_cost', 'fuel_cost', 'warehouse_processing_hours']
    for col in num_cols_zero:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            
    if 'customer_rating' in df.columns:
        df['customer_rating'] = df['customer_rating'].fillna(df['customer_rating'].median())
        
    if 'damage_flag' in df.columns:
        df['damage_flag'] = df['damage_flag'].fillna(0)
    if 'return_flag' in df.columns:
        df['return_flag'] = df['return_flag'].fillna(0)
        
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate records from the logistics DataFrame."""
    df = df.copy()
    if 'order_id' in df.columns:
        df = df.drop_duplicates(subset=['order_id'], keep='first')
    else:
        df = df.drop_duplicates()
    return df

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize casing and strip whitespace from text columns."""
    df = df.copy()
    text_cols = ['warehouse', 'origin_city', 'destination_city', 'product_category', 
                 'shipping_mode', 'delivery_partner', 'delivery_status']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    return df

def clean_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date columns into proper pandas datetime objects."""
    df = df.copy()
    date_cols = ['order_date', 'dispatch_date', 'expected_delivery_date', 'actual_delivery_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def validate_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Validate non-negative and domain-bounded numeric fields."""
    df = df.copy()
    non_negative_cols = ['distance_km', 'quantity', 'weight_kg', 'shipping_cost', 'fuel_cost', 'warehouse_processing_hours']
    for col in non_negative_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: max(0, x))
            
    if 'customer_rating' in df.columns:
        df['customer_rating'] = df['customer_rating'].clip(lower=1.0, upper=5.0)
        
    return df

def validate_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out critical invalid records per business rules (BR-01 to BR-09)."""
    df = df.copy()
    if 'order_id' in df.columns:
        df = df[df['order_id'].notna() & (df['order_id'] != 'Unknown')]
    if 'customer_id' in df.columns:
        df = df[df['customer_id'].notna() & (df['customer_id'] != 'Unknown')]
    if 'quantity' in df.columns:
        df = df[df['quantity'] > 0]
    return df

def create_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create essential business metrics (delivery_days, delay_days, cost_per_km, total_logistics_cost, on_time_flag)."""
    df = df.copy()
    
    # 1. Delivery Days
    if 'actual_delivery_date' in df.columns and 'dispatch_date' in df.columns:
        df['delivery_days'] = (df['actual_delivery_date'] - df['dispatch_date']).dt.days
    else:
        df['delivery_days'] = np.nan

    # 2. Delay Days
    if 'actual_delivery_date' in df.columns and 'expected_delivery_date' in df.columns:
        df['delay_days'] = (df['actual_delivery_date'] - df['expected_delivery_date']).dt.days
    else:
        df['delay_days'] = 0

    # 3. Cost Per KM
    if 'shipping_cost' in df.columns and 'distance_km' in df.columns:
        df['cost_per_km'] = np.where(df['distance_km'] > 0, df['shipping_cost'] / df['distance_km'], 0)
    else:
        df['cost_per_km'] = 0

    # 4. Total Logistics Cost
    shipping = df['shipping_cost'] if 'shipping_cost' in df.columns else 0
    fuel = df['fuel_cost'] if 'fuel_cost' in df.columns else 0
    df['total_logistics_cost'] = shipping + fuel

    # 5. On-Time Flag
    df['on_time_flag'] = np.where(df['delay_days'] <= 0, 1, 0)

    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Master function running the standardized cleaning sequence."""
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = clean_text_columns(df)
    df = clean_date_columns(df)
    df = validate_numeric_columns(df)
    df = validate_business_rules(df)
    df = create_derived_columns(df)
    return df

def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save the cleaned dataset to a CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)