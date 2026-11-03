import os
import pandas as pd
from sklearn.datasets import fetch_california_housing


def load_data():
    """
    Download the California Housing dataset and save it as a CSV file.
    """

    dataset = fetch_california_housing(as_frame=True)

    data = dataset.frame

    os.makedirs("data/raw", exist_ok=True)

    data.to_csv("data/raw/housing.csv", index=False)

    print("Dataset downloaded successfully.")
    print("Dataset shape:", data.shape)


if __name__ == "__main__":
    load_data()