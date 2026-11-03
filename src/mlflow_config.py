import dagshub
import mlflow
import os


def configure_mlflow():
    """Configure MLflow to track experiments on DAGsHub."""

    dagshub.init(
        repo_owner="Vasanthakavyanjali",
        repo_name="homeprice_ml",
        mlflow=True
    )

    mlflow.set_experiment("House Price Prediction")

    print("MLflow tracking configured successfully.")
    print("Tracking URI:", mlflow.get_tracking_uri())


if __name__ == "__main__":
    configure_mlflow()
