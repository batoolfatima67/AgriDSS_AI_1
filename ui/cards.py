"""
=========================================================
Dashboard Cards
=========================================================
"""

import streamlit as st


def metric_card(title, value, unit="", icon="📊"):

    st.markdown(
        f"""
<div class="bio-card">

<h4>{icon} {title}</h4>

<h2 style="color:#2E7D32;">
{value} {unit}
</h2>

</div>
""",
        unsafe_allow_html=True,
    )
