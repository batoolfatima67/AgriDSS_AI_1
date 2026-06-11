import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

from modules.gee_ndvi import (
    get_ndvi_from_gee,
    get_ndvi_map_url
)

# -----------------------------------
# CACHE SHAPEFILE (FAST LOADING)
# -----------------------------------
@st.cache_data
def load_shapefile():
    return gpd.read_file("data/pakistan_tehsil.shp")


# -----------------------------------
# MAIN DASHBOARD
# -----------------------------------
def render_dashboard():

    st.header("🗺 AgriDSS_AI Smart Geo Dashboard")

    # -----------------------------
    # USER INPUT FROM SESSION
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
    # LOAD DATA (CACHED)
    # -----------------------------
    gdf = load_shapefile()

    # detect columns safely
    district_col = None
    tehsil_col = None

    for col in gdf.columns:
        if col.lower() == "district":
            district_col = col
        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None or tehsil_col is None:
        st.error("District/Tehsil columns not found in shapefile")
        return

    # -----------------------------
    # FILTER LOCATION
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

    # -----------------------------
    # CREATE BASE MAP
    # -----------------------------
    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    # -----------------------------
    # ADD BOUNDARY
    # -----------------------------
    folium.GeoJson(
        selected,
        style_function=lambda x: {
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.05
        }
    ).add_to(m)

    # -----------------------------
    # NDVI (REAL SATELLITE LAYER)
    # -----------------------------
    try:
        ndvi_image, ee_geom = get_ndvi_from_gee(geom)

        ndvi_url = get_ndvi_map_url(ndvi_image)

        folium.raster_layers.TileLayer(
            tiles=ndvi_url,
            name="NDVI (Sentinel-2)",
            overlay=True,
            control=True
        ).add_to(m)

    except Exception as e:
        st.warning(f"NDVI not loaded: {e}")

    # -----------------------------
    # LAYER CONTROL
    # -----------------------------
    folium.LayerControl().add_to(m)

    # -----------------------------
    # DISPLAY MAP
    # -----------------------------
    st.subheader("🌍 Satellite NDVI Map")
    st_folium(m, width=1200, height=600)
