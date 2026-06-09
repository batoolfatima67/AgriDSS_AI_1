import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import random


def render_dashboard():

    st.header("🗺 AgriDSS_AI - Smart Geo Dashboard")

    # -----------------------------
    # GET FARM INPUT DATA
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
        st.error(f"Shapefile loading error: {e}")
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
        st.error("Required columns not found in shapefile")
        st.write(gdf.columns.tolist())
        return

    # -----------------------------
    # FILTER AREA
    # -----------------------------
    selected = gdf[
        (gdf[district_col] == district) &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Selected area not found in dataset")
        return

    geom = selected.geometry.iloc[0]
    center = geom.centroid

    # -----------------------------
    # CREATE BASE MAP
    # -----------------------------
    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    # -----------------------------
    # SATELLITE-LIKE CLASSIFIED LAYER
    # -----------------------------
    minx, miny, maxx, maxy = geom.bounds

    def get_class_color(seed):
      np.random.seed(seed)
      r = np.random.random()

    if r < 0.25:
        return "red"
    elif r < 0.55:
        return "green"
    elif r < 0.80:
        return "yellow"
    else:
        return "blue"

    seed = hash(str(district + tehsil)) % 10000

    # Create grid overlay
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
    # SHOW MAP
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
        🔵 Blue → Water Bodies (Canals/Rivers)
        """
    )
