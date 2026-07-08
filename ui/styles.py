"""
=========================================================
CSS Loader
BioDesignAI
=========================================================
"""

import streamlit as st

from ui.theme import get_theme_colors


def load_css():

    colors = get_theme_colors()

    css = f"""
    <style>

    .stApp {{
        background-color:{colors["background"]};
    }}

    /* Remove default Streamlit header */

    header {{
        visibility:hidden;
    }}

    footer {{
        visibility:hidden;
    }}

    #MainMenu {{
        visibility:hidden;
    }}

    /* Titles */

    .main-title {{

        font-size:42px;

        font-weight:700;

        color:{colors["primary"]};

    }}

    .sub-title {{

        font-size:18px;

        color:{colors["muted"]};

    }}

    /* Cards */

    .bio-card {{

        background:{colors["card"]};

        border-radius:18px;

        padding:22px;

        border:1px solid {colors["border"]};

        box-shadow:0px 4px 15px rgba(0,0,0,.08);

    }}

    /* Hero */

    .hero {{

        background:linear-gradient(135deg,#2E7D32,#43A047);

        color:white;

        padding:40px;

        border-radius:22px;

    }}

    /* Footer */

    .footer {{

        text-align:center;

        color:{colors["muted"]};

        font-size:14px;

        padding:20px;

    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
