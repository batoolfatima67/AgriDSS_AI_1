import ee
import pandas as pd
import streamlit as stt

def initialize_gee():

    service_account_info = dict(
    st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    )

    credentials = ee.ServiceAccountCredentials(
    service_account_info["client_email"],
    key_data=json.dumps(service_account_info)
    )

    ee.Initialize(credentials)

initialize_gee()

# --------------------------------
# INITIALIZE EARTH ENGINE
# --------------------------------
try:

    ee.Initialize(
        project="agri-ai-project-496918"
    )

except Exception:

    ee.Authenticate()

    ee.Initialize(
        project="agri-ai-project-496918"
    )

# --------------------------------
# SHAPELY → EE GEOMETRY
# --------------------------------
def shapely_to_ee(geometry):

    geometry = geometry.simplify(
        0.001
    )

    geo_json = geometry.__geo_interface__

    return ee.Geometry(
        geo_json
    )

# --------------------------------
# GET NDVI IMAGE
# --------------------------------
def get_ndvi_from_gee(geometry):

    # EE GEOMETRY
    ee_geometry = shapely_to_ee(
        geometry
    )

    # SENTINEL-2 COLLECTION
    collection = (
        ee.ImageCollection(
            "COPERNICUS/S2_SR_HARMONIZED"
        )
        .filterBounds(ee_geometry)
        .filterDate(
            "2025-01-01",
            "2025-12-31"
        )
        .filter(
            ee.Filter.lt(
                "CLOUDY_PIXEL_PERCENTAGE",
                20
            )
        )
        .select(
            ["B4", "B8"]
        )
    )

    # DEBUG
    print(
        "IMAGE COUNT:",
        collection.size().getInfo()
    )

    # MEDIAN IMAGE
    image = collection.median()

    # NDVI
    ndvi = image.normalizedDifference(
        ["B8", "B4"]
    ).rename("NDVI")

    return (
        ndvi.clip(ee_geometry),
        ee_geometry
    )

# --------------------------------
# NDVI STATISTICS
# --------------------------------
def get_ndvi_stats(
    ndvi_image,
    ee_geometry
):

    stats = ndvi_image.reduceRegion(

        reducer=ee.Reducer.mean(),

        geometry=ee_geometry,

        scale=10,

        maxPixels=1e9
    )

    return stats.getInfo()

# --------------------------------
# NDVI TILE LAYER
# --------------------------------
def get_ndvi_tile_layer(ndvi_image):

    vis_params = {
        "min": 0,
        "max": 1,
        "palette": [
            "red",
            "yellow",
            "green"
        ]
    }

    map_id = ndvi_image.getMapId(
        vis_params
    )

    return map_id["tile_fetcher"].url_format
 
