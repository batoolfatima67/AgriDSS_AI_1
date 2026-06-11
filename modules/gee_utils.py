# modules/gee_utils.py

import ee

def shapely_to_ee(geometry):
    """
    Convert shapely geometry → Earth Engine geometry
    """
    geo_json = geometry.__geo_interface__
    return ee.Geometry(geo_json)


def init_gee():
    """
    Safe initialization (prevents repeated auth errors)
    """
    try:
        ee.Initialize()
    except Exception:
        ee.Authenticate()
        ee.Initialize()
