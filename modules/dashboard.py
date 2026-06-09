import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import ee

from modules.gee_ndvi import get_ndvi_image


# -----------------------------
# SAFE GEE INIT
# -----------------------------
def init_gee():
    try:
        ee.Initialize()
    except Exception:
        pass


def render_dashboard():

    st.header("🗺 AgriDSS_AI - Satellite Intelligence Dashboard")

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
    # AUTO COLUMN DETECTION
    # -----------------------------
    district_col = None
    tehsil_col = None

    for col in gdf.columns:
        if col.lower() == "district":
            district_col = col
        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None or tehsil_col is None:
        st.error("District/Tehsil columns not found")
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
        st.error("Selected area not found")
        return

    geom = selected.geometry.iloc[0]
    center = geom.centroid

    # -----------------------------
    # BASE MAP
    # -----------------------------
    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    # -----------------------------
    # INIT GEE
    # -----------------------------
    init_gee()

    try:
        # -----------------------------
        # GET NDVI IMAGE FROM GEE
        # -----------------------------
        ndvi_img = get_ndvi_image(geom)

        # -----------------------------
        # CONVERT TO TILE LAYER (NO GEEMAP)
        # -----------------------------
        map_id_dict = ee.Image(ndvi_img).getMapId({
            "min": 0,
            "max": 1,
            "palette": ["red", "yellow", "green"]
        })

        tile_url = map_id_dict["tile_fetcher"].url_format

        folium.raster_layers.TileLayer(
            tiles=tile_url,
            name="NDVI",
            overlay=True,
            control=True,
            attr="Google Earth Engine"
        ).add_to(m)

    except Exception as e:
        st.error(f"NDVI loading error: {e}")

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
    st.subheader("🌍 NDVI Satellite Map (GEE)")
    st_folium(m, width=1200, height=600)

    # -----------------------------
    # LEGEND
    # -----------------------------
    st.subheader("🧭 NDVI Legend")

    st.markdown(
        """
        🔴 Red → Low Vegetation (Stress / Bare Soil)  
        🟡 Yellow → Moderate Vegetation  
        🟢 Green → Healthy Crops / Dense Vegetation  
        """
    )
