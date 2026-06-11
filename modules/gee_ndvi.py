import ee
import json
import streamlit as st

@st.cache_data
def get_ndvi_cached(geometry):
    return get_ndvi_from_gee(geometry)
    
# --------------------------------
# SAFE INITIALIZATION
# --------------------------------
def initialize_gee():

    if "GOOGLE_SERVICE_ACCOUNT" not in st.secrets:
        return False, "Missing GOOGLE_SERVICE_ACCOUNT in Streamlit secrets"

    try:
        service_account_info = dict(
            st.secrets["GOOGLE_SERVICE_ACCOUNT"]
        )

        credentials = ee.ServiceAccountCredentials(
            service_account_info["client_email"],
            key_data=json.dumps(service_account_info)
        )

        ee.Initialize(
            credentials,
            project=service_account_info.get(
                "project_id",
                "agri-ai-project-496918"
            )
        )

        return True, "GEE Initialized"

    except Exception as e:
        return False, f"GEE Init Error: {e}"


# --------------------------------
# SHAPELY → EE
# --------------------------------
def shapely_to_ee(geometry):

    return ee.Geometry(
        geometry.__geo_interface__
    )


# --------------------------------
# NDVI
# --------------------------------
def get_ndvi_from_gee(geometry):

    status, msg = initialize_gee()

    if not status:
        raise Exception(msg)

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


# --------------------------------
# STATS
# --------------------------------
def get_ndvi_stats(ndvi_image, ee_geometry):

    stats = ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=ee_geometry,
        scale=10,
        maxPixels=1e9
    )

    return stats.getInfo()


# --------------------------------
# TILE
# --------------------------------
def get_ndvi_tile_layer(ndvi_image):

    vis = {
        "min": 0,
        "max": 1,
        "palette": ["red", "yellow", "green"]
    }

    map_id = ndvi_image.getMapId(vis)

    return map_id["tile_fetcher"].url_format

# REAL_MAP_LAYER
def get_ndvi_map_url(ndvi_image):

    vis_params = {
        "min": -0.2,
        "max": 0.8,
        "palette": [
            "#8b0000",   # very low vegetation
            "#ff4d4d",   # stress
            "#ffff66",   # moderate vegetation
            "#66cc66",   # healthy vegetation
            "#006400"    # dense vegetation
        ]
    }

    map_id = ndvi_image.getMapId(vis_params)

    return map_id["tile_fetcher"].url_format
