import streamlit as st
from datetime import datetime


def generate_report():

    st.header("🧾 Farm Report Generator")

    user_data = st.session_state.get("user_data", None)
    weather = st.session_state.get("weather_data", None)
    ndvi = st.session_state.get("ndvi_value", None)

    if not user_data:
        st.warning("No data available for report")
        return

    report = f"""
    AGRIDSS_AI FARM REPORT
    ----------------------
    Date: {datetime.now()}

    CROP: {user_data['crop']}
    LOCATION: {user_data['latitude']}, {user_data['longitude']}
    AREA: {user_data['area']} acres

    WEATHER:
    Temperature: {weather['temp'] if weather else 'N/A'}
    Humidity: {weather['humidity'] if weather else 'N/A'}
    Wind: {weather['wind'] if weather else 'N/A'}

    NDVI: {ndvi if ndvi else 'N/A'}
    """

    st.text_area("Report Preview", report, height=300)

    st.download_button(
        label="Download Report",
        data=report,
        file_name="AgriDSS_AI_Report.txt",
        mime="text/plain"
    )
