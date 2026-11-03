import streamlit as st
import requests
import os

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 House Price Prediction")
st.write("MLOps Machine Learning Application")

st.subheader("Enter House Details")

med_inc = st.number_input("Median Income", 0.0, value=5.0)
house_age = st.number_input("House Age", 0.0, value=20.0)
ave_rooms = st.number_input("Average Rooms", 0.0, value=5.0)
ave_bedrms = st.number_input("Average Bedrooms", 0.0, value=1.0)
population = st.number_input("Population", 0.0, value=1000.0)
ave_occup = st.number_input("Average Occupancy", 0.0, value=3.0)
latitude = st.number_input("Latitude", -90.0, 90.0, value=34.0)
longitude = st.number_input("Longitude", -180.0, 180.0, value=-118.0)


if st.button("Predict House Price"):

    input_data = {
        "MedInc": med_inc,
        "HouseAge": house_age,
        "AveRooms": ave_rooms,
        "AveBedrms": ave_bedrms,
        "Population": population,
        "AveOccup": ave_occup,
        "Latitude": latitude,
        "Longitude": longitude
    }

    try:
        response = requests.post(
            os.getenv("API_URL", "http://127.0.0.1:8000") + "/predict",
            json=input_data,
            timeout=30
            )

        response.raise_for_status()

        result = response.json()

        st.success(
            f"Predicted House Price: "
            f"${result['predicted_house_price'] * 100000:,.2f}"
        )

    except requests.exceptions.RequestException as error:
        st.error(f"API connection failed: {error}")