import streamlit as st
import requests


def get_weather(lat, lon):

    api_key = st.secrets["2a0c3869482067519b6719f19118aca4"]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    response = requests.get(url)

    return response.json()
    
   
