import streamlit as st
import folium
from streamlit_folium import st_folium


def render_map_module():

    st.title("🌍 Farm Location Map")

    # Default location (Karachi)
    default_lat = 24.8607
    default_lon = 67.0011

    m = folium.Map(location=[default_lat, default_lon], zoom_start=6)

    # Click on map
    map_data = st_folium(m, height=500)

    if map_data and map_data.get("last_clicked"):

        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]

        st.success(f"Selected Location: {lat}, {lon}")

        st.session_state.location = {
            "lat": lat,
            "lon": lon
        }
