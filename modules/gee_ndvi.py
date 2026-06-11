import ee
import json
import streamlit as st


# --------------------------------
# INITIALIZE EARTH ENGINE
# --------------------------------
def initialize_gee():

    service_account_info = dict(
        st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    )

    credentials = ee.ServiceAccountCredentials(
        service_account_info["client_email"],
        key_data=json.dumps(service_account_info)
    )

    ee.Initialize(
        credentials,
        project="agri-ai-project-496918"
    )


try:
    initialize_gee()

except Exception as e:
    print("GEE Initialization Error:", e)


# --------------------------------
# SHAPELY → EE GEOMETRY
# --------------------------------
def shapely_to_ee(geometry):

    geometry = geometry.simplify(0.001)

    geo_json = geometry.__geo_interface__

    return ee.Geometry(geo_json)


# --------------------------------
# GET NDVI IMAGE
# --------------------------------
def get_ndvi_from_gee(geometry):

    ee_geometry = shapely_to_ee(
        geometry
    )

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

    image = collection.median()

    ndvi = image.normalizedDifference(
        ["B8", "B4"]
    ).rename("NDVI")

    return (
        ndvi.clip(ee_geometry),
        ee_geometry
    )


# --------------------------------
# NDVI STATS
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
# TILE URL
# --------------------------------
def get_ndvi_tile_layer(
    ndvi_image
):

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

    return map_id[
        "tile_fetcher"
    ].url_format
