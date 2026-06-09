import streamlit as st
from datetime import datetime

def generate_report():

    st.title("📄 Farm Decision Report")

    weather = st.session_state.get("weather_data")
    ndvi = st.session_state.get("ndvi_value")
    data = st.session_state.get("user_data")

    if not weather or ndvi is None or not data:
        st.warning("No report available. Run analysis first.")
        return

    # ---------------- HEADER ----------------
    st.subheader("🌾 Farm Summary")
    st.write(f"District: {data['district']}")
    st.write(f"Tehsil: {data['tehsil']}")
    st.write(f"Crop: {data['crop']}")

    st.divider()

    # ---------------- WEATHER SECTION ----------------
    st.subheader("🌦 Weather Conditions")

    st.write(f"Temperature: {weather['temperature']} °C")
    st.write(f"Humidity: {weather['humidity']} %")
    st.write(f"Condition: {weather['condition']}")

    st.divider()

    # ---------------- NDVI SECTION ----------------
    st.subheader("🌱 Vegetation Status (NDVI)")

    st.metric("NDVI Value", ndvi)

    if ndvi > 0.6:
        st.success("Crop condition: Healthy 🟢")
        status = "Good"
    elif ndvi > 0.3:
        st.warning("Crop condition: Moderate 🟡")
        status = "Moderate"
    else:
        st.error("Crop condition: Poor 🔴")
        status = "Poor"

    st.divider()

    # ---------------- FINAL DECISION ----------------
    st.subheader("🧠 Final Recommendation")

    if status == "Good":
        st.info("Normal irrigation is sufficient. Monitor regularly.")
    elif status == "Moderate":
        st.info("Increase irrigation slightly and monitor soil moisture.")
    else:
        st.info("Urgent action required: improve irrigation and check crop stress.")

    st.divider()

    # ---------------- FOOTER ----------------
    st.success("Report Generated Successfully ✔")

