import streamlit as st
from modules.weather_module import get_weather
from modules.gee_ndvi import get_ndvi
from modules.recommendation_engine import generate_recommendation


def run_full_analysis():

    st.header("🌾 AgriDSS AI Demo System")

    data = st.session_state.get("user_data")

    if not data:
        st.warning("Select farm location first")
        return

    lat = data["latitude"]
    lon = data["longitude"]
    crop = data["crop"]

    st.success("System Ready 🚀")

    # WEATHER
    weather = get_weather(lat, lon)

    st.subheader("🌦 Weather")
    st.write(weather)

    # NDVI
    ndvi = get_ndvi(lat, lon)

    st.subheader("🌱 NDVI")
    st.metric("Vegetation Index", ndvi)

    # SIMPLE CLASSIFICATION
    if ndvi > 0.6:
        st.success("Healthy Vegetation 🟢")
    elif ndvi > 0.3:
        st.warning("Moderate Vegetation 🟡")
    else:
        st.error("Low Vegetation 🔴")

    # SIMPLE RECOMMENDATION (SAFE DEMO)
    st.subheader("🧠 Recommendation")

    if ndvi > 0.6:
        st.info("Normal irrigation recommended")
    else:
        st.info("Increase irrigation and monitor crop health")
