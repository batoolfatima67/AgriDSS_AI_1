import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

from modules.gee_ndvi import (
    get_ndvi_from_gee,
    get_ndvi_tile_layer,
    get_ndvi_stats
)

@st.cache_data
def load_shapefile():
    return gpd.read_file("data/pakistan_tehsil.shp")
    
def render_dashboard():

    st.header("🗺 AgriDSS_AI Smart Geo Dashboard")

    user_data = st.session_state.get("user_data")

    if not user_data:
        st.warning("Please complete Farm Input first.")
        return

    district = user_data.get("district")
    tehsil = user_data.get("tehsil")

    # -----------------------------
    # LOAD SHAPEFILE
    # -----------------------------
    gdf = load_shapefile()

    district_col = None
    tehsil_col = None

    for col in gdf.columns:
        if col.lower() == "district":
            district_col = col
        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None:
        district_col = gdf.columns[0]

    if tehsil_col is None:
        tehsil_col = gdf.columns[1]

    selected = gdf[
        (gdf[district_col] == district) &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Area not found in shapefile")
        return

    geom = selected.geometry.iloc[0]
    center = geom.centroid

    # -----------------------------
    # MAP
    # -----------------------------
    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    ndvi_value = None

    # -----------------------------
    # SAFE NDVI BLOCK
    # -----------------------------
    try:

        ndvi_image, ee_geometry = get_ndvi_from_gee(geom)

        tile_url = get_ndvi_tile_layer(ndvi_image)

        folium.TileLayer(
            tiles=tile_url,
            name="NDVI",
            attr="GEE",
            overlay=True,
            control=True
        ).add_to(m)

        stats = get_ndvi_stats(ndvi_image, ee_geometry)
        ndvi_value = stats.get("NDVI")

    except Exception as e:
        st.warning(f"NDVI not loaded: {e}")

    # -----------------------------
    # BOUNDARY
    # -----------------------------
    folium.GeoJson(
        selected,
        style_function=lambda x: {
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.05
        }
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.subheader("🌍 Map View")
    st_folium(m, width=1200, height=600)

    if ndvi_value:
        st.metric("NDVI Mean", round(ndvi_value, 3))
    else:
        st.info("NDVI not available (check GEE setup)")
