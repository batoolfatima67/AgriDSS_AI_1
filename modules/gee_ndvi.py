import ee
import streamlit as st

# Initialize once
def init_gee():
    try:
        ee.Initialize()
    except Exception:
        ee.Authenticate()
        ee.Initialize()


def get_ndvi(district_geom):

    init_gee()

    # Convert geometry to GEE format
    coords = district_geom.__geo_interface__["coordinates"]

    region = ee.Geometry.Polygon(coords)

    # Sentinel-2 image collection
    dataset = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(region) \
        .filterDate("2024-01-01", "2024-12-31") \
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20)) \
        .median()

    ndvi = dataset.normalizedDifference(["B8", "B4"]).rename("NDVI")

    return ndvi
