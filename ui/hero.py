"""
=========================================================
BioDesignAI
Hero Section

Author : Batool Fatima
Version : 1.0
=========================================================
"""

import streamlit as st


def render_hero():
    """
    Display the hero banner on the Home page.
    """

    st.markdown(
        """
<div class="hero">

<h1>🌱 BioDesignAI</h1>

<h3>Intelligent Biogas Plant Design System</h3>

<p>
Design • Analyze • Visualize • Optimize
</p>

<hr>

<p>✔ Engineering Calculations</p>

<p>✔ Automatic Plant Drawings</p>

<p>✔ Cost Estimation</p>

<p>✔ Interactive 3D Models</p>

<p>✔ PDF Reports</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")
