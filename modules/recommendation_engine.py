# ---------------------------
# CORE AI RECOMMENDATION ENGINE
# ---------------------------
def generate_recommendation(ndvi, weather, crop):

    # SAFE DEFAULT OUTPUT
    recommendation = {
        "status": "No Data",
        "irrigation": "No recommendation available",
        "fertilizer": "No recommendation available",
        "risk": "Unknown"
    }

    # ---------------------------
    # VALIDATION (VERY IMPORTANT)
    # ---------------------------
    if ndvi is None or weather is None:
        return recommendation

    # Safe weather extraction
    temp = weather.get("temperature", {}).get("value", 30)
    humidity = weather.get("humidity", {}).get("value", 50)

    # ---------------------------
    # NDVI BASED LOGIC (MAIN DRIVER)
    # ---------------------------
    if ndvi < 0.2:

        recommendation["status"] = "Severe Stress"
        recommendation["irrigation"] = "Immediate irrigation required"
        recommendation["fertilizer"] = "High nitrogen fertilizer recommended"
        recommendation["risk"] = "High crop failure risk"

    elif ndvi < 0.5:

        recommendation["status"] = "Moderate Stress"
        recommendation["irrigation"] = "Irrigation required within 2–3 days"
        recommendation["fertilizer"] = "Balanced NPK fertilizer suggested"
        recommendation["risk"] = "Moderate risk"

    else:

        recommendation["status"] = "Healthy Crop"
        recommendation["irrigation"] = "Normal irrigation schedule"
        recommendation["fertilizer"] = "No immediate fertilizer needed"
        recommendation["risk"] = "Low risk"

    # ---------------------------
    # WEATHER MODIFICATIONS
    # ---------------------------
    if temp > 35:
        recommendation["irrigation"] += " | Increase due to heat stress"
        recommendation["risk"] += " | Heat stress risk"

    if humidity < 30:
        recommendation["risk"] += " | Drought stress warning"

    # ---------------------------
    # CROP-SPECIFIC LOGIC
    # ---------------------------
    if crop == "Rice" and ndvi < 0.3:
        recommendation["fertilizer"] += " | Rice requires urgent nutrient correction"

    if crop == "Wheat" and temp > 30:
        recommendation["risk"] += " | Wheat heat stress during grain formation"

    return recommendation
