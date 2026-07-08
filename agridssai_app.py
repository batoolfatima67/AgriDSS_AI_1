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
            "Farm Management",
            "Analysis Center",
            "Dashboard",
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
                "padding": "8px",
                "background-color": "#60A5FA",   # Light Blue
                "border-radius": "15px",
            },

            "icon": {
                "color": "white",
                "font-size": "20px",
            },

            "nav-link": {
                "font-size": "16px",
                "font-weight": "600",
                "text-align": "left",
                "margin": "6px 0",
                "padding": "12px",
                "color": "white",
                "border-radius": "10px",
                "--hover-color": "#93C5FD",
            },

            "nav-link-selected": {
               "background-color": "#2563EB",
               "color": "white",
               "font-weight": "700",
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
padding:10px;
border-radius:6px;
box-shadow:0px 2px 4px rgba(0,0,0,.08);
margin-bottom:5px;
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

if selected == "Farm Management":

    render_input_module()

elif selected == "Analysis Center":

    run_full_analysis()

elif selected == "Dashboard":

    render_dashboard()

elif selected == "AI Advisor":

    render_ai_recommendation()

elif selected == "Reports":

    generate_report()
