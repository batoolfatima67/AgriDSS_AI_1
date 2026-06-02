import streamlit as st


def render_analysis_engine():

    st.header("🚀 Run Complete Analysis")

    user_data = st.session_state.get(
        "user_data",
        None
    )

    if not user_data:
        st.warning(
            "Please complete Input Module first."
        )
        return

    st.subheader("Selected Farm")

    st.write(
        f"Province: {user_data['province']}"
    )

    st.write(
        f"District: {user_data['district']}"
    )

    st.write(
        f"Tehsil: {user_data['tehsil']}"
    )

    st.write(
        f"Crop: {user_data['crop']}"
    )

    if st.button("Run Analysis"):

        with st.spinner(
            "Running AgriDSS_AI analysis..."
        ):

            weather_available = (
                "weather_data"
                in st.session_state
            )

            ndvi_available = (
                "ndvi_value"
                in st.session_state
            )

            recommendation_available = (
                "recommendation"
                in st.session_state
            )

        st.success(
            "Analysis Complete"
        )

        st.subheader(
            "Analysis Summary"
        )

        st.write(
            f"Location: "
            f"{user_data['district']} "
            f"({user_data['latitude']:.4f}, "
            f"{user_data['longitude']:.4f})"
        )

        if weather_available:

            weather = st.session_state.weather_data

            st.info(
                f"Temperature: "
                f"{weather['temp']} °C"
            )

            st.info(
                f"Humidity: "
                f"{weather['humidity']} %"
            )

        else:

            st.warning(
                "Weather analysis not available."
            )

        if ndvi_available:

            ndvi = st.session_state.ndvi_value

            st.success(
                f"NDVI: {ndvi:.3f}"
            )

        else:

            st.warning(
                "NDVI analysis not available."
            )

        if recommendation_available:

            rec = st.session_state.recommendation

            st.success(
                rec["status"]
            )

            st.write(
                rec["irrigation"]
            )

            st.write(
                rec["fertilizer"]
            )

        else:

            st.warning(
                "Recommendation engine not available."
            )
