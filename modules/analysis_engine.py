import streamlit as st

from modules.weather_module import get_weather
from modules.gee_ndvi import get_ndvi
from modules.recommendation_engine import generate_recommendation


# -----------------------------
# RUN FULL AI ANALYSIS PIPELINE
# -----------------------------
def run_full_analysis(lat, lon, crop):

    st.info("🚀 Running AgriDSS AI Analysis Pipeline...")

    # -------------------------
    # STEP 1: WEATHER
    # -------------------------
    weather = get_weather(lat, lon)

    if weather is None:
        st.warning("Weather data not available. Using fallback values.")
        weather = {
            "temperature": {"value": 30},
            "humidity": {"value": 50},
            "wind_speed": {"value": 5},
            "condition": "unknown"
        }

    st.session_state.weather = weather


    # -------------------------
    # STEP 2: NDVI
    # -------------------------
    ndvi_value = get_ndvi(lat, lon)

    if ndvi_value is None:
        st.warning("NDVI not available. Using default value.")
        ndvi_value = 0.4

    st.session_state.ndvi_value = ndvi_value


    # -------------------------
    # STEP 3: AI RECOMMENDATION
    # -------------------------
    recommendation = generate_recommendation(
        ndvi_value,
        weather,
        crop
    )

    st.session_state.recommendation = recommendation


    # -------------------------
    # STEP 4: RETURN RESULTS
    # -------------------------
    return {
        "weather": weather,
        "ndvi": ndvi_value,
        "recommendation": recommendation
    }
