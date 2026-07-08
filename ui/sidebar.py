"""
=========================================================
BioDesignAI Sidebar
Version 1.0

Author : Batool Fatima
=========================================================
"""

from pathlib import Path

import streamlit as st

from ui.theme import toggle_theme


def render_sidebar():
    """
    Render the application sidebar.

    Returns
    -------
    str
        Current selected page.
    """

    with st.sidebar:

        # =====================================================
        # LOGO
        # =====================================================

        project_root = Path(__file__).resolve().parent.parent
        logo_path = project_root / "assets" / "logo.png"

        if logo_path.exists():
            st.image(str(logo_path), width=120)
        else:
            st.warning("Logo not found")
            st.markdown("# 🌱")

        st.markdown("# BioDesignAI")
        st.caption("AI-Powered Biogas Plant Design")
        st.divider()

        # =====================================================
        # HOME
        # =====================================================

        st.markdown("### 🏠 Home")

        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_page = "Home"

        st.divider()

        # =====================================================
        # DESIGN
        # =====================================================

        st.markdown("### 📐 Design")

        if st.button("Plant Design", use_container_width=True):
            st.session_state.current_page = "Plant Design"

        if st.button("Engineering Calculations", use_container_width=True):
            st.session_state.current_page = "Engineering Calculations"

        st.divider()

        # =====================================================
        # VISUALIZATION
        # =====================================================

        st.markdown("### 🖼 Visualization")

        if st.button("Engineering Drawing", use_container_width=True):
            st.session_state.current_page = "Engineering Drawing"

        if st.button("3D Visualization", use_container_width=True):
            st.session_state.current_page = "3D Visualization"

        st.divider()

        # =====================================================
        # ANALYSIS
        # =====================================================

        st.markdown("### 📊 Analysis")

        if st.button("Dashboard Results", use_container_width=True):
            st.session_state.current_page = "Dashboard"

        if st.button("Materials", use_container_width=True):
            st.session_state.current_page = "Materials"

        if st.button("Cost Estimation", use_container_width=True):
            st.session_state.current_page = "Cost Estimation"

        st.divider()

        # =====================================================
        # REPORTS
        # =====================================================

        st.markdown("### 📄 Reports")

        if st.button("Generate Report", use_container_width=True):
            st.session_state.current_page = "Reports"

        st.divider()

        # =====================================================
        # SETTINGS
        # =====================================================

        st.markdown("### ⚙ Settings")

        theme_label = (
            "Switch to Dark Mode"
            if st.session_state.theme == "Light"
            else "Switch to Light Mode"
        )

        if st.button(theme_label, use_container_width=True):
            toggle_theme()
            st.rerun()

        st.divider()

        # =====================================================
        # ABOUT
        # =====================================================

        if st.button("ℹ About", use_container_width=True):
            st.session_state.current_page = "About"

        st.divider()

        st.caption("Version 1.0")
        st.caption("Developed by Batool Fatima")

    return st.session_state.current_page
