import streamlit as st
import geopandas as gpd
import folium

from streamlit_folium import st_folium

from modules.gee_ndvi import (
    get_ndvi_from_gee,
    get_ndvi_tile_layer,
    get_ndvi_stats
)


def render_dashboard():

    st.header(
        "🗺 AgriDSS_AI Smart Geo Dashboard"
    )

    user_data = st.session_state.get(
        "user_data"
    )

    if not user_data:
        st.warning(
            "Please complete Farm Input first."
        )
        return

    district = user_data.get(
        "district"
    )

    tehsil = user_data.get(
        "tehsil"
    )

    st.subheader(
        "📍 Selected Location"
    )

    st.write(
        f"District: {district}"
    )

    st.write(
        f"Tehsil: {tehsil}"
    )

    # -----------------------------
    # LOAD SHAPEFILE
    # -----------------------------
    try:

        gdf = gpd.read_file(
            "data/pakistan_tehsil.shp"
        )

    except Exception as e:

        st.error(
            f"Error loading shapefile: {e}"
        )

        return

    # -----------------------------
    # FIND DISTRICT/TEHSIL COLUMNS
    # -----------------------------
    district_col = None
    tehsil_col = None

    for col in gdf.columns:

        if col.lower() == "district":
            district_col = col

        if col.lower() == "tehsil":
            tehsil_col = col

    if district_col is None:

        district_col = gdf.columns[0]

    if tehsil_col is None:

        tehsil_col = gdf.columns[1]

    # -----------------------------
    # FILTER SELECTED AREA
    # -----------------------------
    selected = gdf[
        (gdf[district_col] == district)
        &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:

        st.error(
            "Selected area not found."
        )

        return

    geom = selected.geometry.iloc[0]

    center = geom.centroid

    # -----------------------------
    # CREATE MAP
    # -----------------------------
    m = folium.Map(
        location=[
            center.y,
            center.x
        ],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    # -----------------------------
    # REAL GEE NDVI
    # -----------------------------
    try:

        with st.spinner(
            "Loading NDVI from Sentinel-2..."
        ):

            ndvi_image, ee_geometry = (
                get_ndvi_from_gee(
                    geom
                )
            )

            tile_url = (
                get_ndvi_tile_layer(
                    ndvi_image
                )
            )

            folium.TileLayer(
                tiles=tile_url,
                attr="Google Earth Engine",
                name="NDVI",
                overlay=True,
                control=True
            ).add_to(m)

            stats = get_ndvi_stats(
                ndvi_image,
                ee_geometry
            )

            ndvi_mean = stats.get(
                "NDVI",
                None
            )

    except Exception as e:

        st.error(
            f"GEE Error: {e}"
        )

        ndvi_mean = None

    # -----------------------------
    # TEHSIL BOUNDARY
    # -----------------------------
    folium.GeoJson(
        selected,
        style_function=lambda x: {
            "fillOpacity": 0.05,
            "color": "black",
            "weight": 2
        }
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # -----------------------------
    # DISPLAY MAP
    # -----------------------------
    st.subheader(
        "🌱 Real Sentinel-2 NDVI"
    )

    st_folium(
        m,
        width=1200,
        height=600
    )

    # -----------------------------
    # NDVI STATISTICS
    # -----------------------------
    st.subheader(
        "📊 NDVI Statistics"
    )

    if ndvi_mean is not None:

        st.metric(
            "Mean NDVI",
            round(
                ndvi_mean,
                3
            )
        )

    else:

        st.warning(
            "NDVI statistics unavailable."
        )

    # -----------------------------
    # LEGEND
    # -----------------------------
    st.subheader(
        "🧭 NDVI Legend"
    )

    st.markdown(
        """
🟥 Red → Bare Soil / Low Vegetation

🟨 Yellow → Moderate Vegetation

🟩 Green → Healthy Vegetation
"""
    )
