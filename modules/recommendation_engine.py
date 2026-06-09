def generate_recommendation(ndvi, weather, crop):

    if ndvi < 0.3:
        return {
            "status": "Stress",
            "irrigation": "Immediate irrigation",
            "fertilizer": "High nitrogen required"
        }

    return {
        "status": "Healthy",
        "irrigation": "Normal schedule",
        "fertilizer": "No urgent need"
    }
