import streamlit as st
from datetime import datetime


def generate_report():

    st.header("📄 Farm Report")

    user_data = st.session_state.get("user_data")
    weather = st.session_state.get("weather_data")
    ndvi = st.session_state.get("ndvi_value")
    rec = st.session_state.get("recommendation")

    if not user_data:
        st.warning("No data available")
        return

    report = f"""
AGRIDSS_AI REPORT
------------------
Date: {datetime.now()}

LOCATION:
{user_data['district']} - {user_data['tehsil']}

CROP: {user_data['crop']}
AREA: {user_data['area']} acres

WEATHER:
{weather}

NDVI:
{ndvi}

RECOMMENDATION:
{rec}
"""

    st.text_area("Report", report, height=300)

    st.download_button(
        "Download Report",
        report,
        file_name="AgriDSS_Report.txt"
    )
