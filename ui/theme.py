"""
=========================================================
Theme Manager
BioDesignAI
=========================================================
"""

import streamlit as st


def initialize_theme():
    """
    Initialize application theme.
    """

    if "theme" not in st.session_state:
        st.session_state.theme = "Light"


def get_theme():

    return st.session_state.theme


def is_dark():

    return st.session_state.theme == "Dark"


def toggle_theme():

    if st.session_state.theme == "Light":
        st.session_state.theme = "Dark"
    else:
        st.session_state.theme = "Light"


def get_theme_colors():

    if is_dark():

        return {

            "background": "#0E1117",

            "card": "#262730",

            "primary": "#43A047",

            "secondary": "#66BB6A",

            "text": "#FAFAFA",

            "muted": "#B0BEC5",

            "border": "#3C4043"

        }

    return {

        "background": "#F7F9FB",

        "card": "#FFFFFF",

        "primary": "#2E7D32",

        "secondary": "#43A047",

        "text": "#263238",

        "muted": "#607D8B",

        "border": "#DADCE0"

    }
