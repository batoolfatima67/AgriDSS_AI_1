import streamlit as st
import geopandas as gpd
from pathlib import Path


# -----------------------------
# LOAD SHAPEFILE (SAFE)
# -----------------------------
@st.cache_data
def load_data():

    shp_path = Path("data/pakistan_tehsil.shp")
    gdf = gpd.read_file(shp_path)

    # Keep geometry column safe
    geom_col = gdf.geometry.name

    # Normalize column names (except geometry)
    new_cols = []
    for col in gdf.columns:
        if col == geom_col:
            new_cols.append(col)
        else:
            new_cols.append(col.upper())

    gdf.columns = new_cols

    return gdf


# -----------------------------
# MAIN INPUT MODULE
# -----------------------------
def render_input_module():

    st.header("📍 Farm Location Input (GIS System)")

    gdf = load_data()

    # -----------------------------
    # Detect columns safely
    # -----------------------------
    district_col = [c for c in gdf.columns if "DIST" in c][0]
    tehsil_col = [c for c in gdf.columns if "TEH" in c or "TAHS" in c or "NAME" in c][0]

    # -----------------------------
    # District selection
    # -----------------------------
    districts = sorted(gdf[district_col].dropna().unique().tolist())

    district = st.selectbox(
        "Select District",
        ["Select District"] + districts
    )

    # -----------------------------
    # Tehsil selection
    # -----------------------------
    district_df = gdf[gdf[district_col] == district] if district != "Select District" else gdf.iloc[0:0]

    if district != "Select District":
        tehsils = sorted(
            district_df[tehsil_col].dropna().unique().tolist()
        )
    else:
        tehsils = []

    tehsil = st.selectbox(
        "Select Tehsil",
        ["Select Tehsil"] + tehsils
    )

    # -----------------------------
    # STOP IF NOT SELECTED
    # -----------------------------
    if district == "Select District" or tehsil == "Select Tehsil":
        st.info("Please select District and Tehsil to continue")
        return

    # -----------------------------
    # FILTER SELECTED AREA
    # -----------------------------
    selected = district_df[district_df[tehsil_col] == tehsil]

    if selected.empty:
        st.error("No spatial data found for selected location")
        return

    # -----------------------------
    # GEOMETRY HANDLING
    # -----------------------------
    geom_col = selected.geometry.name
    geometry = selected.iloc[0][geom_col]

    centroid = geometry.centroid

    lat = float(centroid.y)
    lon = float(centroid.x)

    # -----------------------------
    # DISPLAY LOCATION
    # -----------------------------
    st.subheader("📌 Auto-Detected Farm Location")
    st.write("Latitude:", lat)
    st.write("Longitude:", lon)

    # -----------------------------
    # FARM PARAMETERS
    # -----------------------------
    crop = st.selectbox(
        "Crop Type",
        ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"]
    )

    area = st.number_input(
        "Farm Area (Acres)",
        min_value=0.1,
        value=5.0
    )

    irrigation = st.selectbox(
        "Irrigation Type",
        ["Flood", "Drip", "Sprinkler", "Canal", "Rainfed"]
    )

    # -----------------------------
    # SAVE STATE
    # -----------------------------
    if st.button("Save Farm Data"):

        st.session_state.user_data = {
            "district": district,
            "tehsil": tehsil,
            "latitude": lat,
            "longitude": lon,
            "crop": crop,
            "area": area,
            "irrigation": irrigation
        }

        st.success("Farm data saved successfully")
