import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import numpy as np
import matplotlib.pyplot as plt


def render_dashboard():

    st.header("🗺 Farm Map Dashboard")

    user_data = st.session_state.get("user_data")

    if not user_data:
        st.warning("Please complete Farm Input first.")
        return

    district = user_data["district"]
    tehsil = user_data["tehsil"]

    gdf = gpd.read_file("data/pakistan_tehsil.shp")

    district_col = "DISTRICT"
    tehsil_col = "TEHSIL"

    selected = gdf[
        (gdf[district_col] == district) &
        (gdf[tehsil_col] == tehsil)
    ]

    if selected.empty:
        st.error("Location not found")
        return

    geom = selected.geometry.iloc[0]
    minx, miny, maxx, maxy = geom.bounds

    # ---------------- MAP ----------------
    center = geom.centroid

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

    st.subheader("🗺 Map View")
    st_folium(m, width=1200, height=500)

    st.success("NDVI section reached ✔")

    # ---------------- NDVI LAYER ----------------
    st.subheader("🌱 NDVI Layer (Demo)")

    import pandas as pd
    import numpy as np

    st.subheader("🌱 NDVI Layer (Demo)")

    ndvi_values = np.random.uniform(0.2, 0.9, 100)

    df = pd.DataFrame({
        "pixel": range(100),
        "ndvi": ndvi_values
    })

    st.line_chart(df.set_index("pixel"))

    plt.colorbar(img, ax=ax)

    ax.set_title("NDVI Distribution (Simulated)")

    st.pyplot(fig)
