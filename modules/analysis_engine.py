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

    # ---------------- WEATHER (DEMO) ----------------
    st.subheader("🌦 Weather")

    weather = {
        "temperature": round(random.uniform(20, 40), 1),
        "humidity": round(random.uniform(30, 80), 1),
        "condition": random.choice(["Sunny", "Cloudy", "Partly Cloudy"]),
    }

    st.write(weather)

    # ---------------- NDVI (DEMO) ----------------
    st.subheader("🌱 NDVI")

    ndvi = round(random.uniform(0.2, 0.85), 2)

    st.metric("Vegetation Index", ndvi)

    if ndvi > 0.6:
        st.success("Healthy Vegetation 🟢")
    elif ndvi > 0.3:
        st.warning("Moderate Vegetation 🟡")
    else:
        st.error("Low Vegetation 🔴")
