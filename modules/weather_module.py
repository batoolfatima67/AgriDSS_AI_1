import streamlit as st
import requests
import random 

def get_weather(lat, lon):
    
  OPENWEATHER_API_KEY = "2a0c3869482067519b6719f19118aca4"

    api_key = st.secrets["OPENWEATHER_API_KEY"]

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return {"error": "Weather API failed"}

    return response.json()

def get_weather(lat, lon):

    return {
        "temperature": round(random.uniform(18, 38), 1),
        "humidity": round(random.uniform(30, 80), 1),
        "rainfall": round(random.uniform(0, 20), 1),
        "condition": random.choice(["Sunny", "Cloudy", "Partly Cloudy"])
    }
