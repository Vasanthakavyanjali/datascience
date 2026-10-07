import os
import pandas as pd

def check_file_exists(file_path: str) -> bool:
    """Check if the target CSV file exists at the provided path."""
    return os.path.exists(file_path)

def load_data(file_path: str) -> pd.DataFrame:
    """Load raw logistics data from a CSV file into a Pandas DataFrame."""
    if not check_file_exists(file_path):
        raise FileNotFoundError(f"Dataset not found at path: {file_path}")
    return pd.read_csv(file_path)