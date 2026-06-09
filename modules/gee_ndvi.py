import ee
import geemap

# Initialize Earth Engine
ee.Initialize()


def get_ndvi(district_geom):

    # Convert shapely geometry → EE geometry
    coords = district_geom.__geo_interface__["coordinates"]

    region = ee.Geometry.Polygon(coords)

    # Sentinel-2 Image Collection
    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(region)
        .filterDate("2024-01-01", "2024-12-31")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .median()
    )

    # NDVI Calculation
    ndvi = collection.normalizedDifference(
        ["B8", "B4"]
    ).rename("NDVI")

    return ndvi, region
