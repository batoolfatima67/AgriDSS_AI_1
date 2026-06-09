import streamlit as st


def render_dashboard():

    st.header("📊 AgriDSS_AI Dashboard")

    user_data = st.session_state.get("user_data")
    weather = st.session_state.get("weather_data")
    ndvi = st.session_state.get("ndvi_value")

    st.subheader("Farm Info")

    if user_data:
        st.write(user_data)
    else:
        st.warning("No farm data")

    st.subheader("Weather")

    if weather:
        st.write(weather)
    else:
        st.warning("No weather data")

    st.subheader("NDVI")

    if ndvi is not None:
        st.write(ndvi)
    else:
        st.warning("No NDVI data")
