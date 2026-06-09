import streamlit as st


def run_full_analysis():

    st.header("🌾 AgriDSS AI Demo")

    data = st.session_state.get("user_data")

    if not data:
        st.warning("Select farm location first")
        return

    st.success("System Ready 🚀")
