import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="House Price Prediction API",
    description="MLOps House Price Prediction Service",
    version="1.0"
)

model = joblib.load("models/house_price_model.pkl")


class HouseFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


@app.get("/")
def home():
    """
    Return API information.
    """

    return {
        "message": "House Price Prediction API is running"
    }


@app.post("/predict")
def predict_price(features: HouseFeatures):
    """
    Predict house price using the trained model.
    """

    input_data = pd.DataFrame(
        [features.model_dump()]
    )

    prediction = model.predict(input_data)

    return {
        "predicted_house_price": round(float(prediction[0]), 4),
        "unit": "100,000 USD"
    }