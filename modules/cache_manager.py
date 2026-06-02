import streamlit as st


def init_cache():

    if "cache" not in st.session_state:
        st.session_state.cache = {
            "weather": None,
            "ndvi": None,
            "last_input_hash": None,
            "recommendation": None
        }


def update_cache(key, value):
    st.session_state.cache[key] = value


def get_cache(key):
    return st.session_state.cache.get(key)


def clear_cache():
    st.session_state.cache = {
        "weather": None,
        "ndvi": None,
        "last_input_hash": None,
        "recommendation": None
    }
