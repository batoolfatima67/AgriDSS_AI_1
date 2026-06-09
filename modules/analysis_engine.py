import streamlit as st


def run_full_analysis():

    st.header("🚀 Full AgriDSS_AI Analysis Engine")

    data = st.session_state.get("user_data")

    if not data:
        st.warning("Please complete Farm Input first")
        return

    lat = data["latitude"]
    lon = data["longitude"]
    crop = data["crop"]

    st.subheader("📍 Farm Location")
    st.write(data["district"], "-", data["tehsil"])

    # -------------------------
    # WEATHER
    # -------------------------
    st.subheader("🌦 Weather")

    if "weather_data" not in st.session_state:

        from modules.weather_module import get_weather

        st.session_state.weather_data = get_weather(lat, lon)

    weather = st.session_state.weather_data
    st.write(weather)

    # -------------------------
    # NDVI
    # -------------------------
    st.subheader("🌱 NDVI")

    if "ndvi_value" not in st.session_state:

        from modules.gee_ndvi import get_ndvi

        st.session_state.ndvi_value = get_ndvi(lat, lon)

    ndvi = st.session_state.ndvi_value
    st.write("NDVI:", ndvi)

    # -------------------------
    # RECOMMENDATION
    # -------------------------
    st.subheader("🧠 Recommendation")

    if "recommendation" not in st.session_state:

        from modules.recommendation_engine import generate_recommendation

        st.session_state.recommendation = generate_recommendation(
            ndvi,
            weather,
            crop
        )

    rec = st.session_state.recommendation

    st.success(rec["status"])
    st.write(rec["irrigation"])
    st.write(rec["fertilizer"])
