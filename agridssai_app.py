import streamlit as st
from streamlit_option_menu import option_menu

from modules.input_module import render_input_module
from modules.analysis_engine import run_full_analysis
from modules.dashboard import render_dashboard
from modules.report_generator import generate_report
from modules.ai_recommendation import render_ai_recommendation

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AgriDSS AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

try:
    with open("styles/main.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
except:
    pass

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <h1 style='text-align:center;color:white;margin-bottom:0;'>
        🌾 AgriDSS AI
        </h1>

        <p style='text-align:center;color:#d1d5db;'>
        Agricultural Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True,
    )

    selected = option_menu(
        menu_title=None,

        options=[
            "Dashboard",
            "Farm Management",
            "Analysis Center",
            "AI Advisor",
            "Reports"
        ],

        icons=[
            "house-fill",
            "geo-alt-fill",
            "bar-chart-fill",
            "robot",
            "file-earmark-text-fill"
        ],

        default_index=0,

        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#1E3A8A",
            },

            "icon": {
                "color": "#93C5FD",
                "font-size": "18px",
            },

            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "4px",
                "border-radius": "10px",
            },

            "nav-link-selected": {
                "background-color": "#2563EB",
            },
        },
    )

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
<div style="
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 2px 12px rgba(0,0,0,.08);
margin-bottom:20px;
">

<h2 style="margin-bottom:0;">
🌾 AgriDSS AI
</h2>

<p style="color:gray;">
AI Powered Agricultural Decision Support System
</p>

</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# PAGE ROUTING
# --------------------------------------------------

if selected == "Dashboard":

    render_dashboard()

elif selected == "Farm Management":

    render_input_module()

elif selected == "Analysis Center":

    run_full_analysis()

elif selected == "AI Advisor":

    render_ai_recommendation()

elif selected == "Reports":

    generate_report()
