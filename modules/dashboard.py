import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium


def render_dashboard():

    st.header("🗺 Farm Map Dashboard")

    user_data = st.session_state.get("user_data")

    if not user_data:
        st.warning("Please complete Farm Input first.")
        return

    district = user_data["district"]
    tehsil = user_data["tehsil"]

    gdf = gpd.read_file("data/pakistan_tehsil.shp")

    # -------------------------------
    # AUTO-DETECT COLUMNS (NO ERROR)
    # -------------------------------
    possible_district_cols = ["District", "DISTRICT", "district"]
    possible_tehsil_cols = ["Tehsil", "TEHSIL", "tehsil"]

    district_col = next((col for col in possible_district_cols if col in gdf.columns), None)
    tehsil_col = next((col for col in possible_tehsil_cols if col in gdf.columns), None)

    if district_col is None or tehsil_col is None:
        st.error("District/Tehsil columns not found in shapefile")
        st.write(gdf.columns.tolist())
        return

    # -------------------------------
    # FILTER DATA
    # -------------------------------
    selected = gdf[
        (gdf[district_col] == district) &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Selected location not found in shapefile")
        return

    # -------------------------------
    # MAP CENTER
    # -------------------------------
    center = selected.geometry.centroid.iloc[0]

    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    folium.GeoJson(
        selected,
        style_function=lambda x: {
            "fillColor": "green",
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.3
        }
    ).add_to(m)

    st_folium(m, width=1200, height=600)
