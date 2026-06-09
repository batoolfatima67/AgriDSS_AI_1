import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np


def render_dashboard():

    st.header("🗺 AgriDSS_AI Dashboard")

    # -----------------------------
    # GET FARM INPUT DATA
    # -----------------------------
    user_data = st.session_state.get("user_data")

    if not user_data:
        st.warning("Please complete Farm Input first.")
        return

    district = user_data.get("district")
    tehsil = user_data.get("tehsil")

    st.subheader("📍 Selected Farm Location")
    st.write(f"District: {district}")
    st.write(f"Tehsil: {tehsil}")

    # -----------------------------
    # LOAD SHAPEFILE
    # -----------------------------
    try:
        gdf = gpd.read_file("data/pakistan_tehsil.shp")
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
        return

    # -----------------------------
    # AUTO-DETECT COLUMNS (SAFE)
    # -----------------------------
    district_col = None
    tehsil_col = None

    for col in gdf.columns:
        if col.lower() == "district":
            district_col = col
        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None or tehsil_col is None:
        st.error("District or Tehsil columns not found in shapefile.")
        st.write("Available columns:", gdf.columns.tolist())
        return

    # -----------------------------
    # FILTER SELECTED AREA
    # -----------------------------
    selected = gdf[
        (gdf[district_col] == district) &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Selected location not found in shapefile.")
        return

    geom = selected.geometry.iloc[0]
    center = geom.centroid

    # -----------------------------
    # OPENSTREETMAP
    # -----------------------------
    st.subheader("🗺 Map View (OpenStreetMap)")

    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    folium.GeoJson(
        selected,
        style_function=lambda x: {
            "fillColor": "green",
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.3
        }
    ).add_to(m)

    st_folium(m, width=1200, height=500)

    # -----------------------------
    # NDVI DEMO (STABLE VERSION)
    # -----------------------------
    st.subheader("🌱 NDVI Time-Series (Demo)")

    ndvi_values = np.random.uniform(0.2, 0.9, 7)

    ndvi_df = pd.DataFrame({
        "Day": [
            "Day 1",
            "Day 2",
            "Day 3",
            "Day 4",
            "Day 5",
            "Day 6",
            "Day 7"
        ],
        "NDVI": ndvi_values
    })

    st.line_chart(ndvi_df.set_index("Day"))

    # -----------------------------
    # NDVI STATUS
    # -----------------------------
    latest_ndvi = ndvi_values[-1]

    st.subheader("🌱 Current NDVI Status")

    st.metric("NDVI", round(latest_ndvi, 2))

    if latest_ndvi > 0.6:
        st.success("Healthy Vegetation 🟢")
    elif latest_ndvi > 0.3:
        st.warning("Moderate Vegetation 🟡")
    else:
        st.error("Low Vegetation 🔴")
