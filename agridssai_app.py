import streamlit as st

from modules.input_module import render_input_module
from modules.analysis_engine import run_full_analysis
from modules.dashboard import render_dashboard
from modules.report_generator import generate_report
from modules.ai_recommendation import render_ai_recommendation

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AgriDSS AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD CUSTOM CSS
# ==========================================================

try:
    with open("styles/main.css", "r") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("styles/main.css not found.")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding:10px 0;">
        <h2 style="color:white; margin-bottom:0;">
            🌾 AgriDSS AI
        </h2>

        <p style="color:#E5E7EB; font-size:14px;">
            Agricultural Intelligence Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🚜 Farm Management",
        "📊 Analysis Center",
        "🤖 AI Advisor",
        "📄 Reports",
    ],
)

# ==========================================================
# TOP HEADER
# ==========================================================

st.markdown(
    """
    <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 3px 10px rgba(0,0,0,0.08);
        margin-bottom:20px;
    ">

        <h2 style="margin-bottom:5px;color:#2563EB;">
            AgriDSS AI
        </h2>

        <p style="color:#6B7280;margin:0;">
            AI Powered Agricultural Decision Support System
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# PAGE ROUTING
# ==========================================================

if page == "🏠 Dashboard":
    render_dashboard()

elif page == "🚜 Farm Management":
    render_input_module()

elif page == "📊 Analysis Center":
    run_full_analysis()

elif page == "🤖 AI Advisor":
    render_ai_recommendation()

elif page == "📄 Reports":
    generate_report()
