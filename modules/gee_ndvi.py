import ee
import streamlit as st


def get_ndvi(lat, lon):

    # TEMPORARY SIMULATION (for testing system)
    # Later we replace this with Google Earth Engine

    if lat and lon:
        ndvi = 0.65
    else:
        ndvi = 0.0

    return ndvi
