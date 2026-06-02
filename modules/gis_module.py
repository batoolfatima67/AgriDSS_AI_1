import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os


def render_gis_module():

    st.header("🗺 GIS Viewer")

    # -----------------------------
    # GET USER LOCATION
    # -----------------------------
    user_data = st.session_state.get("user_data", None)

    if user_data:
        lat = user_data.get("latitude", 31.5204)
        lon = user_data.get("longitude", 74.3587)
    else:
        lat, lon = 31.5204, 74.3587
        st.warning("Using default location. Please enter input first.")

    # -----------------------------
    # FILE PATH
    # -----------------------------
    shp_path = "data/districts.shp"

    if not os.path.exists(shp_path):
        st.error("Shapefile not found in /data folder.")
        return

    # -----------------------------
    # LOAD SHAPEFILE SAFELY
    # -----------------------------
    try:
        gdf = gpd.read_file(shp_path)

    except Exception as e:
        st.error("Error loading shapefile.")
        st.exception(e)
        return

    # -----------------------------
    # CREATE MAP
    # -----------------------------
    m = folium.Map(location=[lat, lon], zoom_start=7)

    # Add district boundaries
    folium.GeoJson(
        gdf,
        name="Districts"
    ).add_to(m)

    # Add user location marker
    folium.Marker(
        location=[lat, lon],
        popup="User Location",
        icon=folium.Icon(color="red")
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # -----------------------------
    # RENDER MAP
    # -----------------------------
    st_folium(m, width=1000, height=600)

    # -----------------------------
    # BASIC INFO
    # -----------------------------
    st.subheader("Dataset Info")

    st.write("Number of districts:", len(gdf))

    st.write("Columns:", list(gdf.columns))
