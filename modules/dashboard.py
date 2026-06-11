import ee
import json
import streamlit as st

# -----------------------------------
# CACHE SHAPEFILE (FAST LOAD)
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

