import os
import pandas as pd
from sklearn.model_selection import train_test_split


def preprocess_data():
    """
    Split the housing dataset into training and testing datasets.
    """

    data = pd.read_csv("data/raw/housing.csv")

    data = data.drop_duplicates()
    data = data.dropna()

    X = data.drop("MedHouseVal", axis=1)
    y = data["MedHouseVal"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    train_data = X_train.copy()
    train_data["MedHouseVal"] = y_train

    test_data = X_test.copy()
    test_data["MedHouseVal"] = y_test

    os.makedirs("data/processed", exist_ok=True)

    train_data.to_csv(
        "data/processed/train.csv",
        index=False
    )

    test_data.to_csv(
        "data/processed/test.csv",
        index=False
    )

    print("Data preprocessing completed.")
    print("Training shape:", train_data.shape)
    print("Testing shape:", test_data.shape)


if __name__ == "__main__":
    preprocess_data()