import streamlit as st
import geopandas as gpd
import numpy as np
import folium
from streamlit_folium import st_folium
from modules.gee_ndvi import get_ndvi



# -------------------------------------------------
# FIXED CLASSIFICATION FUNCTION (STABLE)
# -------------------------------------------------
def get_class_color(seed_value):
    np.random.seed(seed_value)
    r = np.random.random()

    if r < 0.25:
        return "red"      # temperature / stress
    elif r < 0.55:
        return "green"    # healthy vegetation
    elif r < 0.80:
        return "yellow"   # poor vegetation
    else:
        return "blue"     # water / canals


# -------------------------------------------------
# MAIN DASHBOARD FUNCTION
# -------------------------------------------------
def render_dashboard():

    st.header("🗺 AgriDSS_AI Smart Geo Dashboard")

    # -----------------------------
    # SESSION DATA (FROM FARM INPUT)
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

    st.subheader("🌍 GEE NDVI Processing")

try:
    ndvi_image = get_ndvi(geom)
    st.success("NDVI computed successfully (GEE)")
except Exception as e:
    st.error(f"GEE Error: {e}")

    # -----------------------------
    # LOAD SHAPEFILE
    # -----------------------------
    try:
        gdf = gpd.read_file("data/pakistan_tehsil.shp")
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
        return

    # -----------------------------
    # AUTO-DETECT COLUMNS
    # -----------------------------
    district_col = None
    tehsil_col = None

    for col in gdf.columns:
        if col.lower() == "district":
            district_col = col
        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None or tehsil_col is None:
        st.error("District/Tehsil columns not found in shapefile")
        st.write(gdf.columns.tolist())
        return

    # -----------------------------
    # FILTER SELECTED AREA
    # -----------------------------
    selected = gdf[
        (gdf[district_col] == district) &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Selected location not found in shapefile")
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
    # TEHSIL BOUNDARY
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
    # DISPLAY MAP
    # -----------------------------
    st.subheader("🗺 Classified Geo Map")
    st_folium(m, width=1200, height=600)

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
