import streamlit as st


def render_dashboard():

    st.header("📊 AgriDSS_AI Command Center")

    user_data = st.session_state.get("user_data", None)
    weather = st.session_state.get("weather_data", None)
    ndvi = st.session_state.get("ndvi_value", None)

    st.subheader("📌 Farm Summary")

    if user_data:
        st.write("🌾 Crop:", user_data["crop"])
        st.write("📍 Location:", user_data["latitude"], user_data["longitude"])
        st.write("📐 Area (Acres):", user_data["area"])
    else:
        st.warning("No input data available")

    st.divider()

    st.subheader("🌦 Weather Snapshot")

    if weather:
        st.metric("Temperature (°C)", weather["temp"])
        st.metric("Humidity (%)", weather["humidity"])
        st.metric("Wind Speed", weather["wind"])
    else:
        st.warning("Weather data not available")

    st.divider()

    st.subheader("🌱 NDVI Snapshot")

    if ndvi is not None:
        st.metric("NDVI Value", round(ndvi, 3))

        if ndvi < 0.2:
            st.error("Severe Vegetation Stress")
        elif ndvi < 0.5:
            st.warning("Moderate Vegetation Health")
        else:
            st.success("Healthy Vegetation")
    else:
        st.warning("NDVI not available")

    st.divider()

    st.subheader("🧠 System Status")

    if user_data and weather and ndvi is not None:
        st.success("System Fully Operational ✔")
    else:
        st.warning("System Incomplete - Missing Modules")
