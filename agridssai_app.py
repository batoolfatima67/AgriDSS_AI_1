import streamlit as st
import folium

from branca.colormap import LinearColormap

from modules.input_module import get_user_input
from modules.weather_module import get_weather
from modules.gis_module import load_shapefile
from modules.geometry_module import get_geometry
from modules.ndvi_interpretation import interpret_ndvi
from modules.recommendation_engine import generate_recommendation
from streamlit_folium import st_folium

from modules.ndvi_timeseries import (
    get_ndvi_timeseries
)

from modules.gee_ndvi import (
    get_ndvi_from_gee,
    get_ndvi_stats,
    get_ndvi_tile_layer
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Agri DSS",
    layout="wide"
)

st.title(
    "🌾 AI-Powered Precision Agriculture Decision Support System (AgriDSS_AI)"
)

st.divider()

# ---------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------
if "analysis_done" not in st.session_state:

    st.session_state.analysis_done = False

# ---------------------------------------------------
# LOAD GIS
# ---------------------------------------------------
@st.cache_data
def get_gis(layer):

    return load_shapefile(layer)

# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------
crop = get_user_input()

district_gdf = get_gis("district")

tehsil_gdf = get_gis("tehsil")

# ---------------------------------------------------
# ADMIN COLUMN
# ---------------------------------------------------
admin_column = None

for col in [
    "DIVISION",
    "division",
    "ADMIN",
    "admin",
    "PROVINCE",
    "province"
]:

    if col in district_gdf.columns:

        admin_column = col
        break

if not admin_column:

    st.error(
        "No administration column found."
    )

    st.stop()

administration = st.selectbox(
    "Select Administration",
    sorted(
        district_gdf[admin_column]
        .dropna()
        .unique()
    )
)

# ---------------------------------------------------
# DISTRICT FILTER
# ---------------------------------------------------
filtered_districts = district_gdf[
    district_gdf[admin_column]
    == administration
]

district_column = None

for col in [
    "DISTRICT",
    "district",
    "NAME",
    "name"
]:

    if col in filtered_districts.columns:

        district_column = col
        break

if not district_column:

    st.error(
        "No district column found."
    )

    st.stop()

selected_district = st.selectbox(
    "Select District",
    sorted(
        filtered_districts[district_column]
        .dropna()
        .unique()
    )
)

# ---------------------------------------------------
# TEHSIL FILTER
# ---------------------------------------------------
tehsil_district_column = None

for col in [
    "DISTRICT",
    "district"
]:

    if col in tehsil_gdf.columns:

        tehsil_district_column = col
        break

filtered_tehsils = tehsil_gdf[
    tehsil_gdf[tehsil_district_column]
    == selected_district
]

tehsil_column = None

for col in [
    "TEHSIL",
    "tehsil",
    "NAME",
    "name"
]:

    if col in filtered_tehsils.columns:

        tehsil_column = col
        break

if not tehsil_column:

    st.error(
        "No tehsil column found."
    )

    st.stop()

selected_tehsil = st.selectbox(
    "Select Tehsil",
    sorted(
        filtered_tehsils[tehsil_column]
        .dropna()
        .unique()
    )
)

# ---------------------------------------------------
# GEOMETRY
# ---------------------------------------------------
filtered_gdf, geometry = get_geometry(
    filtered_tehsils,
    tehsil_column,
    selected_tehsil
)

centroid = geometry.centroid

lat = centroid.y
lon = centroid.x

st.write("## 📍 Location")

st.write(
    "Latitude:",
    round(lat, 6)
)

st.write(
    "Longitude:",
    round(lon, 6)
)

# ---------------------------------------------------
# AUTO RESET WHEN LOCATION CHANGES
# ---------------------------------------------------
current_key = (
    f"{administration}_"
    f"{selected_district}_"
    f"{selected_tehsil}_"
    f"{crop}"
)

if "last_key" not in st.session_state:

    st.session_state.last_key = current_key

if st.session_state.last_key != current_key:

    st.session_state.analysis_done = False

    st.session_state.last_key = current_key

st.divider()

# ---------------------------------------------------
# RUN ANALYSIS
# ---------------------------------------------------
if st.button(
    "Run AI Analysis"
):

    st.session_state.analysis_done = True

    with st.spinner(
        "Running AI-based farm analysis..."
    ):

        # WEATHER
        weather = get_weather(
            lat,
            lon
        )

        # NDVI
        ndvi_image, ee_geometry = (
            get_ndvi_from_gee(
                geometry
            )
        )
        
        st.session_state.weather = weather

        # NDVI STATS
        stats = get_ndvi_stats(
            ndvi_image,
            ee_geometry
        )

        st.session_state.stats = stats
        st.session_state.ndvi_value = stats.get("NDVI")

        # NDVI TIME SERIES
        ndvi_timeseries_df = (
            get_ndvi_timeseries(
                geometry
            )
        )

        # NDVI TILE
        ndvi_tile = get_ndvi_tile_layer(
            ndvi_image
        )

        # SAVE SESSION
        st.session_state.weather = weather

        st.session_state.stats = stats

        st.session_state.ndvi_tile = ndvi_tile

        st.session_state.ndvi_timeseries_df = (
            ndvi_timeseries_df
        )

# ---------------------------------------------------
# DISPLAY RESULTS SAFELY
# ---------------------------------------------------
if (
    st.session_state.analysis_done
    and "ndvi_tile" in st.session_state
):

    weather = st.session_state.weather

    stats = st.session_state.stats

    ndvi_tile = st.session_state.ndvi_tile

    ndvi_timeseries_df = (
        st.session_state.ndvi_timeseries_df
    )

    st.success(
        "✅ Analysis Completed Successfully"
    )

    st.divider()

    # ---------------------------------------------------
    # NDVI MAP
    # ---------------------------------------------------
    st.write("## 🛰 NDVI Visualization")

    m = folium.Map(
        location=[lat, lon],
        zoom_start=10,
        control_scale=True,
        tiles=None
    )

    # BASEMAP
    folium.TileLayer(
        "OpenStreetMap"
    ).add_to(m)

    # ---------------------------------------------------
    # NDVI COLOR LEGEND
    # ---------------------------------------------------
    ndvi_colormap = LinearColormap(
        colors=[
            "red",
            "orange",
            "yellow",
            "green",
            "darkgreen"
        ],
        vmin=0,
        vmax=1,
        caption="NDVI Vegetation Index"
    )

    # NDVI TILE
    folium.TileLayer(
        tiles=ndvi_tile,
        attr="Google Earth Engine",
        name="NDVI Layer",
        overlay=True,
        control=True,
        opacity=0.75
    ).add_to(m)

    # ADD COLORBAR
    ndvi_colormap.add_to(m)

    # FIELD BOUNDARY
    folium.GeoJson(
        geometry.__geo_interface__,
        name="Field Boundary"
    ).add_to(m)

    # CENTER MARKER
    folium.Marker(
        [lat, lon],
        popup="Farm Location",
        icon=folium.Icon(
            color="green"
        )
    ).add_to(m)

    # LAYER CONTROL
    folium.LayerControl().add_to(m)

    # MAP GUIDE
    st.info(
        """
        🛰 NDVI Layer Guide:

        🔴 Red = Very Poor Vegetation
        🟠 Orange = Weak Vegetation
        🟡 Yellow = Moderate Vegetation
        🟢 Green = Healthy Vegetation
        🌳 Dark Green = Dense Healthy Crop
        """
    )

    # DISPLAY MAP
    st_folium(
        m,
        width=900,
        height=550
    )

    st.divider()

    # ---------------------------------------------------
    # WEATHER
    # ---------------------------------------------------
    st.write("## 🌦 Weather Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Temperature",
            f"{weather['temperature']['value']} °C"
        )

    with col2:

        st.metric(
            "Humidity",
            f"{weather['humidity']['value']} %"
        )

    with col3:

        st.metric(
            "Wind Speed",
            f"{weather['wind_speed']['value']} km/h"
        )

    st.info(
        f"Condition: {weather['condition']}"
    )

    st.divider()

    # ---------------------------------------------------
    # NDVI
    # ---------------------------------------------------
    ndvi_value = stats.get("NDVI")

    # ---------------------------------------------------
    # AI CROP HEALTH SCORING ENGINE
    # ---------------------------------------------------
    if ndvi_value is not None:

        if ndvi_value >= 0.75:

            crop_health_score = 95

            health_status = (
                "Excellent Crop Health"
            )

        elif ndvi_value >= 0.60:

            crop_health_score = 80

            health_status = (
                "Healthy Vegetation"
            )

        elif ndvi_value >= 0.45:

            crop_health_score = 65

            health_status = (
                "Moderate Vegetation"
            )

        elif ndvi_value >= 0.30:

            crop_health_score = 45

            health_status = (
                "Weak Vegetation"
            )

        else:

            crop_health_score = 20

            health_status = (
                "Critical Crop Stress"
            )

    else:

        crop_health_score = 0

        health_status = "No NDVI Data"

    st.write("## 🛰 NDVI Statistics")

    st.metric(
        "Mean NDVI",
        round(ndvi_value, 3)
        if ndvi_value
        else "No Data"
    )

    # NDVI INTERPRETATION
    interpretation = interpret_ndvi(
        ndvi_value
    )

    st.success(
        f"Vegetation Status: {interpretation}"
    )

    st.divider()

    # ---------------------------------------------------
    # AI NDVI INTELLIGENCE
    # ---------------------------------------------------
    st.write(
        "## 🧠 AI Crop Health Intelligence"
    )

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        st.metric(
            label="Crop Health Score",
            value=f"{crop_health_score}/100"
        )

    with score_col2:

        st.metric(
            label="Health Condition",
            value=health_status
        )

    # PROGRESS BAR
    st.progress(
        min(
            crop_health_score / 100,
            1.0
        )
    )

    # AI INSIGHT
    if ndvi_value is not None:

        if ndvi_value >= 0.70:

            st.success(
                "AI Insight: Crop canopy is dense and healthy. Vegetation vigor is excellent."
            )

        elif ndvi_value >= 0.50:

            st.info(
                "AI Insight: Vegetation is stable, but some areas may require monitoring."
            )

        elif ndvi_value >= 0.30:

            st.warning(
                "AI Insight: Crop stress detected. Irrigation and nutrient management recommended."
            )

        else:

            st.error(
                "AI Insight: Severe vegetation stress detected. Immediate field inspection recommended."
            )

    st.divider()

    # ---------------------------------------------------
    # NDVI TIME-SERIES ANALYTICS
    # ---------------------------------------------------
    st.write(
        "## 📈 NDVI Time-Series Analytics"
    )

    if not ndvi_timeseries_df.empty:

        st.line_chart(

            ndvi_timeseries_df.set_index(
                "Date"
            )
        )

        latest_ndvi = (
            ndvi_timeseries_df["NDVI"]
            .iloc[-1]
        )

        oldest_ndvi = (
            ndvi_timeseries_df["NDVI"]
            .iloc[0]
        )

        ndvi_change = round(
            latest_ndvi - oldest_ndvi,
            3
        )

        if ndvi_change > 0.05:

            st.success(
                f"NDVI Trend: Improving (+{ndvi_change})"
            )

        elif ndvi_change < -0.05:

            st.error(
                f"NDVI Trend: Declining ({ndvi_change})"
            )

        else:

            st.info(
                f"NDVI Trend: Stable ({ndvi_change})"
            )

    else:

        st.warning(
            "No NDVI time-series data available."
        )

    st.divider()

    # ---------------------------------------------------
    # AI RECOMMENDATIONS
    # ---------------------------------------------------
    if ndvi_value is not None:

    recommendations = generate_recommendation(
        ndvi_value,
        weather,
        crop
    )

    else:

    recommendations = ["No NDVI available for recommendation."]

    st.write("## 🤖 AI Recommendations")

    for r in recommendations:

        st.warning(r)

    st.divider()
