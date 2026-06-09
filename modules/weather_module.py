import streamlit as st
import requests


def get_weather(lat, lon):

    api_key = st.secrets["OPENWEATHER_API_KEY"]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    return requests.get(url).json()
