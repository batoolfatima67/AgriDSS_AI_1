import streamlit as st

from modules.input_module import render_input_module
from modules.analysis_engine import run_full_analysis
from modules.dashboard import render_dashboard
from modules.report_generator import generate_report

st.set_page_config(page_title="AgriDSS_AI", layout="wide")

st.sidebar.title("🌾 AI-Powered Agriculture Decision Support System (AgriDSS_AI)")

page = st.sidebar.radio(
    "Navigation",
    ["Farm Input", "Run Analysis", "Dashboard", "Report"]
)

if page == "Dashboard":
    render_dashboard()
    
elif page == "Farm Input":
    render_input_module()

elif page == "Run Analysis":
    run_full_analysis()

elif page == "Report":
    generate_report()
