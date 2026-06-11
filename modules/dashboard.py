import ee
import json
import streamlit as st

# -----------------------------------
# CACHE SHAPEFILE (FAST LOAD)import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

from modules.gee_ndvi import (
    get_ndvi_from_gee,
    get_ndvi_map_url,
    get_ndvi_stats
)

# -----------------------------------
# CACHE SHAPEFILE
# -----------------------------------
@st.cache_data
def load_shapefile():
    return gpd.read_file("data/pakistan_tehsil.shp")


# -----------------------------------
# DASHBOARD
# -----------------------------------
def render_dashboard():

    st.header("🗺 AgriDSS_AI Smart Geo Dashboard")

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
    # LOAD DATA
    # -----------------------------
    gdf = load_shapefile()

    district_col = None
    tehsil_col = None

    for col in gdf.columns:
        if col.lower() == "district":
            district_col = col
        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None or tehsil_col is None:
        st.error("Missing district/tehsil columns")
        return

    selected = gdf[
        (gdf[district_col] == district) &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Location not found")
        return

    geom = selected.geometry.iloc[0]
    center = geom.centroid

    # -----------------------------
    # MAP BASE
    # -----------------------------
    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    folium.GeoJson(
        selected,
        style_function=lambda x: {
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.05
        }
    ).add_to(m)

    # -----------------------------
    # NDVI PROCESSING
    # -----------------------------
    avg_ndvi = None

    try:
        ndvi_image, ee_geom = get_ndvi_from_gee(geom)

        ndvi_url = get_ndvi_map_url(ndvi_image)

        folium.raster_layers.TileLayer(
            tiles=ndvi_url,
            name="🌿 NDVI Layer",
            overlay=True,
            control=True,
            attr="Sentinel-2 | Google Earth Engine"
        ).add_to(m)

        ndvi_stats = get_ndvi_stats(ndvi_image, ee_geom)
        avg_ndvi = ndvi_stats.get("NDVI", None)

    except Exception as e:
        st.warning(f"NDVI error: {e}")

    folium.LayerControl().add_to(m)

    # -----------------------------
    # MAP OUTPUT
    # -----------------------------
    st.subheader("🌍 Satellite NDVI Map")
    st_folium(m, width=1200, height=600)

    # -----------------------------
    # ANALYTICS
    # -----------------------------
    st.subheader("📊 Vegetation Analytics")

    if avg_ndvi is not None:

        st.metric("🌿 Average NDVI", round(avg_ndvi, 3))

        # Zone classification
        if avg_ndvi < 0.2:
            st.error("🔴 High Vegetation Stress Zone")
        elif avg_ndvi < 0.4:
            st.warning("🟡 Moderate Vegetation Zone")
        elif avg_ndvi < 0.6:
            st.success("🟢 Healthy Vegetation Zone")
        else:
            st.success("🌳 Dense Vegetation Zone")

        # Agriculture Insight
        st.subheader("🚜 Agriculture Insight")

        if avg_ndvi < 0.2:
            st.error("🚨 Immediate irrigation required")
        elif avg_ndvi < 0.4:
            st.warning("⚠ Irrigation needed soon (3–5 days)")
        elif avg_ndvi < 0.6:
            st.info("🌱 Monitor soil moisture")
        else:
            st.success("🌿 Excellent crop condition")

    else:
        st.info("NDVI data not available")
# -----------------------------------
@st.cache_data
def load_shapefile():
    return gpd.read_file("data/pakistan_tehsil.shp")

# -----------------------------------
# GEE INITIALIZATION (SAFE)
# -----------------------------------
def initialize_gee():

    try:
        service_account_info = dict(st.secrets["GOOGLE_SERVICE_ACCOUNT"])

        credentials = ee.ServiceAccountCredentials(
            service_account_info["client_email"],
            key_data=json.dumps(service_account_info)
        )

        ee.Initialize(credentials)

    except Exception as e:
        st.error(f"GEE Initialization Failed: {e}")


initialize_gee()

# -----------------------------------
# SHAPE → EE GEOMETRY
# -----------------------------------
def shapely_to_ee(geometry):
    geo_json = geometry.__geo_interface__
    return ee.Geometry(geo_json)


# -----------------------------------
# NDVI FROM SENTINEL-2
# -----------------------------------
def get_ndvi_from_gee(geometry):

    ee_geometry = shapely_to_ee(geometry)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(ee_geometry)
        .filterDate("2025-01-01", "2025-12-31")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .select(["B4", "B8"])
    )

    image = collection.median()

    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")

    return ndvi.clip(ee_geometry), ee_geometry


# -----------------------------------
# NDVI TILE LAYER (PRO GIS)
# -----------------------------------
def get_ndvi_map_url(ndvi_image):

    vis_params = {
        "min": -0.2,
        "max": 0.8,
        "palette": [
            "#8b0000",
            "#ff4d4d",
            "#ffff66",
            "#66cc66",
            "#006400"
        ]
    }

    map_id = ndvi_image.getMapId(vis_params)
    return map_id["tile_fetcher"].url_format


# -----------------------------------
# NDVI STATISTICS
# -----------------------------------
def get_ndvi_stats(ndvi_image, ee_geometry):

    stats = ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=ee_geometry,
        scale=10,
        maxPixels=1e9
    )

    return stats.getInfo()


# -----------------------------------
# OPTIONAL: VEGETATION CLASSIFICATION
# -----------------------------------
def classify_ndvi(ndvi_image, ee_geometry):

    classified = ndvi_image.expression(
        """
        (b('NDVI') < 0.2) ? 0 :
        (b('NDVI') < 0.4) ? 1 :
        (b('NDVI') < 0.6) ? 2 : 3
        """,
        {"NDVI": ndvi_image}
    )

    return classified.clip(ee_geometry)
    
