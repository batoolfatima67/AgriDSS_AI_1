import streamlit as st
from datetime import datetime


def generate_report():

    st.title("📊 Farm Report")

    weather = st.session_state.get("weather_data")
    ndvi = st.session_state.get("ndvi_value")

    if not weather or ndvi is None:
        st.warning("No analysis data found. Run Analysis first.")
        return

    st.subheader("🌦 Weather Report")
    st.write(weather)

    st.subheader("🌱 NDVI Report")
    st.write("NDVI Value:", ndvi)

    # Interpretation
    if ndvi > 0.6:
        st.success("Healthy Crop 🟢")
    elif ndvi > 0.3:
        st.warning("Moderate Health 🟡")
    else:
        st.error("Poor Condition 🔴")


