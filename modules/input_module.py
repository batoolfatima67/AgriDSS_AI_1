import streamlit as st
import hashlib
import json
from modules.cache_manager import init_cache, update_cache, get_cache
from modules.hash_utils import generate_input_hash

def generate_input_hash(user_data):
    return hashlib.md5(
        json.dumps(user_data, sort_keys=True).encode()
    ).hexdigest()

def render_input_module():
    st.header("📥 Input Module")

    st.info("Enter farm details. This data will be used across GIS, NDVI, and AI modules.")

    # -----------------------------
    # SESSION STATE INIT (CRITICAL)
    # -----------------------------
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    # -----------------------------
    # LOCATION INPUT
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        lat = st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=31.5204
        )

    with col2:
        lon = st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=74.3587
        )

    # -----------------------------
    # CROP SELECTION
    # -----------------------------
    crop = st.selectbox(
        "Select Crop",
        ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"]
    )

    # -----------------------------
    # FARM SIZE
    # -----------------------------
    area = st.number_input(
        "Farm Area (Acres)",
        min_value=0.1,
        value=5.0
    )

    # -----------------------------
    # IRRIGATION TYPE
    # -----------------------------
    irrigation = st.selectbox(
        "Irrigation Type",
        ["Flood", "Drip", "Sprinkler", "Canal", "Rainfed"]
    )

    # -----------------------------
    # SAVE BUTTON
    # -----------------------------
    if st.button("Save Input Data"):

    st.session_state.user_data = {
        "latitude": lat,
        "longitude": lon,
        "crop": crop,
        "area": area,
        "irrigation": irrigation
    }

    new_hash = generate_input_hash(st.session_state.user_data)
    old_hash = get_cache("last_input_hash")

    if new_hash != old_hash:
        update_cache("last_input_hash", new_hash)

        # invalidate dependent modules
        update_cache("weather", None)
        update_cache("ndvi", None)
        update_cache("recommendation", None)

    st.success("Input saved & system updated 🚀")

    # -----------------------------
    # SHOW STORED DATA
    # -----------------------------
    if st.session_state.user_data:
        st.subheader("Current Saved Data")
        st.json(st.session_state.user_data)
