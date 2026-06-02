def compute_ndvi_value(ndvi_value):

    if ndvi_value is None:
        return {"status": "No Data"}

    if ndvi_value < 0.2:
        return {
            "status": "Severe Stress",
            "level": 3
        }

    elif ndvi_value < 0.5:
        return {
            "status": "Moderate Stress",
            "level": 2
        }

    else:
        return {
            "status": "Healthy",
            "level": 1
        }
