"""Login page + auth helpers.

Use on EVERY page (right after st.set_page_config):

    from components.login import require_login
    from components.sidebar import render_sidebar

    require_login()      # shows the login screen and stops the page if not signed in
    render_sidebar()
"""
import base64
import time

import streamlit as st

from components.login_art import FACTORY_SVG
from components.sidebar import LOGO_SVG

DASHBOARD_PAGE = "pages/1_Dashboard.py"   # login ke baad yaha jayega
LOGIN_PAGE = "app.py"                     # logout ke baad yaha jayega (entry file)


def _uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("utf-8")


WHITE_LOGO = LOGO_SVG.replace("#0F2A45", "#FFFFFF").replace("#3F5A72", "#BCD6EA")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
html, body, .stApp, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: radial-gradient(900px 500px at 100% 0%, rgba(120,190,235,.35), transparent 60%), #E4EFF8; }

/* no sidebar / header on the login screen */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"],
[data-testid="stSidebarNav"], [data-testid="stHeader"], footer { display: none !important; }
.block-container { max-width: 1400px; padding: 1.2rem 1.5rem !important; }

/* ---------- LEFT: factory panel ---------- */
.lg-left {
    position: relative; overflow: hidden; border-radius: 26px; padding: 30px 34px 26px;
    min-height: calc(100vh - 2.6rem);
    background: radial-gradient(700px 380px at 85% 0%, rgba(63,160,224,.35), transparent 60%),
                linear-gradient(160deg, #0F2F4E 0%, #12395D 55%, #17628D 130%);
    box-shadow: 0 24px 60px rgba(15,39,64,.28);
    display: flex; flex-direction: column; color: #fff;
    background-blend-mode: normal;
}
.lg-left::before { content:""; position:absolute; inset:0; opacity:.07; pointer-events:none;
    background-image: linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px);
    background-size: 38px 38px; }
.lg-brand img { height: 48px; position: relative; }
.lg-head { position: relative; font-size: 38px; font-weight: 800; line-height: 1.1; letter-spacing: -.02em; margin-top: 26px; }
.lg-head span { color: #7CC4F5; }
.lg-sub { position: relative; color: #BCD6EA; font-size: 14.5px; max-width: 500px; margin-top: 10px; line-height: 1.5; }
.lg-art { position: relative; width: 100%; margin-top: auto; display: block; }
.lg-features { position: relative; display: flex; justify-content: space-between; margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.15); }
.lg-feature { display: flex; align-items: center; gap: 8px; color: #BCD6EA; font-size: 13px; font-weight: 500; }

/* ---------- RIGHT: login card ---------- */
[class*="st-key-login_card"] {
    background: #FFFFFF !important; border: 1px solid #DCE5EE !important; border-radius: 24px !important;
    box-shadow: 0 24px 60px rgba(15,39,64,.20), 0 4px 12px rgba(15,39,64,.08) !important;
    padding: 2.5rem 2.5rem 2rem !important; animation: lgUp .6s cubic-bezier(.22,1,.36,1) both;
}
[data-testid="stVerticalBlockBorderWrapper"]:has([class*="st-key-login_card"]):not([class*="st-key-login_card"]) {
    background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important;
}
@keyframes lgUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: none; } }
.lg-title { font-size: 30px; font-weight: 800; color: #14273A; letter-spacing: -.02em; margin: 12px 0 4px; text-align: center; }
.lg-title-sub { color: #6B7F8E; font-size: 14px; margin-bottom: 24px; text-align: center; }
.lg-foot { text-align: center; color: #8697A5; font-size: 12px; margin-top: 16px; }

[class*="st-key-login_card"] input { border-radius: 12px !important; }
[class*="st-key-login_card"] [data-baseweb="input"] { border-radius: 12px !important; background: #F6F9FC !important; }
[class*="st-key-login_card"] [data-testid="stFormSubmitButton"] button {
    border-radius: 12px !important; font-weight: 650; height: 2.8rem;
    background: linear-gradient(135deg, #183B5B, #2C6E9B) !important; color: #fff !important; border: none !important;
    box-shadow: 0 10px 22px rgba(24,59,91,.32) !important; transition: all .2s ease; width: 100%;
}
[class*="st-key-login_card"] [data-testid="stFormSubmitButton"] button:hover { transform: translateY(-2px); box-shadow: 0 14px 28px rgba(24,59,91,.42) !important; }
[data-testid="stForm"] { border: none !important; padding: 0 !important; }
</style>
"""


def _go_dashboard():
    try:
        st.switch_page(DASHBOARD_PAGE)
    except Exception:
        st.rerun()


def render_login():
    st.markdown(CSS, unsafe_allow_html=True)

    try:
        left, right = st.columns([1.25, 1], gap="large", vertical_alignment="center")
    except TypeError:
        left, right = st.columns([1.25, 1], gap="large")

    # ---------------- LEFT: Reference Styled Art Panel ----------------
    with left:
        st.markdown(
            f"""
            <div class="lg-left">
                <div class="lg-brand"><img src="{_uri(WHITE_LOGO)}"/></div>
                <div class="lg-head">Predict Failures,<br><span>Prevent Downtime</span></div>
                <div class="lg-sub">AI-powered insights for a smarter,<br>more reliable factory.</div>
                <img class="lg-art" src="{_uri(FACTORY_SVG)}"/>
                <div class="lg-features">
                    <div class="lg-feature">📈 Maximize Uptime</div>
                    <div class="lg-feature">🛡️ Reduce Maintenance Cost</div>
                    <div class="lg-feature">📊 Boost Productivity</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------- RIGHT: Clean Login Card ----------------
    with right:
        try:
            box = st.container(border=True, key="login_card")
        except TypeError:
            box = st.container(border=True)
        with box:
            st.markdown(
                """
                <div class="lg-title">Welcome Back!</div>
                <div class="lg-title-sub">Sign in to continue to Anomatrix</div>
                """,
                unsafe_allow_html=True,
            )

            try:
                form = st.form("login_form", border=False)
            except TypeError:
                form = st.form("login_form")
            with form:
                user = st.text_input("Email Address", placeholder="name@company.com")
                pwd = st.text_input("Password", type="password", placeholder="••••••••")
                submitted = st.form_submit_button("Login →", use_container_width=True)

            if submitted:
                # Accepts any non-empty username/password combination
                display_name = user.strip() if user and user.strip() else "Plant Operator"
                with st.spinner("Authenticating and loading your plant…"):
                    time.sleep(0.6)
                st.session_state.update(
                    logged_in=True,
                    user_name=display_name,
                    user_role="Plant Operations",
                    user_initials="PO",
                    login_failures=0,
                )
                st.toast(f"Welcome, {display_name}", icon="✅")
                _go_dashboard()

            st.markdown("<div style='text-align: center; color: #9AAAB8; font-size: 13px; margin: 12px 0 6px;'>or</div>", unsafe_allow_html=True)
            
            # Single centered "Forgot Password?" popover
            _pop = getattr(st, "popover", None)
            if _pop:
                with _pop("Forgot Password?", use_container_width=True):
                    st.write("Demo mode: You can enter any password to log in directly!")

            st.markdown('<div class="lg-foot">ANOMATRIX · Industrial Intelligence · Prototype</div>',
                        unsafe_allow_html=True)


def require_login():
    """Call at the top of every page. If nobody is signed in, show the login screen and stop."""
    if st.session_state.get("logged_in"):
        return
    render_login()
    st.stop()


def logout():
    """Sign out and land on the login screen from any page."""
    for k in ("logged_in", "user_name", "user_role", "user_initials", "login_user", "login_pass",
              "sel_machine", "popup_request", "pending_sel", "_map_sig"):
        st.session_state.pop(k, None)
    st.session_state["logged_in"] = False
    try:
        st.switch_page(LOGIN_PAGE)
    except Exception:
        st.rerun()