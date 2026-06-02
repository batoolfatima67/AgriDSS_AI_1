import streamlit as st
import geopandas as gpd
from pathlib import Path

@st.cache_data
def load_data():

    shp_path = Path("data/pakistan_tehsil.shp")

    gdf = gpd.read_file(shp_path)

    # IMPORTANT: preserve geometry first
    geom_col = gdf.geometry.name

    # normalize columns
    gdf.columns = [col.upper() for col in gdf.columns]

    # restore geometry explicitly
    gdf = gdf.set_geometry(geom_col)

    return gdf

def render_input_module():

    st.header("📍 Farm Location Input (GIS)")

    gdf = load_data()

    # -----------------------------
    # AUTO-DETECT COLUMNS
    # -----------------------------
    district_col = [c for c in gdf.columns if "DIST" in c][0]
    tehsil_col = [c for c in gdf.columns if "TEH" in c or "TAHS" in c or "NAME" in c][0]

    # -----------------------------
    # DISTRICT SELECTION
    # -----------------------------
    districts = sorted(
        gdf[district_col].dropna().unique().tolist()
    )

    district = st.selectbox(
        "Select District",
        districts
    )

    district_df = gdf[gdf[district_col] == district]

    # -----------------------------
    # TEHSIL SELECTION
    # -----------------------------
    tehsils = sorted(
        district_df[tehsil_col].dropna().unique().tolist()
    )

    tehsil = st.selectbox(
        "Select Tehsil",
        tehsils
    )

    selected = district_df[
        district_df[tehsil_col] == tehsil
    ]

    # 🔥 ADD DEBUG HERE (TEMPORARY)
    st.write("Geometry type:", type(selected))
    st.write("Columns:", selected.columns)
    st.write("Has geometry:", selected.geometry.name if hasattr(selected, "geometry") else "NO")
    
    if selected.empty:
        st.error("No spatial data found for selected tehsil")
        return

    # -----------------------------
    # GEOMETRY CENTROID (AUTO LOCATION)
    # -----------------------------
    geometry = selected.iloc[0].geometry

    selected_row = selected.iloc[0]

    geometry = selected_row.geometry

    centroid = geometry.centroid

    lat = centroid.y
    lon = centroid.x

    st.subheader("📌 Auto-Detected Farm Location")

    st.write(f"Latitude: {lat:.6f}")
    st.write(f"Longitude: {lon:.6f}")

    # -----------------------------
    # FARM PARAMETERS
    # -----------------------------
    crop = st.selectbox(
        "Crop",
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

        st.success("Farm data saved successfully 🚀")
