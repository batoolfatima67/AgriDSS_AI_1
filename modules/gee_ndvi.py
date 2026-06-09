import ee
import streamlit as st


# -----------------------------
# INITIALIZE GOOGLE EARTH ENGINE
# -----------------------------
def initialize_gee():

    try:
        ee.Initialize()

    except Exception:
        ee.Authenticate()
        ee.Initialize()


# -----------------------------
# CORE NDVI FUNCTION (SAFE)
# -----------------------------
def get_ndvi(lat, lon):

    try:

        initialize_gee()

        point = ee.Geometry.Point([lon, lat])

        image = (
            ee.ImageCollection("COPERNICUS/S2_SR")
            .filterBounds(point)
            .filterDate("2025-01-01", "2025-12-31")
            .sort("CLOUD_COVER")
            .first()
        )

        # if no image found
        if image is None:
            return None

        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")

        value = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10,
            maxPixels=1e9
        ).get("NDVI")

        if value is None:
            return None

        return value.getInfo()


    except Exception:
        return None
