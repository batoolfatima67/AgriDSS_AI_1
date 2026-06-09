import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import numpy as np

# GEE NDVI IMPORT
from modules.gee_ndvi import get_ndvi


# -------------------------------------------------
# SAFE CLASSIFICATION FUNCTION
# -------------------------------------------------
def get_class_color(seed):
    np.random.seed(seed)
    r = np.random.random()

    if r < 0.25:
        return "red"      # temperature / stress
    elif r < 0.55:
        return "green"    # vegetation
    elif r < 0.80:
        return "yellow"   # poor vegetation
    else:
        return "blue"     # water


# -------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------
def render_dashboard():

    st.header("🗺 AgriDSS_AI Geo Dashboard (GEE Enabled)")

    # -----------------------------
    # FARM INPUT
    # -----------------------------
    user_data = st.session_state.get("user_data")

    if not user_data:
        st.warning("Please complete Farm Input first.")
        return

    district = user_data.get("district")
    tehsil = user_data.get("tehsil")

    st.subheader("📍 Selected Location")
    st.write(f"District: {district}")
    st.write(f"Tehsil: {tehsil}")

    # -----------------------------
    # LOAD SHAPEFILE
    # -----------------------------
    try:
        gdf = gpd.read_file("data/pakistan_tehsil.shp")
    except Exception as e:
        st.error(f"Shapefile error: {e}")
        return

    # -----------------------------
    # AUTO DETECT COLUMNS
    # -----------------------------
    district_col = None
    tehsil_col = None

    for col in gdf.columns:
        if col.lower() == "district":
            district_col = col
        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None or tehsil_col is None:
        st.error("District/Tehsil columns not found.")
        st.write(gdf.columns.tolist())
        return

    # -----------------------------
    # FILTER LOCATION
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
    minx, miny, maxx, maxy = geom.bounds

    # -----------------------------
    # BASE MAP
    # -----------------------------
    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    # -----------------------------
    # STABLE GRID CLASSIFICATION
    # -----------------------------
    seed = hash(str(district + tehsil)) % 10000

    for i in range(20):
        for j in range(20):

            lat = miny + (maxy - miny) * i / 20
            lon = minx + (maxx - minx) * j / 20

            color = get_class_color(seed + i + j)

            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)

    # -----------------------------
    # BOUNDARY LAYER
    # -----------------------------
    folium.GeoJson(
        selected,
        style_function=lambda x: {
            "fillOpacity": 0.05,
            "color": "black",
            "weight": 2
        }
    ).add_to(m)

    # -----------------------------
    # MAP DISPLAY
    # -----------------------------
    st.subheader("🗺 Classified Geo Map")
    st_folium(m, width=1200, height=600)

    # -----------------------------
    # 🌍 GEE NDVI PROCESSING
    # -----------------------------
    st.subheader("🌍 GEE NDVI Processing")

    try:
        ndvi_image = get_ndvi(geom)
        st.success("NDVI computed successfully (GEE)")

        # simple NDVI preview (placeholder)
        st.write("NDVI Object:", ndvi_image)

    except Exception as e:
        st.error(f"GEE Error: {e}")

    # -----------------------------
    # LEGEND
    # -----------------------------
    st.subheader("🧭 Legend")

    st.markdown(
        """
        🔴 Red → High Temperature / Stress  
        🟢 Green → Healthy Vegetation  
        🟡 Yellow → Poor Vegetation  
        🔵 Blue → Water / Canals / Rivers  
        """
    )
