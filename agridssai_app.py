import streamlit as st

from modules.input_module import render_input_module
from modules.analysis_engine import run_full_analysis
from modules.dashboard import render_dashboard
from modules.report_generator import generate_report
from modules.ai_recommendation import render_ai_recommendation

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="AgriDSS AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# LOAD CSS
# -------------------------------------------------------

try:
    with open("styles/main.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
except:
    pass

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

st.sidebar.markdown(
    """
    <div class='sidebar-title'>🌾 AgriDSS AI</div>
    <div class='sidebar-subtitle'>
    Agricultural Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "",
    [
        "🚜 Farm Management",
        "📊 Run Analysis",
        "🏠 Dashboard",
        "🤖 AI Advisor",
        "📄 Reports",
    ],
)

# -------------------------------------------------------
# PAGES
# -------------------------------------------------------

if page == "🏠 Dashboard":
    render_dashboard()

elif page == "🚜 Farm Management":
    render_input_module()

elif page == "📊 Run Analysis":
    run_full_analysis()

elif page == "🤖 AI Advisor":
    render_ai_recommendation()

elif page == "📄 Reports":
    generate_report()
