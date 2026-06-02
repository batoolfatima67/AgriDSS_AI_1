import streamlit as st
import geopandas as gpd
from pathlib import Path


@st.cache_data
def load_tehsil_data():

    shp_path = Path("data/Punjab_Tehsils.shp")

    gdf = gpd.read_file(shp_path)

    return gdf


def render_input_module():

    st.header("📍 Farm Location Input")

    try:
        gdf = load_tehsil_data()

    except Exception as e:
        st.error(f"Unable to load tehsil shapefile: {e}")
        return

    # -----------------------------
    # Province Selection
    # -----------------------------
    provinces = sorted(
        gdf["Province"].dropna().unique().tolist()
    )

    province = st.selectbox(
        "Select Province",
        provinces
    )

    # -----------------------------
    # District Selection
    # -----------------------------
    district_df = gdf[
        gdf["Province"] == province
    ]

    districts = sorted(
        district_df["District"].dropna().unique().tolist()
    )

    district = st.selectbox(
        "Select District",
        districts
    )

    # -----------------------------
    # Tehsil Selection
    # -----------------------------
    tehsil_df = district_df[
        district_df["District"] == district
    ]

    tehsils = sorted(
        tehsil_df["Tehsil"].dropna().unique().tolist()
    )

    tehsil = st.selectbox(
        "Select Tehsil",
        tehsils
    )

    # -----------------------------
    # Selected Tehsil Geometry
    # -----------------------------
    selected = tehsil_df[
        tehsil_df["Tehsil"] == tehsil
    ]

    if selected.empty:
        st.warning("No geometry found.")
        return

    geometry = selected.geometry.iloc[0]

    centroid = geometry.centroid

    lat = centroid.y
    lon = centroid.x

    st.subheader("📌 Location")

    st.write(f"Latitude: {lat:.6f}")
    st.write(f"Longitude: {lon:.6f}")

    # -----------------------------
    # Crop Information
    # -----------------------------
    crop = st.selectbox(
        "Crop",
        [
            "Wheat",
            "Rice",
            "Maize",
            "Cotton",
            "Sugarcane"
        ]
    )

    area = st.number_input(
        "Farm Area (Acres)",
        min_value=0.1,
        value=5.0
    )

    irrigation = st.selectbox(
        "Irrigation Method",
        [
            "Flood",
            "Drip",
            "Sprinkler",
            "Canal",
            "Rainfed"
        ]
    )

    # -----------------------------
    # Save
    # -----------------------------
    if st.button("Save Farm Information"):

        st.session_state.user_data = {

            "province": province,
            "district": district,
            "tehsil": tehsil,

            "latitude": lat,
            "longitude": lon,

            "crop": crop,
            "area": area,
            "irrigation": irrigation
        }

        st.success("Farm information saved.")
