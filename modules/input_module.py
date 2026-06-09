import streamlit as st
import geopandas as gpd
from pathlib import Path


@st.cache_data
def load_data():
    shp_path = Path("data/pakistan_tehsil.shp")
    gdf = gpd.read_file(shp_path)

    gdf.columns = gdf.columns.str.upper()
    return gdf


def render_input_module():

    st.header("📍 Farm Input (GIS)")

    gdf = load_data()

    district_col = [c for c in gdf.columns if "DIST" in c][0]
    tehsil_col = [c for c in gdf.columns if "TEH" in c or "TAHS" in c or "NAME" in c][0]

    districts = sorted(gdf[district_col].dropna().unique().tolist())
    district = st.selectbox("Select District", districts)

    district_df = gdf[gdf[district_col] == district]

    tehsils = sorted(district_df[tehsil_col].dropna().unique().tolist())
    tehsil = st.selectbox("Select Tehsil", tehsils)

    selected = district_df[district_df[tehsil_col] == tehsil]

    if selected.empty:
        st.error("No data found")
        return

    row = selected.iloc[0]
    geometry = row.geometry

    centroid = geometry.centroid

    lat = centroid.y
    lon = centroid.x

    st.subheader("📌 Location")
    st.write(lat, lon)

    crop = st.selectbox("Crop", ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"])
    area = st.number_input("Area (Acres)", 0.1, 100.0, 5.0)

    irrigation = st.selectbox(
        "Irrigation",
        ["Flood", "Drip", "Sprinkler", "Canal", "Rainfed"]
    )

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

        st.success("Saved")
