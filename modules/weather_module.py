import requests
import streamlit as st
import random 

def get_weather(lat, lon):

    OPENWEATHER_API_KEY = "2a0c3869482067519b6719f19118aca4"

    api_key = st.secrets["OPENWEATHER_API_KEY"]

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return {"error": "Weather not found"}

    return {
        "temperature": {
            "value": data["main"]["temp"],
            "unit": "°C"
        },
        "humidity": {
            "value": data["main"]["humidity"],
            "unit": "%"
        },
        "wind_speed": {
            "value": data["wind"]["speed"] * 3.6,  #convert m/s to km/h
            "unit": "km/h"
        },
        "condition": data["weather"][0]["description"]
    }
