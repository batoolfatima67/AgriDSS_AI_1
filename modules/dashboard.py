import streamlit as st


def render_dashboard():

    st.title("📊 AgriDSS Dashboard")

    data = st.session_state.get("user_data")

    if not data:
        st.warning("No farm data available")
        return

    st.subheader("📍 Farm Info")
    st.write(data)

    # OPTIONAL: only show summary, NOT duplicate values
    st.subheader("📌 System Status")

    if "weather_data" in st.session_state:
        st.success("🌦 Weather data available")

    if "ndvi_value" in st.session_state:
        st.success("🌱 NDVI data available")
