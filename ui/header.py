"""
=========================================================
BioDesignAI
Application Header

Author : Batool Fatima
Version : 1.0
=========================================================
"""

import streamlit as st


def render_header():
    """
    Render the application header.
    """

    st.markdown(
        """
        <div class="main-title">
            🌱 BioDesignAI
        </div>

        <div class="sub-title">
            AI-Powered Biogas Plant Design & Decision Support System
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
