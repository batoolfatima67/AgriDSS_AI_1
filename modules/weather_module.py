import streamlit as st
import requests

def get_weather(lat, lon):

    api_key = st.secrets["2a0c3869482067519b6719f19118aca4"]

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    response = requests.get(url)

    return response.json()
   
def render_weather_module():

    st.header("🌦 Weather Module")

    # -----------------------------
    # GET USER DATA
    # -----------------------------
    user_data = st.session_state.get("user_data", None)

    if not user_data:
        st.warning("No input data found. Please fill Input Module first.")
        return

    lat = user_data["latitude"]
    lon = user_data["longitude"]

    st.write("Location:", lat, lon)

    # -----------------------------
    # FETCH WEATHER
    # -----------------------------
    weather = get_weather(lat, lon)

    if weather is None:
        st.error("Failed to fetch weather data. Check API key or internet.")
        return

    st.session_state.weather_data = {
    "temp": weather["main"]["temp"],
    "humidity": weather["main"]["humidity"],
    "wind": weather["wind"]["speed"]
    } 
    
    # -----------------------------
    # DISPLAY WEATHER DATA
    # -----------------------------
    st.subheader("Current Weather")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Temperature (°C)", weather["main"]["temp"])

    with col2:
        st.metric("Humidity (%)", weather["main"]["humidity"])

    with col3:
        st.metric("Wind Speed", weather["wind"]["speed"])

    # -----------------------------
    # DESCRIPTION
    # -----------------------------
    st.write("Condition:", weather["weather"][0]["description"])
