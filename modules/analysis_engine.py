import streamlit as st


def run_full_analysis():

    st.header("AgriDSS AI Analysis")

    data = st.session_state.get("user_data")

    if not data:
        st.warning("No farm data found")
        return

    st.write("System Ready")
