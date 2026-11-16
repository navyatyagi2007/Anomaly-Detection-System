
import streamlit as st

st.set_page_config(
    page_title="ANOMATRIX | Industrial Intelligence",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ANOMATRIX - PAGE NAVIGATION
# ==========================================

dashboard = st.Page(
    "pages/1_Dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True
)

machine_explorer = st.Page(
    "pages/2_Machine_Explorer.py",
    title="Machine Explorer",
    icon=":material/precision_manufacturing:"
)

predictive_lab = st.Page(
    "pages/3_Predictive_Lab.py",
    title="Predictive Lab",
    icon=":material/psychology:"
)

maintenance_hub = st.Page(
    "pages/4_Reliability_Maintenance_Hub.py",
    title="Reliability & Maintenance Hub",
    icon=":material/handyman:"
)

plant_intelligence = st.Page(
    "pages/5_Plant_Intelligence.py",
    title="Plant Intelligence",
    icon=":material/monitoring:"
)

about_help = st.Page(
    "pages/6_About_Help.py",
    title="About & Help",
    icon=":material/help_outline:"
)

# ==========================================
# SIDEBAR BRANDING
# ==========================================

st.sidebar.title("⚙️ ANOMATRIX")

st.sidebar.caption(
    "INDUSTRIAL INTELLIGENCE"
)

st.sidebar.markdown("---")

# ==========================================
# NAVIGATION MENU
# ==========================================

pg = st.navigation(
    [
        dashboard,
        machine_explorer,
        predictive_lab,
        maintenance_hub,
        plant_intelligence,
        about_help
    ]
)

# ==========================================
# RUN SELECTED PAGE
# ==========================================

pg.run()

