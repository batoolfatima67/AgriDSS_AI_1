import ee

# Initialize once
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()


def get_ndvi_image(geometry):

    # Convert shapefile geometry to GEE object
    coords = geometry.__geo_interface__["coordinates"]

    region = ee.Geometry.Polygon(coords)

    # Sentinel-2 image collection
    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(region)
        .filterDate("2024-01-01", "2024-12-31")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .median()
    )

    # NDVI calculation
    ndvi = collection.normalizedDifference(
        ["B8", "B4"]
    ).rename("NDVI")

    return ndvi.clip(region)
