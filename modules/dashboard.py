import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium


def render_dashboard():

    st.header("🗺 Farm Location Map")

    user_data = st.session_state.get("user_data")

    if not user_data:
        st.warning("Please select a farm location first.")
        return

    district = user_data["district"]
    tehsil = user_data["tehsil"]

    # Load shapefile
    gdf = gpd.read_file("data/pakistan_tehsil.shp")

    st.write(gdf.columns.tolist())
    st.stop()

    # --------------------------------------------------
    # IMPORTANT
    # Replace these with the SAME variables used
    # in input_module.py
    # --------------------------------------------------

    district_col = "District"
    tehsil_col = "Tehsil"

    selected = gdf[
        (gdf[district_col] == district)
        &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Selected tehsil not found.")
        return

    # Get centroid
    center = selected.geometry.centroid.iloc[0]

    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    folium.GeoJson(
        selected,
        name="Selected Tehsil",
        style_function=lambda x: {
            "fillColor": "#00ff00",
            "color": "#006400",
            "weight": 3,
            "fillOpacity": 0.25
        }
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st_folium(
        m,
        width=1200,
        height=600
    )
