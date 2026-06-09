import requests
import streamlit as st


# -----------------------------
# WEATHER FUNCTION (CORE LOGIC)
# -----------------------------
def get_weather(lat, lon):

    try:

        api_key = st.secrets["2a0c3869482067519b6719f19118aca4"]

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )

        response = requests.get(url, timeout=10)

        data = response.json()

        weather = {
            "temperature": {
                "value": data["main"]["temp"]
            },
            "humidity": {
                "value": data["main"]["humidity"]
            },
            "wind_speed": {
                "value": data["wind"]["speed"]
            },
            "condition": data["weather"][0]["description"]
        }

        return weather


    except Exception:

        # SAFE FALLBACK (NEVER CRASH APP)
        return {
            "temperature": {"value": 30},
            "humidity": {"value": 50},
            "wind_speed": {"value": 5},
            "condition": "data unavailable"
        }
