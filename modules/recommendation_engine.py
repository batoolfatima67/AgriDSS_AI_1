import streamlit as st


def generate_recommendation(ndvi, weather, crop):

    recommendation = {
        "status": "",
        "irrigation": "",
        "fertilizer": "",
        "risk": ""
    }

    # ---------------------------
    # NDVI LOGIC (PRIMARY DRIVER)
    # ---------------------------
    if ndvi < 0.2:
        recommendation["status"] = "Severe Stress"
        recommendation["irrigation"] = "Immediate irrigation required"
        recommendation["fertilizer"] = "High nitrogen fertilizer recommended"
        recommendation["risk"] = "High crop failure risk"

    elif ndvi < 0.5:
        recommendation["status"] = "Moderate Stress"
        recommendation["irrigation"] = "Schedule irrigation within 2–3 days"
        recommendation["fertilizer"] = "Balanced NPK fertilizer suggested"
        recommendation["risk"] = "Moderate risk"

    else:
        recommendation["status"] = "Healthy Crop"
        recommendation["irrigation"] = "Normal irrigation schedule"
        recommendation["fertilizer"] = "No immediate fertilizer needed"
        recommendation["risk"] = "Low risk"

    # ---------------------------
    # WEATHER MODIFICATION LOGIC
    # ---------------------------
    temp = weather["temp"]
    humidity = weather["humidity"]

    if temp > 35:
        recommendation["irrigation"] += " (Increase frequency due to heat stress)"

    if humidity < 30:
        recommendation["risk"] += " + Drought stress warning"

    # ---------------------------
    # CROP-SPECIFIC LOGIC
    # ---------------------------
    if crop == "Rice" and ndvi < 0.3:
        recommendation["fertilizer"] += " | Paddy requires urgent nutrient correction"

    if crop == "Wheat" and temp > 30:
        recommendation["risk"] += " | Heat stress during grain formation"

    return recommendation


# ---------------------------
# STREAMLIT MODULE
# ---------------------------
def render_recommendation_module():

    st.header("🧠 AI Recommendation Engine")

    user_data = st.session_state.get("user_data", None)
    weather_data = st.session_state.get("weather_data", None)
    ndvi_value = st.session_state.get("ndvi_value", None)

    if not user_data:
        st.warning("Please complete Input Module first.")
        return

    if ndvi_value is None:
        st.warning("Run NDVI analysis first.")
        return

    if weather_data is None:
        st.warning("Run Weather module first.")
        return

    crop = user_data["crop"]

    st.write("Generating AI recommendations...")

    result = generate_recommendation(ndvi_value, weather_data, crop)

    st.subheader("📊 Crop Intelligence Report")

    st.success(f"Status: {result['status']}")
    st.info(f"Irrigation: {result['irrigation']}")
    st.info(f"Fertilizer: {result['fertilizer']}")

    if "High" in result["risk"]:
        st.error(f"Risk: {result['risk']}")
    else:
        st.warning(f"Risk: {result['risk']}")
