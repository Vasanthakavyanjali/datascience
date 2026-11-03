import os
import joblib
import yaml
import pandas as pd
import mlflow
import mlflow.sklearn
import dagshub

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_model():
    """Train, evaluate and log a Random Forest model using MLflow."""

    # Initialize DAGsHub MLflow tracking
    dagshub.init(
        repo_owner="Vasanthakavyanjali",
        repo_name="homeprice_ml",
        mlflow=True
    )

    mlflow.set_experiment("House Price Prediction")

    # Load parameters
    with open("params.yaml", "r") as file:
        params = yaml.safe_load(file)

    # Load training and testing datasets
    train_data = pd.read_csv("data/processed/train.csv")
    test_data = pd.read_csv("data/processed/test.csv")

    X_train = train_data.drop("MedHouseVal", axis=1)
    y_train = train_data["MedHouseVal"]

    X_test = test_data.drop("MedHouseVal", axis=1)
    y_test = test_data["MedHouseVal"]

    # Initialize model
    model = RandomForestRegressor(
        n_estimators=params["train"]["n_estimators"],
        max_depth=params["train"]["max_depth"],
        random_state=params["train"]["random_state"],
        n_jobs=-1
    )

    # Train and track experiment
    with mlflow.start_run(run_name="RandomForestRegressor"):

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        # Calculate evaluation metrics
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, predictions)

        # Log parameters
        mlflow.log_params(params["train"])

        # Log metrics
        mlflow.log_metrics({
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2_Score": r2
        })

        # Save trained model locally
        os.makedirs("models", exist_ok=True)

        joblib.dump(model, "models/house_price_model.pkl")

        # Log model to MLflow
        mlflow.sklearn.log_model(
            model,
            name="house_price_model",
            skops_trusted_types=["sklearn.tree._tree.Tree"]
            )

        print("Model training completed.")
        print("Model saved successfully.")
        print("MAE:", mae)
        print("MSE:", mse)
        print("RMSE:", rmse)
        print("R2 Score:", r2)


if __name__ == "__main__":
    train_model()
