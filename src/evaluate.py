import os
import json
import joblib
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate_model():
    """
    Evaluate the trained model and save performance metrics.
    """

    test_data = pd.read_csv("data/processed/test.csv")

    X_test = test_data.drop("MedHouseVal", axis=1)
    y_test = test_data["MedHouseVal"]

    model = joblib.load("models/house_price_model.pkl")

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, predictions)

    metrics = {
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "R2_Score": round(r2, 4)
    }

    os.makedirs("reports", exist_ok=True)

    with open("reports/metrics.json", "w") as file:
        json.dump(metrics, file, indent=4)

    print("Model evaluation completed.")
    print(metrics)


if __name__ == "__main__":
    evaluate_model()