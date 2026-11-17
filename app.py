import streamlit as st

st.set_page_config(
    page_title="ANOMATRIX | Industrial Intelligence",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.login import require_login

# 1) Not signed in -> full-screen login page (nothing else runs)
require_login()

# 2) Signed in -> normal multipage app
pages = [
    st.Page("pages/1_Dashboard.py", title="Factory Command Center", icon=":material/dashboard:", default=True),
    st.Page("pages/2_Machine_Explorer.py", title="Machine Explorer", icon=":material/precision_manufacturing:"),
    st.Page("pages/3_Maintenance_Reports.py", title="Maintenance & Reports", icon=":material/build:"),
    st.Page("pages/4_About_Help.py", title="About & Help", icon=":material/help:"),
]
st.navigation(pages).run()