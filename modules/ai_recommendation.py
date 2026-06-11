import streamlit as st

def render_ai_recommendation():

    st.header("🌾 AI Crop Recommendation System")

    user_data = st.session_state.get("user_data")

    if not user_data:
        st.warning("Please complete Farm Input first.")
        return

    district = user_data.get("district")
    tehsil = user_data.get("tehsil")
    crop = user_data.get("crop", "Unknown")

    st.subheader("📍 Location Info")
    st.write(f"District: {district}")
    st.write(f"Tehsil: {tehsil}")
    st.write(f"Crop: {crop}")

    # -----------------------------
    # NDVI INPUT (FROM SESSION OR DEFAULT)
    # -----------------------------
    avg_ndvi = user_data.get("avg_ndvi", None)

    if avg_ndvi is None:
        st.warning("NDVI not available. Run analysis first.")
        return

    # -----------------------------
    # AI LOGIC ENGINE
    # -----------------------------
    st.subheader("🤖 AI Recommendation")

    if avg_ndvi < 0.2:

        st.error("🔴 CRITICAL ALERT")
        st.write("""
        - Crop is under severe stress  
        - Immediate irrigation required  
        - Check soil moisture  
        - Consider fertilizer application  
        """)

    elif avg_ndvi < 0.4:

        st.warning("🟡 MODERATE STRESS")

        st.write("""
        - Irrigation recommended within 3–5 days  
        - Monitor crop growth closely  
        - Avoid fertilizer overload  
        """)

    elif avg_ndvi < 0.6:

        st.info("🟢 GOOD CONDITION")

        st.write("""
        - Crop health is stable  
        - Normal irrigation schedule  
        - Continue monitoring NDVI trends  
        """)

    else:

        st.success("🌿 EXCELLENT CONDITION")

        st.write("""
        - High vegetation density  
        - No immediate action required  
        - Maintain current farming practices  
        """)

    # -----------------------------
    # BONUS INSIGHT
    # -----------------------------
    st.subheader("📊 AI Summary")

    st.write(f"""
    Based on satellite NDVI analysis for **{crop}**, the selected area shows 
    vegetation condition categorized by remote sensing intelligence.

    This recommendation is generated using NDVI thresholds commonly used in 
    precision agriculture systems.
    """)
