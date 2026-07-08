"""
=========================================================
Application Footer
=========================================================
"""

import streamlit as st


def render_footer():

    st.divider()

    st.markdown(
        """
<div class="footer">

BioDesignAI Version 1.0

Developed by Batool Fatima

© 2026

</div>
""",
        unsafe_allow_html=True,
    )
