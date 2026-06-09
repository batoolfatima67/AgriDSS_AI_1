import streamlit as st


def run_full_analysis():

    st.header("🌾 AgriDSS_AI Analysis Engine")

    data = st.session_state.get("user_data")

    if not data:
        st.warning("Please complete Farm Input first")
        return

    st.success("✅ System Ready")
