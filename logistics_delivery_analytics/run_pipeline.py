import os
from src.data_loader import load_data
from src.data_cleaner import clean_data, save_cleaned_data

def run_pipeline():
    """Execute end-to-end data processing workflow."""
    raw_path = os.path.abspath('data/raw/logistics_data.csv')
    cleaned_path = os.path.abspath('data/cleaned/logistics_cleaned.csv')

    print("Loading raw data...")
    raw_df = load_data(raw_path)

    print("Checking data quality & cleaning data...")
    cleaned_df = clean_data(raw_df)

    print("Saving cleaned data...")
    save_cleaned_data(cleaned_df, cleaned_path)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()