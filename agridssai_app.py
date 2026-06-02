import streamlit as st

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
    st.header("📥 Input Module")

    st.info("This module will collect user location, crop type, and farm parameters.")

    st.text_input("Enter Location")
    st.selectbox("Select Crop", ["Wheat", "Rice", "Maize"])

# ---------------------------
# GIS VIEWER (PLACEHOLDER SAFE)
# ---------------------------
elif page == "GIS Viewer":
    st.header("🗺️ GIS Viewer")

    st.warning("GIS module will be connected with shapefiles in next step.")

    st.write("District and tehsil maps will be rendered here.")

# ---------------------------
# WEATHER MODULE (PLACEHOLDER)
# ---------------------------
elif page == "Weather Module":
    st.header("🌦️ Weather Module")

    st.warning("Weather API integration will be added later.")

    st.write("Real-time weather + forecasts will appear here.")
