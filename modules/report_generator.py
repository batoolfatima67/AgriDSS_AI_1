import streamlit as st


def generate_report():

    st.title("📄 Farm Report")

    weather = st.session_state.get("weather_data")
    ndvi = st.session_state.get("ndvi_value")
    data = st.session_state.get("user_data")

    if not weather or ndvi is None or not data:
        st.warning("No report available. Run analysis first.")
        return

    # ---------------- SINGLE REPORT CONTAINER ----------------
    with st.container():

        st.markdown("### 🌾 Farm Information")
        st.markdown(f"""
        - **District:** {data['district']}
        - **Tehsil:** {data['tehsil']}
        - **Crop:** {data['crop']}
        """)

        st.markdown("---")

        st.markdown("### 🌦 Weather Summary")
        st.markdown(f"""
        - Temperature: **{weather['temperature']} °C**
        - Humidity: **{weather['humidity']} %**
        - Condition: **{weather['condition']}**
        """)

        st.markdown("---")

        st.markdown("### 🌱 Vegetation Health (NDVI)")
        st.markdown(f"**NDVI Value:** {ndvi}")

        if ndvi > 0.6:
            st.success("Crop Condition: Healthy 🟢")
            status = "Good"
        elif ndvi > 0.3:
            st.warning("Crop Condition: Moderate 🟡")
            status = "Moderate"
        else:
            st.error("Crop Condition: Poor 🔴")
            status = "Poor"

        st.markdown("---")

        st.markdown("### 🧠 Recommendation")

        if status == "Good":
            st.info("No major action required. Maintain normal irrigation.")
        elif status == "Moderate":
            st.info("Slight increase in irrigation recommended.")
        else:
            st.info("Urgent attention required: crop stress detected.")

        st.markdown("---")
