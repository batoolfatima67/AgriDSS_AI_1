import streamlit as st
from datetime import datetime


def generate_report():

    st.header("📄 AgriDSS_AI Report")

    data = st.session_state.get("user_data")
    weather = st.session_state.get("weather_data")
    ndvi = st.session_state.get("ndvi_value")

    if not data:
        st.warning("No data available. Please complete Farm Input and Run Analysis first.")
        return

    # Safe defaults
    if weather:
        temperature = weather.get("temperature", "N/A")
        humidity = weather.get("humidity", "N/A")
        condition = weather.get("condition", "N/A")
    else:
        temperature = humidity = condition = "N/A"

    if ndvi is None:
        ndvi = "N/A"
        ndvi_status = "N/A"
    else:
        if ndvi > 0.6:
            ndvi_status = "Healthy Vegetation"
        elif ndvi > 0.3:
            ndvi_status = "Moderate Vegetation"
        else:
            ndvi_status = "Low Vegetation"

    report = f"""
==================================================
                AGRIDSS_AI REPORT
==================================================

Report Date:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

--------------------------------------------------
FARM INFORMATION
--------------------------------------------------

District : {data.get('district', 'N/A')}
Tehsil   : {data.get('tehsil', 'N/A')}
Crop     : {data.get('crop', 'N/A')}
Area     : {data.get('area', 'N/A')}

--------------------------------------------------
WEATHER ANALYSIS
--------------------------------------------------

Temperature : {temperature} °C
Humidity    : {humidity} %
Condition   : {condition}

--------------------------------------------------
NDVI ANALYSIS
--------------------------------------------------

NDVI Value  : {ndvi}
Status      : {ndvi_status}

--------------------------------------------------
SUMMARY
--------------------------------------------------

This report was generated automatically by
AgriDSS_AI Decision Support System.

==================================================
END OF REPORT
==================================================
"""

    st.text_area(
        "Generated Report",
        report,
        height=450
    )

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="AgriDSS_AI_Report.txt",
        mime="text/plain"
    )
