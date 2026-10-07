# ============================================================
# src/data_loader.py
# Reads data from CSV or Excel files.
# Simple and easy to understand.
# ============================================================

'''
User / Application
       |
       v
   load_data()
       |
       +--------------------+
       |                    |
       v                    v
Uploaded File          Default CSV
       |                    |
       v                    v
load_uploaded_data()  load_default_data()
       |                    |
       +---------+----------+
                 |
                 v
              DataFrame
                 |
       +---------+---------+
       |                   |
       v                   v
find_missing_columns()  preview_dataframe()
       |
       v
Validation

'''
import pandas as pd
import streamlit as st

from config import DEFAULT_DATA_FILE, REQUIRED_COLUMNS


# ------------------------------------------------------------
# FUNCTION 1: Load the default CSV file
# ------------------------------------------------------------
def load_default_data():
    """Read the CSV file from the data folder."""
    try:
        df = pd.read_csv(DEFAULT_DATA_FILE)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {DEFAULT_DATA_FILE}")
        return None
    except Exception as e:
        st.error(f"Could not read the file. Error: {e}")
        return None


# ------------------------------------------------------------
# FUNCTION 2: Load a file uploaded by the user
# ------------------------------------------------------------
def load_uploaded_data(uploaded_file):
    """Read a file uploaded by the user (CSV or Excel)."""
    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Please upload a CSV or Excel file.")
            return None
        return df
    except Exception as e:
        st.error(f"Could not read the uploaded file. Error: {e}")
        return None


# ------------------------------------------------------------
# FUNCTION 3: Main loading function (used by the app)
# ------------------------------------------------------------
def load_data(uploaded_file=None):
    """
    Load data from upload if given, otherwise use default file.
    Returns (df, source_label).
    """
    if uploaded_file is not None:
        df = load_uploaded_data(uploaded_file)
        if df is not None:
            return df, f"Uploaded: {uploaded_file.name}"
        return None, "Upload failed"

    df = load_default_data()
    if df is not None:
        return df, f"Default file: {DEFAULT_DATA_FILE.name}"
    return None, "No data loaded"


# ------------------------------------------------------------
# FUNCTION 4: Check which required columns are missing
# ------------------------------------------------------------
def find_missing_columns(df):
    """Return a list of required columns that are missing."""
    if df is None:
        return REQUIRED_COLUMNS

    missing = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)

    return missing


# ------------------------------------------------------------
# FUNCTION 5: Show a small summary of the data
# ------------------------------------------------------------
def show_summary(df):
    """Print basic information about the DataFrame."""
    if df is None:
        print("No data.")
        return

    print("Number of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])
    print("Columns:", list(df.columns))
    print()
    print("First 5 rows:")
    print(df.head())


# ------------------------------------------------------------
# FUNCTION 6: Preview the first few rows (for the app)
# ------------------------------------------------------------
def preview_dataframe(df, n=10):
    """
    Return the first n rows for display purposes.
    Used by app.py to show a small preview.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    return df.head(n)


# ------------------------------------------------------------
# TEST BLOCK
# ------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("DATA LOADER TEST")
    print("=" * 50)

    df = load_default_data()

    if df is not None:
        print("File loaded successfully.")
        print()
        show_summary(df)
        print()

        missing = find_missing_columns(df)
        if missing:
            print("Missing columns:", missing)
        else:
            print("All required columns are present.")
    else:
        print("Could not load data.")