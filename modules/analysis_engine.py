import streamlit as st
import random


def run_full_analysis():

    st.header("🌾 AgriDSS_AI Demo System")

    data = st.session_state.get("user_data")

    if not data:
        st.warning("Select farm location first")
        return

    lat = data["latitude"]
    lon = data["longitude"]

    st.success("System Ready 🚀")

    # ---------------- WEATHER ----------------
    weather = {
        "temperature": round(random.uniform(20, 40), 1),
        "humidity": round(random.uniform(30, 80), 1),
        "condition": "Sunny"
    }

    # SAVE WEATHER
    st.session_state.weather_data = weather

    st.subheader("🌦 Weather")
    st.write(weather)

    # ---------------- NDVI ----------------
    ndvi = round(random.uniform(0.2, 0.85), 2)

    # SAVE NDVI
    st.session_state.ndvi_value = ndvi

    st.subheader("🌱 NDVI")
    st.metric("Vegetation Index", ndvi)
