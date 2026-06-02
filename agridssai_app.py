import streamlit as st
from modules.input_module import render_input_module
from modules.gis_module import render_gis_module
from modules.weather_module import render_weather_module
from modules.gee_ndvi import render_ndvi_module

# Page config (must be first Streamlit command)
st.set_page_config(
    page_title="AgriDSS_AI",
    layout="wide"
)

# ---------------------------
# HEADER
# ---------------------------
st.title("🌾 AgriDSS_AI")
st.subheader("AI + GIS + Remote Sensing Decision Support System")

# ---------------------------
# SIDEBAR NAVIGATION (BASE STRUCTURE)
# ---------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to:",
    [
        "Home",
        "Input Module",
        "GIS Viewer",
        "Weather Module",
        "NDVI (Coming Soon)",
        "Recommendation Engine (Coming Soon)"
    ]
)

# ---------------------------
# HOME PAGE
# ---------------------------
if page == "Home":
    st.success("System is running successfully 🚀")

    st.write("""
    Welcome to AgriDSS_AI.

    This system will integrate:
    - GIS analysis
    - Remote sensing (NDVI)
    - Weather intelligence
    - AI-based agricultural recommendations
    """)

# ---------------------------
# INPUT MODULE (PLACEHOLDER)
# ---------------------------
elif page == "Input Module":
    render_input_module()

# ---------------------------
# GIS VIEWER (PLACEHOLDER SAFE)
# ---------------------------
elif page == "GIS Viewer":
    render_gis_module()
    
    st.header("🗺️ GIS Viewer")

    st.warning("GIS module will be connected with shapefiles in next step.")

    st.write("District and tehsil maps will be rendered here.")

# ---------------------------
# WEATHER MODULE (PLACEHOLDER)
# ---------------------------
elif page == "Weather Module":
    render_weather_module()

    st.header("🌦️ Weather Module")

    st.warning("Weather API integration will be added later.")

    st.write("Real-time weather + forecasts will appear here.")

# ---------------------------
# NDVI Analysis
# ---------------------------
elif page == "NDVI Analysis":
    render_ndvi_module()
