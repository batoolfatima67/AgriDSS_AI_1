import ee
import streamlit as st

# -----------------------------
# INITIALIZE GEE (SAFE)
# -----------------------------
def initialize_gee():
    try:
        ee.Initialize()
    except Exception:
        ee.Authenticate()
        ee.Initialize()


# -----------------------------
# NDVI FUNCTION
# -----------------------------
def get_ndvi(lat, lon):

    initialize_gee()

    point = ee.Geometry.Point([lon, lat])

    image = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(point)
        .filterDate("2025-01-01", "2025-12-31")
        .sort("CLOUD_COVER")
        .first()
    )

    if image is None:
        return None

    ndvi = image.normalizedDifference(
        ["B8", "B4"]
    ).rename("NDVI")

    value = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=10,
        maxPixels=1e9
    ).get("NDVI")

    if value is None:
        return None

    return value.getInfo()


# -----------------------------
# STREAMLIT MODULE
# -----------------------------
def render_ndvi_module():

    st.header("🌱 NDVI Analysis (Remote Sensing)")

    user_data = st.session_state.get(
        "user_data",
        None
    )

    if not user_data:
        st.warning(
            "Please enter input data first."
        )
        return

    lat = user_data["latitude"]
    lon = user_data["longitude"]

    st.write(
        f"Location: {lat:.6f}, {lon:.6f}"
    )

    if st.button("Run NDVI Analysis"):

        with st.spinner(
            "Processing satellite data..."
        ):

            ndvi_value = get_ndvi(
                lat,
                lon
            )

            if ndvi_value is None:
                st.error(
                    "NDVI could not be calculated."
                )
                return

            # SAVE FOR OTHER MODULES
            st.session_state.ndvi_value = ndvi_value

            st.success(
                "NDVI Computed Successfully"
            )

            st.metric(
                "NDVI Value",
                round(ndvi_value, 3)
            )

            # Interpretation
            if ndvi_value < 0.2:

                st.error(
                    "Low vegetation health (Stress condition)"
                )

            elif ndvi_value < 0.5:

                st.warning(
                    "Moderate vegetation health"
                )

            else:

                st.success(
                    "Healthy vegetation"
                )
