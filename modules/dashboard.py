import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from modules.gee_ndvi import get_ndvi_image

import ee

# ensure initialized safely
try:
    ee.Initialize()
except:
    pass

def render_dashboard():

    st.header("🗺 AgriDSS_AI - Satellite Intelligence Dashboard")

    # -----------------------------
    # FARM INPUT DATA
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
        st.error("Selected area not found in dataset")
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
    # REAL GEE NDVI LAYER
    # -----------------------------
    try:
        ndvi_img = get_ndvi_image(geom)

        vis_params = {
            "min": 0,
            "max": 1,
            "palette": ["red", "yellow", "green"]
        }

        ndvi_layer = geemap.ee_tile_layer(ndvi_img, vis_params, "NDVI")
        ndvi_layer.add_to(m)

    except Exception as e:
        st.error(f"GEE NDVI Error: {e}")

    # -----------------------------
    # GET NDVI IMAGE
    # -----------------------------
    ndvi_img = get_ndvi_image(geom)

    # -----------------------------
    # GET TILE LAYER (NO GEEMAP)
    # -----------------------------
    map_id_dict = ee.Image(ndvi_img).getMapId({
       "min": 0,
       "max": 1,
       "palette": ["red", "yellow", "green"]
    })

tile_url = map_id_dict["tile_fetcher"].url_format

# -----------------------------
# ADD TO FOLIUM
# -----------------------------
folium.raster_layers.TileLayer(
    tiles=tile_url,
    attr="Google Earth Engine",
    name="NDVI",
    overlay=True,
    control=True
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
    st.subheader("🌍 Satellite NDVI Map (GEE)")
    st_folium(m, width=1200, height=600)

    # -----------------------------
    # LEGEND
    # -----------------------------
    st.subheader("🧭 Legend")

    st.markdown(
        """
        🟢 Green → High Vegetation (Healthy Crops)  
        🟡 Yellow → Moderate Vegetation  
        🔴 Red → Low Vegetation / Stress Areas  
        """
    )
