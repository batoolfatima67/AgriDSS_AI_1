import ee

# -----------------------------
# SAFE INITIALIZATION ONLY
# -----------------------------
def initialize_gee():

    try:
        ee.Initialize()
    except Exception:
        # In Streamlit Cloud, we do NOT authenticate here
        # Authentication must be done locally only
        raise Exception(
            "Google Earth Engine not initialized. "
            "Run ee.Initialize() locally first."
        )


# -----------------------------
# NDVI FUNCTION (SAFE)
# -----------------------------
def get_ndvi_image(geometry):

    initialize_gee()

    coords = geometry.__geo_interface__["coordinates"]

    region = ee.Geometry.Polygon(coords)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(region)
        .filterDate("2024-01-01", "2024-12-31")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .median()
    )

    ndvi = collection.normalizedDifference(["B8", "B4"]).rename("NDVI")

    return ndvi.clip(region)
