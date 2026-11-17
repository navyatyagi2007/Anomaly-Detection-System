"""Shared sidebar for every page: logo, beige theme, user card + logout.

Usage (right after st.set_page_config on EVERY page):

    from components.sidebar import render_sidebar
    render_sidebar()
"""
import base64

import streamlit as st

LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="310" height="84" viewBox="0 0 310 84">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3FA0E0"/>
      <stop offset="1" stop-color="#0F2F4E"/>
    </linearGradient>
  </defs>
  <rect x="2" y="6" width="72" height="72" rx="19" fill="url(#g)"/>
  <circle cx="38" cy="42" r="23" fill="none" stroke="#FFFFFF" stroke-width="8.5"
          stroke-dasharray="7.6 7.6"/>
  <circle cx="38" cy="42" r="16.5" fill="none" stroke="#FFFFFF" stroke-width="4.2"/>
  <circle cx="38" cy="42" r="6.5" fill="#FFFFFF"/>
  <text x="88" y="45" textLength="216" lengthAdjust="spacingAndGlyphs"
        font-family="Inter, Segoe UI, Arial, sans-serif" font-size="33" font-weight="900"
        fill="#0F2A45" stroke="#0F2A45" stroke-width="0.9">ANOMATRIX</text>
  <text x="89" y="65" textLength="214" lengthAdjust="spacing"
        font-family="Consolas, Menlo, monospace" font-size="11" font-weight="700"
        fill="#3F5A72">INDUSTRIAL INTELLIGENCE</text>
</svg>
"""

SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] { background: #EDEAE4 !important; border-right: 1px solid #DDD8D0 !important; }
[data-testid="stSidebarLogo"], [data-testid="stLogo"], [data-testid="stSidebarHeader"] img {
    height: 4.8rem !important; width: auto !important;
    max-width: 100% !important; object-fit: contain;
}
[data-testid="stSidebarHeader"] {
    height: auto; padding-top: 1.2rem; padding-bottom: 1rem;
    border-bottom: 1px solid #DDD8D0;
}
/* nav links */
[data-testid="stSidebarNav"] a {
    border-radius: 10px !important; color: #3B4A57 !important; font-weight: 500 !important;
}
[data-testid="stSidebarNav"] a:hover { background: #E4E0D8 !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: #DEDAD2 !important; color: #14273A !important; font-weight: 700 !important;
}
/* profile pinned to the bottom */
[data-testid="stSidebarContent"] { display: flex; flex-direction: column; }
[data-testid="stSidebarUserContent"] { margin-top: auto; padding-bottom: 1.2rem; padding-top: 0; }
[data-testid="stSidebarUserContent"] [data-testid="stElementContainer"]:not(:has(.user-card)):not(:has(.stButton)) {
    display: none !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF !important; color: #183B5B !important; border: 1px solid #D9D4CB !important;
    border-radius: 12px; font-weight: 650; height: 2.7rem;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #328BC5 !important; color: #17628D !important; background: #F4FAFE !important;
}
.user-card {
    display: flex; gap: 12px; align-items: center;
    background: #E4E0D8; border-radius: 14px; padding: 12px; margin-bottom: 10px;
}
.user-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: #D3E8F6; color: #17628D; font-weight: 800; font-size: 13px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.user-name { font-weight: 700; font-size: 14px; color: #183B5B; }
.user-role { font-size: 12px; color: #6F7C86; }
</style>
"""


def render_sidebar(name=None, role=None, initials=None):
    name = name or st.session_state.get("user_name", "Plant Admin")
    role = role or st.session_state.get("user_role", "Factory Operations")
    initials = initials or st.session_state.get("user_initials", "PA")
    st.logo(
        "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode("utf-8")).decode("utf-8"),
        size="large",
    )
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    with st.sidebar:
        st.html(
            f"""
            <div class="user-card">
                <div class="user-avatar">{initials}</div>
                <div>
                    <div class="user-name">{name}</div>
                    <div class="user-role">{role}</div>
                </div>
            </div>
            """
        )
        if st.button("⇦  Log out", use_container_width=True, key="logout_btn_sidebar"):
            from components.login import logout   # lazy import (avoids circular import)
            logout()

