
import streamlit as st

st.set_page_config(
    page_title="ANOMATRIX",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main branding
st.sidebar.title("⚙️ ANOMATRIX")
st.sidebar.caption("AI-Powered Industrial Monitoring")

st.title("⚙️ ANOMATRIX")
st.subheader("AI-Powered Industrial Monitoring")

st.markdown("---")

st.markdown(
    "### Detect Early. Predict Failures. Prevent Downtime."
)

st.success("System Status: Monitoring Active")

st.info(
    "Welcome to ANOMATRIX Industrial Monitoring Platform."
)

st.markdown("---")
st.caption("ANOMATRIX | Prototype v1.0")
